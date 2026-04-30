# Vietnam Auto News Hub

ベトナム自動車関連ニュースを複数ソースから集約し、三菱優先で表示・検索できる個人用Webサイト。

## 構成

- **ホスティング**: GitHub Pages (`docs/`)
- **ニュース取得**: GitHub Actions(手動trigger)で `scraper/main.py` を実行 → `docs/data/news.json` を更新
- **フロントエンド**: HTML + CSS + Vanilla JavaScript

## ディレクトリ

```
docs/                  GitHub Pagesで公開する静的サイト
  ├── index.html
  ├── css/style.css
  ├── js/               app.js, filters.js, storage.js
  └── data/news.json    記事データ
scraper/               Python スクレイパー
.github/workflows/     GitHub Actions 設定
```

## 公開URL

(Step 5でGitHub Pagesを有効化したらここに記載)
