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
  fabrication comprise** (jours calendaires, décision 03/11) ; icône « Mon compte » dans l'en-tête ; accueil = Lou qui
  porte le jonc et le collier (repères animés) ; vignettes produits animées (la personnalisation se « remplit »).
  Machine à mots sous les bijoux (accueil) et sous « Caractéristiques » (jonc, bracelet) ; **Noël : avant le 10 décembre**.
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
  Vérifier un recadrage à 100 % avant d'envoyer. Ses photos d'exemple (selfies) = jamais envoyées au modèle.
- **Jonc réel (photo fournisseur envoyée le 03/11)** : jonc ouvert **fin (≈ 4 mm)**, acier argenté poli, face plate gravée,
  **un petit cœur ajouré à chaque extrémité** (à l'arrière du poignet). C'est la seule différence avec les images IA actuelles
  (qui ont aussi un jonc plus large) → images du jonc (fiche + aperçu de gravure du thème) à refaire et à envoyer sur Shopify.
- ⚠️ **Le dépôt GitHub est PUBLIC** : jamais d'adresse, de téléphone, de SIRET ni de donnée personnelle dedans (les mentions
  légales gardent des `[À COMPLÉTER]`, à remplir directement dans Shopify).
- **Nouvelle session : lire `docs/reprise.md`** (état d'avancement, prochaines étapes).

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
- Points déjà identifiés pour cette boutique : caractère virtuel de Lou écrit **dans les politiques, pas dans le slogan**
  (décision utilisateur 02/11) ; mention « image virtuelle » / étiquettes IA ajoutées par l'utilisateur en publiant (loi n° 2023-451, AI Act) ;
  ne jamais faire croire que Lou existe ou fabrique les bijoux ; acier 316L sans nickel (REACH) ; jamais « or » si c'est du plaqué ;
  **pas de droit de rétractation pour un bijou personnalisé** (à écrire dans les CGV, garantie légale due) ; boutique neuve =
  **pas de prix barrés inventés** (règle du prix le plus bas des 30 jours, L112-1-1) → « prix de lancement » ; délai de livraison
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
