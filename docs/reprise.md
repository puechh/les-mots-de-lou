# Reprendre le travail dans une nouvelle session

> **Aperçu cliquable de la bêta (page privée claude.ai)** : https://claude.ai/artifact/1d7266ccUAoSGjfGXKjNz4
> (régénérer : banc `scripts/banc_theme.py` puis `scripts/export_apercu.py <dossier>` et republier).
> Shopify : la boutique est construite et le thème Lou est **publié** (derrière le mot de passe) → voir ci-dessous.

## 🖼️ 03/11/2026 — SITE REMPLI AVEC LA NOUVELLE LOU (carte blanche utilisateur)
- **Accueil** : `lou-hero*.webp` = `contenu/lou/bijoux-v3/01-accueil-sapin.jpg` (recadrages dans `scripts/assets_theme.py`),
  repères `.r-collier` / `.r-jonc` déplacés (lou.css) ; portrait et avatar des bulles = `reference-v3/01-face.jpg`. Envoyé.
- **05/11 : liste de ce qu'il reste avant les annonces → `docs/avant-annonces.md`** (à tenir à jour).
- **Pinterest (04/11)** : règles, textes et CSV prêts (`docs/pinterest-*.md`, `contenu/pinterest/`). Bloquants : réseau
  (api.pinterest.com, cdn.shopify.com), boutique encore privée, compte pro + appli développeur à créer par l'utilisateur.
- **04/11 nuit** : site allégé (« l'essentiel, pas de pavés », décision utilisateur) et bug du quiz corrigé (double toucher).
  Règle : textes courts partout, 1 ligne sous un titre, pas de sections décoratives en plus. Détail : journal du 04/11.
- **Accueil v4 (03/11 soir)** : Lou détourée (3 poses) qui montre 4 pastilles de bijoux (`#scene-lou`, lou.js/lou.css,
  sources `contenu/lou/accueil-png/`). La photo au sapin + zoom (gp-*.webp) n'est plus affichée (fichiers gardés).
- **Accueil** : photo en pleine définition (demande utilisateur « vraiment en 4K ») ; zoom = fondu vers 2 gros plans nets de
  la même scène (`gp-collier.webp`, `gp-jonc.webp`) ; si la photo d'accueil change, refaire ces gros plans et data-gx/gy.
- **Fiches** (`scripts/photos_fiches.py`, carrés 2048 px `contenu/lou/fiches-v3/shopify/`) : produit seul → détails/finitions →
  porté. Jonc : nouvelle photo produit fine avec cœurs (sans coffret), détail cœurs, 3 finitions, poignet, Lou, café. Collier prénom :
  photo produit + finitions, cou « Lou », Lou, marché de Noël. Collier photo : produit, cou, Lou devant la cheminée. Morse : produit,
  macro, carte de Noël, Lou. Textes alternatifs avec « Image virtuelle » quand c'est porté.
- ⚠️ **Reste incohérent : l'« aperçu en direct » du jonc** (1re vue de la fiche, atelier de gravure de l'accueil, vignette animée)
  utilise encore l'ancien jonc large sans cœurs (`jonc-vierge*.webp`, `jonc-carre*.webp`) → refaire un jonc vierge fin à cœurs
  (3 finitions) et re-mesurer la face gravable (tables JONC de lou.js). Idem collier prénom/photo : photos produit encore v2.

## 🚀 03/11/2026 — OUVERTURE EN COURS (Pinterest / Google)
- ✅ **Politiques en ligne, copiées sur Corps-Confiant** (mentions légales, coordonnées, CGV, retours, expédition),
  e-mail `contact@lesmotsdelou.fr`. Reste : **médiateur de la consommation** à souscrire puis ajouter (absent aussi sur
  Corps-Confiant) ; **Livraison copiée sur Corps-Confiant** (France + Belgique, 4,90 € / offerte dès 39,90 € / Garantie 2 mois 7,90 €) ;
  FAQ et fiche produit (Garantie 2 mois) envoyées sur le thème le 03/11 ; vérifier que la boîte contact@lesmotsdelou.fr reçoit bien. Mot de passe à retirer par l'utilisateur. Ensuite : Pinterest (appli Shopify,
  validation du site, catalogue), Google & YouTube (Merchant Center). Fournisseurs DSers à relier AVANT la 1re vente.

## 🎭 03/11/2026 (fin) — LOU DÉFINITIVE : photo `contenu/lou/reference-v3/00-source-lou.webp` + Nano Banana Pro 4K
- L'utilisateur a rejeté les retouches OpenAI (peau « pixelisée », visage mal défini). Comparatif fal.ai sur le même plan
  (`contenu/lou/comparatif-ia/`) : **Nano Banana Pro 4K retenu** (3584×4800, très net, peau lisse naturelle) ; Flux 2 Pro et
  Seedream 5 Pro plus fidèles aux taches de rousseur mais moins définis.
- Planche `contenu/lou/reference-v3/` : 01 face, 02 trois-quarts, 03 profil, 04 rire au café, 05 mains/tasse, 06 miroir en pied,
  07 rue de Paris en automne, 08 canapé. 04 et 07 refaits avec 2 références (ressemblance). ≈ 3 $ fal au total.
- **Étape suivante demandée par l'utilisateur : les plans avec les bijoux** (plage en maillot, gros plans cou / poignet), même
  méthode, bijoux d'après les photos fournisseur. Jonc réel = fin + cœur ajouré à chaque extrémité.
- ✅ **Images bijoux pour le site faites : `contenu/lou/bijoux-v3/`** (Nano Banana Pro 4K, ≈ 2,40 $). Thème choisi : **Noël**
  (lancement avant Black Friday, recherches « idée cadeau » de novembre) + 2 images « toute l'année ». La plage = plus tard
  (fête des mères / été). 01 accueil sapin 16:9 (jonc + collier « Lou ») · 02 marché de Noël · 03 poignet jonc (gravure + cœur)
  1:1 · 04 cou collier prénom 1:1 · 05 collier photo devant la cheminée · 06 Morse, carte de Noël 1:1 · 07 café Paris · 08 rue Paris.
  Bijoux d'après les images de fiches + description du jonc réel (fin, cœurs). **Prochaine étape : les placer sur le site
  (accueil, fiches, Lou) → banc d'abord, accord utilisateur avant envoi.**
- Les images `contenu/images-ia/2026-11-03-lou-v2-*` (ancienne méthode) sont à remplacer.
- Fiche Jonc Shopify à mettre à jour avec les cœurs : il faut la photo fournisseur **en fichier**.

## ✅ 03/11/2026 — clé fal.ai opérationnelle
- Variable `FAL_KEY` (plus de Network secret fal). Test gratuit OK sur `fal.run`, `queue.fal.run`, `rest.fal.ai`,
  `v3.fal.media`, `v3b.fal.media` (`fal.media` seul n'existe pas, sans importance). Détail : `docs/avatar-lou.md`.
- Prochaine étape avatar : LoRA Flux sur ~20 images validées de Lou, Nano Banana Pro, vidéos Kling → **accord avant toute dépense**.

## ✅ 02/11/2026 nuit — REFONTE « LOU, AVATAR DE LA BOUTIQUE » EN LIGNE (derrière le mot de passe)
- **Thème « Les Mots de Lou (thème) » publié par l'utilisateur** ; refonte v0.2 envoyée sans erreur. Tester au banc
  (`python3 scripts/banc_theme.py`) AVANT tout `envoyer_theme.py maj` : c'est le thème en ligne.
- **Lou parle partout** (avatar virtuel assumé) : bulle d'accueil qui s'écrit toute seule, assistante en bas à droite
  (réponses préparées : choisir, idée de phrase, Noël, matière, offre, livraison, « tu es qui ? », contact équipe),
  conseils sur chaque fiche, panier commenté avec jauge -50 %, FAQ en conversation, menu mobile, 404, page d'attente.
- **Aperçus réalistes sur photo** : jonc gravé (3 finitions × 2 polices, gravure qui épouse la face), collier prénom
  accroché à la vraie chaîne (3 finitions), photo de la cliente dans la bulle du collier photo, bracelet Morse dessiné.
  Mini-aperçu flottant sur téléphone, barre « Ajouter au panier » collante, livraison estimée, produit qui vole au panier.
- **Ludique / animé** (GSAP) : titre révélé, cartes qui tombent, cartes problème → solution qui se retournent, machine à
  mots à manette, test des mots, compte à rebours de Noël avec neige, étincelle du laser, cœurs, petits sons, confettis.
- **Images HD 2048 px** sur Shopify et dans le thème (fin du flou sur téléphone).
- **Fiches alignées sur AliExpress** (rapport du 02/11, voir `produits/sourcing-aliexpress.md`) : jonc 20 caractères,
  2 polices, « plupart des poignets » ; collier photo = pendentif métal plaqué + chaîne inox ; Morse = cordon noir seul,
  « perles métalliques » ; **plus aucune promesse d'écrin** (réglage du thème à cocher seulement si le fournisseur le
  confirme par écrit) ; délais 3-7 j + 7-12 j ouvrés (réglages du thème).
- Réseau : `lesmotsdelou.fr` (et `lilytreasures.fr`, `dentica.fr`, `ciaokombucha.com`) non autorisés dans l'environnement
  → Claude ne voit pas la vitrine réelle ni les sites d'inspiration : les ajouter aux domaines autorisés si besoin.

### ⚠️ À faire AVANT d'ouvrir (le mot de passe reste en place)
1. **Fournisseurs (DSers)** : choisir l'annonce de chaque bijou, vérifier prix livré, délais réels, nombre de caractères,
   polices proposées (faire correspondre « Manuscrite / Classique / Moderne » à leurs numéros), finitions, longueur de chaîne,
   **écrin inclus ?** (si oui : cocher le réglage du thème), matière par écrit (grade de l'acier, nickel). Commander un exemplaire
   test de chaque bijou. Comment transmettre le texte/la photo au vendeur (note de commande, maquette avant fabrication).
2. **Photos** : remplacer les images IA par les vraies photos fournisseur si la forme/couleur diffère (puis re-mesurer les
   aperçus du jonc et du collier : méthode dans `docs/journal.md`).
3. **Mentions légales / CGV** : remplir les `[À COMPLÉTER]` directement dans Shopify (identité, SIRET, médiateur).
4. **Paramètres** : livraison France + Belgique, caisse (décocher l'inscription marketing pré-cochée), bannière cookies,
   paiements, domaine `lesmotsdelou.fr` (principal) + `les-mots-de-lou.fr` (redirection).
5. Ajuster les **délais** et la **date limite de Noël** dans les réglages du thème selon le fournisseur choisi
   (si fabrication 8-10 j : date limite plutôt vers le 25-28/11).
6. Commande test (gravure + photo) puis remboursement ; vérifier que la photo et le texte arrivent bien dans la commande.

## 🔥 État au 02/11/2026 fin d'après-midi — BÊTA PRÊTE (carte blanche, utilisateur absent)
**Tout est dans le dépôt ; l'envoi sur Shopify se fait avec `python3 scripts/construire_boutique.py --publier`**
(produits + images, collections, pages, menus, politiques, offre « 2e bijou à -50 % », thème créé ET publié).
La session de construction (02/11) n'avait pas accès à Shopify (réseau du conteneur) : l'envoi a été confié à une session
enfant « Les Mots de Lou : envoi de la bêta sur Shopify ». Vérifier dans `docs/journal.md` si c'est fait.

### Ce qui existe
- Thème sur mesure `theme-lou/` (rose, ludique) : accueil (atelier de gravure en direct, ruban de phrases, cartes inclinées,
  **test des mots**, **machine à mots**, comment ça marche, Lou, réassurance, FAQ), fiche produit avec **aperçu en direct**
  (jonc gravé, collier prénom, pendentif photo, bracelet Morse), finitions, police, envoi de photo, case « j'ai vérifié
  l'orthographe », panier latéral (propriétés de gravure affichées, offre -50 %), collection avec filtres, pages, 404, page
  mot de passe « bientôt » avec inscription. Testé sur le banc local (ordinateur + iPhone 13, aucune erreur JS).
- 4 fiches (`produits/produits.json`) : Jonc « Mes Mots » 29,90 €, Collier Prénom 29,90 €, Collier Souvenir (photo) 34,90 €,
  Bracelet Code Secret 24,90 € ; finitions Argentée/Dorée/Rosée (cordon Noir/Rose poudré/Beige pour le Morse).
- Images IA : `contenu/images-ia/` (produits + Lou). Visage de Lou : `contenu/lou/`.
- Pages : le-test, qui-est-lou, faq, contact, livraison-retours (`contenu/pages/`) ; politiques (`contenu/politiques/`).

### ⚠️ À faire AVANT d'ouvrir (le mot de passe reste en place)
1. **Fournisseurs** : choisir dans DSers (liens dans `produits/sourcing-aliexpress.md`), vérifier prix livré, délais,
   **grade de l'acier / nickel par écrit** (sinon ne pas écrire 316L), écrin cadeau disponible ? Relier chaque fiche dans DSers.
2. **Images produits = IA** : les comparer aux vraies photos fournisseur ; remplacer si la forme/couleur/gravure diffère
   (règle : ne jamais tromper sur l'apparence). L'image « collier photo » montre un rendu idéalisé de la projection.
3. **Mentions légales / CGV** : remplir les `[À COMPLÉTER]` (identité, SIRET, médiateur, e-mail) dans Shopify ou ici
   (⚠️ dépôt public) ; vérifier la phrase sur les droits de douane dans `livraison-retours` (`[À VÉRIFIER]`).
4. **Livraison** (Paramètres → Livraison/Marchés : France + Belgique, tarif choisi), **caisse** (décocher l'inscription
   marketing pré-cochée), **bannière cookies** Shopify, **paiements**, domaine `lesmotsdelou.fr` (principal) +
   `les-mots-de-lou.fr` (redirection).
5. Tester une commande (avec gravure + photo) puis la rembourser ; vérifier que la photo envoyée arrive dans la commande.
6. L'utilisateur a décidé que le caractère virtuel de Lou va dans les politiques : la bêta l'indique aussi en petit sous la
   section Lou de l'accueil (conseil AI Act art. 50 / loi 2023-451) → **à confirmer par l'utilisateur** (retirer si refus).

### Prochaines étapes
- Avatar ultra-réaliste (session dédiée → `docs/avatar-lou.md`), puis refaire les mises en scène de Lou avec la planche.
- Créatives Pinterest (crédit 420 €) et Meta/TikTok, vidéos IA ; Klaviyo (bienvenue, panier abandonné) en brouillon.
## 🎭 Avatar de Lou (02/11/2026 soir)
- Planche de référence prête (`contenu/lou/reference/`, à faire valider par l'utilisateur) ; méthode : `gpt-image-2.5-flare` en retouche avec 2 images de la planche (`docs/avatar-lou.md`). Vidéos : clé fal.ai à ajouter (Kling/Veo).


## 🔥 État au 02/11/2026 (1re session sur ce dépôt)
- Environnement cloud OK : variables `SHOPIFY_*` présentes (boutique `xs4brq-7y.myshopify.com`, app « Claude api LOU »).
- ❌ **Shopify inaccessible** : la politique réseau de l'environnement bloque `xs4brq-7y.myshopify.com` (403 au proxy) →
  l'utilisateur doit ajouter `*.myshopify.com` (ou le domaine exact) aux domaines autorisés de l'environnement « Les Mots de Lou ».
  Puis refaire `python3 scripts/shopify.py check` et **vérifier que c'est Les Mots de Lou et pas Corps-Confiant**.
- ✅ Clé OpenAI OK (gpt-image-2 dispo) mais ❌ **crédit OpenAI épuisé** (429) → l'utilisateur doit recharger (platform.openai.com
  → Billing). Les 3 visages de Lou sont prêts à générer : `contenu/lou/prompts-visages.md`.
- Domaines : `les-mots-de-lou.fr` déjà possédé ; `lesmotsdelou.fr` à prendre = adresse principale. DSers : recherches pas faites.

## 🔥 État au 02/11/2026 soir (création du projet)
- Dépôt créé par l'utilisateur et préparé depuis la session Corps-Confiant : outils copiés (`scripts/`), instructions (`CLAUDE.md`),
  recherche produits (`docs/recherche-produits.md`), marque (`docs/marque.md`), leçons (`docs/lecons-corps-confiant.md`).
- **Rien n'existe encore côté Shopify.**

## Ce que l'utilisateur doit faire (dans l'ordre)
1. Shopify : créer la boutique « Les Mots de Lou » (menu des boutiques → Créer une boutique), puis dans le Dev Dashboard
   l'app « Claude api » avec toutes les portées Admin, installée sur la boutique.
2. Claude : **nouvel environnement cloud « Les Mots de Lou »** avec les variables `SHOPIFY_STORE`, `SHOPIFY_CLIENT_ID`,
   `SHOPIFY_CLIENT_SECRET` (de la NOUVELLE boutique) + Network secret OpenAI (`api.openai.com`). Ne jamais coller de clé dans le chat.
3. Lancer une session sur ce dépôt avec cet environnement : « Lis CLAUDE.md et on commence ».
4. Réserver `lesmotsdelou.fr` et `.com` (IONOS) ; vérifier la marque sur data.inpi.fr.
5. Dans DSers : chercher « custom name necklace 316L », « engraved bangle 316L », « photo projection necklace » → prix livré
   en France, délai, fournisseurs (captures pour Claude).

## Prochaines étapes de Claude (planning ≈ 5 jours, pubs lancées vers le 9-10/11)
1. Vérifier la connexion (`python3 scripts/shopify.py check`) : c'est bien la nouvelle boutique.
2. 3 versions du visage de Lou → choix → planche de référence (`contenu/lou/`).
3. Identité : logo, couleurs, typographies, ton de voix.
4. Choix des fournisseurs (avec les captures DSers) → produits, prix (« prix de lancement », pas de prix barrés inventés),
   personnalisation (champ prénom/texte/photo sur la fiche).
5. Thème sur mesure (`theme-lou/`), pages légales (CGV avec l'exception de rétractation pour le personnalisé, mentions,
   livraison, cookies), paramètres (livraison France/Belgique, caisse, bannière cookies).
6. Créatives et vidéos IA de Lou (mention « image virtuelle »), Pinterest (crédit 420 €), puis Meta/TikTok.
7. Commande test, puis ouverture (accord de l'utilisateur).
