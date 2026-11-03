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

## 2026-11-02 (soir) — Bêta envoyée sur Shopify
- L'utilisateur a ouvert l'accès réseau : `shopify.py check` ✅ « Les Mots De Lou » (xs4brq-7y), boutique vide au départ.
- `construire_boutique.py` exécuté : 4 produits + 8 images, 3 collections, 5 pages, 3 menus, 4 politiques, offre BXGY.
- Corrections : offre « 2e bijou à -50 % » → Shopify refuse « tous les produits » pour une offre BXGY, on liste
  maintenant les produits actifs (et le script signale un vrai échec) ; thème : `lou-footer` refusé (« default » d'un
  link_list ne peut être que main-menu/footer) → défaut retiré, le pied de page lit le menu `legal` par défaut ;
  l'étape thème ne publie plus si l'envoi a des erreurs.
- Thème créé et envoyé sans erreur ; banc local ✅ (accueil, fiche, collection, panier, FAQ ; ordinateur + iPhone 13,
  aucune erreur Liquid/JS). **Publication bloquée** par la sécurité de Claude Code → à confirmer par l'utilisateur.
- Vitrine en ligne non visible depuis la session : redirection vers `lesmotsdelou.fr`, domaine non autorisé dans le réseau.
- `sauvegarde.py` : catalogue, collections, pages, menus, politiques, thème Horizon publié. Vérifié : aucune donnée
  personnelle (seulement des `[À COMPLÉTER]` et contact@lesmotsdelou.fr).

## 2026-11-02 (soir, suite) — Atelier de l'accueil : vraie photo du jonc
- Demande utilisateur : remplacer le dessin du jonc par le « vrai » bijou, avec le texte tapé gravé dessus en direct.
- Photo fournisseur impossible à récupérer (AliExpress bloque les robots, fournisseur pas encore choisi) → retouche IA
  de la photo produit du jonc **sans la gravure** (`contenu/images-ia/2026-11-02-produit-jonc-vierge.png`, même bijou,
  même décor), recadrée en `theme-lou/assets/jonc-vierge.webp` (`assets_theme.py`).
- Le texte est posé en SVG sur une courbe calée sur la face avant du jonc (police manuscrite, effet gravé), il rétrécit
  s'il est long ; mention « Simulation de gravure » sous l'image. Testé au banc (ordinateur + iPhone, sans erreur JS),
  envoyé sur le thème Shopify (toujours non publié). Captures : `docs/captures/atelier-photo-*`.
- `images_ia.py` : modèle par défaut `gpt-image-1` (retiré par OpenAI) → `gpt-image-2` ; la retouche a marché avec
  `OPENAI_IMAGE_MODEL=gpt-image-2.5-flare` (gpt-image-2 renvoyait 502).
- À faire quand le fournisseur sera choisi : remplacer la photo par celle du vrai jonc vierge, puis réajuster la courbe
  (`d="M 90 352 Q 470 425 865 250"` dans `sections/lou-accueil.liquid`).

## 2026-11-02 (soir, suite 2) — Atelier : la gravure épouse vraiment le jonc
- Demande utilisateur : texte qui suit la forme du bracelet, aspect vraiment gravé, aucune lettre qui dépasse.
- Mesure des bords de la face avant sur la photo (profil de luminosité colonne par colonne : chute « liseré brillant →
  face » pour le bord haut, ligne d'ombre pour le bord bas ; lissage polynôme degré 4, écart < 2 px) + extrémités du
  jonc (x ≈ 130 et 950 → ellipse cx 540, a 410 dans l'image 1024). Tables dans `JONC` de `theme-lou/assets/lou.js`
  (repère du recadrage 920×460).
- Rendu canvas (`LOU_graverJonc`) : texte écrit à plat sur une bande « déroulée », taille calculée pour que l'encre
  tienne dans 78 % de la hauteur de la face ; repli colonne par colonne entre bord haut et bord bas (verticales
  verticales, resserrement vers les côtés x = cx + a·sin θ) ; découpe à la forme exacte de la face (rien ne dépasse) ;
  incrustation : creux sombre en « multiplier » (suit les reflets du métal) + liseré clair en « écran » sous le trait.
- Testé au banc (ordinateur ×2, iPhone 13 ; textes court, long, jambages, 3 lettres ; aucune erreur JS), envoyé sur le
  thème Shopify (non publié). Captures `docs/captures/atelier-*`.

## 2026-11-02 (nuit) — Refonte complète : Lou avatar de la boutique, ludique, mobile, HD, fiches alignées AliExpress
- Demandes utilisateur : revoir toute la boutique « en cliente » (surtout téléphone), plus ludique et animée comme
  Corps-Confiant, images nettes, produits fidèles à AliExpress ; puis « boutique axée sur Lou, qu'on comprenne que c'est
  l'avatar du site » (exemple Lily's Treasures). Utilisateur absent : pas de questions.
- Audit iPhone : débordement horizontal (ruban), prix sur 2 lignes, hero trop haut (atelier invisible), aperçus en dessin,
  aperçu invisible pendant la saisie, boutons qui passent à la ligne, images trop petites (panier) ou agrandies (hero).
- Vérification AliExpress (recherche web, AliExpress bloque les robots) : produits existants, promesses corrigées
  (cf. reprise) ; ⚖️ annoncer un écrin ou une matière non livrés = pratique commerciale trompeuse (L121-2).
- Images : `images_ia.py` (formats HD 2048, modèle gpt-image-2.5-flare) ; `scripts/images_hd.sh` (refonte HD fidèle de
  toutes les images + jonc vierge doré/rosé), `scripts/images_hd2.sh` (collier sans pendentif ×3 finitions, portrait HD) ;
  JPEG 92 dans `contenu/images-ia/*-hd.jpg`. Produits Shopify : images remplacées (`construire_boutique.py produits --images`,
  suppression par `fileDelete`), Morse réduit au cordon noir.
- Mesures pour les aperçus : bords du jonc vérifiés sur les 3 finitions HD (écart médian < 1,5 px) ; anneaux du collier
  vierge (1200 px) : (501, 860) et (740, 859) ; bulle du collier photo : centre (888,5 ; 438,5), rayon 176.
- Thème v0.2 : `lou.css` réécrit, `lou.js` (Lou assistante, panier commenté, vol au panier, sons WebAudio, gravure
  généralisée vue bande/carré + polices), `lou-produit.js` (aperçus photo, mini-aperçu, barre d'achat, livraison estimée),
  `lou-anim.js` (GSAP 3.12.5 + ScrollTrigger, copiés de Corps-Confiant), réglages du thème (`settings_schema.json`),
  snippets `lou-assistante`, `entete-page` ; accueil réorganisé (Lou, atelier 3 finitions, coups de cœur, problème →
  solution, test, machine à manette, étapes à glisser, « C'est moi, Lou », compte à rebours Noël, FAQ conversation).
- Textes : page « Qui est Lou » et mentions légales → « avatar de la boutique » ; délais 3-7 j + 7-12 j ouvrés dans
  livraison-retours, CGV et politique de livraison (vérifié avant : identiques au dépôt, rien d'écrasé).
- Tests banc (iPhone 13 + ordinateur) : 15 pages OK, aucune erreur JS, pas de débordement ; parcours testé (texte, finition,
  police, photo, validation, ajout au panier, tiroir, assistante, FAQ, menu). Thème envoyé : 64 fichiers, 0 erreur.
- Captures : `docs/captures/v2-*`.

## 2026-11-02 (nuit, suite) — Collier prénom : la chaîne s'adapte à la longueur du prénom
- Demande utilisateur (capture iPhone) : dans l'aperçu, la chaîne doit toucher les deux bords du prénom, s'ouvrir pour un
  prénom long et se resserrer pour un prénom court — sans rien changer d'autre (taille des lettres comprise).
- `assets_theme.py` : le bas des deux brins (sous y ≈ 630, anneaux compris) est effacé des 3 photos `collier-vierge*.webp`
  (velours recopié 30 px à côté + correction de lumière). Brins mesurés : gauche (640, 367) → (860, 501), droite
  (640, 872) → (860, 740), identiques dans les 3 finitions.
- `lou-produit.js` : les brins sont redessinés maillon par maillon (même éclat que la vraie chaîne) depuis la chaîne de la
  photo jusqu'à un anneau posé sur le premier et le dernier pixel du prénom ; plus de limite de largeur (garde-fou à
  560 px seulement), formule de taille des lettres inchangée. Testé : je, Lou, Emma, Chloé, Marguerite, Léa ; 3 finitions,
  2 polices ; aucune erreur. Envoyé sur le thème en ligne. Capture : `docs/captures/collier-chaine-adaptee.jpg`.

## 2026-11-03 — Retours de l'utilisateur sur la fiche (téléphone)
- Écriture « Manuscrite » : **Allura** remplace Great Vibes partout (jonc, collier, atelier, boutons) — le A majuscule de
  Great Vibes ressemblait à un « a » bizarre (comparaison de 12 écritures manuscrites).
- **Première lettre toujours en majuscule** (jonc, collier prénom, atelier de l'accueil ; le Morse reste tout en majuscules),
  sans déplacer le curseur.
- Liste à coches (bénéfices) retirée du haut de la fiche → rubrique **« Caractéristiques »** (ouverte) dans les accordéons du bas.
- Case « J'ai vérifié l'orthographe » **cochée d'office** (décision utilisateur). ⚖️ Conseil donné : pré-cochée, elle prouve
  moins que la cliente a relu en cas de litige ; le récapitulatif « Vous avez écrit » reste affiché.
- Livraison : **5 à 10 jours ouvrés** (réglages du thème, page livraison-retours, CGV, politique de livraison) ; fabrication
  3 à 7 j inchangée. Estimation le 03/11 : reçu entre le 13 et le 24/11. Noël : avec 7 j + 10 j ouvrés, commande au plus
  tard le 3/12 pour le 24/12 sans marge → date affichée gardée au **1er décembre** (2 jours de marge pour les retards de fin
  d'année ; modifiable dans les réglages du thème).
- En-tête : icône **« Mon compte »** (profil) entre la loupe et le panier + lien dans le menu mobile.
- `construire_boutique.py politiques` : ne touche plus une politique modifiée dans Shopify depuis la dernière sauvegarde.
- Testé au banc (iPhone 13) : « anaïs » → « Anaïs », aucune erreur ; envoyé sur le thème en ligne.

## 2026-11-03 (suite) — Accueil : Lou porte ses bijoux ; vignettes animées ; délai total 5-10 jours
- Demande : sur téléphone, comprendre tout de suite que c'est une boutique de bijoux en voyant Lou. Nouvelle image
  `contenu/images-ia/2026-11-03-lou-hero-bijoux-hd.jpg` (retouche de lou-hero-hd avec les photos produit en référence) : Lou
  porte le jonc « Tu es ma personne » au poignet et le collier « Emma ». Recadrage téléphone 5:4 serré (x 1000→2601,
  y 230→1511), ordinateur 4:5. Repères animés (point qui pulse + étiquette « mon collier prénom », « mon jonc gravé »,
  liens vers les fiches) ; pastille « 💍 Bijoux gravés » ; bulle de Lou : « Vous voyez mon jonc et mon collier ? ».
- Vignettes produits animées (toutes les grilles) : la phrase se grave lettre par lettre sur le jonc vierge, le prénom
  s'écrit sur le collier (la chaîne suit), la photo change dans la bulle du collier photo (couple, mamie et petite-fille,
  chiot : `souvenir-*.webp`, images IA d'exemple), le mot s'écrit en Morse. Seulement à l'écran, rien si « animations
  réduites ». Le dessin du collier prénom est passé dans `lou.js` (`LOU.dessinerPrenom`), partagé avec la fiche.
- Fiche : le petit texte « L'aperçu est une simulation… » est masqué sur téléphone (déplacé dans « Caractéristiques ») ;
  l'étiquette de l'aperçu dit « Aperçu en direct · simulation ».
- Délai (décision utilisateur) : **5 à 10 jours au total entre la commande et la livraison, fabrication comprise**, en jours
  calendaires (commande le 03/11 → reçu entre le 8 et le 13 novembre, comme demandé). Réglages fab_min/fab_max supprimés ;
  textes mis à jour (fiche, FAQ, étapes, Lou, livraison-retours, CGV, politique de livraison).
  ⚖️ Conseil donné : délai très court pour du sur-mesure AliExpress (souvent 2-4 semaines) ; dépassement = la cliente
  peut annuler (L216-2) → à confirmer avec le fournisseur choisi.

## 2026-11-03 (suite 2) — Atelier de l'accueil : on efface l'exemple pour écrire ses mots
- Demande utilisateur : quand on touche le champ de l'atelier, le message d'exemple (démo qui s'écrit toute seule) s'efface
  pour écrire son propre mot. Jonc vierge tant que le champ est vide ; si on quitte le champ vide, l'exemple revient sur le
  jonc ; un texte écrit par la cliente n'est jamais effacé en retouchant le champ. Indication du champ : « Vos mots ici… ».

## 2026-11-03 (suite 3) — Accueil → écriture du jonc ; boutons côte à côte
- « Graver ✨ » et « Je crée mon bijou » mènent tous les deux à la fiche du jonc, directement à l'écriture (`#personnaliser` :
  défilement jusqu'au bloc de personnalisation + mini-aperçu affiché), avec la finition choisie dans l'atelier et la phrase
  **seulement si la cliente l'a écrite** (jamais le texte de la démo). Lou dit « Voilà vos mots 💗 ».
- Téléphone : « Je crée mon bijou » et « Lou, aide-moi ✨ » côte à côte (testé 360, 390, 430 px, sans débordement).

## 2026-11-03 (suite 4) — Cartes « Fini les cadeaux sans âme » : plus lentes, soulignées
- Retournement automatique ralenti : rien pendant 3,5 s (le temps de lire), puis une seule carte à la fois dans l'ordre
  2e → 3e → 4e → 1re, côté solution affiché 4 s, 1,8 s entre deux cartes ; retournement plus doux (1,1 s). Une carte
  touchée par la cliente n'est plus retournée toute seule.
- Le problème n'est plus barré mais **souligné en rose framboise** (lisible).

## 2026-11-03 (suite 5) — Machine à mots sous les bijoux et sur les fiches ; Noël au 10 décembre
- Machine à mots devenue un composant (`snippets/machine-mots.liquid`, JS multi-machines dans `lou.js`).
  Accueil : juste sous les bijoux (fonds réalternés : problème → solution en blanc, test en bande).
  Fiches qui proposent une phrase ou un mot : **jonc** (phrases ≤ 20 caractères) et **bracelet code secret** (mots en
  majuscules ≤ 8 lettres, banque `MOTS`), juste sous « Caractéristiques » ; « Je prends cette phrase / ce mot » remplit le
  champ, remonte à l'aperçu et Lou confirme. Pas de machine sur le collier prénom ni le collier photo.
- Phrases raccourcies à 20 caractères max. (« La best, c'est toi », « Duo de choc », « Toi, ma préférée », « Plus forte que tout »).
- **Noël : commandez avant le 10 décembre** (décision utilisateur ; délai max 10 j → livré au plus tard le 20/12) : réglages du
  thème (en ligne vérifiés identiques avant l'envoi), bandeau, compte à rebours, fiche, FAQ, Lou, page livraison-retours,
  politique de livraison.

## 2026-11-03 (suite 6) — Fiche : aperçu animé ; conseil de Lou compact sous le champ
- Grand aperçu de la fiche animé comme les vignettes tant que la cliente n'a rien écrit : phrase gravée lettre par lettre avec
  étincelle (jonc), prénoms qui s'écrivent (collier), photos d'exemple dans la bulle (collier photo), mots en Morse (bracelet).
  S'arrête dès qu'elle touche le champ / choisit sa photo ; reprend si elle quitte le champ vide. Rien si « animations
  réduites » ou si elle arrive avec un texte (accueil, machine à mots). Étincelle aussi quand elle tape.
- Grande bulle « Mon conseil » de Lou retirée du haut de la fiche ; à la place, petit message d'une ligne (mini photo de Lou)
  qui apparaît sous le champ dès qu'elle écrit (ou sous l'envoi de photo) : « Lou : 10 à 20 caractères, c'est parfait 💗 »…
- Message d'accueil de Lou adapté au collier photo (plus de « Besoin d'une idée de phrase ? »).

## 2026-11-03 (suite 7) — Carte « Ma machine à mots » : lien vers la machine
- Au dos de la carte « Ma machine à mots » (section problème → solution) : pastille « Je l'essaie ↑ » ; toucher la carte
  retournée fait remonter à la machine à mots (accueil) et tire la manette automatiquement.

## 2026-11-03 (suite 8) — « Mes coups de cœur » enfin visibles
- L'utilisatrice ne trouvait pas ses coups de cœur (enregistrés dans le navigateur, sans page pour les voir). Ajouts :
  icône ♡ dans l'en-tête (remplie + compteur quand il y en a), panneau latéral « Mes coups de cœur » (photo, prix,
  « Personnaliser », « Retirer », Lou qui rappelle l'offre -50 %), lien « 💗 Mes coups de cœur » dans le menu mobile et dans
  l'assistante Lou, cœur aussi sur la galerie des fiches produits, petit cœur qui s'envole vers l'en-tête.
  Catalogue pour le panneau : `snippets/coups-de-coeur.liquid` (JSON des produits). En-tête : 4 icônes, testé 360-430 px.
- Les coups de cœur restent propres à chaque navigateur (pas liés au compte client). Capture : `docs/captures/coups-de-coeur.jpg`.

## 2026-11-03 (suite 9) — Accueil : zoom animé sur les bijoux ; site allégé
- Repères : plus de point posé sur les bijoux (ils les cachaient) → fine flèche blanche qui part de l'étiquette et s'arrête
  juste avant le bijou. Zoom animé (×2,1 téléphone, ×1,8 ordinateur) : collier « Emma » (3,2 s), retour, jonc gravé
  (3,2 s), retour… ; l'autre étiquette se cache pendant le zoom ; uniquement quand la photo est à l'écran ; rien si
  « animations réduites ». Le zoom s'applique au <picture> (la parallaxe GSAP reste sur l'<img>).
- Allègement (mesure banc, iPhone, premier écran, sans compression) : accueil 1 180 → 669 Ko, fiche jonc 966 → 676 Ko.
  Images du thème redimensionnées au juste besoin (×3 d'un écran de téléphone) et recompressées (`assets_theme.py`) ;
  avatar de Lou 31 → 6 Ko ; images des vignettes animées chargées seulement quand la vignette arrive à l'écran ;
  polices de gravure « Classique » / « Moderne » chargées seulement sur les fiches ; l'image de l'atelier n'est plus
  prioritaire sur la photo de Lou. Sur Shopify, JS/CSS/HTML sont en plus compressés (≈ -70 %).

## 2026-11-03 (suite 10) — Bracelet code secret : aperçu Morse compréhensible
- Idée utilisateur : le code au-dessus de chaque lettre plutôt que tout sur une ligne. Nouveau décodeur sous le bracelet :
  une colonne par lettre, son code dessiné avec les mêmes perles (rond = point, long = trait) au-dessus, la lettre en
  dessous ; « 1 groupe de perles = 1 lettre » ; légende point / trait en perles. Animation : chaque groupe de perles
  s'allume en rose sur le bracelet en même temps que sa colonne (0,85 s par lettre, pause en fin de mot).
  Capture : `docs/captures/morse-decodeur.jpg`.

## 2026-11-03 (suite 11) — Bracelet : animation lettre par lettre complète, plus de « point / trait » ; collier photo sans case orthographe
- Démo de la fiche bracelet synchronisée : le mot s'écrit, puis chaque lettre s'allume de la première à la dernière (cadre +
  groupe de perles), puis seulement le mot suivant (temps d'arrêt = 0,85 s × (lettres + 1) + 1,2 s).
- « = point / = trait » jugé incompréhensible (utilisateur) → remplacé par « Chaque lettre a son code secret en perles 🤫 » ;
  aide du champ et caractéristique reformulées (« perles rondes et longues », « mot secret traduit en perles »).
- Collier photo : case « J'ai vérifié l'orthographe » retirée (aucun texte). Bulle de Lou du bracelet : « idée de mot secret ».

## 2026-11-03 (suite 12) — Cartes « Fini les cadeaux sans âme » : on comprend qu'on peut les toucher
- Toucher la carte « Ma machine à mots » ne fait plus que la retourner ; seul le bouton « Je l'essaie ↑ » (carte retournée)
  remonte à la machine et tire la manette.
- Pastille « 👆 Touchez-moi » qui pulse sur chaque carte, flèche ↻ au dos, légère rotation au survol (ordinateur),
  consigne « Touchez une carte pour la retourner : je vous montre ma solution 👇 » ; guillemets insécables.

## 2026-11-03 (suite 13) — Conseil : comment rendre Lou vraiment réaliste
- Question utilisateur (quel logiciel pour un avatar qui paraît vraiment réel). Recherche web + options notées dans
  `docs/avatar-lou.md` (Higgsfield Soul ID, OpenArt, ou fal.ai avec LoRA Flux fait par Claude). En attente du choix.

## 2026-11-03 (suite 14) — Option fal.ai choisie : création de la clé
- L'utilisateur crée sa clé fal.ai (préréglage « API » validé). Marche à suivre pour l'ajouter à l'environnement notée dans
  `docs/avatar-lou.md`. Prochaine étape (nouvelle session) : vérifier la clé, entraîner le LoRA de Lou sur 20 images validées.
- Clé ajoutée en 3 « Network secrets » (un par site). Test de la clé à faire dans une nouvelle session.

## 2026-11-03 (suite 15) — Test de la clé fal.ai
- 1er test (session précédente, non poussé : dépôt en lecture seule) : `fal.run` OK ; `queue.fal.run` bloqué (faute de frappe
  « queve.fal.run » dans le secret) ; `rest.fal.ai` 401 ; `fal.media` / `v3.fal.media` non autorisés.
- L'utilisateur a changé la config : variable `FAL_KEY` seule, 3 Network secrets fal supprimés, domaines `fal.run`, `*.fal.run`,
  `rest.fal.ai`, `*.fal.ai`, `fal.media`, `*.fal.media` autorisés.
- 2e test (gratuit, clé non affichée) : ✅ `fal.run` (422), ✅ `queue.fal.run` (404 fausse requête), ✅ `rest.fal.ai` (200),
  ✅ `v3.fal.media` / `v3b.fal.media` ; fausse clé → 401 partout (aucun secret réseau ne remplace l'en-tête) ; `fal.media` seul
  n'a pas d'adresse DNS (sans importance). Détail dans `docs/avatar-lou.md`.
- L'utilisateur indique qu'il ne pense pas garder Lou : **tout travail sur l'avatar est suspendu** jusqu'à discussion.

## 2026-11-03 (suite 16) — Nouvelle Lou
- L'utilisateur ne veut plus de l'ancien physique : brune 20-22 ans, très mignonne, ultra-réaliste, « Shot on iPhone 18 Pro. »
  dans chaque prompt. 3 propositions générées (≈ 1 $ OpenAI) → `contenu/lou/propositions-v2/`. Choix en attente.
- Choix : visage **B** avec **cheveux longs bouclés** → 2 retouches `B2-boucles-1/2.png` (≈ 0,60 $). Variante finale en attente.
- Revirement : l'utilisateur préfère **B avec le chignon** (définitive). Règle notée : **toujours ultra-réaliste, toujours
  « Shot on iPhone 18 Pro. »**. Planche de 6 plans `contenu/lou/reference-v2/` (≈ 2 $ OpenAI).
