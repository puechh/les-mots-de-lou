"""Caractéristiques courtes sur les fiches (demande utilisateur 04/11 : l'essentiel, pas de pavés).

Met à jour produits/produits.json ET le champ méta lou.contenu de chaque produit sur Shopify (seulement « benefices »,
le reste du contenu est gardé tel quel).    python3 scripts/benefices_courts.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURTS = {
    "jonc-mes-mots": ["Jusqu'à 20 caractères", "Acier inoxydable, ne noircit pas", "Fin et ouvert, s'adapte au poignet", "Aperçu en direct"],
    "collier-prenom": ["Jusqu'à 10 lettres", "Acier inoxydable, ne noircit pas", "Chaîne 40 + 5 cm", "Aperçu en direct"],
    "collier-souvenir-photo": ["Votre photo cachée dans la lentille", "Visible en regardant vers la lumière", "Cœur en métal plaqué, chaîne en acier", "Photo nette conseillée"],
    "bracelet-code-secret": ["Jusqu'à 8 lettres en Morse", "Perles argentées, cordon noir", "Cordon réglable", "Clé du code sur la fiche"],
}


def gql(q, v=None):
    r = graphql(q, v)
    return r.get("data", r)


f = os.path.join(ROOT, "produits/produits.json")
d = json.load(open(f))
for p in d["produits"]:
    p["benefices"] = COURTS[p["handle"]]
open(f, "w").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

for h, ben in COURTS.items():
    n = gql('query($q: String!) { products(first: 1, query: $q) { nodes { id metafield(namespace: "lou", key: "contenu") { value } } } }',
            {"q": f"handle:{h}"})["products"]["nodes"][0]
    contenu = json.loads(n["metafield"]["value"])
    contenu["benefices"] = ben
    r = gql("mutation($m: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $m) { userErrors { field message } } }",
            {"m": [{"ownerId": n["id"], "namespace": "lou", "key": "contenu", "type": "json", "value": json.dumps(contenu, ensure_ascii=False)}]})
    print(h, r["metafieldsSet"]["userErrors"] or "OK")
