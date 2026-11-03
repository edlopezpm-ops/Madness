// (kommiBo) Explicit Weekly-only permission; one best-effort view, no queue or identity.
(() => {
  const control = document.querySelector('#weekly-metrics-controls');
  if (!control) return;
  const KEY = 'weekly-leverage-analytics-v1', POLICY = '2026-11-03-weekly-v1';
  const MAX_AGE = 30 * 86400000, ENDPOINT = '/weekly-leverage/api/metrics';
  const accept = control.querySelector('[data-metrics-accept]');
  const reject = control.querySelector('[data-metrics-reject]');
  let failed = false, attempted = false, pending = null, expiry = null;
  let ready = document.querySelector('#language-toggle')?.disabled !== true;
  const privacySignal = () => navigator.globalPrivacyControl === true || navigator.doNotTrack === '1' || window.doNotTrack === '1';
  function choice() {
    try {
      const value = JSON.parse(localStorage.getItem(KEY));
      return value?.policy === POLICY && ['accept', 'reject'].includes(value.choice) &&
        Number.isFinite(value.expires) && value.expires > Date.now() && value.expires <= Date.now() + MAX_AGE ? value : null;
    } catch { failed = true; return null; }
  }
  function state(name) {
    for (const item of control.querySelectorAll('[data-metrics-state]')) item.hidden = item.dataset.metricsState !== name;
  }
  function permitted() { return ready && !failed && !privacySignal() && choice()?.choice === 'accept' && document.visibilityState !== 'hidden'; }
  function update() {
    const saved = choice();
    accept.disabled = !ready || privacySignal(); reject.disabled = false;
    state(failed ? 'failed' : privacySignal() ? 'signal' : saved?.choice === 'accept' ? 'accepted' : 'off');
    clearTimeout(expiry);
    if (saved?.choice === 'accept') expiry = setTimeout(() => { pending?.abort(); update(); }, Math.min(saved.expires - Date.now() + 1, 2147483647));
  }
  function save(next) {
    pending?.abort(); failed = false;
    try {
      localStorage.setItem(KEY, JSON.stringify({ policy: POLICY, choice: next, expires: Date.now() + MAX_AGE }));
      if (choice()?.choice !== next) throw new Error('storage');
    } catch { failed = true; try { localStorage.removeItem(KEY); } catch { /* This document stays off. */ } }
    update();
    if (next === 'accept') void visit();
  }
  function audience() {
    let source = 'unknown';
    try {
      const host = new URL(document.referrer).hostname.toLowerCase();
      const groups = { 'www.google.com': 'google', 'google.com': 'google', 'www.bing.com': 'bing', 'bing.com': 'bing',
        'duckduckgo.com': 'duckduckgo', 'www.duckduckgo.com': 'duckduckgo', 'linkedin.com': 'linkedin', 'www.linkedin.com': 'linkedin',
        'lnkd.in': 'linkedin', 'github.com': 'github', 'www.github.com': 'github', 'instagram.com': 'instagram',
        'www.instagram.com': 'instagram', 'l.instagram.com': 'instagram', 'x.com': 'x', 'www.x.com': 'x', 't.co': 'x', 'twitter.com': 'x' };
      source = host === location.hostname ? 'unknown' : groups[host] || 'other';
    } catch { /* Full referrer and query never leave this tab. */ }
    const ua = navigator.userAgent || '';
    return { language: ['en','es','pt-BR'].includes(document.documentElement.lang) ? document.documentElement.lang : 'en',
      device: !ua ? 'unknown' : /iPad|Tablet|Android(?!.*Mobile)/i.test(ua) ? 'tablet' : /Mobile|iPhone|iPod|Android/i.test(ua) ? 'mobile' : 'desktop', source };
  }
  async function visit() {
    if (attempted || !permitted()) return;
    attempted = true;
    const controller = new AbortController(); pending = controller;
    const timeout = setTimeout(() => controller.abort(), 3000);
    try {
      const options = { credentials: 'omit', cache: 'no-store', redirect: 'error', referrerPolicy: 'no-referrer', signal: controller.signal };
      const response = await fetch(ENDPOINT + '/config', options);
      if (!response.ok || !permitted()) return;
      const config = await response.json();
      if (!Number.isFinite(Date.parse(config.expiresAt)) || config.policy !== POLICY || config.enabled !== true || !Number.isSafeInteger(config.version) || config.version < 1 || Date.parse(config.expiresAt) <= Date.now() || config.retentionDays !== 30 || config.dailyLimit !== 1000) { state('paused'); return; }
      if (!permitted()) return;
      await fetch(ENDPOINT, { ...options, method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ policy: POLICY, consent: true, version: config.version, ...audience() }) });
    } catch { /* Optional counting never blocks the toolkit and is never retried. */ }
    finally { clearTimeout(timeout); if (pending === controller) pending = null; }
  }
  accept.addEventListener('click', () => save('accept'));
  reject.addEventListener('click', () => save('reject'));
  window.addEventListener('storage', event => { if (event.key === KEY || event.key === null) { pending?.abort(); update(); } });
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') pending?.abort(); else { update(); void visit(); } });
  window.addEventListener('pagehide', () => { pending?.abort(); clearTimeout(expiry); });
  document.addEventListener('weekly-language-change', () => { ready = true; update(); void visit(); });
  update(); void visit();
})();
