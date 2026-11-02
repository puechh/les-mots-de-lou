# Reprendre le travail dans une nouvelle session

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
