// LocalStorage 管理: お気に入り・メモ
// グローバルに公開: window.Storage

const FAV_KEY = 'vahn_favorites';
const MEMO_KEY = 'vahn_memos';

const Storage = {
  // ---------- お気に入り ----------
  getFavorites() {
    return JSON.parse(localStorage.getItem(FAV_KEY) || '[]');
  },

  isFavorite(id) {
    return this.getFavorites().includes(id);
  },

  toggleFavorite(id) {
    let favs = this.getFavorites();
    if (favs.includes(id)) {
      favs = favs.filter(f => f !== id);
    } else {
      favs.push(id);
    }
    localStorage.setItem(FAV_KEY, JSON.stringify(favs));
    return favs.includes(id);
  },

  // ---------- メモ ----------
  getMemos() {
    return JSON.parse(localStorage.getItem(MEMO_KEY) || '{}');
  },

  getMemo(id) {
    return this.getMemos()[id] || '';
  },

  saveMemo(id, value) {
    const memos = this.getMemos();
    if (value && value.trim()) {
      memos[id] = value;
    } else {
      delete memos[id];
    }
    localStorage.setItem(MEMO_KEY, JSON.stringify(memos));
  },

  // ---------- メモエクスポート ----------
  exportMemosAsMarkdown(articles) {
    const memos = this.getMemos();
    const items = articles
      .filter(a => memos[a.id] && memos[a.id].trim())
      .map(a => {
        const makers = a.makers.join(', ') || '不明';
        const cats = a.categories.join(', ') || '-';
        return `## ${a.title}\n\n` +
               `- ソース: ${a.source}\n` +
               `- メーカー: ${makers}\n` +
               `- カテゴリ: ${cats}\n` +
               `- URL: ${a.url}\n` +
               `- メモ: ${memos[a.id]}\n`;
      });
    if (items.length === 0) return null;
    const dateStr = new Date().toLocaleString('ja-JP');
    return `# Vietnam Auto News メモ集\n\n出力日: ${dateStr}\n\n---\n\n${items.join('\n---\n\n')}`;
  },
};

window.Storage = Storage;
