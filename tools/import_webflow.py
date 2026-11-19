#!/usr/bin/env python3
"""Aspiration du site Webflow publié (chapi.to) vers des fichiers statiques autonomes.

- télécharge les pages publiées (contenu CMS inclus, tel que rendu par Webflow) ;
- rapatrie toutes les ressources (CDN Webflow, jQuery, GSAP, Finsweet, polices Google) dans assets/ ;
- réécrit les URL en chemins locaux.
Sortie : import/<page>.html + public/assets/…  (étape 1 de la migration, relancer = repartir de zéro)
"""
import hashlib, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_HTML = ROOT / 'import'
ASSETS = ROOT / 'public' / 'assets'
BASE = 'https://chapi.to'
PAGES = {'index': '/', 'solutions': '/solutions', 'realisations': '/realisations', 'partners': '/partners',
         'pricing': '/pricing', 'privacy': '/privacy', '404': '/page-inexistante-404'}
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
HOSTS = r'(?:cdn\.prod\.website-files\.com|uploads-ssl\.webflow\.com|d3e54v103j8qbb\.cloudfront\.net|cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net|ajax\.googleapis\.com)'
URL_HTML = re.compile(r'https?://' + HOSTS + r'/[^"\'\s,<>]+')
URL_CSS = re.compile(r'url\(\s*["\']?(https?://' + HOSTS + r'/[^"\')]+)["\']?\s*\)')
cache = {}
missing = []


def get(url, binary=True):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404 and '404' in url:
            data = e.read()
        else:
            raise
    return data if binary else data.decode('utf-8')


def local_name(url):
    u = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(u.path)
    name = re.sub(r'[^A-Za-z0-9._-]+', '-', os.path.basename(path)).strip('-') or 'index'
    ext = os.path.splitext(name)[1].lower()
    if u.netloc.endswith('website-files.com') or 'webflow.com' in u.netloc:
        parts = u.path.strip('/').split('/')
        sub = 'cms' if parts[0] != '669562b12cd180ce7d9ce6fc' else ('css' if ext == '.css' else 'js' if ext == '.js' else 'img')
    else:
        sub = 'vendor'
    if u.query:  # ex. jquery ?site=…
        name = name
    return f'{sub}/{name}'


def fetch_asset(url):
    url = url.replace('&amp;', '&')
    if url in cache:
        return cache[url]
    rel = local_name(url)
    dst = ASSETS / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        try:
            data = get(url)
        except urllib.error.HTTPError as e:
            print(f'⚠ {e.code} {url} (URL conservée telle quelle)')
            missing.append(url)
            cache[url] = None
            return None
        if rel.endswith('.css'):
            css = data.decode('utf-8')
            css = URL_CSS.sub(lambda m: f'url("/assets/{r}")' if (r := fetch_asset(m.group(1))) else m.group(0), css)
            data = css.encode('utf-8')
        dst.write_bytes(data)
    cache[url] = rel
    return rel


def google_fonts_css():
    css = get('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap', binary=False)
    def dl(m):
        url = m.group(1)
        name = 'poppins-' + hashlib.md5(url.encode()).hexdigest()[:10] + '.woff2'
        dst = ASSETS / 'fonts' / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            dst.write_bytes(get(url))
        return f'url("/assets/fonts/{name}")'
    css = re.sub(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', dl, css)
    (ASSETS / 'css').mkdir(parents=True, exist_ok=True)
    (ASSETS / 'css' / 'fonts.css').write_text(css)


def clean(html):
    # Weglot (traduction anglaise abandonnée)
    html = re.sub(r'<script[^>]*weglot[^>]*></script>', '', html)
    html = re.sub(r'<script[^>]*>\s*Weglot\.initialize\(.*?</script>', '', html, flags=re.S)
    # chargeur Google Fonts → polices locales
    html = re.sub(r'<script[^>]*webfont\.js[^>]*></script>', '', html)
    html = re.sub(r'<script[^>]*>\s*WebFont\.load\(.*?</script>', '<link href="/assets/css/fonts.css" rel="stylesheet" type="text/css"/>', html, flags=re.S)
    html = re.sub(r'<link[^>]+fonts\.(googleapis|gstatic)\.com[^>]*>', '', html)
    # script de protection propre à l'hébergement Webflow/Cloudflare
    html = re.sub(r'<script[^>]*src="/[0-9A-Za-z]{20,}/[^"]+"[^>]*></script>', '', html)
    html = re.sub(r'<link[^>]+rel="preconnect"[^>]*website-files[^>]*>', '', html)
    html = re.sub(r'<link[^>]+rel="dns-prefetch"[^>]*>', '', html)
    return html


def main():
    OUT_HTML.mkdir(exist_ok=True)
    google_fonts_css()
    for name, path in PAGES.items():
        html = get(BASE + path, binary=False)
        html = clean(html)
        html = URL_HTML.sub(lambda m: ('/assets/' + r) if (r := fetch_asset(m.group(0))) else m.group(0), html)
        (OUT_HTML / f'{name}.html').write_text(html)
        print(f'{name}: {len(html)} car.', flush=True)
    # les JS Webflow peuvent référencer d'autres URL distantes
    for js in (ASSETS / 'js').glob('*.js'):
        if re.search(HOSTS, js.read_text(errors='ignore')):
            print('⚠ URL distante dans', js.name)
    n = sum(1 for _ in ASSETS.rglob('*') if _.is_file())
    size = sum(f.stat().st_size for f in ASSETS.rglob('*') if f.is_file())
    print(f'{n} ressources, {size / 1e6:.1f} Mo')


if __name__ == '__main__':
    main()
