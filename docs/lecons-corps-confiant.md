# Leçons tirées de Corps-Confiant (octobre-novembre 2026) — à appliquer ici dès le départ

Source : dépôt `puechh/boutique-corps-confiant` (voir son `docs/journal.md` pour le détail).

## Shopify
- Le **mot de passe de la boutique** reste en place jusqu'à l'accord explicite de l'utilisateur.
- **Livraison** : les tarifs par marché se règlent dans **Paramètres → Marchés** (invisibles pour l'app « Claude api ») ; après
  chaque réglage, vérifier les frais réels à la caisse (France, Belgique). Corps-Confiant a eu 7,99 / 4,99 au lieu des tarifs voulus.
- **Caisse** : décocher la case d'inscription marketing présélectionnée (⚖️ consentement non valable) ; décocher « Exiger une
  étape de confirmation » (une étape de moins).
- **Cookies** : utiliser la bannière Shopify (Paramètres → Confidentialité) et ne pas en ajouter une seconde dans le thème ;
  page « Cookies et partenaires » à jour à chaque appli/balise ; ne pas modifier la politique de confidentialité automatique.
- Format des prix « 29,90 € ». Médiateur de la consommation obligatoire avant de vendre.
- Tester une commande réelle (puis rembourser) : débloque aussi l'objectif « Ventes » de Pinterest.
- Depuis le cloud (IP américaine) : tester la caisse avec les cookies `localization=FR` et `cart_currency=EUR`.

## Thème
- Thème sur mesure dans un dossier source, envoyé par `scripts/envoyer_theme.py`, sauvegardé par `scripts/sauvegarde.py`.
- Tester chaque changement avec Playwright (ordinateur 1300×900 et iPhone 13) et montrer une capture avant de publier.
- Ne pas mettre `scroll-behavior: smooth` si on utilise GSAP ScrollTrigger ; sur mobile, ne pas bloquer le défilement du hero.
- Le banc de test local de Corps-Confiant (`scripts/banc_theme.py`, python-liquid) peut être adapté.

## Klaviyo
- Offre gratuite : **250 profils actifs / 500 envois par mois** ; au-delà, offre E-mail payante (≈ 20 $/mois).
- Tout créer en **brouillon** ; c'est l'utilisateur qui active. Les flux utilisent des **copies** des modèles (modifier la copie).
- Domaine d'envoi dédié (`send.<domaine>`, enregistrements NS chez IONOS) + adresse `contact@<domaine>` avant le 1er envoi.
- Désactiver le flux Shopify « paiement abandonné » natif quand celui de Klaviyo est actif (doublon).

## Pubs
- Pinterest : balise à associer au compte pub (Shopify → appli Pinterest) ; objectif « Ventes » bloqué tant qu'il n'y a pas d'achat.
- Meta : vérifier le pixel dans le Gestionnaire d'événements ; page pro + compte pub au nom de la boutique.
- Google Merchant Center : limiter aux pays vendus, renseigner livraison et retours, revendiquer le site.

## E-mail VIP de Corps-Confiant (01/11/2026)
- 229 délivrés, ~19 % d'ouverture, **0 clic** avec -10 % seul : une offre doit être forte et le bouton visible tout de suite.
