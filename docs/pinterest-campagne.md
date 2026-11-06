# Campagne Pinterest de Noël : plan pour le crédit de 420 € (préparé le 05/11/2026)
> ⚠️ 06/11 : « Image virtuelle » retirée des épingles et des pubs à la demande de l'utilisateur (conseil légal donné, voir journal).

*À valider par l'utilisateur. Chiffres à ajuster après la 1re semaine. Ce n'est pas un avis d'avocat (voir `pinterest-regles.md`).*

## 0. Avant de dépenser 1 € (bloquants, voir `avant-annonces.md`)
1. Boutique **ouverte** (mot de passe retiré), DSers relié, **1 vraie commande test** payée puis remboursée.
2. Médiateur de la consommation + SIREN dans les mentions légales.
3. Pinterest : compte pro, **compte publicitaire** + moyen de paiement, **crédit 420 € activé** → lire ses conditions (date limite,
   dépense minimale à faire soi-même, campagnes éligibles). ⚠️ Le crédit a souvent une **date d'expiration** : la noter ici.
4. Catalogue Pinterest **approuvé** (4 produits « actifs »), balise + **API de conversion** actives (appli Pinterest de Shopify).

## 1. Les visuels (prêts)
`contenu/pinterest/pubs-2026-11/final/` : 2000×3000 (2:3), photos Nano Banana Pro 4K (« Shot on iPhone 18 Pro by an amateur
photographer », prompts dans les .txt), textes ajoutés par `scripts/pinterest_pubs.py`. Bijoux vérifiés à 100 % : jonc fin à cœurs,
collier prénom fin, collier photo à 1 seul pendentif.

| Visuel | Lou ? | Lien (page d'arrivée) | Titre de l'épingle (≤ 100 car.) |
|---|---|---|---|
| pub-1-jonc-lou | oui → « Image virtuelle » | fiche Jonc | Jonc gravé avec vos mots – idée cadeau Noël |
| pub-2-prenom-lou | oui → « Image virtuelle » | fiche Collier prénom | Collier prénom personnalisé – cadeau de Noël |
| pub-3-photo-lou | oui → « Image virtuelle » | fiche Collier photo | Collier photo personnalisé : un souvenir dans un cœur |
| pub-4-duo-cadeau | non | page d'accueil (offre duo) | 2e bijou à -50 % sur le moins cher des deux |
| pub-5-jonc-macro | non | fiche Jonc | Bracelet jonc gravé : voyez votre gravure en direct |

Description type (à adapter) : « Gravez une phrase, un prénom ou un souvenir sur un bijou en acier inoxydable. Aperçu en direct sur
le site, fabriqué pour vous en 5 à 10 jours. 2e bijou à -50 % sur le moins cher des deux. Commandez avant le 10 décembre pour Noël. »
+ « Image virtuelle » à la fin pour pub-1/2/3. Liens avec `?utm_source=pinterest&utm_medium=paid&utm_campaign=noel2026&utm_content=pub-1`.
En publiant : cocher la déclaration « contenu modifié/généré par l'IA » si Pinterest la propose.

## 2. Répartition des 420 € (≈ 10/11 → 10/12, 30 jours)
| Campagne | Objectif Pinterest | Budget | Contenu |
|---|---|---|---|
| A. **Catalogue / Shopping** | Ventes (conversions catalogue) | **6 €/jour ≈ 180 €** | les 4 produits du catalogue, ciblage automatique |
| B. **Épingles « Noël »** | Conversions (achat) ; si < 5 achats en 7 jours → « ajout au panier » | **7 €/jour ≈ 210 €** | pub-1 à pub-5 dans un seul groupe |
| Réserve | — | **30 €** | renforcer la meilleure pub fin novembre (Black Friday 27/11 → Cyber Monday 30/11) |

Ciblage campagne B : **femmes 25-55 ans, France + Belgique, français** ; centres d'intérêt : bijoux, idées cadeaux, Noël, mode
femme ; mots-clés : « bracelet gravé », « jonc personnalisé », « collier prénom », « collier photo », « bijou personnalisé »,
« cadeau maman noël », « cadeau meilleure amie », « cadeau sœur », « cadeau couple ». Ciblage élargi (« expansion ») : activé.
Dès ≈ 100 visiteurs : ajouter une audience **« visiteurs du site sans achat »** (reciblage, petite part du budget).

## 3. Calendrier et règles de décision
- **Semaine 1** (test) : tout tourne, on ne touche à rien pendant 4-5 jours (l'algorithme apprend).
- **Semaine 2** : couper les 2 visuels les plus faibles (taux de clic < 0,3 % ou coût par clic > 1 €) ; garder 3 visuels.
- **27/11 → 30/11** : Black Friday : ajouter la réserve sur la meilleure pub. ⚖️ Pas de faux « -X % Black Friday » : seule l'offre
  réelle « 2e à -50 % » (ou une vraie baisse calculée sur le prix le plus bas des 30 jours, art. L112-1-1).
- **10/12 au soir** : retirer tout message « pour Noël » / « avant le 10 décembre » (délai 5 à 10 jours) ; passer aux visuels
  « toute l'année » ou couper.

## 4. Rentabilité (ordres de grandeur à confirmer dans DSers)
- 1 bijou à 29,90 € : achat ≈ 8-10 € livré + douane ≈ 3 € + paiement ≈ 1 € → **≈ 15 € de marge pour payer la pub**.
- Panier duo (29,90 + 14,95 = 44,85 €) : ≈ 20 € de marge → l'offre duo est la plus rentable : la mettre en avant.
- Repère : **coût par achat ≤ 15 €** = OK ; 15-25 € = à améliorer (visuels, fiche) ; > 25 € = couper / revoir.
- Le crédit offert n'est pas de l'argent perdu, mais juger les pubs comme si on le payait (pour savoir quoi garder après).

## 5. Rappels légaux (pubs)
- Offre **toujours avec sa condition** (« sur le moins cher des deux »), valable pour toutes, retirée à la fin de l'offre.
- « Image virtuelle » quand Lou apparaît (AI Act art. 50, loi n° 2023-451) ; aucune fausse cliente, aucun faux avis.
- Pas de « livré avant Noël garanti », pas d'« or » (finitions colorées), pas de « 316L / sans nickel » avant confirmation écrite.
- Règles Pinterest du **12/11/2026** (produits déformés par l'IA interdits) : relire le texte officiel ce jour-là ; comparer les
  visuels aux vraies photos fournisseur DSers avant de lancer.
