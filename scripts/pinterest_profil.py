#!/usr/bin/env python3
"""Profil Pinterest (06/11) : bannière 1920×1080, photo de profil 1000×1000, favicons (512, 180, 32).
    python3 scripts/pinterest_profil.py  → contenu/pinterest/profil/
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POL, I, OUT = os.path.join(ROOT, "scripts/polices"), os.path.join(ROOT, "contenu/pinterest/idees-2026-11"), os.path.join(ROOT, "contenu/pinterest/profil")
FRAMB, CREME, PRUNE, BLANC = (226, 69, 122), (255, 250, 248), (59, 31, 43), (255, 255, 255)
def f(nom, t, poids=None):
    x = ImageFont.truetype(os.path.join(POL, nom), t)
    if poids:
        try: x.set_variation_by_name(poids)
        except Exception: pass
    return x
allura = lambda t: f("Allura-Regular.ttf", t)
mont = lambda t, p="SemiBold": f("Montserrat-variable.ttf", t, p)
play = lambda t, p="Regular": f("PlayfairDisplay-variable.ttf", t, p)
os.makedirs(OUT, exist_ok=True)

def couvrir(im, w, h):
    k = max(w / im.width, h / im.height); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x, y, x + w, y + h))

# Photo de profil : « Lou » manuscrit blanc sur framboise (Pinterest l'affiche en rond)
p = Image.new("RGB", (1000, 1000), FRAMB); d = ImageDraw.Draw(p)
d.text((500, 330), "LES MOTS DE", font=mont(70), fill=BLANC, anchor="mm")
d.text((500, 600), "Lou", font=allura(430), fill=BLANC, anchor="mm")
p.save(os.path.join(OUT, "photo-profil-1000.png"))

# Favicon : « L » manuscrit blanc sur framboise, coins arrondis
for t in (512, 180, 32):
    k = 4; g = Image.new("RGBA", (t * k, t * k), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    d.rounded_rectangle((0, 0, t * k - 1, t * k - 1), radius=int(t * k * .22), fill=FRAMB)
    d.text((t * k * .5, t * k * .56), "L", font=allura(int(t * k * .82)), fill=BLANC, anchor="mm")
    g.resize((t, t), Image.LANCZOS).save(os.path.join(OUT, f"favicon-{t}.png"))

# Bannière : texte à gauche sur crème, 3 photos verticales à droite (le centre reste lisible sur mobile)
W, H = 1920, 1080
b = Image.new("RGB", (W, H), CREME); d = ImageDraw.Draw(b)
photos = ["03-poignet-stack-3-joncs", "02-sous-le-sapin", "06-coupelle-chevet"]
x0, l, e = 900, 320, 14
for i, n in enumerate(photos):
    im = couvrir(Image.open(os.path.join(I, n + ".jpg")).convert("RGB"), l, H - 120)
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, l - 1, H - 121), 26, fill=255)
    b.paste(im, (x0 + i * (l + e), 60), m)
d.text((470, 300), "LES MOTS DE LOU", font=mont(40), fill=FRAMB, anchor="mm")
d.text((470, 450), "Vos mots,", font=play(110), fill=PRUNE, anchor="mm")
d.text((450, 590), "gravés pour toujours", font=allura(104), fill=FRAMB, anchor="mm")
d.text((470, 760), "Bijoux personnalisés · aperçu en direct", font=mont(34, "Medium"), fill=PRUNE, anchor="mm")
d.text((470, 815), "lesmotsdelou.fr", font=mont(32, "Medium"), fill=(125, 90, 105), anchor="mm")
b.save(os.path.join(OUT, "banniere-1920x1080.jpg"), quality=92)
print("OK", os.listdir(OUT))


# Bannière v2 (demande utilisateur 06/11) : Lou qui écrit ses mots, pas « pub » : juste une ligne manuscrite à gauche
src = Image.open(os.path.join(OUT, "banniere-lou-source.jpg")).convert("RGB")
b2 = couvrir(src, W, H); d = ImageDraw.Draw(b2)
for xy, t, fo, col in [((300, 420), "Vos mots,", allura(150), PRUNE), ((330, 560), "gravés pour toujours", allura(96), FRAMB),
                       ((330, 660), "lesmotsdelou.fr", mont(30, "Medium"), (125, 90, 105))]:
    d.text((xy[0] + 2, xy[1] + 2), t, font=fo, fill=(255, 255, 255, 200), anchor="mm"); d.text(xy, t, font=fo, fill=col, anchor="mm")
b2.save(os.path.join(OUT, "banniere-lou-1920x1080.jpg"), quality=92); print("bannière Lou OK")
