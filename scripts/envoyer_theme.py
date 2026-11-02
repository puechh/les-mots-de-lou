#!/usr/bin/env python3
"""Envoie le thème `theme-lou/` sur Shopify.

    python3 scripts/envoyer_theme.py creer            # crée le thème (non publié) à partir d'un zip
    python3 scripts/envoyer_theme.py maj [fichiers…]  # met à jour les fichiers du thème déjà créé (tous si aucun n'est donné)
    python3 scripts/envoyer_theme.py publier          # le rend public (l'ancien thème reste dans la bibliothèque)

Le thème est retrouvé par son nom (THEME_NAME). Rien n'est publié sans la commande « publier ».
"""
import base64, os, sys, time, zipfile, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shopify import graphql, upload_file  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME_DIR = os.path.join(ROOT, "theme-lou")
THEME_NAME = "Les Mots de Lou (thème)"
TEXT = (".liquid", ".json", ".css", ".js", ".svg", ".txt")


def theme_files():
    for d, _, files in os.walk(THEME_DIR):
        for f in sorted(files):
            full = os.path.join(d, f)
            yield os.path.relpath(full, THEME_DIR).replace(os.sep, "/"), full


def find_theme():
    for t in graphql("{ themes(first: 30) { nodes { id name role processing } } }")["themes"]["nodes"]:
        if t["name"] == THEME_NAME:
            return t
    return None


def creer():
    if find_theme():
        sys.exit("Le thème existe déjà : utilisez « maj ».")
    tmp = os.path.join(tempfile.mkdtemp(), "les-mots-de-lou-theme.zip")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, full in theme_files():
            z.write(full, rel)
    url = upload_file(tmp, "application/zip")
    r = graphql("""mutation($s: URL!, $n: String) { themeCreate(source: $s, name: $n, role: UNPUBLISHED) { theme { id name role processing } userErrors { field message } } }""",
                {"s": url, "n": THEME_NAME})["themeCreate"]
    print(r)
    t = r["theme"]
    while t and t.get("processing"):
        time.sleep(4)
        t = find_theme()
        print("traitement…", t and t.get("processing"))
    return t


def maj(only=None):
    t = find_theme()
    if not t:
        sys.exit("Thème introuvable : lancez d'abord « creer ».")
    batch, sent, errors = [], 0, []
    def flush():
        nonlocal batch, sent
        if not batch:
            return
        r = graphql("""mutation($id: ID!, $f: [OnlineStoreThemeFilesUpsertFileInput!]!) { themeFilesUpsert(themeId: $id, files: $f) { upsertedThemeFiles { filename } userErrors { filename code message } } }""",
                    {"id": t["id"], "f": batch})["themeFilesUpsert"]
        errors.extend(r["userErrors"])
        sent += len(r["upsertedThemeFiles"] or [])
        batch = []
    for rel, full in theme_files():
        if only and rel not in only:
            continue
        if rel.endswith(TEXT):
            body = {"type": "TEXT", "value": open(full, encoding="utf-8").read()}
        else:
            body = {"type": "BASE64", "value": base64.b64encode(open(full, "rb").read()).decode()}
        batch.append({"filename": rel, "body": body})
        if len(batch) >= 20:
            flush()
    flush()
    print(f"{sent} fichier(s) envoyé(s) vers {t['name']} ({t['id']})")
    for e in errors:
        print("ERREUR", e)
    return not errors


def publier():
    t = find_theme()
    r = graphql("""mutation($id: ID!) { themePublish(id: $id) { theme { id name role } userErrors { field message } } }""", {"id": t["id"]})
    print(r["themePublish"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "creer":
        creer()
    elif cmd == "maj":
        maj(set(sys.argv[2:]) or None)
    elif cmd == "publier":
        publier()
    else:
        sys.exit(__doc__)
