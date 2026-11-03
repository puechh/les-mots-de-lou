#!/usr/bin/env python3
"""Construit (ou met à jour) la boutique Les Mots de Lou sur Shopify à partir du dépôt.

    python3 scripts/construire_boutique.py              # tout, sauf la publication du thème
    python3 scripts/construire_boutique.py --publier    # … et publie le thème « Les Mots de Lou (thème) »
    python3 scripts/construire_boutique.py produits --images   # … en remplaçant les images des produits
    python3 scripts/construire_boutique.py produits     # une seule étape : verif, produits, collections, pages,
                                                        #   menus, politiques, offre, theme

Idempotent : relancer le script met à jour ce qui existe déjà (retrouvé par handle / titre).
Ne retire JAMAIS le mot de passe de la boutique.
"""
import glob, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql, upload_file  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "produits/produits.json")))


def gql(q, v=None, cle=None):
    r = graphql(q, v or {})
    if cle:
        r = r[cle]
        errs = r.get("userErrors") or []
        if errs:
            print("  ⚠️", cle, errs)
    return r


# ---------------------------------------------------------------- vérification
def verif():
    s = gql("{ shop { name myshopifyDomain primaryDomain { host } } }")["shop"]
    print(f"Boutique : {s['name']} ({s['myshopifyDomain']})")
    if "corps" in s["name"].lower() or "confiant" in s["name"].lower():
        sys.exit("STOP : ce n'est pas la boutique Les Mots de Lou !")
    return s


def publication_boutique_en_ligne():
    for p in gql("{ publications(first: 20) { nodes { id name } } }")["publications"]["nodes"]:
        if p["name"] in ("Online Store", "Boutique en ligne"):
            return p["id"]
    return None


# ---------------------------------------------------------------- produits
def image_locale(nom):
    f = sorted(glob.glob(os.path.join(ROOT, "contenu", "**", f"*{nom}.png"), recursive=True) +
               glob.glob(os.path.join(ROOT, "contenu", "**", f"*{nom}.jpg"), recursive=True))
    return f[-1] if f else None


def supprimer_medias(ids):
    """Retire des images d'un produit (fileDelete sur les MediaImage)."""
    if ids:
        gql("mutation($ids: [ID!]!) { fileDelete(fileIds: $ids) { deletedFileIds userErrors { field message } } }", {"ids": ids}, "fileDelete")


def produits():
    pub = publication_boutique_en_ligne()
    for p in DATA["produits"]:
        existant = gql("query($q: String!) { products(first: 1, query: $q) { nodes { id handle media(first: 30) { nodes { id } } } } }",
                       {"q": f"handle:{p['handle']}"})["products"]["nodes"]
        contenu = {k: p[k] for k in ("accroche", "benefices", "perso", "apercu", "seo")}
        entree = {
            "handle": p["handle"], "title": p["title"], "productType": p["type"], "vendor": "Les Mots de Lou",
            "status": "ACTIVE", "tags": p["tags"],
            "descriptionHtml": f"<p>{p['accroche']}</p><p>{p['seo']}</p>",
            "seo": {"title": f"{p['title']} personnalisé | Les Mots de Lou", "description": p["seo"][:320]},
            "productOptions": [{"name": p["option"], "values": [{"name": v} for v in p["variantes"]]}],
            "variants": [{"optionValues": [{"optionName": p["option"], "name": v}], "price": p["prix"],
                          "inventoryPolicy": "CONTINUE", "taxable": True} for v in p["variantes"]],
            "metafields": [{"namespace": "lou", "key": "contenu", "type": "json", "value": json.dumps(contenu, ensure_ascii=False)}],
        }
        if existant:
            entree["id"] = existant[0]["id"]
        r = gql("""mutation($i: ProductSetInput!) { productSet(input: $i, synchronous: true) { product { id handle } userErrors { field message } } }""",
                {"i": entree}, "productSet")
        prod = r["product"]
        if not prod:
            continue
        print("Produit :", prod["handle"])
        # Images : envoyées si le produit n'en a pas encore, ou remplacées avec --images (ex. passage en HD)
        if existant and existant[0]["media"]["nodes"] and "--images" in sys.argv:
            supprimer_medias([m["id"] for m in existant[0]["media"]["nodes"]])
            existant[0]["media"]["nodes"] = []
        if not (existant and existant[0]["media"]["nodes"]):
            medias = []
            for nom in p["images"]:
                f = image_locale(nom)
                if not f:
                    print("  image manquante :", nom)
                    continue
                url = upload_file(f, "image/jpeg" if f.endswith(".jpg") else "image/png", "IMAGE")
                medias.append({"originalSource": url, "mediaContentType": "IMAGE", "alt": p["title"]})
            if medias:
                gql("""mutation($id: ID!, $m: [CreateMediaInput!]!) { productCreateMedia(productId: $id, media: $m) { media { id } mediaUserErrors { message } } }""",
                    {"id": prod["id"], "m": medias})
                print(f"  {len(medias)} image(s)")
        if pub:
            gql("""mutation($id: ID!, $p: ID!) { publishablePublish(id: $id, input: [{publicationId: $p}]) { userErrors { message } } }""",
                {"id": prod["id"], "p": pub}, "publishablePublish")


# ---------------------------------------------------------------- collections
def collections():
    pub = publication_boutique_en_ligne()
    for handle, titre, tag, desc in [
        ("joncs", "Joncs gravés", "jonc", "Des joncs gravés avec vos mots : une phrase, une date, un prénom."),
        ("colliers", "Colliers", "collier", "Colliers prénom et colliers photo, personnalisés pour elle."),
        ("bracelets", "Bracelets", "bracelet", "Bracelets à message secret."),
    ]:
        ex = gql("query($q: String!) { collections(first: 1, query: $q) { nodes { id } } }", {"q": f"handle:{handle}"})["collections"]["nodes"]
        entree = {"handle": handle, "title": titre, "descriptionHtml": f"<p>{desc}</p>",
                  "ruleSet": {"appliedDisjunctively": False, "rules": [{"column": "TAG", "relation": "EQUALS", "condition": tag}]}}
        if ex:
            entree["id"] = ex[0]["id"]
            r = gql("mutation($i: CollectionInput!) { collectionUpdate(input: $i) { collection { id } userErrors { message } } }", {"i": entree}, "collectionUpdate")
        else:
            r = gql("mutation($i: CollectionInput!) { collectionCreate(input: $i) { collection { id } userErrors { message } } }", {"i": entree}, "collectionCreate")
        c = r.get("collection")
        if c and pub:
            gql("mutation($id: ID!, $p: ID!) { publishablePublish(id: $id, input: [{publicationId: $p}]) { userErrors { message } } }",
                {"id": c["id"], "p": pub}, "publishablePublish")
        print("Collection :", handle)


# ---------------------------------------------------------------- pages
def pages():
    for f in sorted(glob.glob(os.path.join(ROOT, "contenu/pages/*.json"))):
        meta = json.load(open(f))
        corps = open(f[:-5] + ".html").read()
        ex = gql("query($q: String!) { pages(first: 1, query: $q) { nodes { id } } }", {"q": f"handle:{meta['handle']}"})["pages"]["nodes"]
        entree = {"title": meta["title"], "handle": meta["handle"], "body": corps, "isPublished": True}
        if meta.get("template_suffix"):
            entree["templateSuffix"] = meta["template_suffix"]
        if ex:
            gql("mutation($id: ID!, $p: PageUpdateInput!) { pageUpdate(id: $id, page: $p) { page { id } userErrors { message } } }",
                {"id": ex[0]["id"], "p": entree}, "pageUpdate")
        else:
            gql("mutation($p: PageCreateInput!) { pageCreate(page: $p) { page { id } userErrors { message } } }", {"p": entree}, "pageCreate")
        print("Page :", meta["handle"])


# ---------------------------------------------------------------- menus
def menus():
    def lien(titre, url):
        return {"title": titre, "type": "HTTP", "url": url, "items": []}
    voulus = {
        "main-menu": ("Menu principal", [lien("Tous les bijoux", "/collections/all"), lien("Joncs gravés", "/collections/joncs"),
                                         lien("Colliers", "/collections/colliers"), lien("Le test des mots", "/pages/le-test"),
                                         lien("Qui est Lou ?", "/pages/qui-est-lou")]),
        "footer": ("Aide", [lien("Questions fréquentes", "/pages/faq"), lien("Livraison & retours", "/pages/livraison-retours"),
                            lien("Nous écrire", "/pages/contact")]),
        "legal": ("Informations légales", [lien("Mentions légales", "/policies/legal-notice"), lien("CGV", "/policies/terms-of-service"),
                                           lien("Retours", "/policies/refund-policy"), lien("Livraison", "/policies/shipping-policy"),
                                           lien("Confidentialité", "/policies/privacy-policy")]),
    }
    existants = {m["handle"]: m["id"] for m in gql("{ menus(first: 30) { nodes { id handle } } }")["menus"]["nodes"]}
    for handle, (titre, items) in voulus.items():
        if handle in existants:
            gql("mutation($id: ID!, $t: String!, $h: String!, $i: [MenuItemUpdateInput!]!) { menuUpdate(id: $id, title: $t, handle: $h, items: $i) { menu { id } userErrors { message } } }",
                {"id": existants[handle], "t": titre, "h": handle, "i": items}, "menuUpdate")
        else:
            gql("mutation($t: String!, $h: String!, $i: [MenuItemCreateInput!]!) { menuCreate(title: $t, handle: $h, items: $i) { menu { id } userErrors { message } } }",
                {"t": titre, "h": handle, "i": items}, "menuCreate")
        print("Menu :", handle)


# ---------------------------------------------------------------- politiques
def politiques():
    types = {"legal-notice": "LEGAL_NOTICE", "terms-of-service": "TERMS_OF_SERVICE", "refund-policy": "REFUND_POLICY", "shipping-policy": "SHIPPING_POLICY"}
    actuelles = {p["type"]: p["body"] or "" for p in gql("{ shop { shopPolicies { type body } } }")["shop"]["shopPolicies"]}
    for nom, t in types.items():
        corps = open(os.path.join(ROOT, "contenu/politiques", nom + ".html")).read()
        if actuelles.get(t) and "[À COMPLÉTER" not in actuelles[t]:
            print("Politique déjà complétée dans Shopify, non écrasée :", nom)
            continue
        # Prudence : si la politique a été modifiée dans Shopify depuis la dernière sauvegarde (même partiellement), on n'y touche pas
        try:
            sauv = {p["type"]: p["body"] for p in json.load(open(os.path.join(ROOT, "contenu/politiques.json")))}
        except Exception:
            sauv = {}
        norm = lambda x: " ".join((x or "").split())
        if actuelles.get(t) and t in sauv and norm(actuelles[t]) != norm(sauv[t]):
            print("Politique modifiée dans Shopify depuis la dernière sauvegarde, non écrasée :", nom)
            continue
        gql("mutation($p: ShopPolicyInput!) { shopPolicyUpdate(shopPolicy: $p) { shopPolicy { id } userErrors { message } } }",
            {"p": {"type": t, "body": corps}}, "shopPolicyUpdate")
        print("Politique :", nom)
    print("  (la politique de confidentialité automatique de Shopify n'est pas modifiée)")


# ---------------------------------------------------------------- offre 2e à -50 %
def offre():
    titre = "2e bijou à -50 %"
    ex = gql("query($q: String!) { discountNodes(first: 5, query: $q) { nodes { id discount { ... on DiscountAutomaticBxgy { title status } } } } }",
             {"q": f"title:'{titre}'"})["discountNodes"]["nodes"]
    if any((n.get("discount") or {}).get("title") == titre for n in ex):
        print("Offre déjà créée :", titre)
        return
    # « Tous les produits » est refusé pour une offre BXGY : on liste les produits de la boutique.
    ids = [n["id"] for n in gql("{ products(first: 100, query: \"status:active\") { nodes { id } } }")["products"]["nodes"]]
    items = {"products": {"productsToAdd": ids}}
    r = gql("""mutation($d: DiscountAutomaticBxgyInput!) { discountAutomaticBxgyCreate(automaticBxgyDiscount: $d) { automaticDiscountNode { id } userErrors { field message } } }""",
            {"d": {"title": titre, "startsAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "customerBuys": {"items": items, "value": {"quantity": "1"}},
                   "customerGets": {"items": items, "value": {"discountOnQuantity": {"quantity": "1", "effect": {"percentage": 0.5}}}},
                   "usesPerOrderLimit": "5"}}, "discountAutomaticBxgyCreate")
    print("Offre créée :" if r.get("automaticDiscountNode") else "❌ Offre NON créée :", titre)


# ---------------------------------------------------------------- thème
def theme(publier=False):
    import envoyer_theme as et
    t = et.find_theme() or et.creer()
    ok = et.maj()
    if publier and not ok:
        print("❌ Erreurs dans le thème : publication annulée (corriger theme-lou/ puis relancer).")
        return
    if publier:
        et.publier()
    print("Thème :", "publié" if publier else "envoyé (non publié)")


ETAPES = {"verif": verif, "produits": produits, "collections": collections, "pages": pages, "menus": menus,
          "politiques": politiques, "offre": offre, "theme": theme}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    publier = "--publier" in sys.argv
    verif()
    for nom in (args or ["produits", "collections", "pages", "menus", "politiques", "offre", "theme"]):
        print(f"\n== {nom} ==")
        try:
            ETAPES[nom](publier) if nom == "theme" else ETAPES[nom]()
        except Exception as e:  # on continue les autres étapes
            print(f"  ❌ {nom} : {e}")
    print("\nTerminé. Pensez à : python3 scripts/sauvegarde.py")
