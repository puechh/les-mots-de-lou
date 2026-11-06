#!/usr/bin/env python3
"""Banque d'images Pinterest SANS TEXTE (2:3, 4K, Nano Banana Pro) : beaucoup de scènes différentes à tester (demande 05/11).

    python3 scripts/pinterest_idees.py [nom …]     # toutes les scènes, ou seulement celles nommées
Sortie : contenu/pinterest/idees-2026-11/<nom>.jpg + .txt (prompt). Bijoux d'après les photos produits (références).
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = "contenu/pinterest/idees-2026-11"
L = ["contenu/lou/reference-v3/00-source-lou.webp", "contenu/lou/reference-v3/01-face.jpg"]
JR, CP = "contenu/lou/fiches-v3/jonc-1-produit.jpg", "contenu/images-ia/2026-11-02-produit-collier-prenom-1-hd.jpg"
PH, MO = "contenu/images-ia/2026-11-02-produit-collier-photo-1-hd.jpg", "contenu/images-ia/2026-11-02-produit-bracelet-morse-1-hd.jpg"
H = "Shot on iPhone 18 Pro by an amateur photographer."
LOU = ("The woman is exactly the same person as in the first two reference photos: identical soft youthful face, facial features, "
       "hazel-brown eyes, eyebrows, lips, sun-kissed skin tone and the same dark chestnut-brown hair in a loose messy bun with "
       "face-framing strands. She looks 20 years old: smooth skin, no wrinkles, only a few very faint freckles on the nose.")
Q = ("Single continuous photo filling the whole vertical frame. Ultra-realistic, true-to-life 4K iPhone photo: extremely sharp, "
     "fine detail in skin, fabric and metal, clean natural colors, no pixelation, no AI smoothing, no beauty filter, no studio "
     "lighting. Absolutely no text, no letters, no logo, no watermark anywhere except the engravings described.")
J = ("thin open cuff bangle only about 4 mm wide (slim band) in polished stainless steel, flat outer face engraved in a thin elegant "
     "handwritten script, each open end finishing in a small rounded tab with a tiny heart-shaped cut-out, exactly like the bangle "
     "in the bangle reference photo")
N = "dainty fine chain name necklace with a single-line cursive cut-out name pendant, exactly like the name necklace reference photo"
P = "heart pendant necklace with a small round lens in its center, exactly like the photo necklace reference photo (no projected image visible)"
M = "Morse code bracelet exactly like the Morse bracelet reference photo"
MAIN = "Realistic hands with exactly five fingers each, natural short nails, smooth sun-kissed skin."

SCENES = {
    "01-table-petit-dejeuner": ([JR, CP, PH, MO], f"{H} Overhead flat lay on a rustic light oak breakfast table on a winter morning: a cappuccino, a croissant on a small plate, a linen napkin, a sprig of pine. Arranged casually: a silver-tone {J} engraved 'Merci maman'; a silver-tone {N} reading 'Jade'; a silver-tone {P}; a {M}. Soft window light. {Q}"),
    "02-sous-le-sapin": ([JR], f"{H} Low angle photo under a decorated Christmas tree at night, warm fairy lights bokeh: a small open blush pink gift box on kraft-wrapped presents, inside on satin a silver-tone {J} engraved 'Tu es ma personne', the engraving readable. {Q}"),
    "03-poignet-stack-3-joncs": ([JR, MO], f"{H} Close-up of a young woman's wrist stack seen from the top of the wrist (no face), hand resting on a cream chunky knit sweater on her lap: three stacked {J} — one silver-tone engraved 'Maman', one gold-tone engraved 'Toujours', one rose-gold-tone engraved 'Léa' — plus one {M}. IMPORTANT: the front faces of the bangles are plain smooth metal with only the engraving, NO holes and NO hearts on the front; the little heart cut-outs exist only on the two open ends, which sit under the wrist and are hidden from this angle. {MAIN} {Q}"),
    "04-poignet-stack-chocolat": ([JR], f"{H} Close-up of two hands holding a big mug of hot chocolate with whipped cream, red knit sleeve pushed up, Christmas lights blurred behind; on the wrist two stacked {J}: a silver-tone one engraved 'Crois en toi' and a rose-gold-tone one engraved 'Sœurs'. {MAIN} {Q}"),
    "05-mains-cadeau": ([JR], f"{H} Close-up of two different people's hands over a wooden table at Christmas: one hand gives the other a small open pink gift box containing a silver-tone {J} engraved 'Pour toujours', the other hand reaches for it. Candles and pine branches softly blurred. {MAIN} {Q}"),
    "06-coupelle-chevet": ([JR, CP], f"{H} Close-up of a small white ceramic jewelry dish on a bedside table in soft morning light, next to a glass of water and an open book: inside the dish a gold-tone {J} engraved 'Ma personne' and a gold-tone {N} reading 'Inès'. {Q}"),
    "07-neige-fenetre": ([JR], f"{H} A rose-gold-tone {J} engraved 'Merci' resting on fresh snow on a wooden window sill, frosty window and warm interior lights behind, blue hour, crisp detail of snow crystals. {Q}"),
    "08-chaussette-noel": ([CP], f"{H} A red knit Christmas stocking hanging on a white mantelpiece, a silver-tone {N} reading 'Emma' spilling out of it, the pendant perfectly readable, garland and fairy lights around. {Q}"),
    "09-marbre-salle-de-bain": ([JR, CP], f"{H} Close-up on a white marble bathroom vanity in soft morning daylight, a small perfume bottle without label and a green eucalyptus sprig: a gold-tone {N} reading 'Lou' laid in a soft curve and a gold-tone {J} engraved 'Vos mots'. {Q}"),
    "10-paume-collier-photo": ([PH], f"{H} Close-up of an open palm holding the {P}, warm Christmas tree lights bokeh behind, the pendant perfectly sharp. {MAIN} {Q}"),
    "11-lou-fenetre-stack": (L + [JR], f"{H} {LOU} Candid photo by a friend near a window on a winter afternoon, soft daylight, she wears an oversized cream sweater and smiles, chin resting on her hand, so her wrist is close to the camera showing two stacked {J}: a silver-tone one engraved 'Ma sœur' and a gold-tone one engraved 'Toujours', engravings readable and not mirrored. Front faces plain metal with only the engraving, no hearts on the front (the heart cut-outs are on the open ends, under the wrist). {MAIN} {Q}"),
    "12-lou-plaid-canape": (L + [JR], f"{H} {LOU} Candid photo by a friend: she sits on a sofa wrapped in a plaid blanket, laughing, holding her wrist up toward the camera to show a silver-tone {J} engraved 'Tu es ma personne', engraving readable, Christmas tree blurred behind. {MAIN} {Q}"),
    # Collier prénom (06/11) : 5 scènes pour les pubs design
    "c1-cou-3-colliers": ([CP], f"{H} Close-up of a young woman's neck and collarbones, cropped just under the chin (no face visible), smooth sun-kissed skin, a few strands of dark chestnut-brown hair, wearing a cream chunky knit sweater with a wide boat neckline (modest), soft daylight. She wears THREE layered {N}s at three different lengths: the shortest in silver-tone reading 'Emma', the middle one in gold-tone reading 'Léa', the longest in rose-gold-tone reading 'Jade'. All three names perfectly sharp and readable, chains fine and dainty. {Q}"),
    "c2-trio-tissu": ([CP], f"{H} Overhead close-up flat lay on blush pink linen: three {N}s laid in soft curves side by side, one silver-tone reading 'Maman', one gold-tone reading 'Inès', one rose-gold-tone reading 'Chloé'; a small kraft gift with red-and-white twine and a pine sprig in a corner. Names perfectly readable. {Q}"),
    "c3-neige-maman": ([CP], f"{H} A gold-tone {N} reading 'Maman' laid on fresh snow on a wooden window sill at blue hour, warm lights of the house glowing behind the frosted window, crisp snow crystals, the name perfectly sharp. {Q}"),
    "c4-ecrin-sapin": ([CP], f"{H} Under a decorated Christmas tree with warm fairy lights bokeh: an open blush pink gift box on kraft-wrapped presents, inside on satin a silver-tone {N} reading 'Jade', laid so the name is perfectly readable. {Q}"),
    "c5-main-pendentif": ([CP], f"{H} Close-up of a woman's hand (no face) holding up a rose-gold-tone {N} between two fingers so the pendant reading 'Louise' dangles in front of warm Christmas lights bokeh, the name perfectly sharp. {MAIN} {Q}"),
}


def gen(nom):
    refs, prompt = SCENES[nom]
    cmd = ["python3", "scripts/fal_images.py", "fal-ai/nano-banana-pro/edit", prompt, "--nom", nom, "--dossier", D,
           "--param", "resolution=4K", "--param", "aspect_ratio=2:3", "--param", "output_format=jpeg"]
    for r in refs: cmd += ["--ref", r]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return nom + " : " + (out.stdout.strip().splitlines() or [out.stderr[-300:]])[-1]


noms = sys.argv[1:] or list(SCENES)
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(gen, noms): print(r)
