# Journal des modifications

## 2026-11-02 — Création du projet
- Idée née dans le projet Corps-Confiant : 2e boutique pour Noël 2026. Recherche produits (deux tours, coûts AliExpress) →
  choix de l'utilisateur : **bijoux personnalisés** ; marque **« Les Mots de Lou »** avec une égérie virtuelle (idée utilisateur).
- Dépôt préparé : `CLAUDE.md`, outils (`shopify.py`, `sauvegarde.py`, `envoyer_theme.py` → `theme-lou/`, `images_ia.py`,
  `klaviyo.py`, hook de mémoire), `docs/` (reprise, marque, recherche, leçons Corps-Confiant, veille légale).
- Décision : le slogan ne dit pas que Lou n'existe pas ; mention dans les politiques ; slogans proposés dans `docs/marque.md`.
- Slogan choisi par l'utilisateur : « Vos mots, gravés pour toujours. »

## 2026-11-02 (après-midi) — 1re session sur le dépôt
- Lecture de la mémoire. `shopify.py check` : ❌ bloqué par le réseau de l'environnement (myshopify.com non autorisé).
  `images_ia.py check` : ✅ clé OK. Infos utilisateur : app « Claude api LOU » ; domaine `les-mots-de-lou.fr` déjà possédé,
  `lesmotsdelou.fr` = adresse principale ; recherches DSers pas encore faites.
- Visages de Lou : 1 image test OK puis **crédit OpenAI épuisé** (429). Prompts des 3 versions dans `contenu/lou/prompts-visages.md`.

## 2026-11-02 (après-midi, suite) — Bêta « carte blanche » (utilisateur absent)
- Demande : bêta complète en rose, très ludique (test), inspirée des sites donnés pour Corps-Confiant (Lily's Treasures,
  Dentica, Ciao Kombucha) et de Corps-Confiant ; carte blanche, pas de questions.
- Réseau : Shopify et AliExpress toujours bloqués dans ce conteneur (réglage réseau appliqué aux nouvelles sessions seulement).
- 3 visages générés (`contenu/lou/propositions/`) ; **visage C retenu provisoirement** (`contenu/lou/reference-visage.png`).
- L'utilisateur veut **un seul visage (Lou), le plus réaliste possible** → session Claude séparée « avatar de Lou ultra-réaliste »
  créée pour chercher la meilleure méthode (rapport attendu dans `docs/avatar-lou.md`, planche dans `contenu/lou/reference/`).
- Annonces AliExpress repérées (non vérifiées) : `produits/sourcing-aliexpress.md`. Fiches de la bêta : `produits/produits.json`.

## 2026-11-02 (soir) — Avatar de Lou : méthode et planche de référence (session parallèle, utilisateur absent)
- Recherche web (nov. 2026) sur les égéries IA cohérentes (OpenAI, Nano Banana, Flux.2, Seedream, Midjourney, Higgsfield, LoRA,
  vidéo Kling/Veo/Sora/Runway/HeyGen) → rapport `docs/avatar-lou.md`.
- 3 essais de réalisme (gpt-image-2, 2.5-flare, 2.5-sunburst) à partir du visage C → **flare retenu** (peau la plus naturelle,
  11 s, pas de 502). Visage C conservé.
- Planche de référence (face, trois-quarts, profil, sourire, mains) dans `contenu/lou/reference/` + `planche-lou.jpg`, prompts en .txt.
  Outil `contenu/lou/generer_lou.py` (sortie dans contenu/lou/, nouvel essai auto sur 502). 8 images au total (qualité medium).
- Recommandation vidéo : compte fal.ai (Kling 3.0 / Veo) — à créer par l'utilisateur si accord (étapes dans le rapport).
- ⚖️ Décret n° 2026-233 du 30/03/2026 (modalités de la mention « image virtuelle ») signalé, à vérifier sur Légifrance.
- Thème `theme-lou/` écrit (rose, ludique : atelier de gravure en direct, test des mots, machine à mots, cartes inclinées,
  aperçus jonc / prénom / photo / Morse), testé sur le banc local `scripts/banc_theme.py` (ordinateur + iPhone 13 : aucune
  erreur JS, aucun débordement). Pages (`contenu/pages/`), politiques avec `[À COMPLÉTER]` (`contenu/politiques/`).
- Choix de prudence : pas de « carte message » (rien ne prouve que le fournisseur l'imprime) ; pas de « 316L / sans nickel »
  sur les fiches tant que le fournisseur ne l'a pas confirmé ; image du coffret retirée des fiches (le jonc y a un motif non vendu).
- Images IA produits + Lou (`contenu/images-ia/`) ; `gpt-image-2` donne souvent des 502 → utiliser `gpt-image-2.5-flare`
  (conseil de la session avatar, `docs/avatar-lou.md`). Portrait et avatar du thème = planche `contenu/lou/reference/`.
- Script `scripts/construire_boutique.py` (produits, images, collections, pages, menus, politiques, offre -50 %, thème).
  Veille légale faite (AI Act art. 50 applicable depuis le 02/08/2026 ; douane 3 €/catégorie).

## 2026-11-02 (fin de journée) — Session d'envoi de la bêta sur Shopify : bloquée
- `shopify.py check` → 403 du proxy sur `xs4brq-7y.myshopify.com` (journal du proxy : « policy denial »). Le domaine n'est
  toujours pas autorisé dans l'environnement « Les Mots de Lou » (ou la session a été lancée avant le changement).
- Rien envoyé, rien modifié côté Shopify. Consigne ajoutée en haut de `docs/reprise.md` (où cliquer pour autoriser le domaine,
  puis nouvelle session et `construire_boutique.py --publier`).
- Shopify toujours bloqué (la session d'envoi a confirmé le 403). Aperçu statique cliquable publié pour l'utilisateur :
  https://claude.ai/artifact/1d7266ccUAoSGjfGXKjNz4 (script `scripts/export_apercu.py`). Accueil mobile : photo de Lou en tête.
  Captures : `docs/captures/`.
