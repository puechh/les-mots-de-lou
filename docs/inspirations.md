# Inspirations (reprises du projet Corps-Confiant, adaptées à Les Mots de Lou)

Sites donnés par l'utilisateur pour Corps-Confiant (analyse complète : dépôt `puechh/boutique-corps-confiant`,
`docs/inspirations.md`). ⚠️ Les sites eux-mêmes ne s'ouvrent pas depuis l'environnement cloud tant que leurs domaines
(`lilytreasures.fr`, `ciaokombucha.com`, `dentica.fr`) ne sont pas ajoutés aux domaines autorisés de l'environnement
« Les Mots de Lou ».

## Lily's Treasures — https://lilytreasures.fr/ (modèle principal pour Lou, demande utilisateur 02/11/2026)
- La mascotte **incarne la boutique** : section « C'est moi, Lily », ton personnel et chaleureux, elle parle à la cliente.
- Univers « carnet / scrapbooking » rose : washi tape sur les cartes, papier ligné, écriture manuscrite, cœurs.
- Cartes produits **légèrement inclinées** qui se redressent au survol, cœur favori, badge, bouton direct.
- **Calendrier interactif** qui s'ouvre tout seul, avis présentés comme une **conversation de messagerie**, FAQ en cartes,
  bandeau défilant.
- Repris pour Lou : Lou parle partout (bulles, assistante, FAQ en conversation avec elle, panier commenté par elle, menu
  mobile, page d'attente), cartes inclinées + washi tape + cœurs qui éclatent, compte à rebours de Noël (pas de calendrier
  tant qu'il n'y a pas de vraies offres quotidiennes).

## Ciao Kombucha — https://www.ciaokombucha.com/ (effet « waouh », très animé)
- GSAP + ScrollTrigger, entrées au défilement, objets qui bougent. Repris : titre révélé ligne par ligne, cartes qui
  tombent en place, ruban qui se balance, parallaxe de la photo de Lou (`theme-lou/assets/lou-anim.js`).

## Dentica — https://dentica.fr/ (marketing, ordre des sections)
- Problème → solution, bénéfices cochés, « recevez-le avant le JJ/MM », FAQ, réassurance, produits complémentaires.
- Repris : cartes « Fini les cadeaux sans âme » qui se retournent (problème → solution), 4 bénéfices cochés sur la fiche,
  **livraison estimée** (date calculée), offre 2e bijou à -50 % avec jauge dans le panier, réassurance.
- ⚖️ Jamais de faux avis ni de chiffres inventés : pas de section avis tant qu'il n'y a pas de vrais avis.
