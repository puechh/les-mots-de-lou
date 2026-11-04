"""Fichier CSV d'épingles programmées (import en masse Pinterest) — 1 épingle par jour, 18 h 30 (heure de Paris).

Images : photos des fiches (cdn.shopify.com, lues par l'API Admin) + images verticales de contenu/pinterest/images.json.
Liens : fiches produits de lesmotsdelou.fr avec suivi UTM (utm_source=pinterest) pour GA4.
Règles appliquées (docs/pinterest-regles.md) : pas de faux avis, pas de prix barré, offre -50 % avec sa condition,
« Image virtuelle » sur les épingles où l'on voit le visage de Lou (personne créée par IA).
    python3 scripts/pinterest_csv.py   →   contenu/pinterest/epingles-2026-11.csv
"""
import csv
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://lesmotsdelou.fr/products/"
B_CADEAUX, B_NOEL, B_JONCS, B_COLLIERS, B_PHRASES = ("Idées cadeaux personnalisés", "Cadeaux de Noël personnalisés",
                                                     "Joncs et bracelets gravés", "Colliers prénom et photo", "Idées de phrases à graver")
OFFRE = "2e bijou à -50 % sur le moins cher des deux."
VIRT = " · Image virtuelle."

# (image, produit, tableau, titre, description, mots-clés, visage de Lou ?)
EPINGLES = [
    ("pin-marche-noel", "jonc-mes-mots", B_NOEL, "Idée cadeau de Noël : un bijou gravé avec vos mots",
     "Un jonc gravé avec la phrase qui compte et un collier prénom : le cadeau de Noël qui se garde. Aperçu de la gravure en direct, livraison suivie. Pour Noël, commandez avant le 10 décembre.", "cadeau noel femme, bijou gravé, jonc personnalisé, collier prénom", True),
    ("jonc-01-produit", "jonc-mes-mots", B_JONCS, "Jonc gravé personnalisé « Tu es ma personne »",
     "Jonc fin en acier inoxydable gravé avec votre message, jusqu'à 20 caractères. Deux petits cœurs ajourés aux extrémités. Argenté, doré ou rosé.", "jonc gravé, bracelet personnalisé, bracelet message, bijou acier inoxydable", False),
    ("prenom-03-cou", "collier-prenom", B_COLLIERS, "Collier prénom personnalisé en écriture manuscrite",
     "Son prénom écrit d'un trait, en écriture manuscrite, sur une chaîne fine. Acier inoxydable argenté, doré ou rosé. Aperçu du prénom en direct.", "collier prénom, collier personnalisé, bijou prénom, cadeau personnalisé", False),
    ("photo-03-lou-feu", "collier-souvenir-photo", B_NOEL, "Collier photo : votre souvenir caché dans un cœur",
     "Une photo cachée dans la lentille d'un pendentif cœur : on la voit en regardant à travers, vers la lumière. Le cadeau souvenir pour maman, mamie ou votre amour.", "collier photo, collier projection photo, cadeau maman, cadeau souvenir", True),
    ("morse-02-macro", "bracelet-code-secret", B_JONCS, "Bracelet code Morse : un mot secret à porter",
     "Votre mot secret traduit en code Morse, en perles argentées sur un cordon noir réglable. Personne ne sait ce qu'il dit… sauf vous deux.", "bracelet code morse, bracelet message secret, cadeau meilleure amie, bracelet couple", False),
    ("jonc-04-poignet", "jonc-mes-mots", B_PHRASES, "Que graver sur un bracelet ? « Tu es ma personne »",
     "Idée de phrase à graver : « Tu es ma personne ». Courte, tendre, elle tient sur un jonc (20 caractères). Essayez la vôtre, le rendu s'affiche en direct.", "phrase à graver, idée gravure bracelet, message bijou, citation courte amour", False),
    ("pin-cafe-paris", "collier-prenom", B_CADEAUX, "Bijoux personnalisés : prénom et message gravé",
     "Un collier prénom et un jonc gravé, à porter tous les jours. Acier inoxydable qui ne noircit pas. " + OFFRE, "bijoux personnalisés, collier prénom, jonc gravé, idée cadeau femme", True),
    ("photo-02-cou", "collier-souvenir-photo", B_COLLIERS, "Collier photo personnalisé, pendentif cœur",
     "Le collier qui cache votre plus belle photo dans un petit cœur. Une idée cadeau émouvante pour une naissance, un anniversaire ou Noël.", "collier photo personnalisé, pendentif photo, cadeau naissance, cadeau émouvant", False),
    ("jonc-03-finitions", "jonc-mes-mots", B_JONCS, "Jonc gravé : argenté, doré ou rosé ?",
     "Le même jonc gravé en trois finitions : argentée, dorée ou rosée (finitions colorées sur acier inoxydable). Choisissez la sienne et gravez vos mots.", "jonc doré, bracelet rose gold, jonc argenté gravé, bracelet personnalisé femme", False),
    ("morse-03-carte", "bracelet-code-secret", B_NOEL, "Cadeau de Noël original : un mot secret en Morse",
     "Glissez un mot secret sous le sapin : le bracelet code Morse, avec la clé du code. Pour une meilleure amie, une sœur ou un amour. Commandez avant le 10 décembre pour Noël.", "cadeau noel original, bracelet morse, cadeau sœur, cadeau meilleure amie", False),
    ("prenom-05-marche-noel", "collier-prenom", B_NOEL, "Collier prénom : le cadeau de Noël personnalisé",
     "Son prénom, en écriture manuscrite, à porter près du cœur. Un cadeau de Noël personnalisé qui fait plaisir à coup sûr. Livraison suivie en France et en Belgique.", "cadeau noel personnalisé, collier prénom, cadeau noel maman, bijou prénom", True),
    ("jonc-02-coeurs", "jonc-mes-mots", B_JONCS, "Jonc gravé : le détail des petits cœurs",
     "Deux petits cœurs ajourés aux extrémités du jonc, à l'arrière du poignet. Un détail discret pour un bijou gravé avec vos mots.", "jonc cœur, bracelet jonc femme, bijou détail cœur, jonc personnalisé", False),
    ("morse-04-lou", "bracelet-code-secret", B_CADEAUX, "Idée cadeau meilleure amie : le bracelet code secret",
     "Un mot que vous seules savez lire, traduit en Morse. Le cadeau d'amitié qui se porte tous les jours, cordon réglable. " + OFFRE, "cadeau meilleure amie, bracelet amitié, bracelet morse, cadeau bff", True),
    ("prenom-04-lou", "collier-prenom", B_COLLIERS, "Collier prénom manuscrit : doré, argenté ou rosé",
     "Un prénom découpé d'un seul trait (jusqu'à 10 lettres) sur une chaîne fine 40 + 5 cm. Le vôtre, ou celui de quelqu'un que vous aimez.", "collier prénom doré, collier prénom argent, collier écriture manuscrite, bijou personnalisé", True),
    ("jonc-06-cafe", "jonc-mes-mots", B_PHRASES, "5 phrases courtes à graver sur un bijou",
     "Idées de mots à graver : « Toi, toujours », « Crois en toi », « Merci maman », « Sœurs pour toujours », « Même loin, tout près ». Testez-les sur le jonc, en direct.", "phrases à graver, idée message bijou, citation courte, mots doux", True),
    ("pin-collier-photo-feu", "collier-souvenir-photo", B_CADEAUX, "Collier photo : le cadeau qui fait pleurer (de joie)",
     "Votre photo cachée dans la lentille d'un pendentif cœur. On regarde à travers, vers la lumière… et le souvenir apparaît. Idée cadeau pour maman ou mamie.", "collier photo, cadeau maman, cadeau mamie, cadeau souvenir photo", True),
    ("jonc-05-lou", "jonc-mes-mots", B_CADEAUX, "Bracelet personnalisé femme : le jonc gravé",
     "Un jonc fin et ouvert, gravé avec vos mots, qui s'adapte au poignet. Acier inoxydable, ne noircit pas. Aperçu de la gravure en direct.", "bracelet personnalisé femme, jonc gravé, bracelet gravé prénom, bijou message", True),
    ("morse-02-macro", "bracelet-code-secret", B_PHRASES, "Quel mot cacher en code Morse ?",
     "Idées de mots secrets : NOUS, TOUJOURS, MAMAN, AMIES, JETAIME (jusqu'à 8 lettres). Chaque perle est un point, chaque barrette un trait.", "mot secret, code morse, bracelet message, idée cadeau couple", False),
    ("prenom-03-cou", "collier-prenom", B_NOEL, "Cadeau de Noël pour maman : son prénom en collier",
     "Le prénom de maman, ou ceux de ses enfants, en écriture manuscrite. Pour l'avoir sous le sapin, commandez avant le 10 décembre.", "cadeau noel maman, collier prénom maman, bijou personnalisé noel, idée cadeau maman", False),
    ("pin-rue-paris", "jonc-mes-mots", B_CADEAUX, "Bijoux gravés : des mots qui restent",
     "Un « merci », un « je t'aime », un prénom… gravés pour qu'ils restent. Jonc, collier prénom, collier photo et bracelet code secret. " + OFFRE, "bijoux gravés, cadeau personnalisé femme, jonc gravé, collier prénom", True),
    ("jonc-01-produit", "jonc-mes-mots", B_NOEL, "Jonc gravé : l'idée cadeau de Noël pour elle",
     "Gravez la phrase qu'elle n'oubliera pas sur un jonc fin en acier inoxydable. Aperçu en direct avant de commander. Commandez avant le 10 décembre pour Noël.", "cadeau noel pour elle, jonc gravé, bracelet message, cadeau copine", False),
    ("photo-02-cou", "collier-souvenir-photo", B_COLLIERS, "Comment marche un collier photo à projection ?",
     "La photo est reproduite en tout petit dans une lentille au centre du cœur. Pour la voir : on regarde à travers, vers une lumière. Conseil : une photo nette et lumineuse.", "collier projection, collier photo comment ça marche, pendentif photo cœur, collier souvenir", False),
    ("jonc-04-poignet", "jonc-mes-mots", B_PHRASES, "Phrase à graver pour sa sœur : « Sœurs pour toujours »",
     "Une idée de gravure pour une sœur : « Sœurs pour toujours ». Elle tient sur le jonc (20 caractères). Écrivez-la, le rendu s'affiche en direct.", "cadeau sœur, phrase pour sa sœur, jonc gravé, bijou sœur", False),
    ("morse-03-carte", "bracelet-code-secret", B_CADEAUX, "Cadeau couple : un mot secret en Morse",
     "Un bracelet code Morse avec un mot rien qu'à vous deux. Perles argentées, cordon noir réglable, clé du code fournie sur la fiche.", "cadeau couple, bracelet couple, bracelet morse, cadeau saint valentin", False),
    ("prenom-05-marche-noel", "collier-prenom", B_COLLIERS, "Collier prénom : à porter tous les jours",
     "Un collier prénom en acier inoxydable qui ne noircit pas, à porter tous les jours. Finition argentée, dorée ou rosée.", "collier prénom, collier personnalisé femme, bijou du quotidien, collier acier inoxydable", True),
    ("pin-marche-noel", "collier-prenom", B_NOEL, "Noël : le cadeau personnalisé qui se garde",
     "Un bijou avec SES mots plutôt qu'une bougie de plus. Jonc gravé, collier prénom, collier photo ou bracelet code secret. Pour Noël : avant le 10 décembre.", "cadeau noel personnalisé, idée cadeau noel femme, bijou gravé, cadeau original", True),
    ("jonc-03-finitions", "jonc-mes-mots", B_CADEAUX, "Jonc gravé à offrir : 3 finitions au choix",
     "Argenté, doré ou rosé : choisissez la finition, gravez vos mots, recevez en 5 à 10 jours avec suivi. " + OFFRE, "jonc gravé, bijou à offrir, bracelet personnalisé, cadeau femme", False),
    ("pin-collier-photo-feu", "collier-souvenir-photo", B_NOEL, "Collier photo : un souvenir sous le sapin",
     "Cachez votre plus belle photo dans un pendentif cœur et offrez-la pour Noël. Commandez avant le 10 décembre pour une livraison avant le 24.", "collier photo noel, cadeau souvenir, cadeau noel maman, collier cœur photo", True),
    ("pin-cafe-paris", "jonc-mes-mots", B_PHRASES, "Que graver sur un jonc ? 3 idées tendres",
     "« Toi, toujours », « Ma personne préférée », « Crois en toi » : trois idées courtes pour un jonc gravé. Essayez la vôtre en direct sur la fiche.", "idée gravure jonc, phrase courte, message à graver, cadeau personnalisé", True),
]


def gql(q, v=None):
    r = graphql(q, v)
    return r.get("data", r)


urls = {}
for p in gql("{ products(first: 10) { nodes { media(first: 20) { nodes { ... on MediaImage { image { url } } } } } } }")["products"]["nodes"]:
    for m in p["media"]["nodes"]:
        u = m["image"]["url"]; urls[u.split("/files/")[-1].split("?")[0].rsplit(".", 1)[0]] = u
for k, v in json.load(open(os.path.join(ROOT, "contenu/pinterest/images.json"))).items():
    urls[k] = v["url"]

debut = dt.datetime(2026, 11, 6, 17, 30)   # 18 h 30 à Paris = 17 h 30 UTC (heure d'hiver)
f = os.path.join(ROOT, "contenu/pinterest/epingles-2026-11.csv")
with open(f, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"])
    for i, (img, h, board, titre, desc, mots, lou) in enumerate(EPINGLES):
        assert img in urls, img
        d = desc + (VIRT if lou else "")
        assert len(titre) <= 100 and len(d) <= 500, (titre, len(d))
        lien = f"{SITE}{h}?utm_source=pinterest&utm_medium=organic&utm_campaign=epingles-2026-11"
        w.writerow([titre, urls[img], board, "", d, lien, (debut + dt.timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S"), mots])
print(len(EPINGLES), "épingles →", os.path.relpath(f, ROOT), "| du", debut.date(), "au", (debut + dt.timedelta(days=len(EPINGLES) - 1)).date())
