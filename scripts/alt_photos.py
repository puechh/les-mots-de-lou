"""Retire « (Image virtuelle) » / mentions IA des textes alternatifs des photos produits (décision utilisateur 04/11 :
la mention n'apparaît que sur la page « Qui est Lou »).    python3 scripts/alt_photos.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql  # noqa: E402


def gql(q, v=None):
    r = graphql(q, v)
    return r.get("data", r)


prods = gql("{ products(first: 20) { nodes { id handle media(first: 50) { nodes { id alt } } } } }")["products"]["nodes"]
for p in prods:
    maj = []
    for m in p["media"]["nodes"]:
        alt = m.get("alt") or ""
        nouv = re.sub(r"\s*\((Image virtuelle|image virtuelle)\)", "", alt).replace("l'avatar virtuel", "l'avatar")
        if nouv != alt:
            maj.append({"id": m["id"], "alt": nouv})
    if maj:
        r = gql("mutation($p: ID!, $m: [UpdateMediaInput!]!) { productUpdateMedia(productId: $p, media: $m) { mediaUserErrors { message } } }",
                {"p": p["id"], "m": maj})
        print(p["handle"], len(maj), "texte(s) modifié(s)", r["productUpdateMedia"]["mediaUserErrors"] or "OK")
    else:
        print(p["handle"], "rien à modifier")
