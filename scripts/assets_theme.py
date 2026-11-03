#!/usr/bin/env python3
"""Prépare les images du thème (tailles et qualités réglées pour un site léger, 03/11/2026) (theme-lou/assets/*.webp, favicon) à partir de contenu/lou et contenu/images-ia.

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


# Lou (accueil, 03/11 v3) : Lou près du sapin, jonc « Tu es ma personne » + collier « Lou » (contenu/lou/bijoux-v3, 5504×3072).
# Ordinateur 4:5 : x 1523 → 3981 (toute la hauteur) ; téléphone 5:4 : x 930 → 4770 (toute la hauteur).
# Bijoux sur l'image d'origine : pendentif ≈ (2852, 1951), jonc ≈ (2702, 2677) → repères .r-collier / .r-jonc (lou.css).
_hero = os.path.join(ROOT, "contenu/lou/bijoux-v3/01-accueil-sapin.jpg")
_h = Image.open(_hero).convert("RGB")
enregistrer(_h.crop((1523, 0, 3981, 3072)), "lou-hero.webp", 1400, 74)
enregistrer(_h.crop((930, 0, 4770, 3072)), "lou-hero-mobile.webp", 1400, 72)
# Versions HD chargées en arrière-plan par lou.js juste avant le zoom (zoom x2,1 sur iPhone : il faut ~2 500 px de large)
enregistrer(_h.crop((1523, 0, 3981, 3072)), "lou-hero-hd.webp", 2458, 76)
enregistrer(_h.crop((930, 0, 4770, 3072)), "lou-hero-mobile-hd.webp", 2600, 76)
_face = Image.open(os.path.join(ROOT, "contenu/lou/reference-v3/01-face.jpg")).convert("RGB")   # 3584×4800
enregistrer(_face.crop((0, 240, 3584, 4720)), "lou-portrait.webp", 1000, 78)                     # 4:5
enregistrer(_face.crop((650, 1100, 3050, 3500)), "lou-avatar.webp", 192, 80)                     # visage, carré

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
    enregistrer(im.crop((round(90 * k), round(360 * k), round(1010 * k), round(820 * k))), dest, 1080, 76)

# Fiche du jonc : même photo en carré (x 90→1010, y 104→1024 du repère 1024)
for nom, dest in [("produit-jonc-vierge-hd", "jonc-carre.webp"), ("produit-jonc-vierge-doree-hd", "jonc-carre-doree.webp"),
                  ("produit-jonc-vierge-rosee-hd", "jonc-carre-rosee.webp")]:
    im = Image.open(trouver(nom)).convert("RGB"); k = im.width / 1024
    enregistrer(im.crop((round(90 * k), round(104 * k), round(1010 * k), round(1024 * k))), dest, 1080, 74)

# Collier prénom (aperçu en direct) : chaîne sans pendentif, 3 finitions. Le bas des deux brins (sous y = 640, anneaux
# compris) est effacé : le thème redessine les brins jusqu'aux bords du prénom, qui s'écartent ou se resserrent selon
# sa longueur (lou-produit.js, BRIN_G / BRIN_D). Brins mesurés sur l'image 1200 px (identiques dans les 3 finitions).
BRIN_G = [(626, 361), (640, 367), (680, 394), (720, 411), (760, 437), (800, 466), (840, 490), (860, 501)]
BRIN_D = [(626, 879), (640, 872), (680, 849), (720, 829), (760, 803), (800, 783), (840, 757), (860, 740)]


def effacer_bas_chaine(im):
    """Efface le bas des brins : velours recopié à côté (vers l'intérieur du V), puis lumière corrigée pour qu'il se fonde."""
    import numpy as np
    from PIL import ImageFilter
    a = np.asarray(im, dtype=float)
    out = a.copy()
    flou = lambda x, r: np.stack([np.asarray(Image.fromarray(np.clip(x[..., c], 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(r)), dtype=float) for c in range(3)], axis=-1)
    for brin, decal in ((BRIN_G, 30), (BRIN_D, -30)):
        m = Image.new("L", im.size, 0); d = ImageDraw.Draw(m)
        d.line([(x, y) for y, x in brin], fill=255, width=26, joint="curve")
        y, x = brin[-1]; d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=255)
        dur = np.asarray(m, dtype=float) / 255
        m = np.asarray(m.filter(ImageFilter.GaussianBlur(1.5)), dtype=float) / 255
        rampe = np.clip((np.arange(a.shape[0]) - 626) / 18, 0, 1)[:, None]   # la vraie chaîne s'efface en douceur
        m = m * rampe
        source = np.roll(out, -decal, axis=1)
        # correction de lumière : moyenne locale du velours autour du brin (hors brin) contre celle de la source
        hors = (dur < .01)[..., None]
        poids = flou(hors.repeat(3, axis=2) * 255.0, 18) / 255 + 1e-3
        fond = flou(out * hors, 18) / poids
        src_m = flou(source, 18)
        source = source + (fond - src_m)
        out = out * (1 - m[..., None]) + source * m[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"))


for nom, dest in [("collier-prenom-vierge-hd", "collier-vierge.webp"), ("collier-prenom-vierge-doree-hd", "collier-vierge-doree.webp"),
                  ("collier-prenom-vierge-rosee-hd", "collier-vierge-rosee.webp")]:
    src = trouver(nom)
    if "vierge" in os.path.basename(src):
        im = Image.open(src).convert("RGB").resize((1200, 1200), Image.LANCZOS)
        enregistrer(effacer_bas_chaine(im), dest, 1080, 74)

# Collier photo (aperçu en direct) : photo produit HD, la photo de la cliente se pose dans la bulle
enregistrer(Image.open(trouver("produit-collier-photo-1-hd", "produit-collier-photo-1")).convert("RGB"), "collier-photo.webp", 1080, 74)

# Vignettes produits animées (lou.js) : jonc vierge plein cadre (même cadrage que la photo produit), collier sans prénom,
# photos d'exemple pour la bulle du collier photo
enregistrer(Image.open(trouver("produit-jonc-vierge-hd")).convert("RGB"), "jonc-vierge-plein.webp", 560, 74)
enregistrer(Image.open(os.path.join(A, "collier-vierge.webp")).convert("RGB"), "collier-vierge-carte.webp", 560, 74)
_cp = Image.open(trouver("produit-collier-photo-1-hd")).convert("RGB").resize((1200, 1200), Image.LANCZOS)
enregistrer(_cp.crop((724, 274, 1053, 603)), "souvenir-couple.webp", 320, 76)
for nom in ("souvenir-mamie", "souvenir-chiot"):
    f = trouver(nom)
    if nom in os.path.basename(f):
        im = Image.open(f).convert("RGB"); w, h = im.size; c = min(w, h)
        enregistrer(im.crop(((w - c) // 2, (h - c) // 2, (w + c) // 2, (h + c) // 2)), nom + ".webp", 320, 76)
