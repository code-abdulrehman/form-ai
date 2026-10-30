const CACHE='form-ai-20261030-195010';
const SHELL=["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-180.png", "./icons/icon-maskable-192.png", "./icons/icon-maskable-512.png"];
const CDN=["https://unpkg.com/lucide@0.468.0/dist/umd/lucide.js", "https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js", "https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;const url=new URL(e.request.url);
 const nav=e.request.mode==='navigate'||(url.origin===location.origin&&/\/(index\.html)?$/.test(url.pathname));
 if(nav){/* app shell: network-first so updates land immediately; cached copy only when offline */
  e.respondWith(fetch(e.request).then(res=>{const copy=res.clone();caches.open(CACHE).then(c=>c.put('./index.html',copy)).catch(()=>{});return res}).catch(()=>caches.match('./index.html').then(h=>h||caches.match('./'))));return}
 if(url.origin===location.origin){/* static assets: cache-first */
  e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(res=>{const copy=res.clone();caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{});return res}).catch(()=>caches.match('./index.html'))));return}
 if(!CDN.some(u=>url.origin===new URL(u).origin))return;
 e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(res=>{if(res.ok){const copy=res.clone();caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{})}return res})))});
