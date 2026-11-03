// (kommiBo) Only the two opt-in metrics routes execute code; assets stay native.
const ROOT = '/weekly-leverage/api/metrics';
const POLICY = '2026-11-03-weekly-v1';
const HEADERS = {
  'Cache-Control': 'no-store, no-transform', 'X-Content-Type-Options': 'nosniff',
  'Strict-Transport-Security': 'max-age=15552000', 'Referrer-Policy': 'no-referrer',
  'X-Frame-Options': 'DENY', 'Cross-Origin-Opener-Policy': 'same-origin',
  'Content-Security-Policy': "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=()',
};
const reply = (status, value) => new Response(value === undefined ? null : JSON.stringify(value),
  { status, headers: { ...HEADERS, ...(value === undefined ? {} : { 'Content-Type': 'application/json; charset=utf-8' }) } });
const keys = ['policy', 'consent', 'version', 'language', 'device', 'source'];
export function validPublic(value) {
  return value && typeof value === 'object' && !Array.isArray(value) && Object.keys(value).length === keys.length &&
    keys.every(key => Object.hasOwn(value, key)) && value.policy === POLICY && value.consent === true &&
    Number.isSafeInteger(value.version) && value.version > 0 && ['en', 'es', 'pt-BR'].includes(value.language) &&
    ['desktop', 'mobile', 'tablet', 'unknown'].includes(value.device) &&
    ['google', 'bing', 'duckduckgo', 'linkedin', 'github', 'instagram', 'x', 'other', 'unknown'].includes(value.source);
}
async function readBody(request) {
  if (!/^application\/json(?:\s*;\s*charset=utf-8)?$/i.test(request.headers.get('content-type') || '')) throw 415;
  const length = request.headers.get('content-length');
  if (length !== null && (!/^\d+$/.test(length) || Number(length) > 512)) throw 413;
  const reader = request.body?.getReader();
  if (!reader) throw 400;
  let size = 0, text = '', timer;
  const decoder = new TextDecoder('utf-8', { fatal: true });
  const deadline = new Promise((_, reject) => { timer = setTimeout(() => reject(408), 3000); });
  try {
    while (true) {
      const part = await Promise.race([reader.read(), deadline]);
      if (part.done) break;
      size += part.value.byteLength;
      if (size > 512) throw 413;
      text += decoder.decode(part.value, { stream: true });
    }
    return JSON.parse(text + decoder.decode());
  } catch (error) { throw [408, 413, 415].includes(error) ? error : 400; } finally { clearTimeout(timer); void reader.cancel().catch(() => {}); reader.releaseLock(); }
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.origin !== 'https://aekr.io') return reply(404);
    if (![ROOT, ROOT + '/config'].includes(url.pathname)) return env.ASSETS ? env.ASSETS.fetch(request) : reply(404);
    if (url.search) return reply(400);
    const config = url.pathname.endsWith('/config');
    if (request.method !== (config ? 'GET' : 'POST')) return reply(405);
    if (request.headers.get('sec-fetch-site') !== 'same-origin' ||
        request.headers.has('origin') && request.headers.get('origin') !== url.origin ||
        !config && request.headers.get('origin') !== url.origin ||
        request.headers.has('cookie') || request.headers.has('authorization') ||
        request.headers.get('sec-gpc') === '1' || request.headers.get('dnt') === '1') return reply(403);
    if (!env.WEEKLY_METRICS) return reply(503);
    try {
      if (config) return reply(200, await env.WEEKLY_METRICS.config());
      const value = await readBody(request);
      if (!validPublic(value)) return reply(400);
      // Client country fields are forbidden. Only Cloudflare edge geography enters the service.
      const country = /^[A-Z]{2}$/.test(request.cf?.country || '') ? request.cf.country : 'unknown';
      const status = await env.WEEKLY_METRICS.record({ ...value, country });
      return reply([204, 400, 409, 429, 503].includes(status) ? status : 503);
    } catch (error) { return reply([400, 408, 413, 415].includes(error) ? error : error instanceof SyntaxError ? 400 : 503); }
  },
};
