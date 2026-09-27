(() => {
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#navigation');
  if (menu && nav) {
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', open ? 'ปิดเมนู' : 'เปิดเมนู');
      nav.classList.toggle('open', open);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false');
        menu.setAttribute('aria-label', 'เปิดเมนู'); menu.focus();
      }
    });
  }
  const grid = document.querySelector('.searchable');
  if (!grid) return;
  const cards = [...grid.querySelectorAll('.news-card')];
  const search = document.querySelector('#news-search');
  const category = document.querySelector('#category-filter');
  const year = document.querySelector('#year-filter');
  const pager = document.querySelector('.pagination');
  const prev = document.querySelector('#prev-page');
  const next = document.querySelector('#next-page');
  let page = 1;
  const pageSize = 12;
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  if ([...category.options].some(o => o.value === params.get('category'))) category.value = params.get('category');
  if ([...year.options].some(o => o.value === params.get('year'))) year.value = params.get('year');
  function render(reset = false) {
    if (reset) page = 1;
    const q = search.value.trim().normalize('NFC').toLocaleLowerCase('th');
    const matches = cards.filter(c => (!category.value || c.dataset.category === category.value) &&
      (!year.value || c.dataset.year === year.value) && c.dataset.search.normalize('NFC').toLocaleLowerCase('th').includes(q));
    const total = Math.max(1, Math.ceil(matches.length / pageSize));
    page = Math.min(page, total);
    cards.forEach(c => { c.hidden = true; });
    matches.slice((page - 1) * pageSize, page * pageSize).forEach(c => { c.hidden = false; });
    document.querySelector('#result-count').textContent = `พบ ${matches.length} รายการ จากทั้งหมด ${cards.length} รายการ`;
    document.querySelector('#empty-state').hidden = matches.length !== 0;
    document.querySelector('#page-status').textContent = `หน้า ${page} / ${total}`;
    pager.hidden = total < 2; prev.disabled = page <= 1; next.disabled = page >= total;
    const url = new URL(location.href);
    [['q', search.value], ['category', category.value], ['year', year.value]].forEach(([key, value]) => {
      if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
    });
    history.replaceState(null, '', url);
  }
  search.addEventListener('input', () => render(true));
  category.addEventListener('change', () => render(true));
  year.addEventListener('change', () => render(true));
  const go = delta => { page += delta; render(); document.querySelector('.filters').scrollIntoView({block:'start'}); };
  prev.addEventListener('click', () => go(-1)); next.addEventListener('click', () => go(1));
  render();
})();
