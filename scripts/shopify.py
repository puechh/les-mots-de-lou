"""Accès à l'API Admin Shopify via le flux client credentials.

Lit SHOPIFY_STORE, SHOPIFY_CLIENT_ID et SHOPIFY_CLIENT_SECRET dans l'environnement.
Le jeton est mis en cache dans .shopify_token.json (ignoré par git) jusqu'à son expiration.
N'affiche jamais le secret ni le jeton.
"""

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_VERSION = "2026-10"
TOKEN_CACHE = Path(__file__).resolve().parent.parent / ".shopify_token.json"


def _env(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Variable d'environnement manquante : {name}")
    return value


def _store():
    return _env("SHOPIFY_STORE").removeprefix("https://").strip("/")


def _post(url, payload, headers=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"Erreur HTTP {e.code} sur {url} : {e.read().decode(errors='replace')[:500]}")


def access_token():
    store = _store()
    try:
        cached = json.loads(TOKEN_CACHE.read_text())
        if cached["store"] == store and cached["expires_at"] > time.time() + 300:
            return cached["access_token"]
    except (OSError, ValueError, KeyError):
        pass

    data = _post(
        f"https://{store}/admin/oauth/access_token",
        {
            "client_id": _env("SHOPIFY_CLIENT_ID"),
            "client_secret": _env("SHOPIFY_CLIENT_SECRET"),
            "grant_type": "client_credentials",
        },
    )
    token = data["access_token"]
    TOKEN_CACHE.write_text(json.dumps({
        "store": store,
        "access_token": token,
        "expires_at": time.time() + int(data.get("expires_in", 86399)),
    }))
    TOKEN_CACHE.chmod(0o600)
    return token


def graphql(query, variables=None):
    data = _post(
        f"https://{_store()}/admin/api/{API_VERSION}/graphql.json",
        {"query": query, "variables": variables or {}},
        {"X-Shopify-Access-Token": access_token()},
    )
    if data.get("errors"):
        sys.exit(f"Erreurs GraphQL : {json.dumps(data['errors'], ensure_ascii=False, indent=2)}")
    return data["data"]


STAGED_UPLOAD = """
mutation($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
"""


def upload_file(path, mime_type, resource="FILE"):
    """Envoie un fichier local vers le stockage temporaire Shopify et renvoie son resourceUrl.

    Le resourceUrl s'utilise ensuite comme originalSource (productSet, fileCreate) ou source (themeCreate).
    """
    path = Path(path)
    result = graphql(STAGED_UPLOAD, {"input": [{
        "resource": resource,
        "filename": path.name,
        "mimeType": mime_type,
        "httpMethod": "POST",
        "fileSize": str(path.stat().st_size),
    }]})["stagedUploadsCreate"]
    if result["userErrors"]:
        sys.exit(f"Erreur d'envoi de {path.name} : {result['userErrors']}")
    target = result["stagedTargets"][0]
    form = [arg for p in target["parameters"] for arg in ("-F", f"{p['name']}={p['value']}")]
    subprocess.run(["curl", "-sSf", "--retry", "3", "-o", "/dev/null", *form, "-F", f"file=@{path}", target["url"]],
                   check=True)
    return target["resourceUrl"]


CHECK_QUERY = """
{
  shop { name myshopifyDomain primaryDomain { url } currencyCode plan { displayName } }
  products(first: 1) { nodes { id } }
  productsCount { count }
  themes(first: 20) { nodes { name role } }
}
"""


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("check", "gql"):
        sys.exit("Usage : shopify.py check | shopify.py gql '<requête>' ['<variables JSON>']")
    if sys.argv[1] == "check":
        result = graphql(CHECK_QUERY)
    else:
        variables = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
        result = graphql(sys.argv[2], variables)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
