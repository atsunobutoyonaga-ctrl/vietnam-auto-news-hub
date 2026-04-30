// 記事の絞り込み・検索・並び替え
// グローバルに公開: window.Filters

const Filters = {
  /**
   * 記事一覧から「メーカー名 → 件数」の配列を取得(降順)
   */
  getMakerCounts(articles) {
    const counts = {};
    articles.forEach(a => {
      a.makers.forEach(m => { counts[m] = (counts[m] || 0) + 1; });
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  },

  /**
   * フィルタ・検索・優先ソートを適用した記事配列を返す
   *
   * @param {Array} articles - 元記事配列
   * @param {Object} state - {vtype, maker, category, view, keyword, priorityMaker}
   * @param {Function} isFav - id を渡すとお気に入りかを返す関数
   * @param {Function} hasMemo - id を渡すとメモが存在するかを返す関数
   */
  apply(articles, state, isFav, hasMemo) {
    let result = articles.slice();

    // 車種フィルタ
    if (state.vtype !== 'all') {
      if (state.vtype === 'four_wheel') {
        // 仕様: 四輪のみ選択時は unknown も含める(誤判定救済)
        result = result.filter(a => a.vehicleType === 'four_wheel' || a.vehicleType === 'unknown');
      } else {
        result = result.filter(a => a.vehicleType === state.vtype);
      }
    }

    // メーカーフィルタ
    if (state.maker !== 'all') {
      result = result.filter(a => a.makers.includes(state.maker));
    }

    // カテゴリフィルタ
    if (state.category !== 'all') {
      result = result.filter(a => a.categories.includes(state.category));
    }

    // 表示フィルタ
    if (state.view === 'favorites') {
      result = result.filter(a => isFav(a.id));
    } else if (state.view === 'memos') {
      result = result.filter(a => hasMemo(a.id));
    }

    // キーワード検索 (タイトル+サマリー+メーカー+ソース 部分一致)
    if (state.keyword) {
      const kw = state.keyword.toLowerCase();
      result = result.filter(a =>
        a.title.toLowerCase().includes(kw) ||
        a.summary.toLowerCase().includes(kw) ||
        a.makers.some(m => m.toLowerCase().includes(kw)) ||
        a.source.toLowerCase().includes(kw)
      );
    }

    // 優先メーカーが指定されていれば該当記事を上位にソート
    if (state.priorityMaker) {
      result.sort((a, b) => {
        const aP = a.makers.includes(state.priorityMaker) ? 1 : 0;
        const bP = b.makers.includes(state.priorityMaker) ? 1 : 0;
        if (aP !== bP) return bP - aP;
        return new Date(b.publishedAt) - new Date(a.publishedAt);
      });
    }

    return result;
  },
};

window.Filters = Filters;
