"""Passe une image carrée (ou paysage) en format VERTICAL 3:4 en prolongeant le décor en haut et en bas (outpainting fal.ai
Bria Expand) — décision utilisateur 15/11/2026 : « toutes les images du site doivent être en format vertical ».
Les pixels d'origine sont gardés tels quels (le bijou n'est jamais redessiné) : seul le décor autour est ajouté.

    python3 scripts/fal_vertical.py source.jpg sortie.jpg [--haut 0.4]

--haut : part de l'ajout placée au-dessus (0.5 = centré ; 0.3 = plus d'ajout en bas).
Clé : FAL_KEY (variable d'environnement). Jamais dans le dépôt.
"""
import argparse
import io
import sys
import time
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fal_images import entetes, envoyer_fichier  # noqa: E402

MODELE = "fal-ai/bria/expand"


def appeler(corps):
    r = requests.post(f"https://queue.fal.run/{MODELE}", headers=entetes(), json=corps, timeout=60)
    r.raise_for_status()
    d = r.json()
    for _ in range(200):
        s = requests.get(d["status_url"], headers=entetes(), timeout=60).json()
        if s.get("status") == "COMPLETED":
            break
        time.sleep(3)
    else:
        sys.exit("fal : délai dépassé")
    return requests.get(d["response_url"], headers=entetes(), timeout=60).json()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("sortie")
    p.add_argument("--haut", type=float, default=0.5)
    p.add_argument("--max", type=int, default=2048, help="largeur envoyée (Bria limite la taille)")
    a = p.parse_args()
    im = Image.open(a.source).convert("RGB")
    if im.width > a.max:
        im = im.resize((a.max, round(im.height * a.max / im.width)), Image.LANCZOS)
    w, h = im.size
    H = round(w * 4 / 3)
    if H <= h:
        sys.exit("Déjà vertical (3:4 ou plus haut).")
    tmp = Path(a.sortie).with_suffix(".src.jpg")
    im.save(tmp, quality=95)
    y = round((H - h) * a.haut)
    res = appeler({"image_url": envoyer_fichier(tmp), "canvas_size": [w, H], "original_image_size": [w, h],
                   "original_image_location": [0, y], "num_images": 1, "sync_mode": False})
    tmp.unlink()
    url = res["image"]["url"] if "image" in res else res["images"][0]["url"]
    out = Image.open(io.BytesIO(requests.get(url, timeout=120).content)).convert("RGB")
    if out.size != (w, H):
        out = out.resize((w, H), Image.LANCZOS)
    out.paste(im, (0, y))   # pixels d'origine remis à l'identique (bijou intact)
    out.save(a.sortie, quality=93)
    print(a.sortie, out.size, "original en y =", y)


if __name__ == "__main__":
    main()
