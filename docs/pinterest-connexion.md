# Pinterest Les Mots de Lou : plan de connexion (04/11/2026)

But : compte professionnel propre, 5 tableaux, épingles publiées régulièrement (d'abord par CSV, ensuite par l'API).

## État au 04/11/2026
- Environnement vérifié : `SHOPIFY_STORE` = xs4brq-7y.myshopify.com (Les Mots De Lou) ✅
- ❌ `api.pinterest.com`, `www.pinterest.com` et `cdn.shopify.com` **bloqués** par le réseau de l'environnement (refus 403).
- Aucune clé Pinterest dans l'environnement.
- La boutique est encore **privée** (mot de passe) : Pinterest ne peut ni revendiquer le site, ni lire les fiches → à lancer avant.

## Étape 0 — Ouvrir le réseau (utilisateur)
Barre de titre de la session → menu de l'environnement cloud « Les Mots de Lou » → **Modifier** → **Accès réseau** → **Domaines
autorisés** : ajouter `api.pinterest.com`, `api-sandbox.pinterest.com`, `www.pinterest.com`, `cdn.shopify.com` (laisser cochée la case
des gestionnaires de paquets). Pris en compte dans une **nouvelle session**. Doc : https://code.claude.com/docs/en/cloud-environments#network-access

## Étape 1 — Compte professionnel (utilisateur, ~10 min)
1. Sur pinterest.com, connecté au compte de Corps-Confiant : photo de profil (en haut à droite) → **Ajouter un compte** →
   **Créer un compte professionnel** (jusqu'à 4 comptes pro liés à la même connexion : les deux boutiques restent séparées).
   Ou un compte neuf avec l'e-mail `contact@lesmotsdelou.fr`.
2. Remplir le profil avec les textes de `docs/pinterest-compte.md`.
3. Créer les **5 tableaux** avec leurs noms exacts et leurs descriptions (même fichier).

## Étape 2 — Relier la boutique (utilisateur, après le lancement de la boutique)
Shopify → **Applications** → installer **Pinterest** → **Se connecter** avec le compte pro Les Mots de Lou → l'appli revendique
`lesmotsdelou.fr`, installe la balise Pinterest et envoie le **catalogue** (épingles produits avec prix). ⚖️ La balise dépose des
cookies : elle doit attendre l'accord de la bannière cookies (Shopify → Paramètres → Confidentialité des clients).

## Étape 3 — Programmer le 1er mois (sans API)
Pinterest → **Créer** → **Créer des épingles en masse** (ou « Importer un fichier CSV ») → envoyer
`contenu/pinterest/epingles-2026-11.csv`. Vérifier ensuite 2-3 épingles programmées (image, lien, date/heure). Si l'option CSV n'existe
pas sur le compte (Pinterest la réserve parfois au gestionnaire de publicités), le dire à Claude : on passera par l'API (étape 4).
⚠️ La 1re épingle est programmée le 06/11 : la boutique doit être en ligne avant, sinon les liens tombent sur la page « bientôt ».

## Étape 4 — Appli développeur (utilisateur, ~10 min)
1. https://developers.pinterest.com → se connecter avec le **compte pro Les Mots de Lou** → **Mes applications** → **Connecter une appli**.
2. Nom : `Les Mots de Lou – publication` ; description : `Publication des épingles et tableaux de la boutique Les Mots de Lou
   (lesmotsdelou.fr) depuis notre outil interne.` ; site : `https://lesmotsdelou.fr` ; adresse de redirection (redirect URI) :
   `https://lesmotsdelou.fr/`.
3. **Réutiliser l'appli de Corps-Confiant ?** Techniquement possible (une appli peut être autorisée par un autre compte), mais
   **déconseillé** : l'accès Standard est examiné pour UNE appli et UN usage, et les deux boutiques doivent rester séparées (CLAUDE.md).
   → une appli par boutique.
4. Après validation (accès **Trial**, en général rapide) : dans la page de l'appli → **Générer un jeton** avec les autorisations
   `boards:read`, `boards:write`, `pins:read`, `pins:write`, `user_accounts:read`.
5. **Ne jamais coller la clé ni le jeton dans le chat.** Les mettre dans l'environnement : menu de l'environnement → Modifier →
   **Variables d'environnement** :
   - `PINTEREST_ACCESS_TOKEN` = le jeton (valable ~30 jours)
   - `PINTEREST_APP_ID` et `PINTEREST_APP_SECRET` = identifiants de l'appli (pour renouveler le jeton)
   Puis nouvelle session.
6. Claude teste (`GET /v5/user_account`), crée les tableaux s'ils manquent et une épingle test. ⚠️ En **Trial**, ce que crée
   l'API n'est **visible que par vous** (bac à sable).

## Étape 5 — Accès Standard (pour publier pour de vrai)
Page de l'appli → **Demander l'accès Standard** → formulaire + **vidéo de démonstration** (enregistrement d'écran : connexion OAuth et
création d'une épingle avec l'outil). Claude prépare l'outil et le script de la vidéo une fois l'étape 4 faite. Délai : souvent
plusieurs semaines → le CSV (étape 3) couvre l'attente.

## Ensuite
Chaque mois : `python3 scripts/pinterest_csv.py` (nouvelles épingles, nouvelles images) puis import, ou publication directe par l'API
quand l'accès Standard est accordé.
