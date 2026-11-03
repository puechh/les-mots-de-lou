"""Remplace les photos des fiches produits (et seulement les photos) — 03/11/2026.

Ordre de chaque fiche : photo produit seule → détails / finitions → photos portées (gros plan, puis Lou).
Images carrées 2048 px dans contenu/lou/fiches-v3/shopify/ (ou contenu/images-ia/ pour les photos produit gardées).
Les anciennes photos ne sont retirées que si toutes les nouvelles ont bien été ajoutées.

    python3 scripts/photos_fiches.py [--essai]
"""
import glob
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql, upload_file  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "Image virtuelle"
FICHES = {
    "jonc-mes-mots": [
        ("jonc-01-produit", "Jonc « Mes Mots » argenté gravé « Tu es ma personne », extrémités à petits cœurs ajourés"),
        ("jonc-02-coeurs", "Détail des deux petits cœurs ajourés aux extrémités du jonc"),
        ("jonc-03-finitions", "Le jonc en trois finitions : argentée, dorée et rosée"),
        ("jonc-04-poignet", f"Jonc gravé porté au poignet, gravure et cœur visibles ({V})"),
        ("jonc-05-lou", f"Lou, l'avatar de la boutique, porte le jonc gravé ({V})"),
        ("jonc-06-cafe", f"Lou porte le jonc et le collier prénom en terrasse à Paris ({V})"),
    ],
    "collier-prenom": [
        ("produit-collier-prenom-1-hd", "Collier prénom argenté en écriture manuscrite"),
        ("produit-collier-prenom-finitions-hd", "Le collier prénom en trois finitions : argentée, dorée et rosée"),
        ("prenom-03-cou", f"Collier prénom « Lou » porté, gros plan ({V})"),
        ("prenom-04-lou", f"Lou, l'avatar de la boutique, porte son collier prénom ({V})"),
        ("prenom-05-marche-noel", f"Lou au marché de Noël avec son collier prénom ({V})"),
    ],
    "collier-souvenir-photo": [
        ("produit-collier-photo-1-hd", "Collier Souvenir cœur argenté avec photo cachée dans la petite lentille"),
        ("photo-02-cou", f"Collier Souvenir porté, gros plan ({V})"),
        ("photo-03-lou-feu", f"Lou regarde la photo cachée dans la lentille du collier ({V})"),
    ],
    "bracelet-code-secret": [
        ("produit-bracelet-morse-1-hd", "Bracelet Code Secret : perles et barrettes en code Morse sur cordon noir"),
        ("morse-02-macro", "Gros plan des perles (points) et barrettes (traits) du code Morse"),
        ("morse-03-carte", f"Bracelet Code Secret porté en écrivant une carte de Noël ({V})"),
        ("morse-04-lou", f"Lou porte le bracelet Code Secret ({V})"),
    ],
}


def fichier(nom):
    f = glob.glob(os.path.join(ROOT, "contenu/lou/fiches-v3/shopify", nom + ".jpg"))
    f = f or sorted(glob.glob(os.path.join(ROOT, "contenu/images-ia", f"*{nom}.jpg")))
    if not f:
        sys.exit(f"Image introuvable : {nom}")
    return f[-1]


def gql(q, v=None):
    r = graphql(q, v)
    return r.get("data", r)


def main():
    essai = "--essai" in sys.argv
    for handle, images in FICHES.items():
        p = gql("query($q: String!) { products(first: 1, query: $q) { nodes { id media(first: 50) { nodes { id } } } } }",
                {"q": f"handle:{handle}"})["products"]["nodes"][0]
        anciens = [m["id"] for m in p["media"]["nodes"]]
        fichiers = [(fichier(n), alt) for n, alt in images]
        print(f"{handle} : {len(anciens)} photo(s) actuelle(s) → {len(fichiers)} nouvelle(s)")
        if essai:
            for f, alt in fichiers:
                print("   ", os.path.relpath(f, ROOT), "|", alt)
            continue
        medias = [{"originalSource": upload_file(f, "image/jpeg", "IMAGE"), "mediaContentType": "IMAGE", "alt": alt} for f, alt in fichiers]
        r = gql("mutation($id: ID!, $m: [CreateMediaInput!]!) { productCreateMedia(productId: $id, media: $m) { media { id } mediaUserErrors { message } } }",
                {"id": p["id"], "m": medias})["productCreateMedia"]
        if r["mediaUserErrors"] or len(r["media"]) != len(medias):
            print("  ❌ ajout incomplet, anciennes photos gardées :", r["mediaUserErrors"])
            continue
        if anciens:
            gql("mutation($ids: [ID!]!) { fileDelete(fileIds: $ids) { deletedFileIds userErrors { message } } }", {"ids": anciens})
        print(f"  ✅ {len(medias)} photo(s) en place, {len(anciens)} ancienne(s) retirée(s)")
        time.sleep(1)


if __name__ == "__main__":
    main()
