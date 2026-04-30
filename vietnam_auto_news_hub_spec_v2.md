# Vietnam Auto News Hub - 仕様書 v2 (本実装版)

**Version**: 2.0 (Final)
**Date**: 2026-04-30
**Owner**: Atsunobu Toyonaga (Hakuhodo Vietnam Group)
**Status**: 実装着手可能

---

## 1. プロジェクト概要

### ゴール
ベトナム自動車関連ニュースを、複数ソースから集約・三菱優先で表示・検索できる個人用Webサイトを構築する。スマホ・PC両対応で、URL公開して任意の端末からアクセス可能にする。

### 制約条件
- 完全無料 (ホスティング、API、ドメイン全て無料枠)
- コーディング初心者対応
- 個人用 (認証不要)

---

## 2. 技術スタック

- ホスティング: GitHub Pages
- バージョン管理: GitHub
- ニュース取得: GitHub Actions (手動trigger)
- フロントエンド: HTML + CSS + Vanilla JavaScript
- データ形式: JSON静的ファイル
- スクレイピング: Python (feedparser, requests)
- 翻訳: ブラウザ自動翻訳に委譲

---

## 3. データソース (確定版)

### RSSソース (6サイト、各最大50件)
1. VnExpress: https://vnexpress.net/rss/oto-xe-may.rss
2. VietnamNet: https://vietnamnet.vn/rss/oto-xe-may.rss
3. Tuoi Tre: https://tuoitre.vn/rss/xe.rss
4. Dan Tri: https://dantri.com.vn/rss/o-to-xe-may.rss
5. Thanh Nien: https://thanhnien.vn/rss/xe.rss
6. AutoPro: https://autopro.com.vn/xe-may.rss

### Google News RSS (3クエリ並走、Mitsubishi強化)
1. Mitsubishi Vietnam (英語): https://news.google.com/rss/search?q=Mitsubishi+Vietnam&hl=en-US&gl=US&ceid=US:en
2. Mitsubishi Việt Nam (越語): https://news.google.com/rss/search?q=Mitsubishi+Vi%E1%BB%87t+Nam&hl=vi&gl=VN&ceid=VN:vi
3. 車種名 (Xpander/Triton/Outlander/Pajero/Attrage): https://news.google.com/rss/search?q=Xpander+OR+Triton+OR+Outlander+OR+Pajero+OR+Attrage&hl=vi&gl=VN&ceid=VN:vi

各クエリ最大50件取得。タイトル末尾の ` - ソース名` をパースしてメディア名を抽出。

---

## 4. データ処理ロジック

### 除外キーワード (交通事故・違反系)
事故系: tai nạn, đâm, va chạm, lật xe, đụng
違反系: phạt, vi phạm, biên bản, CSGT, cảnh sát giao thông, quá tốc độ, không biển số
飲酒・薬物: say xỉn, nồng độ cồn, rượu bia, ma túy
死傷系: tử vong, chết, thiệt mạng, bị thương, cấp cứu
運転トラブル: buồn ngủ, cãi cọ, thót tim
犯罪: trộm, cướp

### 車種判定 (vehicleType)
1. URLに xe-may → two_wheel
2. URLに o-to/xe-hoi → four_wheel
3. キーワードスコア比較 (二輪語 vs 四輪語)
4. バイクブランド名 (Yadea, Vespa等) → two_wheel
5. それ以外 → unknown

UI上は「四輪のみ」フィルタ時に unknown も含める(誤判定救済)。

### メーカー判定 (22メーカー)
特別扱い: Mitsubishi (Xpander, Outlander, Pajero, Triton, Attrage, Mirage, Eclipse Cross)
他: Toyota, Honda, Mazda, Nissan, Suzuki, Isuzu, Hyundai, Kia, VinFast, BYD, Chery, Geely, MG, Wuling, Haval, Ford, Mercedes, BMW, Audi, Porsche, Skoda, Volvo

### カテゴリ判定
- EV: xe điện, EV, BEV, electric vehicle
- HEV: hybrid, HEV, PHEV
- Policy: thuế, chính sách, quy định, nghị định
- Sales: doanh số, tiêu thụ, bán chạy
- Launch: ra mắt, công bố, giới thiệu
- Recall: triệu hồi, thu hồi, recall (赤バッジ強調)

---

## 5. データ構造 (news.json)

```json
{
  "lastUpdated": "ISO datetime",
  "totalCount": 408,
  "stats": { "totalRaw": 450, "excluded": 37, "afterDedup": 408 },
  "sources": ["VnExpress", ...],
  "articles": [
    {
      "id": "unique_id",
      "source": "VnExpress",
      "sourceCategory": "general",
      "sourceTag": "RSS",
      "title": "ベトナム語タイトル",
      "url": "https://...",
      "publishedAt": "ISO datetime",
      "summary": "200文字以内",
      "thumbnail": "url or empty",
      "vehicleType": "four_wheel|two_wheel|unknown",
      "makers": ["Mitsubishi"],
      "categories": ["Recall", "Sales"]
    }
  ]
}
```

LocalStorage (ブラウザ保存):
- vahn_favorites: お気に入り記事ID配列
- vahn_memos: { id: メモテキスト }

---

## 6. UI仕様

### デザイン
- ベトナム国旗カラー (赤 #da251d / 黄 #ffcd00) ヘッダーグラデ
- iOS的角丸カードデザイン
- スマホファースト (360px〜)
- 固有名詞には translate="no" 属性 (Chrome翻訳除外)

### 画面構成
- ヘッダー (赤→黄グラデ、最終更新時刻表示)
- 検索ボックス
- フィルタ群:
  - 車種: 四輪のみ(デフォルト) / 二輪のみ / すべて
  - 推し: ⭐Mitsubishi優先 (デフォルトON、上位ソート+オレンジ枠強調)
  - メーカー: 全メーカー件数表示
  - カテゴリ: すべて / 🔴リコール / EV / HEV / 政策 / 販売 / 発表
  - 表示: すべて / お気に入り / メモあり
- 記事カード (50件ずつ、もっと読み込むボタン)

### カラーパレット
- mitsubishi-red: #ff3b30 (Mitsubishiタグ・リコール)
- priority-orange: #ff9500 (優先記事枠)
- four-wheel-green: #34c759
- two-wheel-purple: #af52de
- googlenews-purple: #5856d6 (Google News由来)

---

## 7. 機能要件

### マスト機能 (Phase 1)
1. 記事一覧表示 (公開日新しい順、50件ずつページネーション)
2. キーワード検索 (タイトル+サマリー+メーカー+ソース部分一致、リアルタイム)
3. フィルタ群 (車種/メーカー優先/メーカー単独/カテゴリ/表示)
4. 元記事リンク (新タブ、ブラウザ翻訳前提)
5. お気に入り (LocalStorage)
6. メモ機能 (LocalStorage、自動保存、Markdownエクスポート)
7. 手動更新 (GitHub Actions workflow_dispatch)

### 推奨機能 (Phase 2)
1. 統計ダッシュボード (stats.html、Chart.js使用)
2. リコール記事タイムライン

---

## 8. ファイル構成---

## 9. 実装ステップ

### Step 1: プロジェクト初期化
1. GitHubで新規リポジトリ vietnam-auto-news-hub 作成 (Public)
2. ローカルに clone
3. ファイル構成スケルトン作成
4. .gitignore作成

### Step 2: スクレイパー実装
1. config.py: ソースリスト、キーワード辞書
2. filter.py: 除外キーワード判定
3. classifier.py: 車種・メーカー・カテゴリ判定
4. fetcher.py: RSS取得・パース共通処理
5. main.py: 全ソース統合実行 → docs/data/news.json 出力
6. ローカル動作確認

### Step 3: フロントエンド実装
1. docs/index.html
2. docs/css/style.css (reference_prototype.htmlから移植)
3. docs/js/storage.js (LocalStorage管理)
4. docs/js/filters.js (フィルタ・検索・ソート)
5. docs/js/app.js (メイン制御・レンダリング)
6. ローカル動作確認 (python -m http.server)

### Step 4: GitHub Actions設定
1. .github/workflows/update-news.yml
   - workflow_dispatch (手動trigger)
   - Python環境セットアップ
   - pip install -r scraper/requirements.txt
   - python scraper/main.py
   - git commit & push
2. テスト実行

### Step 5: GitHub Pages 公開
1. Settings > Pages で docs/ を公開ディレクトリ指定
2. 公開URL確認
3. スマホアクセステスト

---

## 10. リスクと対応策

- サイトHTML変更でスクレイパー停止 → RSSメインで影響軽微
- robots.txt変更 → 月1確認、別サイトに置換
- Google Newsクエリ仕様変更 → 英語/越語両並走で冗長化済み
- GitHub Actions無料枠超過 → 手動更新のみで月20分以下
- 著作権 → タイトル+サマリー+リンクのみ、本文転載しない
- ブラウザ翻訳ぶれ → translate="no" で対策済み

---

## 11. 重要な参考ファイル

reference_prototype.html: 完成イメージのHTML。動作・デザイン・機能の実装の参考にする。新規実装時にこのファイルのCSSとJSロジックを移植して使うこと。

---

## 付録: 進め方ルール (Claude Code向け)

ユーザーはコーディング初心者なので:
1. Step 1から順番に進める
2. 各Step開始時に「これから何をするか」を日本語で説明
3. コードを書いたら「何のためのコードか」を簡潔に説明
4. 各Step完了時に動作確認方法を提示し、確認まで次に進まない
5. エラーや想定外の動作は原因を日本語で説明し、対応案を提示
6. 専門用語は初出時に簡単な解説を入れる

End of Specification v2
