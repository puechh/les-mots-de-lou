"""Envoie les politiques de contenu/politiques/*.html sur Shopify, en remplissant l'identité de l'éditeur.

Le dépôt est PUBLIC : le nom et l'adresse de l'éditeur n'y sont jamais écrits. Ils sont remplacés par {{EDITEUR}} et
{{ADRESSE}} dans les modèles, et remplis au moment de l'envoi, depuis (au choix) :
  - les variables d'environnement LOU_EDITEUR et LOU_ADRESSE ;
  - ou les politiques de Corps-Confiant (même éditeur, décision utilisateur 03/11/2026) :
      python3 scripts/publier_politiques.py --depuis /home/user/boutique-corps-confiant/contenu/politiques.json

  python3 scripts/publier_politiques.py [--depuis FICHIER] [--essai]   (--essai : affiche sans envoyer)
"""

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shopify import graphql  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
TYPES = {"legal-notice": "LEGAL_NOTICE", "contact-information": "CONTACT_INFORMATION", "terms-of-service": "TERMS_OF_SERVICE",
         "refund-policy": "REFUND_POLICY", "shipping-policy": "SHIPPING_POLICY"}


def identite():
    editeur, adresse = os.environ.get("LOU_EDITEUR"), os.environ.get("LOU_ADRESSE")
    if "--depuis" in sys.argv:
        pols = {p["type"]: re.sub(r"<[^>]+>", "\n", p["body"]) for p in json.load(open(sys.argv[sys.argv.index("--depuis") + 1]))}
        editeur = editeur or re.search(r"Responsable de la publication\s*:\s*([^\n]+)", pols["LEGAL_NOTICE"]).group(1).strip()
        adresse = adresse or re.search(r"Adresse physique\s*:\s*([^\n]+)", pols["CONTACT_INFORMATION"]).group(1).strip()
    if not (editeur and adresse):
        sys.exit("Identité de l'éditeur introuvable (LOU_EDITEUR / LOU_ADRESSE ou --depuis).")
    return editeur, adresse


def main():
    editeur, adresse = identite()
    for nom, t in TYPES.items():
        corps = (RACINE / "contenu/politiques" / f"{nom}.html").read_text(encoding="utf-8")
        corps = corps.replace("{{EDITEUR}}", editeur).replace("{{ADRESSE}}", adresse)
        if "{{" in corps or "À COMPLÉTER" in corps:
            sys.exit(f"Marqueur restant dans {nom} : envoi annulé.")
        if "--essai" in sys.argv:
            print(f"[essai] {nom} : {len(corps)} caractères")
            continue
        r = graphql("mutation($p: ShopPolicyInput!) { shopPolicyUpdate(shopPolicy: $p) { userErrors { field message } } }",
                    {"p": {"type": t, "body": corps}})
        r = r.get("data", r)
        print(nom, ":", r["shopPolicyUpdate"]["userErrors"] or "OK")


if __name__ == "__main__":
    main()
