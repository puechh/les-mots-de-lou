"""Détoure une image (fond transparent) avec fal.ai BiRefNet v2 — 03/11/2026.

    python3 scripts/fal_detourer.py entree.png sortie.png
"""
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fal_images import entetes, envoyer_fichier  # noqa: E402

src, dest = sys.argv[1], sys.argv[2]
corps = {"image_url": envoyer_fichier(src), "model": "General Use (Heavy)", "operating_resolution": "2048x2048",
         "output_format": "png", "refine_foreground": True}
r = requests.post("https://fal.run/fal-ai/birefnet/v2", headers=entetes(), json=corps, timeout=600)
if not r.ok:
    sys.exit(f"Erreur fal ({r.status_code}) : {r.text[:400]}")
url = r.json()["image"]["url"]
open(dest, "wb").write(requests.get(url, timeout=300).content)
print("OK →", dest)
