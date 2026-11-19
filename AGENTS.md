# Consignes pour les assistants IA (ChatGPT, Codex…)

Site vitrine statique de Chapitô (chapi.to), généré par Hugo 0.164 (`hugo` produit `public/`).

## Règles

1. Modifier uniquement `content/` (pages), `layouts/` (structure commune, menu, pied de page), `hugo.toml` (`[params]`) et, pour les images, styles ou scripts, `static/assets/`.
2. Ne jamais modifier `static/assets/js/webflow.*.js` ni `static/assets/css/chapito-preprod.webflow.shared.*.css` : ce sont les fichiers d'origine de Webflow (menu, animations).
3. Conserver les attributs `data-w-id`, `data-wf-page` et les classes existantes (`w-nav`, `hover-state`, `heading-style-h2`…) : les animations et le menu mobile en dépendent.
4. Le menu et le pied de page sont communs à toutes les pages (`layouts/partials/navbar.html` et `footer.html`) : ne pas les recopier dans une page.
5. Ne pas ajouter `w--current` ni `aria-current` à la main : c'est calculé à la génération.
6. Une page de `content/` contient un en-tête `---` puis uniquement son contenu HTML (pas de `<html>`, `<head>`, menu ni pied de page). Ne pas ajouter de balise `<script>` ou `<style>` dans le contenu (celles qui y sont déjà viennent des blocs « embed » de Webflow, les laisser en place) : les nouveaux styles vont dans un fichier de `static/assets/css/pages/` déclaré dans `css:`, le JavaScript dans `static/assets/js/pages/` déclaré dans `scripts:`.
7. Nouvelle page : copier `content/privacy.html`, changer l'en-tête (`title`, `description`) et le contenu. Le nom du fichier donne l'adresse (`content/ma-page.html` → `/ma-page`). L'ajouter au menu et au pied de page si besoin.
8. Les styles de la page camping sont isolés sous `.camping-page` : tout nouveau sélecteur de cette page doit commencer par `.camping-page`.
9. Écrire en français, avec les accents et la typographie française (espace insécable avant « ? ! : ; »).
10. Un seul `<h1>` par page. Pour un titre secondaire qui doit garder l'apparence d'un h1, utiliser `<h2 class="h1-look …">`.
11. Un élément cliquable qui n'est ni un lien ni un bouton doit avoir `role="button" tabindex="0"` (le clavier est géré par `static/assets/js/site.js`).
12. Vérifier avec `hugo` qu'il n'y a pas d'erreur avant de proposer la modification.

## Contenu

- Aucun prix, chiffre, client ou témoignage inventé : reprendre uniquement ce qui figure déjà sur le site ou ce que l'équipe fournit.
- « Camping Les Pins Dorés » est un camping fictif de démonstration, pas un client.
- Le seul appel à l'action est la prise de démonstration (lien cal.com dans `hugo.toml`).
