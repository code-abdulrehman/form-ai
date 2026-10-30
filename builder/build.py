#!/usr/bin/env python3
"""Regenerate the FORM / AI app: index.html at the project root + PWA assets
(manifest.webmanifest, sw.js, icons/). Sources stay in builder/."""
import json
import time
from pathlib import Path

# builder/ sources
root = Path(__file__).resolve().parent
# project root — the distributable tree (index.html must live here)
dist = root.parent

# ---------- assemble index.html ----------
html = (root / 'template.html').read_text(encoding='utf-8')
html = html.replace('/* INJECT_STYLES */', (root / 'styles.css').read_text(encoding='utf-8'))
weeks = json.loads((root / 'curriculum.json').read_text(encoding='utf-8'))
snippets = json.loads((root / 'snippets.json').read_text(encoding='utf-8'))
assert len(weeks) == 9 and sum(len(w['days']) for w in weeks) == 63
assert len(snippets) == 63
challenges = json.loads((root / 'challenge_snippets.json').read_text(encoding='utf-8'))
assert len(challenges) == 63
js_data = 'const WEEKS = ' + json.dumps(weeks, ensure_ascii=False, separators=(',', ':')) + ';\n'
js_data += 'const SNIPPETS = ' + json.dumps(snippets, ensure_ascii=False, separators=(',', ':')) + ';\n'
js_data += 'const CHALLENGES = ' + json.dumps(challenges, ensure_ascii=False, separators=(',', ':')) + ';'
html = html.replace('/* INJECT_DATA */', js_data)
html = html.replace('/* INJECT_LABS */', (root / 'extra_labs.js').read_text(encoding='utf-8'))
html = html.replace('/* INJECT_APP */', (root / 'app.js').read_text(encoding='utf-8'))
(dist / 'index.html').write_text(html, encoding='utf-8')
print('Generated:', dist / 'index.html')

# ---------- PWA icons (needs Pillow; skipped gracefully without it) ----------
ICONS = {
    'icon-192.png': (192, False),
    'icon-512.png': (512, False),
    'icon-180.png': (180, False),      # apple-touch-icon
    'icon-maskable-192.png': (192, True),
    'icon-maskable-512.png': (512, True),
}
BG = (15, 23, 42, 255)      # slate-900
FG = (193, 147, 168, 255)   # mauve-400

def make_icon(size, maskable):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        # full-bleed slate background, glyph inside the 80% safe circle
        d.rectangle([0, 0, size - 1, size - 1], fill=BG)
        d.ellipse([size * .08, size * .08, size * .92, size * .92],
                  fill=(23, 33, 52, 255))
        glyph = size * .40
    else:
        # rounded slate square on transparent ground
        r = size // 5
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)
        glyph = size * .52
    font_file = Path('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf')
    if not font_file.exists():
        font_file = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    font = ImageFont.truetype(str(font_file), int(glyph))
    d.text((size / 2, size / 2), '\u0192', font=font, fill=FG, anchor='mm')
    return img

icons_ok = True
icons_dir = dist / 'icons'
icons_dir.mkdir(exist_ok=True)
try:
    for name, (size, maskable) in ICONS.items():
        make_icon(size, maskable).save(icons_dir / name)
except ImportError:
    icons_ok = False
    print('Pillow not available — PWA icons skipped (manifest written without icons).')
print('Icons:', ', '.join(f'icons/{n}' for n in ICONS) if icons_ok else 'skipped')

# ---------- manifest.webmanifest ----------
manifest = {
    'name': 'FORM / AI — Independent Research Learning System',
    'short_name': 'FORM / AI',
    'description': 'Independent AI learning LMS: 63 lessons, quizzes, labs and local progress tracking.',
    'start_url': './index.html',
    'scope': './',
    'display': 'standalone',
    'background_color': '#0f172a',
    'theme_color': '#0f172a',
    'icons': [],
}
if icons_ok:
    manifest['icons'] = [
        {'src': './icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': './icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': './icons/icon-maskable-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'maskable'},
        {'src': './icons/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ]
(dist / 'manifest.webmanifest').write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
print('Generated:', dist / 'manifest.webmanifest')

# ---------- sw.js (offline app shell; CDN assets cached at runtime) ----------
stamp = time.strftime('%Y%m%d-%H%M%S')
shell = ['./', './index.html', './manifest.webmanifest']
if icons_ok:
    shell += [f'./icons/{n}' for n in ICONS]
cdn = [
    'https://unpkg.com/lucide@0.468.0/dist/umd/lucide.js',
    'https://cdn.jsdelivr.net/npm/chart.js@4.5.1/dist/chart.umd.min.js',
    'https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap',
]
shell_js = json.dumps(shell)
cdn_js = json.dumps(cdn)
sw = f"""const CACHE='form-ai-{stamp}';
const SHELL={shell_js};
const CDN={cdn_js};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{if(e.request.method!=='GET')return;const url=new URL(e.request.url);
 const nav=e.request.mode==='navigate'||(url.origin===location.origin&&/\\/(index\\.html)?$/.test(url.pathname));
 if(nav){{/* app shell: network-first so updates land immediately; cached copy only when offline */
  e.respondWith(fetch(e.request).then(res=>{{const copy=res.clone();caches.open(CACHE).then(c=>c.put('./index.html',copy)).catch(()=>{{}});return res}}).catch(()=>caches.match('./index.html').then(h=>h||caches.match('./'))));return}}
 if(url.origin===location.origin){{/* static assets: cache-first */
  e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(res=>{{const copy=res.clone();caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{{}});return res}}).catch(()=>caches.match('./index.html'))));return}}
 if(!CDN.some(u=>url.origin===new URL(u).origin))return;
 e.respondWith(caches.match(e.request).then(hit=>hit||fetch(e.request).then(res=>{{if(res.ok){{const copy=res.clone();caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{{}})}}return res}})))}});
"""
(dist / 'sw.js').write_text(sw, encoding='utf-8')
print('Generated:', dist / 'sw.js', f'(cache form-ai-{stamp})')
