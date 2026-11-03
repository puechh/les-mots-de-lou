"""Recopie l'état actuel de la boutique Shopify dans le dépôt (la « mémoire »).

Usage : python3 scripts/sauvegarde.py

- theme/                   fichiers du thème publié (remplacés à chaque sauvegarde)
- produits/catalogue.json  produits, variantes, prix, images, statuts
- contenu/collections.json, contenu/pages.json, contenu/menus.json, contenu/politiques.json

Aucune donnée client ni commande n'est exportée.
"""

import base64
import json
import shutil
import urllib.request
from pathlib import Path

from shopify import graphql

ROOT = Path(__file__).resolve().parent.parent


def paginate(query, path, variables=None):
    """Parcourt une connexion GraphQL paginée ; path = clés menant à la connexion."""
    after, nodes = None, []
    while True:
        data = graphql(query, {**(variables or {}), "after": after})
        for key in path:
            data = data[key]
        nodes += data["nodes"]
        if not data["pageInfo"]["hasNextPage"]:
            return nodes
        after = data["pageInfo"]["endCursor"]


def write_json(relative, data):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


THEME_FILES = """
query($id: ID!, $after: String) {
  theme(id: $id) {
    files(first: 50, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes {
        filename
        body {
          ... on OnlineStoreThemeFileBodyText { content }
          ... on OnlineStoreThemeFileBodyBase64 { contentBase64 }
          ... on OnlineStoreThemeFileBodyUrl { url }
        }
      }
    }
  }
}
"""


def save_theme():
    theme = graphql('{ themes(first: 1, roles: [MAIN]) { nodes { id name } } }')["themes"]["nodes"][0]
    files = paginate(THEME_FILES, ["theme", "files"], {"id": theme["id"]})
    target = ROOT / "theme"
    shutil.rmtree(target, ignore_errors=True)
    for f in files:
        path = target / f["filename"]
        path.parent.mkdir(parents=True, exist_ok=True)
        body = f["body"]
        if "content" in body:
            path.write_text(body["content"])
        elif "contentBase64" in body:
            path.write_bytes(base64.b64decode(body["contentBase64"]))
        else:
            with urllib.request.urlopen(body["url"], timeout=60) as resp:
                path.write_bytes(resp.read())
    return f"thème « {theme['name']} » ({len(files)} fichiers)"


PRODUCTS = """
query($after: String) {
  products(first: 20, after: $after, sortKey: TITLE) {
    pageInfo { hasNextPage endCursor }
    nodes {
      handle title status vendor productType tags templateSuffix descriptionHtml
      seo { title description }
      options { name values }
      collections(first: 20) { nodes { handle } }
      media(first: 50) { nodes { ... on MediaImage { image { url altText } } } }
      variants(first: 100) {
        nodes {
          title sku price compareAtPrice taxable inventoryPolicy
          selectedOptions { name value }
          image { url }
          inventoryItem { tracked requiresShipping unitCost { amount } }
        }
      }
    }
  }
}
"""


def save_products():
    products = paginate(PRODUCTS, ["products"])
    for p in products:
        p["collections"] = [c["handle"] for c in p["collections"]["nodes"]]
        p["images"] = [m["image"] for m in p.pop("media")["nodes"] if m]
        p["variants"] = p["variants"]["nodes"]
    write_json("produits/catalogue.json", products)
    return f"{len(products)} produits"


def save_content():
    collections = paginate("""query($after: String) { collections(first: 50, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes { handle title descriptionHtml templateSuffix ruleSet { appliedDisjunctively rules { column relation condition } }
                productsCount { count } } } }""", ["collections"])
    pages = paginate("""query($after: String) { pages(first: 50, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes { handle title body isPublished templateSuffix } } }""", ["pages"])
    menus = paginate("""query($after: String) { menus(first: 50, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes { handle title items { title type url items { title type url } } } } }""", ["menus"])
    policies = graphql("{ shop { shopPolicies { type title body } } }")["shop"]["shopPolicies"]
    # Dépôt PUBLIC : les politiques qui contiennent l'identité de l'éditeur (nom, adresse) ne sont pas recopiées.
    # Leur modèle (avec {{EDITEUR}} / {{ADRESSE}}) est dans contenu/politiques/ ; envoi : scripts/publier_politiques.py
    modeles = {"LEGAL_NOTICE": "legal-notice", "CONTACT_INFORMATION": "contact-information"}
    for p in policies:
        if p["type"] in modeles:
            p["body"] = f"(non sauvegardé : contient l'identité de l'éditeur — modèle dans contenu/politiques/{modeles[p['type']]}.html)"
    write_json("contenu/collections.json", collections)
    write_json("contenu/pages.json", pages)
    write_json("contenu/menus.json", menus)
    write_json("contenu/politiques.json", policies)
    return f"{len(collections)} collections, {len(pages)} pages, {len(menus)} menus, {len(policies)} politiques"


def main():
    for step in (save_theme, save_products, save_content):
        print("Sauvegardé :", step())


if __name__ == "__main__":
    main()
