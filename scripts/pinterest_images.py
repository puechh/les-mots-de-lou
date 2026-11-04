"""Images verticales (2:3, format conseillé par Pinterest) pour les épingles, hébergées sur Shopify (Contenu → Fichiers).

Recadre les photos 3:4 de Lou avec les bijoux (contenu/lou/bijoux-v3) en 2:3, 1600×2400, les envoie dans les Fichiers
Shopify et écrit leurs adresses publiques dans contenu/pinterest/images.json.    python3 scripts/pinterest_images.py
"""
import json
import os
import sys
import time

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql, upload_file  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(ROOT, "contenu/pinterest")
# nom de l'épingle → (source, position verticale du recadrage 0 = haut … 1 = bas, texte alternatif)
SOURCES = {
    "pin-marche-noel": ("contenu/lou/bijoux-v3/02-marche-noel.jpg", .35, "Jonc gravé et collier prénom portés au marché de Noël"),
    "pin-collier-photo-feu": ("contenu/lou/bijoux-v3/05-collier-photo-feu.jpg", .3, "Collier photo cœur devant la cheminée de Noël"),
    "pin-cafe-paris": ("contenu/lou/bijoux-v3/07-cafe-paris.jpg", .4, "Jonc gravé et collier prénom en terrasse à Paris"),
    "pin-rue-paris": ("contenu/lou/bijoux-v3/08-rue-paris.jpg", .35, "Collier prénom et jonc gravé dans une rue de Paris"),
}


def gql(q, v=None):
    r = graphql(q, v)
    return r.get("data", r)


os.makedirs(SORTIE, exist_ok=True)
res = {}
for nom, (src, haut, alt) in SOURCES.items():
    im = Image.open(os.path.join(ROOT, src)).convert("RGB")
    w, h = im.size
    nh = round(w * 3 / 2)
    if nh > h:                                   # image trop large : on coupe les côtés
        nw = round(h * 2 / 3); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        y = round((h - nh) * haut); im = im.crop((0, y, w, y + nh))
    chemin = os.path.join(SORTIE, nom + ".jpg")
    im.resize((1600, 2400), Image.LANCZOS).save(chemin, quality=90, optimize=True)
    url = upload_file(chemin, "image/jpeg", "FILE")
    f = gql("mutation($f: [FileCreateInput!]!) { fileCreate(files: $f) { files { id } userErrors { message } } }",
            {"f": [{"originalSource": url, "contentType": "IMAGE", "alt": alt}]})["fileCreate"]
    if f["userErrors"]:
        sys.exit(f"{nom} : {f['userErrors']}")
    fid = f["files"][0]["id"]
    for _ in range(30):                          # Shopify prépare l'image : on attend son adresse publique
        n = gql("query($id: ID!) { node(id: $id) { ... on MediaImage { fileStatus image { url } } } }", {"id": fid})["node"]
        if n and n.get("image"):
            break
        time.sleep(2)
    res[nom] = {"url": n["image"]["url"], "alt": alt}
    print(nom, "→", n["image"]["url"][:80])
json.dump(res, open(os.path.join(SORTIE, "images.json"), "w"), ensure_ascii=False, indent=2)
