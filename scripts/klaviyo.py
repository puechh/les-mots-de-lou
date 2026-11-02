"""Accès à l'API de Klaviyo (compte e-mail de la boutique).

Lit la clé privée dans KLAVIYO_API_KEY (ou laisse le proxy de l'environnement cloud l'injecter).
N'affiche, ne logge et n'écrit jamais la clé.

Usage :
    python3 scripts/klaviyo.py check            # teste l'accès (compte)
    python3 scripts/klaviyo.py get /flows/      # GET brut, affiche le JSON
Depuis Python : from klaviyo import get, post, patch, delete, get_all
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://a.klaviyo.com/api"
REVISION = "2025-10-15"
BETA_REVISION = "2025-10-15.pre"  # création de flux (API en bêta)


def _headers(beta=False, revision=None):
    h = {
        "accept": "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
        "revision": revision or (BETA_REVISION if beta else REVISION),
    }
    key = os.environ.get("KLAVIYO_API_KEY")
    if key:
        h["Authorization"] = f"Klaviyo-API-Key {key}"
    return h


def request(method, path, payload=None, beta=False, tries=5, revision=None):
    url = path if path.startswith("http") else BASE + path
    data = json.dumps(payload).encode() if payload is not None else None
    for i in range(tries):
        req = urllib.request.Request(url, data=data, headers=_headers(beta, revision), method=method)
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = resp.read()
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code == 429 and i < tries - 1:
                time.sleep(int(e.headers.get("Retry-After") or 2 ** (i + 1)))
                continue
            raise RuntimeError(f"HTTP {e.code} {method} {url} : {msg[:1500]}") from None


def get(path, **kw):
    return request("GET", path, **kw)


def post(path, payload, **kw):
    return request("POST", path, payload, **kw)


def patch(path, payload, **kw):
    return request("PATCH", path, payload, **kw)


def delete(path, **kw):
    return request("DELETE", path, **kw)


def get_all(path, **kw):
    """Suit la pagination (links.next) et renvoie toutes les entrées de data."""
    out, url = [], path
    while url:
        d = get(url, **kw)
        out += d.get("data", [])
        url = (d.get("links") or {}).get("next")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        a = get("/accounts/")["data"][0]["attributes"]
        print("OK :", a["contact_information"]["organization_name"], "| fuseau", a["timezone"], "| devise", a["preferred_currency"])
    elif cmd == "get":
        print(json.dumps(get(sys.argv[2]), indent=1, ensure_ascii=False))
