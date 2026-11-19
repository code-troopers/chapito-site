# chapi.to — site statique

Copie statique du site Webflow chapi.to (novembre 2026), générée avec [Hugo](https://gohugo.io/) (même outil que code-troopers.com), plus la nouvelle page `/camping`.
Aucune dépendance à Webflow à l'exécution : pages, images, polices et scripts sont dans ce dépôt.

## Démarrer

Installer Hugo 0.164 (un seul exécutable, pas de Node) : https://github.com/gohugoio/hugo/releases/tag/v0.164.0

    hugo server      # aperçu sur http://localhost:1313/ avec rechargement automatique
    hugo             # génère le site dans public/

Dans `hugo server`, les pages s'ouvrent avec leur extension (`/solutions.html`) ; une fois en ligne, `/solutions` fonctionne aussi, comme sur Webflow.

## Où modifier quoi

| Je veux modifier… | Fichier |
|---|---|
| Le contenu d'une page | `content/_index.html` (accueil), `content/solutions.html`, `realisations.html`, `partners.html`, `pricing.html`, `privacy.html`, `camping.html` |
| Les pages partenaires | `content/yurplan.html`, `partenaire-heeds.html`, `wilout.html`, `partenaire-spotify.html`, `partenaire-deezer.html` |
| Titre, description, image de partage d'une page | en-tête `---` du fichier de la page |
| Le menu (toutes les pages) | `layouts/partials/navbar.html` |
| Le pied de page (toutes les pages) | `layouts/partials/footer.html` |
| Lien cal.com, ID Google Analytics, formulaire Brevo | `hugo.toml`, section `[params]` |
| `<head>` commun, ordre des scripts | `layouts/_default/baseof.html` |
| Ajustements communs (accessibilité, titres, animations réduites) | `static/assets/css/site.css`, `static/assets/js/site.js` |
| Styles ou scripts propres à une page | `static/assets/css/pages/`, `static/assets/js/pages/` (déclarés dans l'en-tête de la page : `css`, `scripts`) |
| Styles de la page camping | `static/assets/camping/camping.css` (isolé sous `.camping-page`) et `camping-site.css` |
| Images | `static/assets/…` |

En-tête d'une page (`content/*.html`) :

    ---
    title: "Chapitô : tarifs"               # <title>
    description: "…"                         # description et partage
    wfPage: "66b0b2559d1632d0f9e5486f"       # identifiant Webflow de la page (animations)
    webflow: ["webflow.1946f659….js"]        # bundle d'animations Webflow de la page
    css: ["/assets/css/pages/….css"]         # facultatif
    scripts: ["/assets/js/pages/….js"]       # facultatif, chargés en fin de page
    ---

Le lien actif du menu (`w--current`) est calculé à la génération : ne pas l'écrire à la main.
Guide pour les modifications assistées par IA (ChatGPT, Codex…) : [`AGENTS.md`](AGENTS.md).

## Newsletter (Brevo)

La pop-up newsletter de la page d'accueil reste masquée tant que Brevo n'est pas configuré.

1. Brevo → Contacts → Formulaires → créer un formulaire d'inscription (liste « Newsletter Chapitô », double opt-in conseillé).
2. Dans le code HTML d'intégration fourni par Brevo, copier l'URL de l'attribut `action` du `<form>` (forme `https://….sibforms.com/serve/…`).
3. La coller dans `hugo.toml` → `brevoFormAction`, puis regénérer.

Avant de couper Webflow : exporter les inscriptions déjà reçues (Webflow → Site settings → Forms → export CSV) et les importer dans Brevo.

## Déploiement

Le site est publié sur **GitHub Pages** par `.github/workflows/pages.yml` à chaque push sur `main` (dépôt `code-troopers/chapito-site`).

- Test : https://beta.chapi.to (enregistrement Cloudflare `CNAME beta → code-troopers.github.io`, sans proxy).
- Le domaine personnalisé se règle dans GitHub : Settings → Pages → Custom domain.
- `/campings` redirige vers `/camping` par une page de redirection générée par Hugo (`aliases` dans `content/camping.html`).

### Bascule de chapi.to (plus tard)

1. Vérifier le site sur beta.chapi.to, puis geler Webflow ou reporter ses dernières modifications.
2. Baisser le TTL des enregistrements `chapi.to` et `www` chez Cloudflare.
3. GitHub → Settings → Pages → Custom domain : `chapi.to`.
4. Cloudflare : remplacer les enregistrements Webflow par `A chapi.to` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, les `AAAA` équivalents (`2606:50c0:8000::153` à `8003::153`), et `CNAME www → code-troopers.github.io` (sans proxy le temps que GitHub émette le certificat). GitHub redirige alors www vers chapi.to.
5. Cocher « Enforce HTTPS » dans GitHub une fois le certificat émis.
6. Garder Webflow actif 2 à 4 semaines (retour arrière possible), puis résilier.

## Comment cette copie a été produite (pour mémoire)

Scripts de `tools/`, lancés une seule fois : aspiration de chapi.to (`import_webflow.py`, `split_pages.py`), intégration de la one-page camping (`scope_css.mjs`, `import_camping.py`), passage d'une première version Eleventy à Hugo (`eleventy_to_hugo.py`), puis import des pages partenaires (`import_partner_pages.py`).

**Webflow est toujours modifiable** : la copie date du 18/11/2026 à 17 h (republication du jour incluse : page Deezer). Toute modification faite dans Webflow d'ici la bascule devra être reportée ici à la main, ou Webflow gelé.
Ils ne sont plus à relancer : `content/`, `layouts/` et `static/` sont désormais la source de vérité.

## Corrections faites par rapport au site Webflow

- `lang="fr"` (le site était déclaré en anglais), balises canoniques, `sitemap.xml` et `robots.txt` (absents).
- Lien « Découvrez notre widget » qui pointait vers la préproduction Webflow.
- Téléphone de Jérémy : le lien appelait le numéro de Nicolas.
- « Carte interractive » → « Carte interactive ».
- Weglot (traduction anglaise) et sélecteur FR/EN retirés ; document HTML collé par erreur dans un bloc de code de l'accueil supprimé.
- Polices Poppins hébergées localement (plus d'appel à Google Fonts).
- Image de partage en JPEG (l'AVIF n'est pas lu par tous les réseaux sociaux).

Après l'audit du 18/11/2026 :

- Pages partenaires (Yurplan, Heeds, Wilout, Spotify, Deezer) reprises, liens de /partners en relatif.
- Fautes visibles corrigées (« exprérience », « vots », « travaillez avez », texte Espace Malraux, fiches Réalisations, « démo », « Carte interactive »…), espaces insécables avant ? ! : ;
- Pied de page et page 404 en français, titre « Politique de confidentialité », lien e-mail de la politique réparé, lien LinkedIn public.
- Un seul h1 par page (rendu inchangé, classe `h1-look`), `<main>`, `<footer>`, lien « Aller au contenu ».
- Clavier : fiches et filtres de /realisations, FAQ de /pricing, fermeture du bandeau ; liens réseaux sociaux nommés ; textes alternatifs décoratifs vidés ; `rel="noopener"`.
- Animations : réduction respectée (`data-wf-ix-vacation`), en-tête collant qui ne masque plus le focus (`scroll-padding-top`).
- Performance : widget de /solutions chargé une seule fois à l'approche (12 Mo → 0,8 Mo au chargement), agenda cal.com de /camping chargé à l'approche et initialisé une seule fois, images du haut de /camping en `srcset`.
- Feuille de style Webflow mise à jour (version du 18/11, identique hormis la page Deezer).

Ce qui reste à décider ou à faire : voir [`TICKETS.md`](TICKETS.md).

## Page /camping

- Contenu de la one-page V2 de Nicolas, avec le menu et le pied de page du site, et « Campings » ajouté au menu et au pied de page. `/campings` redirige vers `/camping`.
- Formulations héritées du prompt corrigées (« véritable back-office », « sans les présenter comme inclus d'office », « selon les modalités Chapitô »…).
- Emplacement « TODO vidéo » remplacé par la vidéo de présentation (voix off provisoire).
- Images converties en WebP (25 Mo → 1,4 Mo), `noindex` retiré.
- Le texte lui-même n'a pas été retravaillé (longueur, doublons de la FAQ) : à faire avec Nicolas.
