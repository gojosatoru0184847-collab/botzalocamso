/* Chọn nền tảng / bản game bằng 2 nút gạt, đồng bộ với <select id="version"> gốc để JS cũ vẫn chạy. */
(() => {
  const select = document.getElementById('version');
  const host = document.getElementById('version-picker');
  if (!select || !host) return;

  const groups = [
    { label: 'Nền tảng', options: [['android', 'Android'], ['ios', 'iOS']] },
    { label: 'Bản game', options: [['normal', 'Free Fire thường'], ['max', 'Free Fire MAX']] }
  ];
  const parts = () => select.value.split('-');           // ['android','normal']
  const buttons = [];

  groups.forEach((group, gi) => {
    const seg = document.createElement('div');
    seg.className = 'seg';
    seg.setAttribute('role', 'group');
    seg.setAttribute('aria-label', group.label);
    group.options.forEach(([value, text]) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = text;
      b.dataset.group = gi;
      b.dataset.value = value;
      b.addEventListener('click', () => {
        const next = parts();
        next[gi] = value;
        const target = next.join('-');
        if (select.value === target || select.disabled) return;
        select.value = target;
        select.dispatchEvent(new Event('change', { bubbles: true }));
        sync();
      });
      seg.append(b);
      buttons.push(b);
    });
    host.append(seg);
  });

  function sync() {
    const current = parts();
    buttons.forEach(b => {
      b.setAttribute('aria-pressed', String(current[b.dataset.group] === b.dataset.value));
      b.disabled = select.disabled;
    });
  }

  select.addEventListener('change', sync);
  window.addEventListener('alok-version-change', sync);
  new MutationObserver(sync).observe(select, { attributes: true, attributeFilter: ['disabled'] });
  sync();
})();
