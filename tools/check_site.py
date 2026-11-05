#!/usr/bin/env python3
"""Revisión de integridad del proyecto; usa exclusivamente Python estándar."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import sys
import hashlib
import base64
ROOT = Path(__file__).resolve().parent.parent / 'public'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inline_scripts=[]; self.script_text=None; self.policy=""; self.targets=[];self.h1=0;self.title=0;self.meta_description=0;self.bad=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.title += 1
        if tag == 'meta' and a.get('name') == 'description': self.meta_description += 1
        if 'id' in a: self.ids.append(a['id'])
        if 'style' in a or any(k.startswith('on') for k in a): self.bad.append((tag,'inline-style/handler'))
        if tag == 'meta' and a.get('http-equiv') == 'Content-Security-Policy': self.policy = a.get('content', '')
        if tag == 'script' and 'src' not in a: self.script_text = ''
        for key in ('href','src'):
            if key in a and tag in ('a','link','script','img','use'):
                self.targets.append((tag,a[key]))

    def handle_data(self, data):
        if self.script_text is not None: self.script_text += data
    def handle_endtag(self, tag):
        if tag == 'script' and self.script_text is not None:
            self.inline_scripts.append(self.script_text)
            self.script_text = None

errors=[]
for p in ROOT.rglob('*.html'):
    page=Page();page.feed(p.read_text(encoding='utf-8'))
    for script in page.inline_scripts:
        digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
        if p != ROOT/'index.html' or f"'sha256-{digest}'" not in page.policy or "'strict-dynamic'" not in page.policy:
            errors.append(f'{p}: script inline sin autorización CSP exacta')
    if not page.policy: errors.append(f'{p}: falta CSP de página')
    if page.title!=1: errors.append(f'{p}: falta/duplica <title>')
    if page.h1!=1: errors.append(f'{p}: encabezados h1: {page.h1}')
    if page.meta_description!=1: errors.append(f'{p}: falta meta descripción')
    if len(page.ids)!=len(set(page.ids)): errors.append(f'{p}: ID duplicado')
    for tag,issue in page.bad: errors.append(f'{p}: {tag}: {issue}')
    for tag,target in page.targets:
        if target.startswith(('http:','https:','mailto:','#','data:')): continue
        filename=unquote(target.split('#')[0].split('?')[0])
        if not filename: continue
        candidate=((ROOT / filename.lstrip('/')) if filename.startswith('/') else (p.parent / filename)).resolve()
        if candidate.is_dir(): candidate/= 'index.html'
        if not candidate.is_relative_to(ROOT.resolve()):errors.append(f'{p}: enlace fuera del sitio {target}')
        elif not candidate.is_file():errors.append(f'{p}: destino inexistente {target}')

headers=ROOT/'_headers'
if not headers.exists():errors.append('Falta _headers')
elif 'Content-Security-Policy:' not in headers.read_text():errors.append('Falta Content-Security-Policy en _headers')
print(f'Páginas HTML: {len(list(ROOT.rglob("*.html")))}. Problemas detectados: {len(errors)}')
for e in errors: print('ERROR:',e)
sys.exit(1 if errors else 0)
