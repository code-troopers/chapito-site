#!/usr/bin/env python3
"""Conversion ponctuelle de la version Eleventy (src/) vers Hugo (content/, layouts/, static/).

- chaque page : le bloc main devient content/<page>.html, les autres blocs passent dans l'en-tête ;
- styles et scripts propres à une page déplacés dans static/assets/{css,js}/pages/ ;
- base.njk et les partials deviennent layouts/_default/baseof.html et layouts/partials/.
Ne plus relancer une fois content/ modifié (écraserait).
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
PAGES = ['index', 'solutions', 'realisations', 'partners', 'pricing', 'privacy', 'camping']


def blocks(text):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r'{% block (\w+) %}(.*?){% endblock %}', text, re.S)}


def front_matter(text):
    fm = text.split('---', 2)[1]
    out = {}
    for line in fm.strip().splitlines():
        k, v = line.split(':', 1)
        out[k.strip()] = json.loads(v.strip()) if v.strip().startswith('"') else v.strip()
    return out


def yaml_str(v):
    return json.dumps(v, ensure_ascii=False)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


for name in PAGES:
    text = (SRC / f'{name}.njk').read_text()
    fm, b = front_matter(text), blocks(text)
    css, js, webflow, extra = [], [], [], {}

    head = b.get('head', '')
    for href in re.findall(r'<link href="([^"]+)" rel="stylesheet"[^>]*>', head):
        css.append(href)
    styles = re.findall(r'<style>(.*?)</style>', head, re.S)
    if styles:
        write(ROOT / f'static/assets/css/pages/{name}.css', '\n'.join(s.strip() for s in styles) + '\n')
        css.append(f'/assets/css/pages/{name}.css')
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    if ld:
        extra['schema'] = ld.group(1).strip()

    webflow = re.findall(r'src="/assets/js/(webflow\.[^"]+)"', b.get('webflow', ''))

    scripts = b.get('scripts', '')
    inline = []
    for m in re.finditer(r'<script([^>]*)>(.*?)</script>', scripts, re.S):
        src = re.search(r'src="([^"]+)"', m.group(1))
        if src:
            js.append(src.group(1))
        else:
            inline.append(m.group(2).strip())
            target = f'/assets/js/pages/{name}.js' if name != 'camping' else '/assets/camping/cal-init.js'
            if target not in js:
                js.insert(len(js) if name != 'camping' else 0, target)
    if inline:
        target = f'static/assets/js/pages/{name}.js' if name != 'camping' else 'static/assets/camping/cal-init.js'
        write(ROOT / target, '\n\n'.join(inline) + '\n')

    if 'before' in b:
        extra['newsletterPopup'] = True
        popup = b['before']
        popup = popup.replace('{% if site.brevoFormAction %}', '{{ with site.Params.brevoFormAction }}')
        popup = popup.replace('{{ site.brevoFormAction }}', '{{ . }}').replace('{% endif %}', '{{ end }}')
        write(ROOT / 'layouts/partials/newsletter-popup.html', popup + '\n')

    lines = ['---', f'title: {yaml_str(fm["title"])}']
    if 'ogTitle' in fm:
        lines.append(f'ogTitle: {yaml_str(fm["ogTitle"])}')
    lines.append(f'description: {yaml_str(fm["description"])}')
    lines.append(f'wfPage: {yaml_str(fm["wfPage"])}')
    if 'ogImage' in fm:
        lines.append(f'ogImage: {yaml_str(fm["ogImage"])}')
    if 'wrapperClass' in fm:
        lines.append(f'wrapperClass: {yaml_str(fm["wrapperClass"])}')
    if name == 'camping':
        lines.append('aliases: ["/campings.html"]')
    if extra.get('newsletterPopup'):
        lines.append('newsletterPopup: true')
    for key, vals in (('css', css), ('webflow', webflow), ('scripts', js)):
        if vals:
            lines.append(f'{key}:')
            lines += [f'  - {yaml_str(v)}' for v in vals]
    if 'schema' in extra:
        lines.append('schema: |')
        lines += ['  ' + l for l in extra['schema'].splitlines()]
    lines.append('---')
    out = 'content/_index.html' if name == 'index' else f'content/{name}.html'
    write(ROOT / out, '\n'.join(lines) + '\n' + b['main'] + '\n')
    print(out, 'css', css, 'webflow', webflow, 'js', js)


# --- partials
NAV_LINK = re.compile(r'<a ([^>]*?)class="([^"]*)"([^>]*?)href="(/[a-z]*)"')


def current(m):
    pre, cls, mid, href = m.groups()
    cond = f'{{{{ if eq $path "{href}" }}}}'
    return f'<a {pre}{cond}aria-current="page" {{{{ end }}}}class="{cls}{cond} w--current{{{{ end }}}}"{mid}href="{href}"'


for p in (SRC / '_includes/partials').glob('*.njk'):
    t = p.read_text()
    t = re.sub(r'{{ site\.(\w+) }}', r'{{ site.Params.\1 }}', t)
    t = t.replace('{% if site.brevoFormAction %}', '{{ if site.Params.brevoFormAction }}').replace('{% endif %}', '{{ end }}')
    if p.stem in ('navbar', 'footer'):
        t = '{{ $path := partial "path.html" . }}\n' + NAV_LINK.sub(current, t)
    assert '{%' not in t, p
    write(ROOT / f'layouts/partials/{p.stem}.html', t)
    print('partial', p.stem)
