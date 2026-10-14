/* LIMINAL local mode. This build runs without the original Supabase account/points backend. */
(() => {
  const heading = () => document.getElementById('fish-mod-turns');
  if (heading()) heading().textContent = 'Bản chạy cục bộ · không cần đăng nhập';
  window.fishCheckExport = async count => ({ id: 'local-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2), user: 'local', count: Number(count) || 1, local: true });
  window.fishChargeExport = async ticket => {
    if (!ticket || !ticket.local) throw new Error('Phiên xuất cục bộ không hợp lệ.');
    if (heading()) heading().textContent = 'Bản chạy cục bộ · không trừ điểm';
    return true;
  };
})();
