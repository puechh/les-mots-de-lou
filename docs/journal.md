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
