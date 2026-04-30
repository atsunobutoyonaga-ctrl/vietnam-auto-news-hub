# Vietnam Auto News Hub

ベトナム自動車関連ニュースを複数ソースから集約し、三菱優先で表示・検索できる個人用Webサイト。

## 公開URL

**https://atsunobutoyonaga-ctrl.github.io/vietnam-auto-news-hub/**

スマホ/PC両対応。

## 構成

- **ホスティング**: GitHub Pages (`docs/` 配下)
- **ニュース取得**: GitHub Actions(手動trigger)で `scraper/main.py` を実行 → `docs/data/news.json` を更新
- **フロントエンド**: HTML + CSS + Vanilla JavaScript

## ディレクトリ

```
docs/                       GitHub Pagesで公開する静的サイト
  ├── index.html
  ├── css/style.css
  ├── js/                   storage.js, filters.js, app.js
  └── data/news.json        記事データ
scraper/                    Python スクレイパー
  ├── config.py             ソース・除外/分類辞書
  ├── filter.py             除外フィルタ
  ├── classifier.py         車種・メーカー・カテゴリ判定
  ├── fetcher.py            RSS取得
  ├── main.py               統合実行 (scraper の入口)
  └── requirements.txt
.github/workflows/
  └── update-news.yml       手動実行ワークフロー
```

## 運用: ニュースを最新化する

[Actions タブ](https://github.com/atsunobutoyonaga-ctrl/vietnam-auto-news-hub/actions/workflows/update-news.yml)
→ 「Run workflow」 ボタン → 「Run workflow」(緑)。

数十秒〜数分で完了し、`docs/data/news.json` が自動コミットされ、GitHub Pages に即反映される。

## ローカル開発

```sh
# 仮想環境
python3 -m venv venv
./venv/bin/pip install -r scraper/requirements.txt

# スクレイパー実行 (docs/data/news.json を生成)
./venv/bin/python scraper/main.py

# プレビュー (http://localhost:8000)
cd docs && ../venv/bin/python -m http.server 8000
```

## データソース

### RSS (6サイト × 最大50件)
VnExpress / VietnamNet / Tuoi Tre / Dan Tri / Thanh Nien / AutoPro

### Google News RSS (3クエリ × 最大50件、Mitsubishi 強化)
- `Mitsubishi Vietnam` (英語)
- `Mitsubishi Việt Nam` (越語)
- `Xpander OR Triton OR Outlander OR Pajero OR Attrage`

## 主な機能

- キーワード検索(タイトル+サマリー+メーカー+ソース 部分一致)
- 車種フィルタ(四輪 / 二輪 / すべて)
- メーカー優先(デフォルト ⭐ Mitsubishi 上位ソート + オレンジ枠強調)
- カテゴリフィルタ(🔴 リコール / EV / HEV / 政策 / 販売 / 発表)
- 表示フィルタ(すべて / お気に入り / メモあり)
- ⭐ お気に入り(LocalStorage 保存)
- 📝 営業メモ(LocalStorage 保存・Markdown エクスポート)
- 事故・違反系記事を自動除外
