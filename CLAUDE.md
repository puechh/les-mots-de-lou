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
  Concept, ton et règles : `docs/marque.md`. Domaines `lesmotsdelou.fr` / `.com` libres au 02/11 (à réserver par l'utilisateur, IONOS).
- **Tout en IA** : photos **et vidéos** (pas de tournage).
- **Pub** : environ 300 € par boutique + **420 € de crédit Pinterest offert**. Pinterest en priorité (femmes 25-55 ans), puis Meta/TikTok.
- Leçons tirées de Corps-Confiant (pièges Shopify, Klaviyo, cookies, pubs) : `docs/lecons-corps-confiant.md`.
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
`SHOPIFY_STORE` (`xxxx.myshopify.com`), `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET`. App « Claude api » créée dans le Dev
Dashboard Shopify, installée sur la boutique avec toutes les portées Admin API ; jeton par *client credentials* (~24 h), mis en
cache dans `.shopify_token.json` (ignoré par git).

```bash
python3 scripts/shopify.py check                     # teste la connexion, affiche infos boutique
python3 scripts/shopify.py gql '{ shop { name } }'   # requête GraphQL Admin
```
Depuis Python : `from shopify import graphql` (avec `scripts/` dans le path). Préférer l'API GraphQL Admin.

## Images et vidéos IA (API OpenAI)
`scripts/images_ia.py` crée ou retouche des images via l'API d'OpenAI. Clé = « Network secret » de l'environnement cloud (site
`api.openai.com`, en-tête Authorization, injectée par le proxy) ou `OPENAI_API_KEY`. Jamais dans le chat ni le dépôt.
Images rangées dans `contenu/images-ia/` avec leur prompt. **Lou doit rester la même d'une image à l'autre** (toujours repartir
des images de référence validées, `contenu/lou/`). **Ne jamais altérer l'apparence réelle des bijoux** (forme, couleur, taille,
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
