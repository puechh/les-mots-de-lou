#!/usr/bin/env python3
"""Prépare les images du thème (theme-lou/assets/*.webp, favicon) à partir de contenu/lou et contenu/images-ia.

    python3 scripts/assets_theme.py

Les images sont enregistrées assez grandes pour rester nettes sur un écran de téléphone (×3) :
une photo affichée sur toute la largeur d'un iPhone (390 points) a besoin d'environ 1 170 pixels.
Priorité aux versions HD (« -hd », 2048 px) quand elles existent.
"""
import glob, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "theme-lou", "assets")


def trouver(*noms):
    """Premier fichier trouvé (png ou jpg) pour l'un des noms, dans contenu/."""
    for n in noms:
        f = sorted(glob.glob(os.path.join(ROOT, "contenu", "**", f"*{n}.png"), recursive=True) +
                   glob.glob(os.path.join(ROOT, "contenu", "**", f"*{n}.jpg"), recursive=True))
        if f:
            return f[-1]
    return os.path.join(ROOT, "contenu/lou/reference-visage.png")


def enregistrer(im, dest, largeur, qualite=82):
    if im.width > largeur:
        im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    im.save(os.path.join(A, dest), "WEBP", quality=qualite, method=6)
    print(f"{dest:28s} {im.size}  {os.path.getsize(os.path.join(A, dest)) // 1024} Ko")


def recadrer(src, ratio, largeur, dest, haut=0.0, gauche=0.5, qualite=82):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = int((w - nw) * gauche); im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / ratio); y = int((h - nh) * haut); im = im.crop((0, y, w, y + nh))
    enregistrer(im, dest, largeur, qualite)


# Lou (accueil) : grande photo ordinateur (4:5) et bandeau téléphone (16:11), recadré sur Lou
recadrer(trouver("lou-hero-hd", "lou-hero"), 4 / 5, 1200, "lou-hero.webp", 0.5, 0.68)
recadrer(trouver("lou-hero-hd", "lou-hero"), 16 / 11, 1200, "lou-hero-mobile.webp", 0.18, 0.5)
recadrer(trouver("lou-portrait-hd", "reference/04-sourire", "reference-visage"), 4 / 5, 1000, "lou-portrait.webp", 0.1)
recadrer(trouver("lou-portrait-hd", "reference/01-face", "lou-avatar", "reference-visage"), 1, 400, "lou-avatar.webp", 0.12)

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

# Atelier de gravure (accueil + fiche du jonc) : photo du jonc vierge dans les 3 finitions, recadrée autour du jonc.
# Recadrage x 90→1010, y 360→820 du repère 1024×1024 (×2 sur les images HD 2048). Les bords de la face avant
# (tables JONC de lou.js, repère 920×460) restent valables tant que ce recadrage et la photo ne changent pas.
for nom, dest in [("produit-jonc-vierge-hd", "jonc-vierge.webp"), ("produit-jonc-vierge-doree-hd", "jonc-vierge-doree.webp"),
                  ("produit-jonc-vierge-rosee-hd", "jonc-vierge-rosee.webp")]:
    src = trouver(nom)
    im = Image.open(src).convert("RGB"); k = im.width / 1024
    enregistrer(im.crop((round(90 * k), round(360 * k), round(1010 * k), round(820 * k))), dest, 1380, 86)

# Fiche du jonc : même photo en carré (x 90→1010, y 104→1024 du repère 1024)
for nom, dest in [("produit-jonc-vierge-hd", "jonc-carre.webp"), ("produit-jonc-vierge-doree-hd", "jonc-carre-doree.webp"),
                  ("produit-jonc-vierge-rosee-hd", "jonc-carre-rosee.webp")]:
    im = Image.open(trouver(nom)).convert("RGB"); k = im.width / 1024
    enregistrer(im.crop((round(90 * k), round(104 * k), round(1010 * k), round(1024 * k))), dest, 1200, 84)

# Collier prénom (aperçu en direct) : chaîne sans pendentif, 3 finitions, si elles existent
for nom, dest in [("collier-prenom-vierge-hd", "collier-vierge.webp"), ("collier-prenom-vierge-doree-hd", "collier-vierge-doree.webp"),
                  ("collier-prenom-vierge-rosee-hd", "collier-vierge-rosee.webp")]:
    src = trouver(nom)
    if "vierge" in os.path.basename(src):
        enregistrer(Image.open(src).convert("RGB"), dest, 1200, 84)

# Collier photo (aperçu en direct) : photo produit HD, la photo de la cliente se pose dans la bulle
enregistrer(Image.open(trouver("produit-collier-photo-1-hd", "produit-collier-photo-1")).convert("RGB"), "collier-photo.webp", 1200, 84)
