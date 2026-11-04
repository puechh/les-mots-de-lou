"""Titres et méta-descriptions Google des fiches et collections (04/11/2026, demande utilisateur : référencement).

Règles : mot-clé que les gens tapent en premier (« jonc gravé personnalisé »…), titre ≤ 60 caractères, description
≈ 140-160 caractères, rien de non vérifié (pas « acier » pour les perles du Morse), aucune mention IA (décision 04/11).
L'accueil et la page d'attente ont leur titre / description dans theme-lou/layout/*.liquid.
    python3 scripts/seo.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUITS = {
    "jonc-mes-mots": ("Jonc gravé personnalisé, votre message | Les Mots de Lou",
                      "Jonc gravé avec votre phrase, en acier inoxydable argenté, doré ou rosé. Aperçu de la gravure en direct. L'idée cadeau pour Noël, livraison suivie."),
    "collier-prenom": ("Collier prénom personnalisé | Les Mots de Lou",
                       "Collier prénom personnalisé en écriture manuscrite, acier inoxydable argenté, doré ou rosé. Aperçu en direct, l'idée cadeau pour Noël. Livraison suivie."),
    "collier-souvenir-photo": ("Collier photo personnalisé, cœur à projection | Les Mots de Lou",
                               "Collier photo personnalisé : votre photo cachée dans la lentille d'un pendentif cœur. Un cadeau souvenir pour maman, mamie ou votre amour. Livraison suivie."),
    "bracelet-code-secret": ("Bracelet code Morse personnalisé | Les Mots de Lou",
                             "Bracelet code Morse personnalisé : votre mot secret en perles argentées sur cordon noir réglable. Cadeau meilleure amie, sœur ou couple. Livraison suivie."),
}
COLLECTIONS = {
    "joncs": ("Joncs gravés personnalisés | Les Mots de Lou",
              "Joncs gravés avec vos mots : phrase, date ou prénom, en acier inoxydable argenté, doré ou rosé. Aperçu en direct, livraison suivie France et Belgique."),
    "colliers": ("Colliers personnalisés : prénom et photo | Les Mots de Lou",
                 "Colliers personnalisés : prénom en écriture manuscrite ou photo cachée dans un cœur. Aperçu en direct, l'idée cadeau pour Noël. Livraison suivie."),
    "bracelets": ("Bracelets personnalisés code Morse | Les Mots de Lou",
                  "Bracelets personnalisés : un mot secret en code Morse, perles argentées sur cordon réglable. L'idée cadeau amitié ou couple. Livraison suivie."),
}


def gql(q, v=None):
    r = graphql(q, v)
    return r.get("data", r)


for h, (t, d) in PRODUITS.items():
    assert len(t) <= 65 and len(d) <= 160, (h, len(t), len(d))
    pid = gql("query($q: String!) { products(first: 1, query: $q) { nodes { id } } }", {"q": f"handle:{h}"})["products"]["nodes"][0]["id"]
    r = gql("mutation($p: ProductUpdateInput!) { productUpdate(product: $p) { userErrors { message } } }", {"p": {"id": pid, "seo": {"title": t, "description": d}}})
    print("produit", h, len(t), len(d), r["productUpdate"]["userErrors"] or "OK")
for h, (t, d) in COLLECTIONS.items():
    assert len(t) <= 65 and len(d) <= 160, (h, len(t), len(d))
    n = gql("query($q: String!) { collections(first: 1, query: $q) { nodes { id } } }", {"q": f"handle:{h}"})["collections"]["nodes"]
    if not n:
        print("collection absente :", h); continue
    r = gql("mutation($c: CollectionInput!) { collectionUpdate(input: $c) { userErrors { message } } }", {"c": {"id": n[0]["id"], "seo": {"title": t, "description": d}}})
    print("collection", h, len(t), len(d), r["collectionUpdate"]["userErrors"] or "OK")

# même texte dans produits/produits.json (source du dépôt) pour qu'un nouvel envoi ne l'écrase pas
f = os.path.join(ROOT, "produits/produits.json")
dj = json.load(open(f))
for p in dj["produits"]:
    p["seo_titre"], p["seo"] = PRODUITS[p["handle"]]
open(f, "w").write(json.dumps(dj, ensure_ascii=False, indent=2) + "\n")
