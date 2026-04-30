"""Vietnam Auto News Hub - スクレイパー本体。

全RSSソースを取得 → 除外フィルタ → 重複排除 → 分類タグ付け → ソート →
docs/data/news.json に書き出し。

実行:
    python scraper/main.py
"""
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# scraper/ 内のモジュールを import 可能にする
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from config import RSS_SOURCES, GOOGLE_NEWS_SOURCES  # noqa: E402
from fetcher import fetch_rss  # noqa: E402
from filter import is_excluded  # noqa: E402
from classifier import classify_vehicle, classify_makers, classify_categories  # noqa: E402


_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, ".."))
_OUTPUT_PATH = os.path.join(_PROJECT_ROOT, "docs", "data", "news.json")


def _parse_date(s):
    """RSSの日付文字列を datetime に変換。失敗時は最小値。"""
    if not s:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        d = parsedate_to_datetime(s)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d
    except (TypeError, ValueError):
        return datetime.min.replace(tzinfo=timezone.utc)


def fetch_all():
    """全ソースを取得して生記事リストを返す。"""
    all_articles = []
    for source in RSS_SOURCES + GOOGLE_NEWS_SOURCES:
        print(f"  Fetching {source['name']} ... ", end="", flush=True)
        try:
            articles = fetch_rss(source)
            print(f"{len(articles)} articles")
            all_articles.extend(articles)
        except Exception as e:
            print(f"ERROR: {e}")
    return all_articles


def main():
    print("=== Vietnam Auto News Hub - Scraper ===")
    print()
    print("[1/4] RSS取得")
    raw = fetch_all()
    total_raw = len(raw)
    print(f"  -> 合計 {total_raw} 件取得")
    print()

    print("[2/4] 除外フィルタ")
    filtered = [a for a in raw if not is_excluded(a)]
    excluded = total_raw - len(filtered)
    print(f"  -> 除外 {excluded} 件 / 残り {len(filtered)} 件")
    print()

    print("[3/4] URL重複排除")
    seen = set()
    deduped = []
    for a in filtered:
        if a["url"] in seen:
            continue
        seen.add(a["url"])
        deduped.append(a)
    print(f"  -> 重複排除後 {len(deduped)} 件")
    print()

    print("[4/4] 分類・ソート・書き出し")
    sources_seen = set()
    for a in deduped:
        a["vehicleType"] = classify_vehicle(a)
        a["makers"] = classify_makers(a)
        a["categories"] = classify_categories(a)
        sources_seen.add(a["source"])

    deduped.sort(key=lambda a: _parse_date(a["publishedAt"]), reverse=True)

    output = {
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
        "totalCount": len(deduped),
        "stats": {
            "totalRaw": total_raw,
            "excluded": excluded,
            "afterDedup": len(deduped),
        },
        "sources": sorted(sources_seen),
        "articles": deduped,
    }

    os.makedirs(os.path.dirname(_OUTPUT_PATH), exist_ok=True)
    with open(_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  -> 書き出し完了: {_OUTPUT_PATH}")
    print()
    print(f"=== 完了: {len(deduped)} 件 (raw {total_raw} / excluded {excluded}) ===")


if __name__ == "__main__":
    main()
