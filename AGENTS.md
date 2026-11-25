# AGENTS.md

Instructions pour tout agent IA (Codex, ChatGPT, Claude, Copilot, Cursor…) qui travaille sur ce dépôt. À lire en entier avant la première modification.

## 1. Contexte

- Site vitrine de **Chapitô**, application mobile pour les festivals, événements et campings : https://chapi.to
- Site statique **Hugo 0.164**, sans autre outil : pas de Node, pas de dépendance. Site entièrement en français.
- Les pages viennent d'un export Webflow, indenté depuis : beaucoup de classes et d'attributs dont dépendent le menu mobile et les animations.
- La personne qui te parle n'est **pas forcément développeuse** (par exemple l'équipe commerciale). Elle ne verra pas si tu casses une page, un gabarit ou une animation. **C'est à toi d'être prudent à sa place.**
- Relecteurs techniques : l'équipe GitHub `@code-troopers/owners` (les développeurs).
- **Un merge dans `main` = mise en ligne automatique** en quelques minutes (GitHub Actions publie sur GitHub Pages). Toute modification passe par une pull request (PR) : GitHub refuse les envois directs sur `main`, sauf aux développeurs.

### Parler à l'utilisateur

- Mots simples. Pas de jargon (branche, commit, PR, CI, merge, en-tête…) sans l'expliquer en quelques mots : une PR est une « demande de mise en ligne », merger veut dire « publier ».
- Ne pose une question que si la réponse change ce que tu vas faire. Une demande précise (« remplace X par Y ») s'exécute sans redemander confirmation.
- Une question à la fois, à laquelle on répond par oui, non ou un choix simple, avec ta recommandation.
- Ne lui demande jamais de choisir un nom de branche, un message de commit ou le niveau de la demande : c'est ton travail.
- Garde pour toi les détails techniques qui ne demandent aucune décision de sa part (commandes lancées, structure des fichiers). S'il y a un vrai doute sur le contenu (texte présent à plusieurs endroits, formulation ambiguë), pose-le en citant la page du site concernée, pas le fichier.

## 2. Règle d'or : classer la demande avant d'agir

Avant toute modification, classe la demande dans un des deux niveaux et annonce-le à l'utilisateur en une phrase simple : « C'est une petite modification de contenu, tu pourras la publier toi-même » ou « C'est une modification technique, un développeur devra la relire avant publication ».

### Niveau 1 : petite modification de contenu (publiée par l'utilisateur lui-même)

Uniquement :

- corriger une faute d'orthographe, de grammaire ou de typographie ;
- modifier un texte **à la demande explicite** de l'utilisateur (une phrase, un titre, un chiffre qu'il fournit) ;
- remplacer une image par une autre, ou modifier son texte alternatif ;
- modifier le `title` ou la `description` dans l'en-tête d'une page ;
- remplacer l'adresse d'un lien **existant** (lien `https://` ou page du site).

Fichiers concernés (et **uniquement** ceux-là) :

- `content/*.html` : seulement le texte entre les balises, l'en-tête `title` / `description`, et pour une image ou un lien les attributs décrits dans les recettes (section 6) ;
- les fichiers image (`.webp`, `.jpg`, `.png`, `.svg`, `.avif`) de `static/assets/img/`, `static/assets/cms/` et `static/assets/camping/`.

Une modification de niveau 1 touche **une seule page ou un seul sujet**. Plusieurs fautes sur une même page : une seule PR. Une nouvelle section, un nouveau bloc, une refonte de texte sur plusieurs paragraphes : niveau 2.

### Niveau 2 : tout le reste (pull request relue par un développeur)

En particulier :

- tout fichier hors des chemins ci-dessus : gabarits (`layouts/`), menu et pied de page, styles (`static/assets/css/`), scripts (`static/assets/js/`, fichiers `.js` et `.css` de `static/assets/camping/`), configuration (`hugo.toml`, `.github/`), ce fichier `AGENTS.md` ;
- ajouter, déplacer ou supprimer une balise, une classe, un `id` ou un attribut dans une page (hors recettes de la section 6) ;
- ajouter une section, un bloc, une carte, une page ; supprimer une page ; changer l'adresse d'une page ;
- changer la mise en page, les couleurs, les polices ;
- modifier les champs de l'en-tête autres que `title` et `description` (`css`, `scripts`, `webflow`, `wfPage`, `schema`, `aliases`…) ;
- intégrer une vidéo, un formulaire, un widget ou tout élément externe (`<iframe>`, `<script>`, `<style>`, attributs `onclick`…) ;
- modifier le lien de prise de démonstration ou le formulaire newsletter (`hugo.toml`) ;
- une demande de contenu qui t'oblige à toucher un fichier du niveau 2.

**En cas de doute, c'est du niveau 2.**

### Toujours interdit

- Pousser directement sur `main` (sauf demande explicite d'un développeur de `@code-troopers/owners`, qui peut contourner la règle), faire un `git push --force`, réécrire l'historique publié.
- Merger une PR de niveau 2, ou dire à l'utilisateur de le faire : seul un développeur de `@code-troopers/owners` la publie, après relecture.
- Ajouter un script tiers, un traceur, une police externe, un iframe ou un CDN.
- Inventer des faits : chiffres, clients, témoignages, tarifs, dates. Tout ce qui est affirmé sur le site doit venir de l'utilisateur ou du contenu existant.
- Supprimer ou réécrire du contenu existant qui n'est pas visé par la demande.
- Committer des secrets, le dossier `public/` (généré) ou des fichiers personnels.
- Contourner un garde-fou (désactiver la CI, modifier `.github/CODEOWNERS`, ignorer une erreur de build).

## 3. Lancer le site en local

Installer Git et [Hugo 0.164](https://github.com/gohugoio/hugo/releases/tag/v0.164.0) (un seul fichier à télécharger, rien d'autre). Sur macOS : `brew install hugo` convient si `hugo version` affiche 0.164 ou plus.

```bash
hugo server   # aperçu sur http://localhost:1313/ avec rechargement automatique (Ctrl+C pour arrêter)
hugo          # générer le site dans public/, comme la mise en ligne
```

En local, les pages s'ouvrent avec leur extension (`http://localhost:1313/pricing.html`) ; en ligne, `/pricing` fonctionne aussi.

## 4. Workflow Git et publication

Toute modification, quel que soit son niveau, passe par une branche et une PR vers `main`.

1. Partir de `main` à jour (`git switch main && git pull`), créer une branche courte et explicite : `content/typo-tarifs`, `content/logo-egaluantes`, `fix/…`, `feat/…`.
2. Faire la modification, et rien d'autre. Lancer `hugo` : aucune erreur ni avertissement ne doit apparaître. En cas d'erreur que tu ne sais pas corriger sans sortir du niveau de la demande, annuler et expliquer le problème.
3. **Faire vérifier le rendu par l'utilisateur.** Comment dépend de l'endroit où tu tournes :
   - **Sur l'ordinateur de l'utilisateur** (Codex CLI, application Codex ouverte sur un dossier local, Claude Code…) : faire valider en local, **avant tout commit** :
     - Lancer `hugo server` en arrière-plan : le serveur tourne en continu, ne pas attendre qu'il se termine. Si l'outil ne permet pas de laisser tourner une commande, demander à l'utilisateur de lancer `hugo server` dans un terminal, depuis le dossier du dépôt.
     - Donner l'adresse exacte de chaque page modifiée, avec l'extension `.html` (par exemple `http://localhost:1313/pricing.html`, ou `http://localhost:1313/` pour l'accueil), dire où regarder sur la page, et demander de la vérifier sur ordinateur **et** en largeur mobile (fenêtre étroite, ou mode « appareil » des outils de développement du navigateur).
     - **Attendre l'accord explicite de l'utilisateur avant de committer.** S'il demande une retouche, la faire et lui redemander de vérifier.
     - Arrêter le serveur une fois la modification validée.
   - **Dans le cloud** (Codex dans ChatGPT, agent lancé depuis GitHub…) : l'utilisateur ne peut pas ouvrir ton `localhost`, ne lui demande pas de lancer de commande. Committe, ouvre la PR, et la vérification se fait sur la preview Netlify (étape 6), **avant publication**.
   - Dans le doute, considère que tu es dans le cloud : la preview Netlify montre de toute façon le vrai site.
4. Committer avec un message **en anglais** (même si la conversation est en français) au format Conventional Commits, sans mention d'IA ni trailer `Co-Authored-By` :
   - `fix(content): fix typo on pricing page`
   - `chore(content): replace Semaine du Golfe logo`
5. Pousser et ouvrir la PR vers `main`. Le dépôt est public : **titre et description en anglais**, sans mention d'IA. La description dit ce qui change sur le site et pourquoi :
   ```bash
   git push -u origin HEAD
   gh pr create --base main --title "<commit message>" --body "<what changes on the site and why>"
   ```
   Sans `gh`, donner à l'utilisateur le lien que `git push` affiche.
6. Attendre les vérifications (`gh pr checks`) :
   - **CI** (`build`) : le site se génère sans erreur ;
   - **Netlify** : une preview du site, prête quelques minutes après l'ouverture de la PR (lien `https://deploy-preview-<numéro de la PR>--<site>.netlify.app/`, donné par Netlify dans la PR). **Donne à l'utilisateur l'adresse exacte de chaque page modifiée sur la preview, avec l'extension `.html`** (par exemple `https://deploy-preview-12--<site>.netlify.app/pricing.html`) et demande-lui de la vérifier sur ordinateur et sur téléphone. Attends son accord explicite avant de publier. S'il demande une retouche, la faire sur la même branche : la preview se met à jour.
7. Publier (merger) :
   - niveau 1, CI verte, preview validée par l'utilisateur : `gh pr merge --squash --delete-branch`. Si tu ne peux pas merger (pas de `gh`, agent dans le cloud), explique-lui comment faire : ouvrir le lien de la PR, cliquer sur le bouton vert en bas de la page (choisir « Squash and merge » si un menu propose plusieurs options), puis « Confirm squash and merge ». Il n'a besoin de l'accord de personne ;
   - niveau 2 : ne pas merger. Dis-lui simplement qu'un développeur de l'équipe va relire, et que la modification sera publiée après son approbation.
8. Après le merge, la mise en ligne prend quelques minutes. Vérifier la page sur https://chapi.to.

Une PR = un sujet. Ne mélange pas une correction de faute et une nouvelle section.

## 5. Où modifier quoi

| Élément du site | Fichier | Niveau |
| --- | --- | --- |
| Accueil (`/`) | `content/_index.html` | 1 pour le texte et les images |
| La solution (`/solutions`) | `content/solutions.html` | 1 pour le texte et les images |
| Réalisations (`/realisations`) | `content/realisations.html` | 1 pour le texte et les images, 2 pour ajouter ou retirer une carte |
| Partenaires (`/partners`) et pages partenaires | `content/partners.html`, `content/partenaire-*.html`, `content/yurplan.html`, `content/wilout.html` | 1 pour le texte et les images |
| Tarifs (`/pricing`) | `content/pricing.html` | 1 pour le texte (prix fournis par l'utilisateur) |
| Campings (`/camping`) | `content/camping.html` | 1 pour le texte et les images |
| Politique de confidentialité (`/privacy`) | `content/privacy.html` | 1 |
| Menu, bandeau du haut | `layouts/partials/navbar.html` | 2 |
| Pied de page (adresse, téléphone, réseaux) | `layouts/partials/footer.html` | 2 |
| Pop-up newsletter | `layouts/partials/newsletter-popup.html` | 2 |
| Lien de prise de démonstration, Matomo, formulaire newsletter | `hugo.toml` (`[params]`) | 2 |
| Styles | `static/assets/css/` | 2 |

Pour trouver le fichier qui contient un texte : `grep -rln "texte exact" content layouts`.

## 6. Recettes (niveau 1)

### Corriger une faute ou modifier un texte

- Trouver le texte : `grep -rn "texte exact" content`. S'il n'est que dans `layouts/`, c'est du niveau 2.
- Ne modifier que les mots visés, entre les balises. Ne pas reformuler le reste de la phrase ni du paragraphe.
- Ne toucher à aucune balise ni attribut autour. Les `<br/>` et les caractères invisibles (`‍`) déjà présents restent en place.
- Ne pas réindenter ni reformater le fichier. Ne jamais ajouter d'espace ou de retour à la ligne entre deux balises qui sont collées (par exemple deux `<img>` ou deux liens côte à côte) : cela ajouterait un espace visible sur la page.

### Remplacer une image

1. Déposer la nouvelle image dans le même dossier que l'ancienne (`static/assets/img/` ou `static/assets/cms/`), avec un nom en minuscules, chiffres et tirets.
2. Dans la balise `<img>` concernée, et seulement celle-là :
   - remplacer la valeur de `src` par `/assets/<dossier>/<nouveau-nom>` ;
   - si la balise a des attributs `srcset` et `sizes`, les supprimer (ils listent des versions de l'ancienne image) ;
   - mettre à jour `width` et `height` s'ils sont présents, avec les dimensions de la nouvelle image (ou les proportions de l'ancienne si l'image est redimensionnée par le style) ;
   - écrire un `alt` qui décrit l'image (le nom du festival ou du partenaire pour un logo). `alt=""` seulement pour une image purement décorative.
3. Ne pas supprimer l'ancienne image : un développeur fera le ménage.

### Remplacer l'adresse d'un lien existant

- Ne modifier que la valeur de `href`. Adresse en `https://` pour un site externe, ou chemin du site sans extension (`/pricing`, `/camping`).
- Ne pas ajouter de lien là où il n'y en a pas : c'est du niveau 2.

## 7. Règles éditoriales

- Français, ton direct et concret, sans jargon marketing creux.
- Typographie française : espace insécable (`&nbsp;` ou U+00A0) avant `:` `;` `!` `?`.
- Éviter les tics d'écriture d'IA : pas de tiret cadratin (—), pas de formules creuses.
- Aucun prix, chiffre, client ou témoignage inventé : reprendre uniquement ce qui figure déjà sur le site ou ce que l'utilisateur fournit.
- « Camping Les Pins Dorés » est un camping fictif de démonstration, pas un client.
- Le seul appel à l'action est la prise de démonstration (lien cal.com dans `hugo.toml`).

## 8. Images

- Formats : `.webp` de préférence, `.jpg` pour les photos, `.png` pour les captures, `.svg` pour les logos. Pas de `.heic`, pas de `.tiff`.
- Poids : **moins de 500 Ko** par image, largeur adaptée à l'affichage (inutile de dépasser 2 fois la largeur affichée). Compresser avant d'ajouter.
- Un `.svg` ne doit contenir ni `<script>` ni lien vers une ressource externe.
- Ne jamais supprimer une image existante sans vérifier qu'elle n'est plus utilisée : `grep -rn "nom-du-fichier" content layouts static`.

## 9. Pour les tâches techniques (niveau 2)

À lire seulement si l'utilisateur demande une modification technique ; elle sera relue.

1. Ne jamais modifier `static/assets/js/webflow.*.js` ni `static/assets/css/chapito-preprod.webflow.shared.*.css` : ce sont les fichiers d'origine de Webflow (menu, animations).
2. Conserver les attributs `data-w-id`, `data-wf-page` et les classes existantes (`w-nav`, `hover-state`, `heading-style-h2`…) : les animations et le menu mobile en dépendent.
3. Le menu et le pied de page sont communs à toutes les pages (`layouts/partials/navbar.html` et `footer.html`) : ne pas les recopier dans une page.
4. Ne pas ajouter `w--current` ni `aria-current` à la main : c'est calculé à la génération.
5. Une page de `content/` contient un en-tête `---` puis uniquement son contenu HTML (pas de `<html>`, `<head>`, menu ni pied de page). Ne pas ajouter de balise `<script>` ou `<style>` dans le contenu (celles qui y sont déjà viennent des blocs « embed » de Webflow, les laisser en place) : les nouveaux styles vont dans un fichier de `static/assets/css/pages/` déclaré dans `css:`, le JavaScript dans `static/assets/js/pages/` déclaré dans `scripts:`.
6. Nouvelle page : copier `content/privacy.html`, changer l'en-tête (`title`, `description`) et le contenu. Le nom du fichier donne l'adresse (`content/ma-page.html` → `/ma-page`). L'ajouter au menu et au pied de page si besoin. `noindex: true` dans l'en-tête l'exclut des moteurs de recherche et du plan du site.
7. Les styles de la page camping sont isolés sous `.camping-page` : tout nouveau sélecteur de cette page doit commencer par `.camping-page`.
8. Un seul `<h1>` par page. Pour un titre secondaire qui doit garder l'apparence d'un h1, utiliser `<h2 class="h1-look …">`.
9. Un élément cliquable qui n'est ni un lien ni un bouton doit avoir `role="button" tabindex="0"` (le clavier est géré par `static/assets/js/site.js`).
10. Aucune nouvelle dépendance ni outil de build sans accord explicite d'un membre de `@code-troopers/owners`.
11. Une modification technique ne doit pas changer le rendu des pages non concernées. Comparer `public/` avant et après quand c'est possible.

## 10. Garde-fous en place

- **Règle « Protect main »** sur GitHub : PR obligatoire, CI verte obligatoire, pas de `push --force` ni de suppression de `main`. Seuls les développeurs de `@code-troopers/owners` peuvent la contourner.
- **CODEOWNERS** (`.github/CODEOWNERS`) : une PR qui touche autre chose que les pages (`content/`) et les images exige l'approbation d'un développeur de `@code-troopers/owners`. GitHub ne voit pas la différence entre une faute corrigée et une nouvelle section dans une page : le classement de la section 2 reste ta responsabilité.
- **CI** (`.github/workflows/pages.yml`) : sur chaque PR, vérifie que le site se génère ; sur `main`, génère et publie.
- **Preview Netlify** sur chaque PR, pour relire le rendu avant publication (`netlify.toml`). La publication reste faite par GitHub Pages.

## 11. Comment rendre compte à l'utilisateur

À la fin de chaque tâche, en français simple :

1. ce qui a été modifié (pages du site, pas noms de fichiers techniques) ;
2. le niveau (petite modification ou relecture nécessaire) ;
3. le lien de la PR et l'adresse de chaque page modifiée sur la preview Netlify (ou, une fois publiée, sur https://chapi.to) ;
4. ce qui reste à faire de son côté (vérifier la preview, publier, ou attendre la relecture).

Si une vérification échoue et que tu ne sais pas la corriger sans toucher au niveau 2, arrête-toi et explique le problème au lieu de contourner.
