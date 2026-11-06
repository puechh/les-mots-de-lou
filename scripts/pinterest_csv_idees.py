#!/usr/bin/env python3
"""CSV d'import Pinterest pour les nouvelles images (06/11) : 12 photos sans texte, 6 pubs design, 5 pubs de la 1re série.

1. Redimensionne en 1600×2400 (2:3), envoie dans Shopify → Contenu → Fichiers (adresse publique cdn.shopify.com),
   mémorise les adresses dans contenu/pinterest/idees-2026-11/images.json (pas de nouvel envoi si déjà fait).
2. Écrit contenu/pinterest/epingles-idees-2026-11.csv : toutes publiées tout de suite à l'import (date vide), pour les pubs
   du soir même (décision utilisateur 06/11).
Règles : offre avec sa condition (« Image virtuelle » retirée, décision utilisateur 06/11), pas de prix barré ni d'avis, messages « Noël » avant le 10/12.
    python3 scripts/pinterest_csv_idees.py
"""
import csv, datetime as dt, json, os, sys, time
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql, upload_file  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I = "contenu/pinterest/idees-2026-11"
TMP = os.path.join(ROOT, I, "pinterest-1600")
JSON = os.path.join(ROOT, I, "images.json")
SITE = "https://lesmotsdelou.fr/"
JONC, PRENOM, PHOTO, MORSE, ACCUEIL = "products/jonc-mes-mots", "products/collier-prenom", "products/collier-souvenir-photo", "products/bracelet-code-secret", ""
B_CADEAUX, B_NOEL, B_JONCS, B_COLLIERS, B_PHRASES = ("Idées cadeaux personnalisés", "Cadeaux de Noël personnalisés",
                                                     "Joncs et bracelets gravés", "Colliers prénom et photo", "Idées de phrases à graver")
OFFRE = "2e bijou à -50 % sur le moins cher des deux."
NOEL = "Pour Noël, commandez avant le 10 décembre."

# (fichier, lien, tableau, titre, description, mots-clés, Lou visible ?)
EPINGLES = [
    (f"{I}/pubs/design-1-vos-mots-stack.jpg", JONC, B_JONCS, "Bracelets gravés : vos mots, en stack",
     "Argenté, doré, rosé : empilez les joncs gravés de vos mots, avec un bracelet code Morse. Aperçu de la gravure en direct. " + OFFRE, "stack bracelet, jonc gravé, bracelet personnalisé femme, bracelet message", False),
    (f"{I}/02-sous-le-sapin.jpg", JONC, B_NOEL, "Sous le sapin : un jonc gravé avec vos mots",
     "Le cadeau qui se garde : un jonc fin gravé de la phrase qui compte, dans son écrin. " + NOEL, "cadeau noel femme, jonc gravé, idée cadeau noel, bijou personnalisé", False),
    (f"{I}/pubs/design-3-edition-noel-lou.jpg", JONC, B_NOEL, "L'édition Noël : le bijou gravé qui fait sourire",
     "Un jonc gravé avec vos mots, à offrir ou à s'offrir. " + OFFRE + " " + NOEL, "cadeau noel personnalisé, jonc gravé, bijou message, idée cadeau femme", True),
    (f"{I}/03-poignet-stack-3-joncs.jpg", JONC, B_JONCS, "3 joncs gravés + 1 bracelet Morse : le stack qui parle",
     "« Maman », « Toujours », « Léa » : un mot par jonc, une finition par mot. Acier inoxydable qui ne noircit pas.", "bracelet stack, jonc personnalisé, bracelet prénom, bracelet morse", False),
    (f"{I}/pubs/design-2-cadeau-qui-reste.jpg", JONC, B_CADEAUX, "Le cadeau qui reste pour toujours",
     "Un bijou gravé avec vos mots, qu'on garde longtemps. " + OFFRE, "cadeau personnalisé, cadeau qui dure, bijou gravé, cadeau maman", False),
    (f"{I}/01-table-petit-dejeuner.jpg", ACCUEIL, B_CADEAUX, "4 bijoux personnalisés pour dire les choses",
     "Jonc gravé, collier prénom, collier photo et bracelet code Morse : choisissez celui qui porte vos mots. " + OFFRE, "bijoux personnalisés, idées cadeaux femme, collier prénom, jonc gravé", False),
    (f"{I}/04-poignet-stack-chocolat.jpg", JONC, B_PHRASES, "Idées de mots à graver : « Crois en toi », « Sœurs »",
     "Deux joncs, deux messages : un encouragement, un lien. Trouvez les vôtres et voyez la gravure en direct.", "phrase à graver, cadeau sœur, bracelet encouragement, jonc gravé", False),
    (f"{I}/pubs/design-4-un-mot-neige.jpg", JONC, B_JONCS, "Un mot. Pour toujours.",
     "Le jonc gravé en finition argentée, dorée ou rosée. Un seul mot suffit parfois. " + OFFRE, "jonc gravé, bracelet message, bijou minimaliste, bracelet rose gold", False),
    (f"{I}/05-mains-cadeau.jpg", JONC, B_NOEL, "Offrir des mots qui restent",
     "Le moment où l'on ouvre l'écrin et où l'on lit son prénom ou sa phrase. " + NOEL, "offrir un bijou, cadeau noel, jonc gravé, cadeau émouvant", False),
    (f"{I}/06-coupelle-chevet.jpg", PRENOM, B_COLLIERS, "Collier prénom et jonc gravé, finition dorée",
     "Le duo à porter tous les jours, finition dorée sur acier inoxydable. " + OFFRE, "collier prénom doré, jonc doré gravé, bijoux dorés, duo bijoux", False),
    (f"{I}/pubs/design-5-quatre-bijoux.jpg", ACCUEIL, B_CADEAUX, "4 bijoux. Vos mots dessus.",
     "Jonc gravé, collier prénom, collier photo, bracelet code Morse. " + OFFRE, "bijoux personnalisés, idée cadeau, bijou message, collier personnalisé", False),
    (f"{I}/07-neige-fenetre.jpg", JONC, B_PHRASES, "Que graver ? « Merci », tout simplement",
     "Un seul mot gravé sur un jonc rosé : merci. Pour une maman, une maîtresse, une amie.", "cadeau merci, cadeau maîtresse, jonc rosé, mot à graver", False),
    (f"{I}/08-chaussette-noel.jpg", PRENOM, B_NOEL, "Un prénom dans la chaussette de Noël",
     "Le collier prénom en écriture manuscrite, la petite surprise qui fait plaisir. " + NOEL, "cadeau noel fille, collier prénom, chaussette de noel, petit cadeau noel", False),
    (f"{I}/pubs/design-6-toujours-lou.jpg", JONC, B_JONCS, "Les joncs qui disent tout",
     "« Ma sœur », « Toujours » : deux joncs gravés, deux finitions. " + OFFRE, "jonc gravé, bracelet sœur, stack bracelets, bijou message", True),
    (f"{I}/09-marbre-salle-de-bain.jpg", PRENOM, B_COLLIERS, "Collier prénom doré « Lou » et jonc gravé",
     "Finition dorée sur acier inoxydable, qui ne noircit pas. Le prénom de votre choix, jusqu'à 10 lettres.", "collier prénom doré, bijou prénom, jonc doré, collier personnalisé", False),
    (f"{I}/10-paume-collier-photo.jpg", PHOTO, B_CADEAUX, "Collier photo : un souvenir caché dans un cœur",
     "Votre photo cachée dans la lentille du pendentif : on la voit en regardant à travers, vers la lumière. Idée cadeau pour maman ou mamie.", "collier photo, cadeau maman, cadeau mamie, collier projection", False),
    (f"{I}/11-lou-fenetre-stack.jpg", JONC, B_CADEAUX, "Deux joncs gravés : « Ma sœur » et « Toujours »",
     "Argenté et doré, à porter ensemble. Aperçu de la gravure en direct sur le site.", "bracelet sœur, jonc gravé, cadeau sœur, bracelets empilés", True),
    (f"{I}/12-lou-plaid-canape.jpg", JONC, B_NOEL, "« Tu es ma personne » : le jonc gravé",
     "La phrase qui dit tout, gravée sur un jonc fin. " + NOEL, "tu es ma personne, jonc gravé, cadeau meilleure amie, cadeau couple", True),
    ("contenu/pinterest/pubs-2026-11/final/pub-1-jonc-lou.jpg", JONC, B_NOEL, "Jonc gravé avec vos mots – idée cadeau Noël",
     "Gravez une phrase sur un jonc en acier inoxydable. " + OFFRE + " " + NOEL, "jonc gravé, cadeau noel, bracelet personnalisé, idée cadeau femme", True),
    ("contenu/pinterest/pubs-2026-11/final/pub-2-prenom-lou.jpg", PRENOM, B_NOEL, "Collier prénom personnalisé – cadeau de Noël",
     "Son prénom en écriture manuscrite. " + OFFRE + " " + NOEL, "collier prénom, cadeau noel, bijou prénom, collier personnalisé", True),
    ("contenu/pinterest/pubs-2026-11/final/pub-3-photo-lou.jpg", PHOTO, B_CADEAUX, "Collier photo personnalisé : un souvenir dans un cœur",
     "Votre photo cachée dans le pendentif. " + OFFRE, "collier photo, collier projection, cadeau souvenir, cadeau maman", True),
    ("contenu/pinterest/pubs-2026-11/final/pub-4-duo-cadeau.jpg", ACCUEIL, B_CADEAUX, "2e bijou à -50 % sur le moins cher des deux",
     "Un jonc gravé et un collier prénom à offrir ensemble. " + NOEL, "duo bijoux, cadeau personnalisé, jonc gravé, collier prénom", False),
    ("contenu/pinterest/pubs-2026-11/final/pub-5-jonc-macro.jpg", JONC, B_JONCS, "Bracelet jonc gravé : voyez votre gravure en direct",
     "Tapez vos mots, la gravure s'affiche sur le jonc. Argenté, doré ou rosé. " + OFFRE, "jonc gravé, bracelet personnalisé, gravure bracelet, bracelet message", False),
]


def gql(q, v=None):
    r = graphql(q, v); return r.get("data", r)


os.makedirs(TMP, exist_ok=True)
urls = json.load(open(JSON)) if os.path.exists(JSON) else {}
for f, *_ in EPINGLES:
    nom = "lou-pin-" + os.path.basename(f)[:-4]
    if nom in urls: continue
    im = Image.open(os.path.join(ROOT, f)).convert("RGB")
    w, h = im.size; nh = round(w * 3 / 2)
    if nh <= h: y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    else: nw = round(h * 2 / 3); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    chemin = os.path.join(TMP, nom + ".jpg"); im.resize((1600, 2400), Image.LANCZOS).save(chemin, quality=88, optimize=True)
    src = upload_file(chemin, "image/jpeg", "FILE")
    r = gql("mutation($f: [FileCreateInput!]!) { fileCreate(files: $f) { files { id } userErrors { message } } }",
            {"f": [{"originalSource": src, "contentType": "IMAGE", "alt": "Les Mots de Lou"}]})["fileCreate"]
    if r["userErrors"]: sys.exit(f"{nom} : {r['userErrors']}")
    fid = r["files"][0]["id"]
    for _ in range(40):
        n = gql("query($id: ID!) { node(id: $id) { ... on MediaImage { image { url } } } }", {"id": fid})["node"]
        if n and n.get("image"): break
        time.sleep(2)
    urls[nom] = n["image"]["url"]; print(nom, "→", urls[nom][:90])
    json.dump(urls, open(JSON, "w"), indent=2)

debut = dt.datetime(2026, 11, 7, 12, 30)
sortie = os.path.join(ROOT, "contenu/pinterest/epingles-idees-2026-11.csv")
with open(sortie, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"])
    for k, (f, lien, tab, titre, desc, mots, lou) in enumerate(EPINGLES):
        nom = "lou-pin-" + os.path.basename(f)[:-4]
        url = f"{SITE}{lien}?utm_source=pinterest&utm_medium=organic&utm_campaign=idees-2026-11&utm_content={os.path.basename(f)[:-4]}"
        assert len(titre) <= 100 and len(desc) <= 500
        w.writerow([titre, urls[nom], tab, "", desc, url, "", mots])
print(sortie, len(EPINGLES), "épingles")
