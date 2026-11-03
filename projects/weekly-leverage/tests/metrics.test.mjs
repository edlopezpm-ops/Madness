// (kommiBo) Actual request boundary and optional-choice behavior; no provider effects.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import worker from '../hosting/worker.mjs';
const origin = 'https://aekr.io', path = '/weekly-leverage/api/metrics';
const value = () => ({policy:'2026-11-03-weekly-v1',consent:true,version:1,language:'pt-BR',device:'mobile',source:'x'});
function request(body=value(),headers={},route=path,method='POST') {
  const req = new Request(origin+route,{method,headers:{Origin:origin,'Sec-Fetch-Site':'same-origin','Content-Type':'application/json',...headers},...(method==='POST'?{body:typeof body==='string'?body:JSON.stringify(body)}:{})});
  Object.defineProperty(req,'cf',{value:{country:'CL'}}); return req;
}
test('public metrics route forwards only validated categories plus edge-derived country',async () => {
  const seen=[];
  const response=await worker.fetch(request(),{WEEKLY_METRICS:{async record(v){seen.push(v);return 204;}}});
  assert.equal(response.status,204);assert.equal(response.headers.has('set-cookie'),false);assert.match(response.headers.get('cache-control'),/no-store/);
  assert.deepEqual(seen,[{...value(),country:'CL'}]);
  assert.equal((await worker.fetch(request({...value(),country:'US'}),{WEEKLY_METRICS:{}})).status,400);
});
test('origin/privacy/cookie/auth/method/query/unknown-route failures never reach the service',async () => {
  let calls=0;const env={WEEKLY_METRICS:{async record(){calls++;return 204;},async config(){calls++;return {};}}};
  for(const headers of [{Origin:'https://evil.invalid'},{'Sec-Fetch-Site':'same-site'},{Cookie:'owner=synthetic'},{Authorization:'Bearer synthetic'},{'Sec-GPC':'1'},{DNT:'1'}])assert.equal((await worker.fetch(request(value(),headers),env)).status,403);
  assert.equal((await worker.fetch(request(value(),{},path+'?x=1'),env)).status,400);
  assert.equal((await worker.fetch(request(value(),{},path+'/unknown'),env)).status,404);
  assert.equal((await worker.fetch(request(value(),{},path,'GET'),env)).status,405);assert.equal(calls,0);
});
test('malformed, oversized and unknown-field bodies fail closed; missing service is unavailable',async () => {
  const env={WEEKLY_METRICS:{async record(){throw new Error('should not reach');}}};
  assert.equal((await worker.fetch(request('{'),env)).status,400);
  assert.equal((await worker.fetch(request('x'.repeat(513)),env)).status,413);
  assert.equal((await worker.fetch(request(value(),{'Content-Type':'text/plain'}),env)).status,415);
  assert.equal((await worker.fetch(request({...value(),context:'SECRET'}),env)).status,400);
  assert.equal((await worker.fetch(request(),{})).status,503);
});
function browser(options={}) {
  const events={},windowEvents={},requests=[],storage=new Map(),listeners={};let current=Date.now();
  const saved=options.saved; if(saved)storage.set('weekly-leverage-analytics-v1',JSON.stringify(saved));
  const states=['off','accepted','signal','failed','paused'].map(name=>({dataset:{metricsState:name},hidden:true}));
  const accept={disabled:true,addEventListener(_name,fn){listeners.accept=fn;}},reject={disabled:true,addEventListener(_name,fn){listeners.reject=fn;}};
  const control={querySelector(selector){return selector.includes('accept')?accept:reject;},querySelectorAll(){return states;}};
  const document={visibilityState:'visible',referrer:'https://t.co/private?secret=CANARY',documentElement:{lang:options.lang||'es'},querySelector(selector){return selector.includes('controls')?control:{disabled:false};},addEventListener(name,fn){events[name]=fn;}};
  const window={addEventListener(name,fn){windowEvents[name]=fn;}};
  const timers=new Map();let id=0;
  const context={document,window,navigator:{userAgent:'Synthetic Mobile',globalPrivacyControl:options.gpc,doNotTrack:options.dnt},location:{hostname:'aekr.io'},localStorage:{getItem(key){if(options.readFail)throw Error('unavailable');return storage.get(key)||null;},setItem(key,value){if(options.writeFail)throw Error('unavailable');storage.set(key,value);},removeItem(key){storage.delete(key);}},Date:class extends Date{static now(){return current;}},URL,AbortController,setTimeout(fn){timers.set(++id,fn);return id;},clearTimeout(key){timers.delete(key);},async fetch(url,init){requests.push({url,init});if(options.delayConfig&&url.endsWith('config'))await options.delayConfig;return {ok:true,async json(){return {policy:'2026-11-03-weekly-v1',enabled:!options.paused,version:1,expiresAt:options.invalidExpiry ? 'invalid' : new Date(current+300000).toISOString(),retentionDays:30,dailyLimit:1000};}};}};
  vm.runInNewContext(readFileSync(new URL('../usage.js',import.meta.url),'utf8'),context);
  return {requests,storage,accept,reject,states,document,events,windowEvents,allow:()=>listeners.accept(),deny:()=>listeners.reject(),advance(ms){current+=ms;}};
}
const flush=()=>new Promise(resolve=>setImmediate(resolve));
const saved=()=>({policy:'2026-11-03-weekly-v1',choice:'accept',expires:Date.now()+10000});
test('no consent sends nothing; explicit opt-in sends exactly one closed view without credentials or referrer text',async () => {
  const b=browser();await flush();assert.equal(b.requests.length,0);b.allow();await flush();
  assert.equal(b.requests.length,2);const post=b.requests[1];assert.equal(post.init.credentials,'omit');assert.equal(post.init.referrerPolicy,'no-referrer');
  const body=JSON.parse(post.init.body);assert.deepEqual(Object.keys(body).sort(),Object.keys(value()).sort());assert.equal(body.language,'es');assert.equal(body.source,'x');assert(!post.init.body.includes('CANARY'));
  b.allow();b.events['visibilitychange']();await flush();assert.equal(b.requests.filter(r=>r.init.method==='POST').length,1);
});
test('refusal, privacy signals, expiry, hidden documents and storage failures never send events',async () => {
  for(const options of [{gpc:true,saved:saved()},{dnt:'1',saved:saved()},{readFail:true,saved:saved()},{saved:{...saved(),expires:Date.now()-1}}]){const b=browser(options);await flush();assert.equal(b.requests.length,0);}
  const denied=browser();denied.deny();await flush();assert.equal(denied.requests.length,0);
  const failure=browser({writeFail:true});failure.allow();await flush();assert.equal(failure.requests.length,0);assert.equal(failure.storage.size,0);
  const hidden=browser();hidden.document.visibilityState='hidden';hidden.allow();await flush();assert.equal(hidden.requests.length,0);
});
test('withdrawal in another tab while configuration is pending stops the prospective view',async () => {
  let finish;const delayConfig=new Promise(resolve=>finish=resolve),b=browser({delayConfig});b.allow();await flush();
  b.storage.clear();b.windowEvents.storage({key:'weekly-leverage-analytics-v1'});finish();await flush();
  assert.equal(b.requests.filter(r=>r.init.method==='POST').length,0);
});
test('current-language labels are sent after opt-in in all three locales; central pause sends no event',async () => {
  for(const lang of ['en','es','pt-BR']){const b=browser({lang});b.allow();await flush();assert.equal(JSON.parse(b.requests[1].init.body).language,lang);}
  const paused=browser({paused:true});paused.allow();await flush();assert.equal(paused.requests.filter(r=>r.init.method==='POST').length,0);assert.equal(paused.states.find(s=>s.dataset.metricsState==='paused').hidden,false);
});

test('malformed central configuration expiry fails closed without a view',async()=>{
  const b=browser({invalidExpiry:true});b.allow();await flush();assert.equal(b.requests.filter(r=>r.init.method==='POST').length,0);
});
