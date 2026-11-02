#!/usr/bin/env bash
# Refait en haute définition (2048 px) les images IA de la boutique, à l'identique (02/11/2026).
# Usage : bash scripts/images_hd.sh   (≈ 0,2-0,3 $ par image ; résultats dans contenu/images-ia/*-hd.png)
cd "$(dirname "$0")/.."
P="Reproduis cette photo à l'identique en haute définition : même cadrage, mêmes objets, même bijou (forme, largeur, couleur, reflets, texte gravé identique lettre pour lettre), même décor, même lumière. Améliore uniquement la netteté et les détails fins (texture du métal, du tissu, de la peau). Ne change, n'ajoute et ne retire rien."
PL="Reproduis cette photo à l'identique en haute définition : même personne (même visage, mêmes traits, mêmes taches de rousseur, même coiffure, même expression), même tenue, même bijou, même décor, même lumière, même cadrage. Améliore uniquement la netteté et les détails fins. Ne change, n'ajoute et ne retire rien."
hd() { python3 scripts/images_ia.py modifier "$1" "contenu/images-ia/2026-11-02-$2.png" --nom "$2-hd" --format "$3" --qualite high > "/tmp/hd-$2.log" 2>&1 && echo "OK $2" || { echo "ÉCHEC $2"; cat "/tmp/hd-$2.log"; }; }
hd "$P" produit-jonc-vierge carre-hd &
hd "$P" produit-jonc-1 carre-hd &
hd "$P" produit-jonc-finitions carre-hd &
hd "$P" produit-collier-prenom-1 carre-hd &
wait
hd "$P" produit-collier-prenom-finitions carre-hd &
hd "$P" produit-collier-photo-1 carre-hd &
hd "$P" produit-bracelet-morse-1 carre-hd &
hd "$P" coffret-cadeau carre-hd &
wait
hd "$PL" lou-jonc portrait-hd &
hd "$PL" lou-collier-prenom portrait-hd &
hd "$PL" lou-hero paysage-hd &
wait
# Finitions du jonc vierge (même photo, seule la couleur du métal change) : pour l'aperçu de gravure
F="Retouche minimale : change uniquement la couleur du métal du jonc en %s. Ne change rien d'autre : exactement la même forme, la même position, la même largeur, les mêmes reflets et ombres, la même face avant lisse et vierge sans aucune gravure, le même cadrage, la même boîte rose, le même tissu, la même lumière."
python3 scripts/images_ia.py modifier "$(printf "$F" "acier doré (finition dorée jaune or, chaude et brillante)")" contenu/images-ia/2026-11-02-produit-jonc-vierge-hd.png --nom produit-jonc-vierge-doree-hd --format carre-hd --qualite high > /tmp/hd-doree.log 2>&1 && echo "OK doree" || { echo "ÉCHEC doree"; cat /tmp/hd-doree.log; } &
python3 scripts/images_ia.py modifier "$(printf "$F" "acier rosé (finition or rose, rose cuivré doux et brillant)")" contenu/images-ia/2026-11-02-produit-jonc-vierge-hd.png --nom produit-jonc-vierge-rosee-hd --format carre-hd --qualite high > /tmp/hd-rosee.log 2>&1 && echo "OK rosee" || { echo "ÉCHEC rosee"; cat /tmp/hd-rosee.log; } &
wait
echo FINI
