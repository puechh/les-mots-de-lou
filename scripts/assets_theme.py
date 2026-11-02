#!/usr/bin/env python3
"""Prépare les images du thème (theme-lou/assets/*.webp, favicon) à partir de contenu/lou et contenu/images-ia.

    python3 scripts/assets_theme.py
"""
import glob, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "theme-lou", "assets")


def trouver(*noms):
    for n in noms:
        f = sorted(glob.glob(os.path.join(ROOT, "contenu", "**", f"*{n}*.png"), recursive=True))
        if f:
            return f[-1]
    return os.path.join(ROOT, "contenu/lou/reference-visage.png")


def recadrer(src, ratio, largeur, dest, haut=0.0):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / ratio); y = int((h - nh) * haut); im = im.crop((0, y, w, y + nh))
    im = im.resize((largeur, int(largeur / ratio)), Image.LANCZOS)
    im.save(os.path.join(A, dest), "WEBP", quality=82)
    print(dest, "←", os.path.relpath(src, ROOT))


recadrer(trouver("lou-hero"), 4 / 5, 900, "lou-hero.webp", 0.5)
recadrer(trouver("reference/04-sourire", "reference-visage"), 4 / 5, 700, "lou-portrait.webp", 0.1)
recadrer(trouver("reference/01-face", "lou-avatar", "reference-visage"), 1, 240, "lou-avatar.webp", 0.12)

# Favicon : cœur blanc sur rond framboise
fv = Image.new("RGBA", (128, 128), (0, 0, 0, 0)); d = ImageDraw.Draw(fv)
d.ellipse((0, 0, 127, 127), fill=(226, 69, 122))
try:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 78)
except OSError:
    f = ImageFont.load_default()
d.text((64, 62), "L", font=f, fill="white", anchor="mm")
fv.save(os.path.join(A, "favicon.png"))
print("favicon.png")

# Atelier de l'accueil : photo du jonc vierge, recadrée autour du jonc (le texte est posé dessus en SVG, cf. lou.js).
# Recadrage x 90→1010, y 360→820 de l'image 1024×1024 : si on change l'image, ajuster la courbe JONC_COURBE de lou.js.
_src = trouver("produit-jonc-vierge")
Image.open(_src).convert("RGB").crop((90, 360, 1010, 820)).save(os.path.join(A, "jonc-vierge.webp"), "WEBP", quality=86)
print("jonc-vierge.webp ←", os.path.relpath(_src, ROOT))
