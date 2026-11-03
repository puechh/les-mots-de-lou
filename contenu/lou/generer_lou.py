"""Génère ou retouche des images de Lou (API OpenAI) et les range dans contenu/lou/<dossier>/ avec leur prompt.

Différence avec scripts/images_ia.py : sortie dans contenu/lou/, délai d'attente long (10 min), nouvel essai
automatique en cas d'erreur 502/503/504 (délai du proxy), paramètre input_fidelity pour garder le visage.

  python3 contenu/lou/generer_lou.py modifier "prompt" contenu/lou/reference-visage.png --nom face --dossier reference
  python3 contenu/lou/generer_lou.py creer "prompt" --nom essai --modele gpt-image-2.5-flare

Clé : Network secret de l'environnement cloud (api.openai.com) ou OPENAI_API_KEY. Jamais dans le dépôt.
"""

import argparse
import base64
import mimetypes
import os
import sys
import time
from pathlib import Path

import requests

API = "https://api.openai.com/v1"
ICI = Path(__file__).resolve().parent
FORMATS = {"carre": "1024x1024", "portrait": "1024x1536", "paysage": "1536x1024", "portrait-hd": "2048x3072"}


def _entetes():
    cle = os.environ.get("OPENAI_API_KEY")
    return {"Authorization": f"Bearer {cle}"} if cle else {}


def _envoyer(url, **kw):
    for essai in range(3):
        t = time.time()
        resp = requests.post(url, headers=_entetes(), timeout=600, **kw)
        if resp.ok:
            print(f"  OK en {time.time() - t:.0f} s")
            return resp.json()
        if resp.status_code in (502, 503, 504) and essai < 2:
            print(f"  Erreur {resp.status_code}, nouvel essai dans 10 s…")
            time.sleep(10)
            continue
        try:
            message = resp.json()["error"]["message"]
        except Exception:
            message = resp.text[:300]
        sys.exit(f"Erreur OpenAI ({resp.status_code}) : {message}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("action", choices=["creer", "modifier"])
    p.add_argument("prompt")
    p.add_argument("images", nargs="*", help="images de référence (pour modifier)")
    p.add_argument("--nom", required=True)
    p.add_argument("--dossier", default="essais")
    p.add_argument("--modele", default="gpt-image-2")
    p.add_argument("--format", choices=FORMATS, default="portrait")
    p.add_argument("--qualite", choices=["low", "medium", "high"], default="medium")
    p.add_argument("--fidelite", choices=["low", "high", "aucune"], default="high")
    a = p.parse_args()

    champs = {"model": a.modele, "prompt": a.prompt, "size": FORMATS[a.format], "quality": a.qualite, "n": 1}
    if a.action == "creer":
        data = _envoyer(f"{API}/images/generations", json=champs)
    else:
        if a.fidelite != "aucune":
            champs["input_fidelity"] = a.fidelite
        fichiers = [("image[]", (Path(x).name, open(x, "rb"), mimetypes.guess_type(x)[0] or "image/png")) for x in a.images]
        data = _envoyer(f"{API}/images/edits", data={k: str(v) for k, v in champs.items()}, files=fichiers)

    sortie = ICI / a.dossier
    sortie.mkdir(parents=True, exist_ok=True)
    chemin = sortie / f"{a.nom}.png"
    chemin.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    note = f"Modèle : {a.modele} (qualité {a.qualite}"
    note += f", input_fidelity {a.fidelite})\n" if a.action == "modifier" else ")\n"
    note += f"Prompt : {a.prompt}\n"
    if a.images:
        note += "Images de référence : " + ", ".join(a.images) + "\n"
    (sortie / f"{a.nom}.txt").write_text(note)
    print(chemin)


if __name__ == "__main__":
    main()
