"""Images IA via fal.ai (Nano Banana Pro, Flux 2 Pro, Seedream…) — rangées avec leur prompt.

Clé : variable d'environnement FAL_KEY (la clé seule ; envoyée en « Authorization: Key … »). Jamais dans le dépôt.

  python3 scripts/fal_images.py fal-ai/nano-banana-pro/edit "prompt" --ref contenu/lou/reference-v3/00-source-lou.webp \
      --nom 01-face --dossier contenu/lou/reference-v3 --param resolution=4K --param aspect_ratio=3:4

--param cle=valeur : paramètres propres au modèle (valeur JSON si possible, sinon texte).
Les images de référence sont envoyées sur le stockage fal (rest.fal.ai) puis passées en image_urls.
"""

import argparse
import json
import mimetypes
import os
import sys
import time
from pathlib import Path

import requests

RACINE = Path(__file__).resolve().parent.parent


def entetes():
    cle = os.environ.get("FAL_KEY")
    if not cle:
        sys.exit("FAL_KEY absente de l'environnement.")
    return {"Authorization": f"Key {cle}"}


def envoyer_fichier(chemin):
    chemin = Path(chemin)
    type_ = mimetypes.guess_type(chemin.name)[0] or "application/octet-stream"
    r = requests.post("https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3", headers=entetes(),
                      json={"content_type": type_, "file_name": chemin.name}, timeout=60)
    r.raise_for_status()
    d = r.json()
    requests.put(d["upload_url"], data=chemin.read_bytes(), headers={"Content-Type": type_}, timeout=300).raise_for_status()
    return d["file_url"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("modele")
    p.add_argument("prompt")
    p.add_argument("--ref", action="append", default=[], help="image de référence (plusieurs possibles)")
    p.add_argument("--nom", required=True)
    p.add_argument("--dossier", default="contenu/images-ia")
    p.add_argument("--param", action="append", default=[])
    a = p.parse_args()

    corps = {"prompt": a.prompt}
    if a.ref:
        corps["image_urls"] = [envoyer_fichier(x) for x in a.ref]
    for kv in a.param:
        k, v = kv.split("=", 1)
        try:
            corps[k] = json.loads(v)
        except json.JSONDecodeError:
            corps[k] = v

    t = time.time()
    for essai in range(3):
        r = requests.post(f"https://fal.run/{a.modele}", headers=entetes(), json=corps, timeout=900)
        if r.status_code in (502, 503, 504) and essai < 2:
            print(f"  Erreur {r.status_code}, nouvel essai dans 10 s…")
            time.sleep(10)
            continue
        break
    if not r.ok:
        sys.exit(f"Erreur fal ({r.status_code}) : {r.text[:500]}")
    d = r.json()
    images = d.get("images") or ([d["image"]] if d.get("image") else [])
    if not images:
        sys.exit(f"Pas d'image dans la réponse : {json.dumps(d)[:500]}")
    sortie = RACINE / a.dossier
    sortie.mkdir(parents=True, exist_ok=True)
    for i, im in enumerate(images):
        url = im["url"]
        ext = Path(url.split("?")[0]).suffix or ".png"
        chemin = sortie / (a.nom + (f"-{i + 1}" if len(images) > 1 else "") + ext)
        chemin.write_bytes(requests.get(url, timeout=300).content)
        print(f"  OK en {time.time() - t:.0f} s → {chemin} ({im.get('width')}x{im.get('height')})")
    note = f"Modèle : fal {a.modele}\nParamètres : {json.dumps({k: v for k, v in corps.items() if k not in ('prompt', 'image_urls')}, ensure_ascii=False)}\n"
    note += f"Prompt : {a.prompt}\n"
    if a.ref:
        note += "Images de référence : " + ", ".join(a.ref) + "\n"
    (sortie / f"{a.nom}.txt").write_text(note, encoding="utf-8")


if __name__ == "__main__":
    main()
