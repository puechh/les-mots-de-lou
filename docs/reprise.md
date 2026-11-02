# Reprendre le travail dans une nouvelle session

> **Aperçu cliquable de la bêta (page privée claude.ai)** : https://claude.ai/artifact/1d7266ccUAoSGjfGXKjNz4
> (régénérer : banc `scripts/banc_theme.py` puis `scripts/export_apercu.py <dossier>` et republier).
> **Shopify : RIEN n'est encore envoyé** (réseau de l'environnement) → voir le bloc ⛔ ci-dessous.

## ⛔ 02/11/2026 (session d'envoi de la bêta) — Shopify ENCORE BLOQUÉ, rien n'a été envoyé
- `python3 scripts/shopify.py check` → **403 du proxy** sur `xs4brq-7y.myshopify.com` (politique réseau de l'environnement).
- **À faire par l'utilisateur** : sur claude.ai/code, menu de l'environnement cloud **« Les Mots de Lou »** (barre de titre
  de la session) → **Modifier** → **Accès réseau** : niveau « Limité » (ou « Personnalisé ») et ajouter dans
  **Domaines autorisés** : `*.myshopify.com` (ou exactement `xs4brq-7y.myshopify.com`), en laissant cochée la case
  « Autoriser les gestionnaires de paquets ». Enregistrer, puis **ouvrir une NOUVELLE session** (le réglage ne s'applique
  pas aux sessions déjà lancées). Aide : https://code.claude.com/docs/en/cloud-environments#network-access
- Ensuite, dans la nouvelle session : `python3 scripts/shopify.py check` (vérifier que c'est Les Mots de Lou),
  puis `python3 scripts/construire_boutique.py --publier` (jamais exécuté contre l'API réelle : corriger si une mutation est refusée).

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
