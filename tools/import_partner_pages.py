#!/usr/bin/env python3
"""Import ponctuel des 4 pages partenaires de Webflow oubliées lors de la migration.

Réutilise tools/import_webflow.py (téléchargement des ressources, réécriture des URL),
puis découpe chaque page comme les autres : content/<page>.html + CSS/JS propres à la page.
Ne plus relancer une fois ces pages modifiées (écraserait).
"""
import re, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import import_webflow as iw  # noqa: E402

iw.ASSETS = ROOT / 'static' / 'assets'
SLUGS = ['yurplan', 'partenaire-heeds', 'wilout', 'partenaire-spotify', 'partenaire-deezer']
COMMON = (ROOT / 'layouts/partials/scripts-common.html').read_text() + (ROOT / 'layouts/partials/scripts-webflow-common.html').read_text()


def norm(s):
    return re.sub(r'\s+', '', s)


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


for slug in SLUGS:
    html = iw.get(f'{iw.BASE}/{slug}', binary=False)
    html = iw.clean(html)
    html = iw.URL_HTML.sub(lambda m: ('/assets/' + r) if (r := iw.fetch_asset(m.group(0))) else m.group(0), html)
    s = BeautifulSoup(html, 'html.parser')
    title = s.head.title.get_text()
    desc = (s.head.find('meta', attrs={'name': 'description'}) or {}).get('content', '')
    wf_page = s.html.get('data-wf-page', '')

    css = [],
    styles = ''.join(st.get_text() for st in s.head.find_all('style'))

    webflow, inline, vendor = [], [], []
    for el in s.body.find_all(['script', 'style'], recursive=False):
        txt = str(el)
        src = el.get('src', '')
        if 'jquery-3.5.1' in src:
            continue
        if src.startswith('/assets/js/webflow.'):
            webflow.append(src.rsplit('/', 1)[1])
        elif el.name == 'script' and not src and 'language-switcher-link' in el.get_text():
            continue  # sélecteur de langue Weglot (abandonné)
        elif el.name == 'script' and not src and norm(el.get_text()) and norm(el.get_text()) not in norm(COMMON):
            inline.append(el.get_text().strip())
        elif el.name == 'style' and norm(el.get_text()) not in norm(COMMON):
            styles += '\n' + el.get_text()
        elif src and src not in COMMON:
            vendor.append(src)
    css_files = []
    if styles.strip():
        (ROOT / f'static/assets/css/pages/{slug}.css').write_text(styles.strip() + '\n')
        css_files.append(f'/assets/css/pages/{slug}.css')
    js_files = list(vendor)
    if inline:
        p = ROOT / f'static/assets/js/pages/{slug}.js'
        p.write_text('\n\n'.join(inline) + '\n')
        js_files.append(f'/assets/js/pages/{slug}.js')

    wrapper = s.select_one('.page-wrapper')
    main = wrapper.select_one('.main-wrapper')
    main.select_one(':scope > .footer').decompose()
    body = main.decode_contents().strip()
    body = body.replace(' aria-current="page"', '')
    body = re.sub(r'\s*w--current', '', body)
    wrapper_cls = ' '.join(c for c in wrapper.get('class', []) if c != 'page-wrapper')

    fm = ['---', f'title: {yaml_str(title)}', f'description: {yaml_str(desc)}', f'wfPage: "{wf_page}"']
    if wrapper_cls:
        fm.append(f'wrapperClass: "{wrapper_cls}"')
    for key, vals in (('css', css_files), ('webflow', webflow), ('scripts', js_files)):
        if vals:
            fm.append(f'{key}:')
            fm += [f'  - "{v}"' for v in vals]
    fm.append('---')
    (ROOT / f'content/{slug}.html').write_text('\n'.join(fm) + '\n' + body + '\n')
    print(f'{slug}: {title} | wfPage {wf_page} | webflow {webflow} | css {css_files} | js {js_files} | {len(body)} car.')
print('ressources manquantes :', iw.missing)
