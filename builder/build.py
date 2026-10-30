#!/usr/bin/env python3
"""Regenerate the single-file app into the project root from sources in this builder folder."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent            # builder/ — holds the editable sources
out = root.parent / 'index.html'                  # project root — where index.html is served
html = (root / 'template.html').read_text(encoding='utf-8')
weeks = json.loads((root / 'curriculum.json').read_text(encoding='utf-8'))
snippets = json.loads((root / 'snippets.json').read_text(encoding='utf-8'))
assert len(weeks)==9 and sum(len(w['days']) for w in weeks)==63
assert len(snippets)==63
js_data = 'const WEEKS = ' + json.dumps(weeks, ensure_ascii=False, separators=(',', ':')) + ';\n'
js_data += 'const SNIPPETS = ' + json.dumps(snippets, ensure_ascii=False, separators=(',', ':')) + ';'
html = html.replace('/* INJECT_DATA */', js_data)
html = html.replace('/* INJECT_APP */', (root / 'app.js').read_text(encoding='utf-8'))
out.write_text(html, encoding='utf-8')
print('Generated:', out)
