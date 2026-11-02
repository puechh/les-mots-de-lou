"""Création d'images avec l'API d'OpenAI (le service derrière ChatGPT).

Clé : soit un « Network secret » de l'environnement cloud (en-tête Authorization ajouté
automatiquement pour api.openai.com, la clé n'est jamais visible), soit la variable OPENAI_API_KEY.
Jamais dans le dépôt, jamais affichée.
Les images créées sont rangées dans contenu/images-ia/ avec un fichier .txt qui garde le prompt.

  python3 scripts/images_ia.py check
  python3 scripts/images_ia.py creer "bannière beige douce, ..." --nom banniere-duo --format paysage
  python3 scripts/images_ia.py modifier "même photo, fond crème uni" photo.webp [autre.webp ...] --nom panty-fond-creme

Rappel : ne pas modifier l'apparence d'un produit (forme, dentelle, couleur) sur une photo de vente,
et ne jamais fabriquer de fausses photos de clientes ni de faux avant / après.
"""

import argparse
import base64
import mimetypes
import os
import sys
from datetime import date
from pathlib import Path

import requests

API = "https://api.openai.com/v1"
MODELE = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
SORTIE = Path(__file__).resolve().parent.parent / "contenu" / "images-ia"
FORMATS = {"carre": "1024x1024", "portrait": "1024x1536", "paysage": "1536x1024"}


def _entetes():
    # Sans variable, on compte sur le secret réseau qui ajoute lui-même l'en-tête Authorization
    cle = os.environ.get("OPENAI_API_KEY")
    return {"Authorization": f"Bearer {cle}"} if cle else {}


def _verifier(resp):
    if resp.ok:
        return resp.json()
    try:
        message = resp.json()["error"]["message"]
    except Exception:
        message = resp.text[:300]
    if resp.status_code == 401:
        message += " (clé absente ou invalide : ajouter le secret pour api.openai.com, puis ouvrir une nouvelle session)"
    sys.exit(f"Erreur OpenAI ({resp.status_code}) : {message}")


def _enregistrer(data, nom, prompt, sources=()):
    SORTIE.mkdir(parents=True, exist_ok=True)
    chemins = []
    for i, image in enumerate(data["data"]):
        suffixe = f"-{i + 1}" if len(data["data"]) > 1 else ""
        chemin = SORTIE / f"{date.today()}-{nom}{suffixe}.png"
        chemin.write_bytes(base64.b64decode(image["b64_json"]))
        chemins.append(chemin)
    note = f"Modèle : {MODELE}\nPrompt : {prompt}\n"
    if sources:
        note += "Images de base : " + ", ".join(str(s) for s in sources) + "\n"
    (SORTIE / f"{date.today()}-{nom}.txt").write_text(note)
    for c in chemins:
        print(c)


def check():
    data = _verifier(requests.get(f"{API}/models", headers=_entetes(), timeout=30))
    modeles = sorted(m["id"] for m in data["data"] if "image" in m["id"] or m["id"].startswith("dall-e"))
    print("Connexion OK. Modèles d'image disponibles :", ", ".join(modeles) or "aucun")


def creer(prompt, nom, taille, qualite, nombre):
    payload = {"model": MODELE, "prompt": prompt, "size": taille, "quality": qualite, "n": nombre}
    data = _verifier(requests.post(f"{API}/images/generations", headers=_entetes(), json=payload, timeout=300))
    _enregistrer(data, nom, prompt)


def modifier(prompt, images, nom, taille, qualite, nombre):
    fichiers = [
        ("image[]", (Path(p).name, open(p, "rb"), mimetypes.guess_type(p)[0] or "image/png")) for p in images
    ]
    champs = {"model": MODELE, "prompt": prompt, "size": taille, "quality": qualite, "n": str(nombre)}
    data = _verifier(
        requests.post(f"{API}/images/edits", headers=_entetes(), data=champs, files=fichiers, timeout=300)
    )
    _enregistrer(data, nom, prompt, images)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sous = parser.add_subparsers(dest="action", required=True)
    sous.add_parser("check", help="teste la clé et liste les modèles d'image")
    for action in ("creer", "modifier"):
        p = sous.add_parser(action)
        p.add_argument("prompt")
        if action == "modifier":
            p.add_argument("images", nargs="+", help="images de base (photos de la boutique)")
        p.add_argument("--nom", required=True, help="nom du fichier créé, sans extension")
        p.add_argument("--format", choices=FORMATS, default="carre")
        p.add_argument("--qualite", choices=["low", "medium", "high"], default="medium")
        p.add_argument("--nombre", type=int, default=1)
    args = parser.parse_args()
    if args.action == "check":
        check()
    elif args.action == "creer":
        creer(args.prompt, args.nom, FORMATS[args.format], args.qualite, args.nombre)
    else:
        modifier(args.prompt, args.images, args.nom, FORMATS[args.format], args.qualite, args.nombre)


if __name__ == "__main__":
    main()
