#!/usr/bin/env bash
# Images pour les aperçus en direct (02/11/2026) : collier prénom sans pendentif (3 finitions) + portrait de Lou HD.
cd "$(dirname "$0")/.."
python3 - <<'PY'
from PIL import Image
Image.open('contenu/images-ia/2026-11-02-produit-collier-prenom-1-hd.jpg').save('/tmp/collier-src.png')
Image.open('contenu/lou/reference/04-sourire.png').save('/tmp/lou-src.png')
PY
V="Retouche minimale : retire entièrement le pendentif prénom « Emma » du collier. La chaîne reste exactement identique (même position, même finesse, même couleur argentée) ; ses deux extrémités s'arrêtent là où commençait et finissait le prénom, en laissant un espace vide entre elles, sans aucun pendentif. Ne change rien d'autre : même buste en velours rose, même fleurs, même cadrage, même lumière."
python3 scripts/images_ia.py modifier "$V" /tmp/collier-src.png --nom collier-prenom-vierge-hd --format carre-hd --qualite high > /tmp/v1.log 2>&1 && echo "OK vierge" || { echo ÉCHEC vierge; cat /tmp/v1.log; } &
python3 scripts/images_ia.py modifier "Reproduis cette photo à l'identique en haute définition : même personne (même visage, mêmes traits, mêmes taches de rousseur, même coiffure, même sourire), même tenue, même décor, même lumière, même cadrage. Améliore uniquement la netteté et les détails fins. Ne change, n'ajoute et ne retire rien." /tmp/lou-src.png --nom lou-portrait-hd --format portrait-hd --qualite high > /tmp/v2.log 2>&1 && echo "OK portrait" || { echo ÉCHEC portrait; cat /tmp/v2.log; } &
wait
F="Retouche minimale : change uniquement la couleur du métal de la chaîne en %s. Ne change rien d'autre : exactement la même chaîne, au même endroit, avec les deux extrémités au même endroit et l'espace vide entre elles, même buste, mêmes fleurs, même cadrage, même lumière."
f=$(ls contenu/images-ia/*collier-prenom-vierge-hd.png | tail -1)
python3 scripts/images_ia.py modifier "$(printf "$F" "doré (finition dorée jaune or)")" "$f" --nom collier-prenom-vierge-doree-hd --format carre-hd --qualite high > /tmp/v3.log 2>&1 && echo "OK doree" || { echo ÉCHEC doree; cat /tmp/v3.log; } &
python3 scripts/images_ia.py modifier "$(printf "$F" "rosé (finition or rose, rose cuivré doux)")" "$f" --nom collier-prenom-vierge-rosee-hd --format carre-hd --qualite high > /tmp/v4.log 2>&1 && echo "OK rosee" || { echo ÉCHEC rosee; cat /tmp/v4.log; } &
wait
echo FINI
