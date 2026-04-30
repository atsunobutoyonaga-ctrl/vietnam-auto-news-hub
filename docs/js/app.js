// メイン制御: news.json 読み込み・描画・イベント処理
// 依存: storage.js (window.Storage), filters.js (window.Filters)

const PAGE_SIZE = 50;

// アプリ状態
const state = {
  articles: [],
  vtype: 'four_wheel',
  maker: 'all',
  category: 'all',
  view: 'all',
  keyword: '',
  priorityMaker: 'Mitsubishi',
  displayLimit: PAGE_SIZE,
};

// HTMLエスケープ (XSS対策)
function escapeHtml(s) {
  if (s == null) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// 起動
async function init() {
  try {
    const res = await fetch('data/news.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    state.articles = data.articles || [];
    renderHeaderMeta(data);
    renderMakerFilters();
    bindEvents();
    render();
  } catch (e) {
    document.getElementById('newsList').innerHTML =
      `<div class="empty">記事データの読み込みに失敗しました。<br>${escapeHtml(e.message)}</div>`;
  }
}

function renderHeaderMeta(data) {
  const updated = new Date(data.lastUpdated);
  const s = data.stats || {};
  const dateStr = isNaN(updated) ? '' : updated.toLocaleString('ja-JP');
  document.getElementById('updateMeta').textContent =
    `📅 ${dateStr} | 全${data.totalCount}件 (除外${s.excluded || 0}件)`;
}

function renderMakerFilters() {
  const target = document.getElementById('makerFilters');
  target.innerHTML = '';
  Filters.getMakerCounts(state.articles).forEach(([maker, count]) => {
    const chip = document.createElement('span');
    chip.className = 'filter-chip';
    chip.dataset.filter = 'maker';
    chip.dataset.value = maker;
    chip.setAttribute('translate', 'no');
    chip.innerHTML =
      `${escapeHtml(maker)} <span style="opacity:0.6;font-size:10px;">${count}</span>`;
    target.appendChild(chip);
  });
}

function bindEvents() {
  // フィルタチップ
  document.body.addEventListener('click', (e) => {
    const chip = e.target.closest('.filter-chip');
    if (!chip) return;
    handleChipClick(chip);
  });

  // 検索ボックス
  document.getElementById('searchInput').addEventListener('input', (e) => {
    state.keyword = e.target.value.toLowerCase();
    state.displayLimit = PAGE_SIZE;
    render();
  });

  // 「もっと読み込む」
  document.getElementById('loadMoreBtn').addEventListener('click', () => {
    state.displayLimit += PAGE_SIZE;
    render();
  });

  // メモエクスポート
  document.getElementById('exportLink').addEventListener('click', (e) => {
    e.preventDefault();
    exportMemos();
  });
}

function handleChipClick(chip) {
  const filter = chip.dataset.filter;
  const value = chip.dataset.value;

  // 推し(Mitsubishi優先)はトグル
  if (chip.classList.contains('priority')) {
    chip.classList.toggle('active');
    state.priorityMaker = chip.classList.contains('active') ? value : null;
    state.displayLimit = PAGE_SIZE;
    render();
    return;
  }

  // 通常フィルタは同じ filter 内で1つだけ active
  document.querySelectorAll(
    `.filter-chip[data-filter="${filter}"]:not(.priority)`
  ).forEach(c => c.classList.remove('active'));
  chip.classList.add('active');
  state[filter] = value;
  state.displayLimit = PAGE_SIZE;
  render();
}

function render() {
  const filtered = Filters.apply(
    state.articles,
    state,
    (id) => Storage.isFavorite(id),
    (id) => !!Storage.getMemo(id)
  );
  const display = filtered.slice(0, state.displayLimit);

  const priorityCount = state.priorityMaker
    ? filtered.filter(a => a.makers.includes(state.priorityMaker)).length
    : 0;

  document.getElementById('resultCount').innerHTML = state.priorityMaker
    ? `📰 ${filtered.length}件中 ${display.length}件表示 (うち <strong style="color:#ff9500;">${escapeHtml(state.priorityMaker)} ${priorityCount}件</strong>を上位に)`
    : `📰 ${filtered.length}件中 ${display.length}件表示`;

  const list = document.getElementById('newsList');
  if (filtered.length === 0) {
    list.innerHTML = '<div class="empty">該当する記事がありません</div>';
    document.getElementById('loadMoreBtn').style.display = 'none';
    return;
  }

  list.innerHTML = display.map(renderCard).join('');
  document.getElementById('loadMoreBtn').style.display =
    filtered.length > state.displayLimit ? 'block' : 'none';
}

function renderCard(a) {
  const isFav = Storage.isFavorite(a.id);
  const memo = Storage.getMemo(a.id);
  const date = new Date(a.publishedAt);
  const dateStr = isNaN(date) ? '' : date.toLocaleString('ja-JP', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  const vtypeLabel = ({
    four_wheel: '🚗 四輪', two_wheel: '🏍 二輪', unknown: '❓'
  })[a.vehicleType] || '';

  const makerTags = a.makers.map(m => {
    const cls = m === 'Mitsubishi' ? 'maker-tag mitsubishi' : 'maker-tag';
    return `<span class="${cls}" translate="no">${escapeHtml(m)}</span>`;
  }).join('');

  const catTags = a.categories.slice(0, 3).map(c => {
    const cls = c === 'Recall' ? 'cat-tag recall' : 'cat-tag';
    const label = c === 'Recall' ? '🔴 リコール' : c;
    return `<span class="${cls}" translate="no">${escapeHtml(label)}</span>`;
  }).join('');

  const sourceClass = a.sourceCategory === 'googlenews' ? 'source-tag gn' : 'source-tag';
  const sourcePrefix = a.sourceCategory === 'googlenews' ? '🔍 ' : '';

  const priorityClass = (state.priorityMaker && a.makers.includes(state.priorityMaker))
    ? 'priority' : '';

  const thumbHtml = a.thumbnail
    ? `<img class="news-thumb" src="${escapeHtml(a.thumbnail)}" loading="lazy" onerror="this.style.display='none'">`
    : `<div class="news-thumb" style="display:flex;align-items:center;justify-content:center;font-size:24px;">📰</div>`;

  const escId = escapeHtml(a.id);

  return `
    <div class="news-card ${priorityClass}">
      ${thumbHtml}
      <div class="news-content">
        <div class="news-meta">
          <span class="${sourceClass}" translate="no">${sourcePrefix}${escapeHtml(a.source)}</span>
          <span class="vtype-tag ${a.vehicleType}" translate="no">${vtypeLabel}</span>
          <span>${dateStr}</span>
          ${makerTags}
          ${catTags}
        </div>
        <div class="news-title">
          <a href="${escapeHtml(a.url)}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;">${escapeHtml(a.title)}</a>
        </div>
        <div class="news-summary">${escapeHtml(a.summary)}</div>
        <div class="news-actions">
          <a class="action-btn" href="${escapeHtml(a.url)}" target="_blank" rel="noopener">→ 元記事を読む</a>
          <button class="action-btn ${isFav ? 'fav-active' : ''}" onclick="App.toggleFav('${escId}')">${isFav ? '⭐ 解除' : '☆ お気に入り'}</button>
          <button class="action-btn" onclick="App.toggleMemo('${escId}')">📝 ${memo ? 'メモあり' : 'メモ'}</button>
        </div>
        <div class="memo-area" id="memo-${escId}">
          <textarea placeholder="営業メモ / 提案ネタ用メモ..." onblur="App.saveMemo('${escId}', this.value)" onkeyup="App.markUnsaved('${escId}')">${escapeHtml(memo)}</textarea>
          <div class="memo-status" id="memo-status-${escId}"></div>
        </div>
      </div>
    </div>
  `;
}

// インラインハンドラから呼ばれる関数群
const App = {
  toggleFav(id) {
    Storage.toggleFavorite(id);
    render();
  },

  toggleMemo(id) {
    const area = document.getElementById('memo-' + id);
    if (!area) return;
    area.classList.toggle('visible');
    if (area.classList.contains('visible')) {
      area.querySelector('textarea').focus();
    }
  },

  markUnsaved(id) {
    const status = document.getElementById('memo-status-' + id);
    if (status) status.textContent = '入力中...';
  },

  saveMemo(id, value) {
    Storage.saveMemo(id, value);
    const status = document.getElementById('memo-status-' + id);
    if (status) {
      status.textContent = '✓ 保存済み';
      setTimeout(() => { if (status) status.textContent = ''; }, 2000);
    }
  },
};

window.App = App;

function exportMemos() {
  const md = Storage.exportMemosAsMarkdown(state.articles);
  if (!md) {
    alert('保存されているメモがありません');
    return;
  }
  const blob = new Blob([md], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `vahn_memos_${new Date().toISOString().slice(0, 10)}.md`;
  a.click();
  URL.revokeObjectURL(url);
}

// 起動
init();
