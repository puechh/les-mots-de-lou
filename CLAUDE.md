# Les Mots de Lou — instructions pour Claude

Projet de création de la boutique Shopify **Les Mots de Lou** (bijoux personnalisés). Claude gère la boutique (produits,
collections, thème, pages, paramètres…) via l'API Admin de Shopify. Toujours répondre en **français**.
Projet né le 02/11/2026 dans le projet Corps-Confiant (dépôt `puechh/boutique-corps-confiant`, même utilisateur) :
on y reprend les outils et la méthode, mais **les deux boutiques ne se mélangent pas**.

## Contexte (02/11/2026)
- L'utilisateur n'est pas technique : expliquer simplement, étape par étape, avec où cliquer.
- Il a une semaine assez libre à partir du 02/11/2026 et veut lancer cette boutique **avant le Black Friday (27/11/2026)** et
  surtout pour **Noël** (dernière commande pour Noël ≈ **1-3/12** : 2-4 j de fabrication + 8-12 j de livraison).
- **Produits : bijoux personnalisés en acier inoxydable 316L** (dropshipping AliExpress via DSers) : jonc gravé, collier prénom,
  collier photo à projection, éventuellement bracelet code Morse. Recherche complète, prix et sources : `docs/recherche-produits.md`.
- **Marque : « Les Mots de Lou »**, incarnée par **Lou, égérie virtuelle (personne créée par IA)**, idée de l'utilisateur.
  **Slogan : « Vos mots, gravés pour toujours. »** (choisi le 02/11/2026). Concept, ton et règles : `docs/marque.md`. Domaines : l'utilisateur possède déjà **`les-mots-de-lou.fr`** (avec tirets, IONOS) et prend **`lesmotsdelou.fr`** (sans tirets) comme **adresse principale** (l'autre redirigera).
- **Tout en IA** : photos **et vidéos** (pas de tournage).
- **Pub** : environ 300 € par boutique + **420 € de crédit Pinterest offert**. Pinterest en priorité (femmes 25-55 ans), puis Meta/TikTok.
- Leçons tirées de Corps-Confiant (pièges Shopify, Klaviyo, cookies, pubs) : `docs/lecons-corps-confiant.md`.
- **Bêta construite le 02/11/2026** (carte blanche) : thème `theme-lou/`, fiches `produits/produits.json`, pages `contenu/pages/`,
  politiques `contenu/politiques/`, tout envoyé sur Shopify par `scripts/construire_boutique.py`. Banc d'essai local :
  `python3 scripts/banc_theme.py` (http://localhost:8765). Images du thème : `python3 scripts/assets_theme.py`.
- **Lou = l'avatar de la boutique** (demande utilisateur 02/11 soir, exemple Lily's Treasures) : elle parle à la 1re personne
  (bulles, assistante en bas de l'écran à réponses préparées, FAQ en conversation, panier commenté) et se présente comme
  **personnage virtuel créé avec l'IA** ; elle ne fabrique pas les bijoux (« l'atelier grave », « l'équipe vous répond »).
- **Thème publié par l'utilisateur** (02/11 soir) : `theme-lou/` est en ligne derrière le mot de passe → tester au banc AVANT
  `envoyer_theme.py maj`. Réglages du thème (Shopify → Thèmes → Personnaliser → Paramètres) : écrin inclus (non par défaut),
  délais fab/livraison, date limite Noël, Lou, sons. Images IA en **HD 2048 px** (JPEG, `scripts/images_hd*.sh`).
- Inspirations (Lily's Treasures, Ciao Kombucha, Dentica) : `docs/inspirations.md`.
- Fiches (décisions utilisateur 03/11) : écriture manuscrite **Allura** ; **première lettre toujours en majuscule** ; bénéfices
  dans « Caractéristiques » en bas de fiche ; case « orthographe vérifiée » **cochée d'office** ; délai **5 à 10 jours au total,
  fabrication comprise** (jours calendaires, décision 03/11) ; icône « Mon compte » dans l'en-tête ; accueil = Lou détourée qui
  montre ses bijoux (3 poses + 4 pastilles animées, façon Lily's Treasures, 03/11 soir) ; vignettes produits animées (la personnalisation se « remplit »).
  Machine à mots sous les bijoux (accueil) et sous « Caractéristiques » (jonc, bracelet) ; **Noël : avant le 10 décembre**.
- **Textes du site (décision utilisateur 04/11)** : l'essentiel seulement, pas de pavés — titres courts, 1 ligne max sous un
  titre, cartes produits sans description, FAQ courte ; le client doit voir tout de suite l'info utile.
- **LOU = la photo `contenu/lou/reference-v3/00-source-lou.webp`** (envoyée par l'utilisateur le 03/11 : « c'est elle la future
  Lou ») : 20 ans, brune (châtain foncé), chignon décoiffé avec mèches qui encadrent le visage, yeux noisette, peau hâlée.
  **Peau lisse (20 ans, aucune ride), seulement quelques taches de rousseur très légères.** Planche : `contenu/lou/reference-v3/`
  (8 plans + `planche-lou-v3.jpg`). Anciennes versions (`reference/`, `reference-v2/`, `propositions-v2/`) **abandonnées**
  (retouches OpenAI en chaîne → peau « pixelisée », jugée fausse par l'utilisateur).
- **RÈGLE OBLIGATOIRE pour toute image ou vidéo de Lou** : **ultra-réaliste, haute qualité sans pixels (comme une photo 4K
  d'iPhone)**, **« Shot on iPhone 18 Pro by an amateur photographer. » en tête de chaque prompt**.
  **Outil : fal.ai `fal-ai/nano-banana-pro/edit`** (choisi au comparatif du 03/11 contre Flux 2 Pro et Seedream 5 Pro, et
  contre OpenAI) via `scripts/fal_images.py … --param resolution=4K --param aspect_ratio=3:4 --param output_format=jpeg`
  (3584×4800, ≈ 0,30 $/image). **Toujours repartir de `00-source-lou.webp` + `01-face.jpg`** (2 références = meilleure
  ressemblance ; ne jamais retoucher une retouche). Prompts types dans les .txt de `reference-v3/`. Tenues sobres (pubs).
  Vérifier un recadrage à 100 % avant d'envoyer. **Images du site en pleine définition** (demande utilisateur « vraiment en 4K »,
  03/11) ; les petits détails (gravure, prénom) sont flous sur un plan large → toujours prévoir un gros plan dédié. Ses photos d'exemple (selfies) = jamais envoyées au modèle.
- **Jonc réel (photo fournisseur envoyée le 03/11)** : jonc ouvert **fin (≈ 4 mm)**, acier argenté poli, face plate gravée,
  **un petit cœur ajouré à chaque extrémité** (à l'arrière du poignet). Fiches et aperçu de gravure (atelier, fiche, vignette) refaits avec ce jonc (05/11 :
  `contenu/lou/jonc-vierge-v3/` 3 finitions vierges, tables JONC de lou.js en repère 1024, `scripts/mesure_jonc.py`).
- **Politiques (décision utilisateur 03/11) = exactement celles de Corps-Confiant**, même éditeur, sauf l'e-mail
  **`contact@lesmotsdelou.fr`** et les retours (bijoux personnalisés : pas de rétractation, L221-28 3° ; correction/annulation
  tant que la fabrication n'a pas commencé ; garantie légale 2 ans, frais à notre charge). Modèles : `contenu/politiques/*.html`
  avec `{{EDITEUR}}` / `{{ADRESSE}}` ; envoi : `python3 scripts/publier_politiques.py --depuis /home/user/boutique-corps-confiant/contenu/politiques.json`
  (cloner ce dépôt d'abord) ou variables `LOU_EDITEUR` / `LOU_ADRESSE`. `sauvegarde.py` ne recopie plus les mentions légales
  ni les coordonnées (identité). **Livraison = exactement Corps-Confiant (décision utilisateur 03/11)** : zone « France et Belgique » (marché Belgique créé) :
  « Livraison standard » 4,90 € (< 39,90 €), « Livraison standard offerte » dès 39,90 €, **« Livraison + Garantie 2 mois 🛡️ » 7,90 €**
  (même délai ; pour Lou = 2 mois pour renvoyer le bijou **même personnalisé**, remboursé, non porté, emballage d'origine, renvoi à
  la charge de la cliente). Pas d'international (pas demandé).
  ⚠️ **La boutique est passée à « l'expédition par marché »** : les tarifs vus au paiement sont ceux de **chaque marché**
  (`marketUpdate(input:{delivery:{shipping:{optionDefinitionsToCreate/ToDelete}}})`, lecture `markets{delivery{shipping{…}}}`),
  PAS ceux de `deliveryProfileUpdate` (ancien système, modifié pour rien le 03/11). Réglé : France et Belgique = « Livraison
  standard » 4,90 € gratuite dès 39,90 € (`freeDeliveryMinimumValue`) + « Livraison + Garantie 2 mois 🛡️ » 7,90 €.
  ⚠️ **Chaque tarif doit avoir l'emplacement « Shop location »** (`rateGroups … conditions: { originLocationsToAdd }`) : sans lui,
  le panier répond « plus en stock » (incident du 05/11).
- **Référencement (04/11)** : titre et méta-description de l'accueil et de la page d'attente dans `theme-lou/layout/*.liquid` ;
  fiches et collections : `scripts/seo.py` (mot-clé d'abord, titre ≤ 60, description ≈ 150, rien de non vérifié, aucune mention IA).
- **Pinterest (04/11)** : règles `docs/pinterest-regles.md`, textes `docs/pinterest-compte.md`, plan `docs/pinterest-connexion.md` ;
  épingles par CSV (`scripts/pinterest_csv.py`), appli développeur propre à Lou (pas celle de Corps-Confiant), clés en variables
  d'environnement `PINTEREST_*` (jamais dans le chat). « Image virtuelle » dans les épingles où l'on voit Lou.
- **Stock (05/11)** : dropshipping → stock suivi à **999 par variante** + vente autorisée à 0 (CONTINUE), sinon les produits
  apparaissent « épuisés » (catalogues Pinterest/Google). À remettre à 999 si une variante est ajoutée.
- **Cookies (05/11)** : bandeau du thème (`snippets/cookie-banner.liquid`, `assets/lou-cookies.js`, API de consentement Shopify),
  comme Corps-Confiant ; bannière Shopify à laisser désactivée ; page « Cookies et partenaires » à mettre à jour à chaque appli/balise.
- ⚠️ **Le dépôt GitHub est PUBLIC** : jamais d'adresse, de téléphone, de SIRET ni de donnée personnelle dedans (les mentions
  légales gardent des `[À COMPLÉTER]`, à remplir directement dans Shopify).
- **Nouvelle session : lire `docs/reprise.md`** (état d'avancement, prochaines étapes).

- **Outils (décision utilisateur 05/11)** : ne PAS utiliser l'outil Claude Docs (demande une autorisation à chaque appel).
  Pour montrer des images ou un document : page HTML autonome dans le dépôt envoyée par SendUserFile (ex.
  `contenu/pinterest/epingles-apercu.html`). L'utilisateur ne veut pas avoir à accepter d'actions.

## Mémoire du projet sur GitHub (règle obligatoire)
Ce dépôt est la **mémoire** du projet : une nouvelle session ne sait que ce qui y est écrit. **À chaque nouvelle information ou
modification, mettre à jour la mémoire et la pousser sur GitHub, sans attendre qu'on le demande** :
1. **Fichier reçu** → le ranger (`produits/`, `contenu/`, `docs/`, `theme-lou/`).
2. **Modification de la boutique** → `python3 scripts/sauvegarde.py` (recopie l'état réel de la boutique dans le dépôt).
3. **Nouvelle info ou décision** → `CLAUDE.md` (Contexte) ou `docs/`.
4. **Toujours** une entrée datée dans `docs/journal.md`.
5. Vérifier qu'aucun secret ni donnée client n'est inclus, puis **commit et push sur `main`**.

Automatisation (`.claude/settings.json`) : `git pull` au démarrage ; `scripts/hooks/verif_memoire.sh` bloque la fin d'une réponse
tant qu'il reste des modifications non commitées ou non poussées.

## Conseils légaux (préférence utilisateur)
- Donner **à chaque fois** le conseil légal pertinent (consommation, promotions, publicité, IA…), clairement et brièvement.
- **Veille légale obligatoire** : se tenir informé des nouvelles règles (CNIL/RGPD, consommation, e-mails, IA, règles pub
  Meta/Pinterest/Google/TikTok, douane) et **prévenir l'utilisateur dès qu'une nouveauté impose de modifier les textes**.
  Méthode et journal : `docs/veille-legale.md` (le consulter en début de session).
- **La décision finale revient toujours à l'utilisateur.** Une fois le conseil donné, appliquer son choix sans insister.
- Points déjà identifiés pour cette boutique : caractère virtuel de Lou / IA écrit **UNIQUEMENT sur la page « Qui est Lou »**
  (décision utilisateur 04/11, après l'avoir vu dans Google : plus dans l'accueil, la page d'attente, la FAQ, l'assistante, les
  textes alternatifs des photos, les mentions légales ni les CGV ; conseil légal donné) ; mention « image virtuelle » / étiquettes IA ajoutées par l'utilisateur en publiant (loi n° 2023-451, AI Act) ;
  ne jamais faire croire que Lou existe ou fabrique les bijoux ; acier 316L sans nickel (REACH) ; jamais « or » si c'est du plaqué ;
  **pas de droit de rétractation pour un bijou personnalisé** (à écrire dans les CGV, garantie légale due) ; prix barrés :
  **décision utilisateur 05/11 = comme Corps-Confiant, prix × 1,25 arrondi aux 10 centimes (-20 %)**, plus de « prix de lancement »
  (conseil légal donné : L112-1-1, prix barré = prix le plus bas des 30 jours ; à recalculer si le prix change) ; délai de livraison
  annoncé ; médiateur de la consommation obligatoire ; douane 3 €/catégorie depuis le 01/07/2026.

## Règles de sécurité (prioritaires)
- **Prévenir l'utilisateur chaque fois que quelque chose est dangereux à envoyer dans le chat** (mots de passe, clés API, Client
  Secret, infos bancaires, pièces d'identité, données clients). Proposer à la place les variables d'environnement.
- Ne jamais afficher, logger ni committer un secret ou un jeton d'accès. Ne jamais committer de données personnelles de clients.
- N'envoyer les identifiants Shopify qu'à `$SHOPIFY_STORE` (`*.myshopify.com`).
- **Vérifier en début de session que `SHOPIFY_STORE` est bien la boutique Les Mots de Lou** (`python3 scripts/shopify.py check`)
  et pas Corps-Confiant : les deux projets ont des environnements cloud séparés.
- Avant une action difficile à annuler (suppression, changement de thème publié, mise en ligne, retrait du mot de passe) :
  demander confirmation.

## Connexion à Shopify
Identifiants dans les variables d'environnement de l'environnement cloud **« Les Mots de Lou »** (jamais dans le dépôt) :
`SHOPIFY_STORE` (`xxxx.myshopify.com`), `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET`. App **« Claude api LOU »** créée dans le Dev
Dashboard Shopify, installée sur la boutique avec toutes les portées Admin API ; jeton par *client credentials* (~24 h), mis en
cache dans `.shopify_token.json` (ignoré par git).

```bash
python3 scripts/shopify.py check                     # teste la connexion, affiche infos boutique
python3 scripts/shopify.py gql '{ shop { name } }'   # requête GraphQL Admin
```
Depuis Python : `from shopify import graphql` (avec `scripts/` dans le path). Préférer l'API GraphQL Admin.

## Images et vidéos IA (fal.ai pour Lou, OpenAI en secours)
`scripts/images_ia.py` crée ou retouche des images via l'API d'OpenAI. Clé = « Network secret » de l'environnement cloud (site
`api.openai.com`, en-tête Authorization, injectée par le proxy) ou `OPENAI_API_KEY`. Jamais dans le chat ni le dépôt.
Images rangées dans `contenu/images-ia/` avec leur prompt. **Lou doit rester la même d'une image à l'autre** (toujours repartir
de `contenu/lou/reference-v3/` avec `scripts/fal_images.py` + Nano Banana Pro 4K, voir Contexte). **Ne jamais altérer l'apparence réelle des bijoux** (forme, couleur, taille,
gravure) : partir des photos fournisseur pour les bijoux.

```bash
python3 scripts/images_ia.py check
python3 scripts/images_ia.py creer "prompt" --nom lou-portrait --format portrait
python3 scripts/images_ia.py modifier "prompt" contenu/lou/reference.png --nom lou-collier
```

## Organisation du dépôt
- `scripts/` — accès Shopify, sauvegarde, envoi du thème (`envoyer_theme.py` → dossier `theme-lou/`), images IA, Klaviyo
- `produits/` — `catalogue.json` (état réel, via `sauvegarde.py`) ; `contenu/` — pages, politiques, menus, images IA, Lou
- `theme/` — thème publié (via `sauvegarde.py`) ; `theme-lou/` — source du thème de la boutique (à créer)
- `docs/` — reprise, journal, marque, recherche, leçons, veille légale
