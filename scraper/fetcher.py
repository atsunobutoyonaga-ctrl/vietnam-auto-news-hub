"""RSS取得・パース共通処理。

`fetch_rss(source)` を呼ぶと、共通フォーマットの記事辞書のリストを返す。
分類・除外・重複排除は呼び出し元 (main.py) で行う。
"""
import hashlib
import re
from html import unescape

import feedparser

from config import MAX_PER_SOURCE


_TAG_RE = re.compile(r"<[^>]+>")
_SPACE_RE = re.compile(r"\s+")
_IMG_SRC_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.IGNORECASE)


def _strip_html(text):
    """HTMLタグを除去し、連続空白を1つにまとめる。"""
    if not text:
        return ""
    text = _TAG_RE.sub("", text)
    text = unescape(text)
    return _SPACE_RE.sub(" ", text).strip()


def _extract_thumbnail(entry):
    """RSSエントリーからサムネイル画像URLを推測。見つからなければ空文字。"""
    # 1) media:thumbnail
    if getattr(entry, "media_thumbnail", None):
        url = entry.media_thumbnail[0].get("url", "")
        if url:
            return url
    # 2) media:content
    if getattr(entry, "media_content", None):
        url = entry.media_content[0].get("url", "")
        if url:
            return url
    # 3) enclosures (image/*)
    for enc in entry.get("enclosures", []) or []:
        if "image" in enc.get("type", ""):
            href = enc.get("href", "")
            if href:
                return href
    # 4) summary/description 本文中の <img src="...">
    desc = (entry.get("summary", "") or "") + (entry.get("description", "") or "")
    m = _IMG_SRC_RE.search(desc)
    if m:
        return m.group(1)
    return ""


def _parse_google_news_title(title):
    """Google News タイトルは末尾が ' - ソース名'。それを分離。"""
    if " - " in title:
        body, src = title.rsplit(" - ", 1)
        return body.strip(), src.strip()
    return title, "Google News"


def _make_id(source_name, url):
    """ソース名+URLハッシュでユニークIDを生成。"""
    slug = re.sub(r"[^a-z0-9]+", "_", source_name.lower())[:12].strip("_")
    h = hashlib.md5(url.encode("utf-8")).hexdigest()[:10]
    return f"{slug}_{h}"


def fetch_rss(source):
    """RSSソース1つを取得し、整形済み記事辞書の配列を返す。

    Args:
        source: dict. {"name", "url", "category"} を持つ。

    Returns:
        list[dict]. 各記事は title/url/summary/thumbnail/publishedAt 等を含む。
    """
    feed = feedparser.parse(source["url"])
    articles = []

    for entry in feed.entries[:MAX_PER_SOURCE]:
        title = entry.get("title", "").strip()
        url = entry.get("link", "").strip()
        if not title or not url:
            continue

        published = entry.get("published", "") or entry.get("updated", "")
        summary_raw = entry.get("summary", "") or entry.get("description", "")
        summary = _strip_html(summary_raw)[:200]
        thumb = _extract_thumbnail(entry)

        # Google News: タイトル末尾 " - ソース名" を分解して本来のソースに置き換え
        actual_source = source["name"]
        if source["category"] == "googlenews":
            title, actual_source = _parse_google_news_title(title)

        articles.append({
            "id": _make_id(source["name"], url),
            "source": actual_source,
            "sourceCategory": source["category"],
            "sourceTag": "RSS",
            "title": title,
            "url": url,
            "publishedAt": published,
            "summary": summary,
            "thumbnail": thumb,
        })

    return articles
