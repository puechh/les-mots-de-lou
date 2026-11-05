#!/usr/bin/env python3
"""Visuels de PUB Pinterest (2:3, 2000×3000) : photo IA + titre + offre avec sa condition + « Image virtuelle » si Lou apparaît.

Photos : contenu/pinterest/pubs-2026-11/pub-*.jpg (Nano Banana Pro 4K, prompts dans les .txt, « Shot on iPhone 18 Pro… »).
Sortie : contenu/pinterest/pubs-2026-11/final/*.jpg       python3 scripts/pinterest_pubs.py
Règles (docs/pinterest-regles.md) : offre toujours avec sa condition, pas de prix barré, pas de faux avis, pas d'« or »,
pas de « livré avant Noël garanti ». Polices (licence OFL) : scripts/polices/.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "contenu/pinterest/pubs-2026-11")
POL = os.path.join(ROOT, "scripts/polices")
W, H = 2000, 3000
PRUNE, FRAMBOISE, CREME = (59, 31, 43), (226, 69, 122), (255, 250, 248)
OFFRE, CONDITION = "2e bijou à -50 %", "sur le moins cher des deux"


def allura(t): return ImageFont.truetype(os.path.join(POL, "Allura-Regular.ttf"), t)


def mont(t, poids="Medium"):
    f = ImageFont.truetype(os.path.join(POL, "Montserrat-variable.ttf"), t)
    try: f.set_variation_by_name(poids)
    except Exception: pass
    return f


# nom → (titre manuscrit, sous-titre, Lou visible ?, position verticale du recadrage, bas de l'encadré : « offre » ou « noel »)
PUBS = {
    "pub-1-jonc-lou": ("Vos mots, gravés pour toujours", "Le jonc gravé de votre phrase", True, .5, "offre"),
    "pub-2-prenom-lou": ("Son prénom, tout près du cœur", "Le collier prénom personnalisé", True, .45, "offre"),
    "pub-3-photo-lou": ("Un souvenir caché dans un cœur", "Le collier photo personnalisé", True, .5, "offre"),
    "pub-4-duo-cadeau": ("Offrez-en deux", "Jonc gravé + collier prénom", False, .5, "offre"),
    "pub-5-jonc-macro": ("Écrivez, l'atelier grave", "Voyez votre gravure en direct sur le site", False, .5, "noel"),
}


def centre(d, y, txt, f, fill, ombre=None):
    w = d.textlength(txt, font=f)
    if ombre: d.text(((W - w) / 2 + 3, y + 3), txt, font=f, fill=ombre)
    d.text(((W - w) / 2, y), txt, font=f, fill=fill)


def pastille(im, box, rayon, couleur, flou=0):
    calque = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(calque).rounded_rectangle(box, rayon, fill=couleur)
    if flou: calque = calque.filter(ImageFilter.GaussianBlur(flou))
    im.alpha_composite(calque)


def faire(nom, titre, sous, lou, haut, bas):
    im = Image.open(os.path.join(D, nom + ".jpg")).convert("RGB")
    w, h = im.size; nh = round(w * 3 / 2)
    if nh <= h: y = round((h - nh) * haut); im = im.crop((0, y, w, y + nh))
    else: nw = round(h * 2 / 3); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    im = im.resize((W, H), Image.LANCZOS).convert("RGBA")
    # Haut : dégradé doux pour lire le titre
    deg = Image.new("L", (1, H)); [deg.putpixel((0, y), max(0, int(150 * (1 - y / 620)))) for y in range(H)]
    voile = Image.new("RGBA", (W, H), (40, 20, 30, 0)); voile.putalpha(deg.resize((W, H))); im.alpha_composite(voile)
    d = ImageDraw.Draw(im)
    centre(d, 70, "Les Mots de Lou", mont(54, "SemiBold"), CREME)
    f = allura(190)
    while d.textlength(titre, font=f) > W - 160: f = allura(f.size - 6)
    centre(d, 160, titre, f, CREME, ombre=(40, 20, 30, 140))
    centre(d, 400, sous, mont(62, "Medium"), CREME, ombre=(40, 20, 30, 120))
    # Bas : encadré crème
    pastille(im, (150, H - 520, W - 150, H - 150), 70, (40, 20, 30, 70), flou=24)
    pastille(im, (150, H - 530, W - 150, H - 160), 70, CREME + (242,))
    d = ImageDraw.Draw(im)
    if bas == "offre":
        centre(d, H - 495, OFFRE, mont(110, "Bold"), FRAMBOISE)
        centre(d, H - 360, CONDITION, mont(58, "Medium"), PRUNE)
        centre(d, H - 280, "Commandez avant le 10 décembre pour Noël", mont(46, "Regular"), PRUNE)
    else:
        centre(d, H - 485, "Idée cadeau de Noël", mont(96, "Bold"), FRAMBOISE)
        centre(d, H - 360, "Commandez avant le 10 décembre", mont(58, "Medium"), PRUNE)
        centre(d, H - 280, f"{OFFRE} {CONDITION}", mont(46, "Regular"), PRUNE)
    if lou:   # mention obligatoire (personne créée par IA) : lisible, en bas à gauche
        f = mont(40, "SemiBold"); t = "Image virtuelle"; tw = d.textlength(t, font=f)
        pastille(im, (60, H - 120, 60 + tw + 60, H - 50), 35, (40, 20, 30, 150))
        ImageDraw.Draw(im).text((90, H - 113), t, font=f, fill=CREME)
    os.makedirs(os.path.join(D, "final"), exist_ok=True)
    out = os.path.join(D, "final", nom + ".jpg")
    im.convert("RGB").save(out, quality=90, optimize=True)
    print(out)


for nom, args in PUBS.items():
    faire(nom, *args)
