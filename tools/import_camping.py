#!/usr/bin/env python3
"""Intègre la landing camping de Nicolas (one-page V2) comme page /camping du site statique.

- images converties en WebP (redimensionnées) dans public/assets/camping/ ;
- seul le contenu <main> est repris : le menu et le pied de page sont ceux du site ;
- textes « consignes à l'IA » restés visibles corrigés, emplacement vidéo remplacé par la vidéo ;
- CSS isolé sous .camping-page par tools/scope_css.mjs (à lancer avant).
Usage : python3 tools/import_camping.py <dossier de la one-page>
"""
import re, shutil, sys
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'campings/motion-drive/onepage/outputs/chapito-campings-v2'
DST = ROOT / 'public/assets/camping'

# --- images
def convert(rel):
    src = SRC / 'assets' / rel
    out_rel = re.sub(r'\.(png|jpe?g)$', '.webp', rel)
    dst = DST / out_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in ('.png', '.jpg', '.jpeg'):
        im = Image.open(src).convert('RGB')
        max_w = 720 if im.height > im.width else 1400
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(dst, 'WEBP', quality=82, method=6)
    else:
        shutil.copy(src, dst)
    return out_rel

html = (SRC / 'index.html').read_text()
for rel in sorted(set(re.findall(r'assets/([^"#\']+)', html))):
    new = convert(rel)
    html = html.replace(f'assets/{rel}', f'/assets/camping/{new}')
shutil.copy(SRC / 'script.js', DST / 'camping.js')

s = BeautifulSoup(html, 'html.parser')
main = s.find('main')
json_ld = s.find('script', type='application/ld+json')
cal_script = [sc for sc in s.find_all('script') if sc.string and 'Cal(' in sc.string]

# --- emplacement vidéo → vidéo réelle
video = main.select_one('.video-todo')
video_html = '''<section class="video-todo section-pad" aria-labelledby="video-title">
  <div class="container">
    <div class="video-todo-layout">
      <div class="video-todo-copy">
        <p class="overline"><span></span>En vidéo</p>
        <h2 id="video-title">Le quotidien du camping,<br><mark>mis en mouvement.</mark></h2>
        <p>60 secondes pour voir comment Chapitô centralise l’information de votre camping, du back-office jusqu’au téléphone de vos vacanciers.</p>
      </div>
      <div class="camping-video">
        <video controls preload="none" playsinline poster="/assets/camping/video/poster.jpg" width="1920" height="1080">
          <source src="/assets/camping/video/chapito-campings.mp4" type="video/mp4">
        </video>
      </div>
    </div>
  </div>
</section>'''
video.replace_with(BeautifulSoup(video_html, 'html.parser'))

out = str(main)
out = out.replace('<main id="main">', '<div class="camping-page" id="main">', 1)
out = out[: out.rfind('</main>')] + '</div>'

# --- consignes rédactionnelles restées visibles (formulations du prompt d'origine)
FIXES = [
    (r'Le véritable back-office Chapitô', 'Le back-office Chapitô'),
    (r'Les besoins spécifiques sont étudiés sans les présenter comme inclus d’office\.', 'Vos besoins spécifiques sont étudiés avec vous.'),
    (r'\s*Ils ne sont pas présentés comme inclus sans confirmation\.', ''),
    (r', sans promettre un taux de téléchargement', ''),
    (r', sans être présentées comme automatiques ou incluses d’office', ''),
    (r' selon les modalités Chapitô', ''),
    (r' selon ses modalités', ''),
    (r'Identité fictive de démonstration', 'Camping fictif, pour la démonstration'),
]
for pat, rep in FIXES:
    out, n = re.subn(pat, rep, out, flags=re.I)
    print(f'{n} × {pat[:50]}')
for leftover in ('TODO', 'V2', 'faux lecteur', 'sans les présenter', 'selon les modalités'):
    if leftover in out:
        print('⚠ reste :', leftover)

page = f'''---
title: "Application mobile pour camping | Chapitô"
ogTitle: "Moins de questions à l’accueil | Chapitô Campings"
description: "Horaires, animations, plan, informations pratiques : une application mobile aux couleurs de votre camping, mise à jour en autonomie depuis un back-office simple."
wfPage: "67091cb1da6adcd46c46b8b9"
permalink: "/camping.html"
url: "/camping"
ogImage: "/assets/camping/video/poster.jpg"
---
{{% extends "base.njk" %}}
{{% block head %}}
<link href="/assets/camping/camping.css" rel="stylesheet" type="text/css"/>
<link href="/assets/camping/camping-site.css" rel="stylesheet" type="text/css"/>
{json_ld}
{{% endblock %}}
{{% block main %}}
{out}
{{% endblock %}}
{{% block webflow %}}
<!-- bundle Webflow de la page Confidentialité : menu et interactions communes -->
<script src="/assets/js/webflow.1946f659.31192706fadd01dd.js" type="text/javascript"></script>
{{% endblock %}}
{{% block scripts %}}
{''.join(str(c) for c in cal_script)}
<script src="/assets/camping/camping.js"></script>
{{% endblock %}}
'''
(ROOT / 'src/camping.njk').write_text(page)
print('src/camping.njk écrit')
