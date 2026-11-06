#!/usr/bin/env python3
"""Pubs Pinterest « design » (2000×3000) façon magazine : grand titre (parfois DERRIÈRE le sujet détouré), offre avec sa
condition en petit, bouton, logo. Photos sans texte : contenu/pinterest/idees-2026-11/ ; détourages : …/detoure/ (fal BiRefNet).

    python3 scripts/pinterest_design.py        → contenu/pinterest/idees-2026-11/pubs/*.jpg
Règles : offre toujours avec « sur le moins cher des deux », pas de prix barré,
pas de faux avis, pas d'« or ». Polices OFL : scripts/polices/.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "contenu/pinterest/idees-2026-11")
POL = os.path.join(ROOT, "scripts/polices")
W, H = 2000, 3000
BLANC, CREME, PRUNE, FRAMB = (255, 255, 255), (255, 250, 248), (59, 31, 43), (226, 69, 122)
OFFRE, COND = "2e bijou à -50 %", "sur le moins cher des deux"


def police(fichier, t, poids=None):
    f = ImageFont.truetype(os.path.join(POL, fichier), t)
    if poids:
        try: f.set_variation_by_name(poids)
        except Exception: pass
    return f
mont = lambda t, p="Medium": police("Montserrat-variable.ttf", t, p)
play = lambda t, p="Regular": police("PlayfairDisplay-variable.ttf", t, p)
playi = lambda t, p="Italic": police("PlayfairDisplay-Italic-variable.ttf", t, p)
allura = lambda t: police("Allura-Regular.ttf", t)


def cadrer(im):
    k = max(W / im.width, H / im.height); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def photo(nom):
    return cadrer(Image.open(os.path.join(D, nom + ".jpg")).convert("RGB")).convert("RGBA")


def sujet(nom):
    """Sujet détouré, même cadrage que la photo (pour mettre le texte derrière)."""
    p = os.path.join(D, "detoure", nom + ".png")
    m = Image.open(p).convert("RGBA").getchannel("A")
    src = Image.open(os.path.join(D, nom + ".jpg")).convert("RGB")
    m = m.resize(src.size, Image.LANCZOS)
    s = src.convert("RGBA"); s.putalpha(m)
    return cadrer(s)


def calque(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def texte(c, xy, t, f, fill, ancre="mm", esp=0, ombre=None):
    d = ImageDraw.Draw(c)
    if esp:   # espacement des lettres
        larg = sum(d.textlength(ch, font=f) for ch in t) + esp * (len(t) - 1)
        x = xy[0] - larg / 2 if ancre[0] == "m" else xy[0]
        for ch in t:
            if ombre: d.text((x + 3, xy[1] + 3), ch, font=f, fill=ombre, anchor="l" + ancre[1])
            d.text((x, xy[1]), ch, font=f, fill=fill, anchor="l" + ancre[1]); x += d.textlength(ch, font=f) + esp
        return
    if ombre: d.text((xy[0] + 3, xy[1] + 3), t, font=f, fill=ombre, anchor=ancre)
    d.text(xy, t, font=f, fill=fill, anchor=ancre)


def ombre_douce(c, rayon=18, alpha=90):
    a = c.getchannel("A").filter(ImageFilter.GaussianBlur(rayon)).point(lambda v: v * alpha // 255)
    o = Image.new("RGBA", c.size, (40, 20, 30, 0)); o.putalpha(a); return o


def bouton(c, cx, cy, t, f, fond, encre, pad=(70, 34), rond=True):
    d = ImageDraw.Draw(c); w = d.textlength(t, font=f); h = f.size
    box = (cx - w / 2 - pad[0], cy - h / 2 - pad[1], cx + w / 2 + pad[0], cy + h / 2 + pad[1])
    d.rounded_rectangle(box, radius=(box[3] - box[1]) / 2 if rond else 4, fill=fond)
    d.text((cx, cy), t, font=f, fill=encre, anchor="mm")


def degrade(c, haut=True, hauteur=900, alpha=120):
    g = Image.new("L", (1, H))
    for y in range(H):
        v = (1 - y / hauteur) if haut else (1 - (H - y) / hauteur)
        g.putpixel((0, y), int(max(0, v) * alpha))
    v = Image.new("RGBA", (W, H), (35, 18, 26, 0)); v.putalpha(g.resize((W, H))); c.alpha_composite(v)


def virtuelle(c):
    texte(c, (60, H - 60), "Image virtuelle", mont(36, "SemiBold"), (255, 255, 255, 230), "ls")


def sauver(c, nom):
    os.makedirs(os.path.join(D, "pubs"), exist_ok=True)
    c.convert("RGB").save(os.path.join(D, "pubs", nom + ".jpg"), quality=90, optimize=True); print(nom)


# 1. Façon « black friday » : énorme titre DERRIÈRE le poignet empilé
def pub_stack():
    n = "03-poignet-stack-3-joncs"; c = photo(n); degrade(c, True, 1300, 110)
    t = calque()
    texte(t, (W / 2, 560), "vos", mont(560, "Black"), BLANC)
    texte(t, (W / 2, 1060), "mots", mont(560, "Black"), BLANC)
    c.alpha_composite(ombre_douce(t, 30, 70)); c.alpha_composite(t)
    s = sujet(n); c.alpha_composite(s)
    texte(c, (W / 2, 2470), "Gravés pour toujours.", play(96, "SemiBold"), PRUNE)
    bouton(c, W / 2, 2650, "Je crée mon stack", mont(64, "SemiBold"), PRUNE, CREME)
    texte(c, (W / 2, 2820), f"{OFFRE} {COND}", mont(42, "SemiBold"), PRUNE)
    texte(c, (W / 2, 120), "LES MOTS DE LOU", mont(46, "SemiBold"), BLANC, esp=14)
    sauver(c, "design-1-vos-mots-stack")


# 2. Façon « ep jewels » : serif élégant centré sur la boîte sous le sapin
def pub_sapin():
    c = photo("02-sous-le-sapin"); degrade(c, True, 1500, 150)
    texte(c, (W / 2, 190), "les mots de lou", playi(78), CREME)
    texte(c, (W / 2, 520), "Le cadeau", play(250, "Regular"), CREME, ombre=(30, 15, 20, 120))
    texte(c, (W / 2, 790), "QUI RESTE", mont(210, "Medium"), CREME, esp=20, ombre=(30, 15, 20, 120))
    texte(c, (W / 2, 1010), "pour toujours", allura(230), CREME, ombre=(30, 15, 20, 140))
    pl = calque(); bouton(pl, W / 2, 2760, f"{OFFRE} · {COND}", mont(46, "SemiBold"), (255, 250, 248, 235), PRUNE)
    c.alpha_composite(pl)
    texte(c, (W / 2, 2900), "lesmotsdelou.fr", mont(40, "Medium"), CREME, ombre=(30, 15, 20, 160))
    sauver(c, "design-2-cadeau-qui-reste")


# 3. Façon « Banana Republic » : éditorial, grand chiffre, bouton rectangulaire blanc (le jonc reste dégagé)
def pub_lou():
    n = "12-lou-plaid-canape"; c = photo(n); degrade(c, True, 700, 150); degrade(c, False, 700, 200)
    texte(c, (W / 2, 130), "LES MOTS DE LOU", play(64, "Regular"), BLANC, esp=10)
    texte(c, (W / 2, 330), "L'ÉDITION NOËL", play(150, "Regular"), BLANC, esp=10, ombre=(30, 15, 20, 120))
    texte(c, (W / 2, 2560), "-50 % SUR LE 2e BIJOU", play(118, "Regular"), BLANC, ombre=(30, 15, 20, 150))
    bouton(c, W / 2, 2750, "JE PERSONNALISE", mont(52, "Bold"), BLANC, PRUNE, pad=(110, 40), rond=False)
    texte(c, (W / 2, 2895), "Sur le moins cher des deux", mont(34, "Medium"), (255, 255, 255, 220))
    sauver(c, "design-3-edition-noel-lou")


# 4. Minimal neige : script géant + petite ligne
def pub_neige():
    c = photo("07-neige-fenetre"); degrade(c, True, 1400, 120)
    texte(c, (W / 2, 140), "LES MOTS DE LOU", mont(46, "SemiBold"), BLANC, esp=14)
    texte(c, (W / 2, 560), "Un mot.", play(230, "Regular"), BLANC, ombre=(20, 25, 45, 120))
    texte(c, (W / 2, 830), "Pour toujours.", playi(200), BLANC, ombre=(20, 25, 45, 120))
    texte(c, (W / 2, 1040), "Jonc gravé · argenté, doré ou rosé", mont(56, "Medium"), BLANC, ombre=(20, 25, 45, 150))
    bouton(c, W / 2, 2780, "Gravez le vôtre", mont(58, "SemiBold"), BLANC, PRUNE)
    texte(c, (W / 2, 2920), f"{OFFRE} {COND}", mont(38, "Medium"), BLANC, ombre=(20, 25, 45, 160))
    sauver(c, "design-4-un-mot-neige")


# 5. Table du petit-déjeuner : grand titre bicolore en bas sur bandeau crème
def pub_table():
    c = photo("01-table-petit-dejeuner"); d = ImageDraw.Draw(c)
    d.rectangle((0, 2280, W, H), fill=CREME + (255,))
    texte(c, (W / 2, 2440), "4 bijoux.", play(170, "SemiBold"), PRUNE)
    texte(c, (W / 2, 2620), "Vos mots dessus.", playi(150), FRAMB)
    texte(c, (W / 2, 2790), f"{OFFRE.upper()}  ·  {COND.upper()}", mont(42, "SemiBold"), PRUNE, esp=3)
    texte(c, (W / 2, 2900), "lesmotsdelou.fr", mont(38, "Medium"), (125, 90, 105, 255))
    texte(c, (W / 2, 130), "LES MOTS DE LOU", mont(46, "SemiBold"), BLANC, esp=14, ombre=(30, 15, 20, 140))
    sauver(c, "design-5-quatre-bijoux")


# 6. Lou à la fenêtre : « toujours » en script framboise sur le pull, au-dessus des joncs
def pub_fenetre():
    n = "11-lou-fenetre-stack"; c = photo(n); degrade(c, True, 600, 120)
    texte(c, (W / 2, 140), "LES MOTS DE LOU", mont(46, "SemiBold"), BLANC, esp=14)
    texte(c, (520, 2080), "toujours", allura(300), FRAMB)
    texte(c, (W / 2, 2600), "Les joncs qui disent tout", play(104, "Regular"), PRUNE)
    bouton(c, W / 2, 2770, "Je crée le mien", mont(58, "SemiBold"), PRUNE, CREME)
    texte(c, (W / 2, 2915), f"{OFFRE} {COND}", mont(40, "SemiBold"), PRUNE)
    sauver(c, "design-6-toujours-lou")


for f in (pub_stack, pub_sapin, pub_lou, pub_neige, pub_table, pub_fenetre): f()
