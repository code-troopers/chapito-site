#!/usr/bin/env python3
"""Étape 2 (exécutée une fois) : découpe les pages aspirées (import/) en sources Eleventy (src/).

- le menu, le pied de page, les styles globaux et les scripts communs deviennent des partials ;
- chaque page devient un fichier .njk : front matter (titre, description…) + blocs HTML propres à la page.
Après cette étape, src/ est la source de vérité : on édite src/, pas import/.
"""
import hashlib, re
from pathlib import Path
from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
IMP = ROOT / 'import'
SRC = ROOT / 'src'
INC = SRC / '_includes'
PAGES = ['index', 'solutions', 'realisations', 'partners', 'pricing', 'privacy', '404']
URLS = {'index': '/', '404': '/404', **{p: f'/{p}' for p in PAGES if p not in ('index', '404')}}


def soup(name):
    return BeautifulSoup((IMP / f'{name}.html').read_text(), 'html.parser')


def md5(x):
    return hashlib.md5(str(x).encode()).hexdigest()


def strip_current(html):
    html = html.replace(' aria-current="page"', '')
    return re.sub(r'\s*w--current', '', html)


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# --- scripts présents sur toutes les pages (hors bundles Webflow propres à chaque page)
bodies = {p: soup(p) for p in PAGES}
script_sets = [set(md5(s) for s in b.body.find_all(['script', 'style'], recursive=False)) for b in bodies.values()]
common = set.intersection(*script_sets)

INC.mkdir(parents=True, exist_ok=True)
(INC / 'partials').mkdir(exist_ok=True)
ref = bodies['solutions']

# partials extraits d'une page de référence (sans l'état « lien actif », recalculé au build)
(INC / 'partials' / 'navbar.njk').write_text(strip_current(str(ref.select_one('.navbar-2'))) + '\n')
(INC / 'partials' / 'footer.njk').write_text(strip_current(str(ref.select_one('.main-wrapper > .footer'))) + '\n')
(INC / 'partials' / 'global-styles.njk').write_text(str(ref.select_one('.global-styles')) + '\n')

common_tail = []
for el in ref.body.find_all(['script', 'style'], recursive=False):
    if md5(el) in common and 'jquery' not in str(el):
        common_tail.append(str(el))
(INC / 'partials' / 'scripts-common.njk').write_text('\n'.join(common_tail) + '\n')

for name in PAGES:
    s = bodies[name]
    head = s.head
    title = head.title.get_text() if head.title else 'Chapitô'
    desc_el = head.find('meta', attrs={'name': 'description'})
    desc = desc_el['content'] if desc_el else ''
    wf_page = s.html.get('data-wf-page', '')
    # styles d'état initial des interactions (propres à la page)
    head_extra = ''.join(str(st) for st in head.find_all('style'))

    body = s.body
    wrapper = body.select_one('.page-wrapper')
    before = ''.join(str(e) for e in body.find_all(recursive=False) if 'popup-overlay' in (e.get('class') or []))
    wf_scripts, tail = [], []
    for el in body.find_all(['script', 'style'], recursive=False):
        txt = str(el)
        if md5(el) in common or 'jquery-3.5.1' in txt or '<title>Document</title>' in txt:
            continue
        (wf_scripts if 'webflow.' in txt and '/assets/js/' in txt else tail).append(txt)

    if wrapper is not None:
        main = wrapper.select_one('.main-wrapper')
        main.select_one(':scope > .footer').decompose()
        main_html = main.decode_contents()
        wrapper_cls = ' '.join(c for c in wrapper.get('class', []) if c != 'page-wrapper')
    else:  # page 404 (utility page)
        main_html = ''.join(str(e) for e in body.find_all(recursive=False) if e.name not in ('script', 'style'))
        wrapper_cls = ''

    fm = ['---', f'title: {yaml_str(title)}', f'description: {yaml_str(desc)}', f'wfPage: "{wf_page}"',
          f'permalink: "{"/index.html" if name == "index" else f"/{name}.html"}"', f'url: "{URLS[name]}"']
    if wrapper_cls:
        fm.append(f'wrapperClass: "{wrapper_cls}"')
    if name == '404':
        fm += ['layoutMode: "utility"', 'sitemap: false']
    fm.append('---')
    out = '\n'.join(fm) + '\n{% extends "base.njk" %}\n'
    if head_extra:
        out += '{% block head %}\n' + head_extra + '\n{% endblock %}\n'
    if before:
        out += '{% block before %}\n' + before + '\n{% endblock %}\n'
    out += '{% block main %}\n' + main_html + '\n{% endblock %}\n'
    out += '{% block webflow %}\n' + '\n'.join(wf_scripts) + '\n{% endblock %}\n'
    if tail:
        out += '{% block scripts %}\n' + '\n'.join(tail) + '\n{% endblock %}\n'
    (SRC / f'{name}.njk').write_text(out)
    print(f'{name}: main {len(main_html)} car., {len(wf_scripts)} bundles Webflow, {len(tail)} scripts propres')
