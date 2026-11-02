#!/usr/bin/env python3
"""Banc d'essai local du thème Shopify `theme-lou/` (sans passer par Shopify).

Rend les gabarits Liquid avec les vrais produits du dépôt (`produits/catalogue.json`) et les
contenus `contenu/fiches/*.json`, et imite le panier Shopify (/cart.js, /cart/add.js, /cart/change.js)
avec l'offre « le 2e à -50 % ». Sert à tester le thème dans un navigateur (Playwright) avant l'envoi.

    python3 scripts/banc_theme.py [port]      # puis http://localhost:8765/

Ce n'est qu'une imitation : quelques filtres et objets Shopify sont simplifiés.
"""
import json, os, re, sys, glob, html, urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from liquid import Environment, DictLoader
from liquid.builtin.filters.misc import default as _default  # noqa: F401 (vérifie l'installation)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(ROOT, "theme-lou")
IMG_DIR = os.environ.get("BANC_IMAGES", "")  # dossier local des photos produits (sinon CDN Shopify)

# ---------- Données ----------
def money(cents):
    return f"{cents / 100:.2f}".replace(".", ",") + " €"

def img_local(nom):
    for f in sorted(glob.glob(os.path.join(ROOT, "contenu/images-ia", "*" + nom + ".png"))):
        return "/local/" + os.path.relpath(f, ROOT)
    return "/local/contenu/lou/reference-visage.png"

def load_products():
    src = json.load(open(os.path.join(ROOT, "produits/produits.json")))["produits"]
    prods, vid, iid = [], 1000, 5000
    for p in src:
        h = p["handle"]; images = []
        for nom in p["images"]:
            iid += 1
            images.append({"id": iid, "src": img_local(nom), "alt": p["title"], "width": 1024, "height": 1024, "aspect_ratio": 1.0, "position": len(images) + 1})
        variants = []
        for val in p["variantes"]:
            vid += 1
            variants.append({"id": vid, "title": val, "options": [val], "option1": val, "available": True, "price": round(float(p["prix"]) * 100),
                             "compare_at_price": None, "featured_image": None})
        contenu = {k: p[k] for k in ("accroche", "benefices", "perso", "apercu", "seo")}
        prods.append({
            "id": len(prods) + 1, "handle": h, "title": p["title"], "url": f"/products/{h}", "type": p["type"],
            "price": variants[0]["price"], "compare_at_price": None, "available": True, "description": "<p>" + p["seo"] + "</p>",
            "images": images, "featured_image": images[0] if images else None, "media": images,
            "variants": variants, "selected_or_first_available_variant": variants[0],
            "options": [p["option"]], "options_with_values": [{"name": p["option"], "values": p["variantes"]}], "has_only_default_variant": False,
            "tags": p["tags"], "collections": [], "metafields": {"lou": {"contenu": {"value": contenu}}},
        })
    return prods

PRODUCTS = load_products()
BY_HANDLE = {p["handle"]: p for p in PRODUCTS}
VARIANTS = {v["id"]: (p, v) for p in PRODUCTS for v in p["variants"]}

def coll(handle, title, test, desc=""):
    ps = [p for p in PRODUCTS if test(p)]
    c = {"handle": handle, "title": title, "url": f"/collections/{handle}", "products": ps, "products_count": len(ps),
         "all_products_count": len(ps), "description": desc, "image": None, "id": handle}
    for p in ps:
        if handle != "all":
            p["collections"].append({"handle": handle, "title": title, "url": c["url"]})
    return c

COLLECTIONS = {c["handle"]: c for c in [
    coll("joncs", "Joncs gravés", lambda p: "jonc" in p["tags"]),
    coll("colliers", "Colliers", lambda p: "collier" in p["tags"]),
    coll("all", "Tous les bijoux", lambda p: True),
]}

def link(title, url, typ="http_link", obj=None):
    return {"title": title, "url": url, "type": typ, "object": obj, "active": False, "child_active": False, "links": []}

def menus():
    m = {}
    m["main-menu"] = {"title": "Menu principal", "links": [link("Tous les bijoux", "/collections/all"), link("Joncs gravés", "/collections/joncs"), link("Colliers", "/collections/colliers"), link("Le test des mots", "/pages/le-test"), link("Qui est Lou ?", "/pages/qui-est-lou")]}
    m["footer"] = {"title": "Aide", "links": [link("FAQ", "/pages/faq"), link("Livraison & retours", "/pages/livraison-retours"), link("Nous écrire", "/pages/contact")]}
    m["legal"] = {"title": "Légal", "links": [link("Mentions légales", "/policies/legal-notice"), link("CGV", "/policies/terms-of-service"), link("Retours", "/policies/refund-policy"), link("Confidentialité", "/policies/privacy-policy")]}
    return m

PAGES = {}
def load_pages():
    for f in glob.glob(os.path.join(ROOT, "contenu/pages/*.json")):
        p = json.load(open(f))
        p["content"] = open(f[:-5] + ".html").read() if os.path.exists(f[:-5] + ".html") else ""
        PAGES[p["handle"]] = p
load_pages()

# ---------- Panier imité (une seule visiteuse) ----------
CART = {"lines": []}  # [{"id": variant_id, "quantity": n, "key": str}]

def cart_json():
    units = []
    for li, l in enumerate(CART["lines"]):
        p, v = VARIANTS[l["id"]]
        units += [(li, v["price"])] * l["quantity"]
    # le 2e à -50 % : dans chaque paire (triée du plus cher au moins cher), le 2e est à moitié prix
    order = sorted(range(len(units)), key=lambda i: -units[i][1])
    disc = [0] * len(CART["lines"])
    for k, i in enumerate(order):
        if k % 2 == 1:
            disc[units[i][0]] += units[i][1] // 2
    items, total = [], 0
    for li, l in enumerate(CART["lines"]):
        p, v = VARIANTS[l["id"]]
        line = v["price"] * l["quantity"]
        img = (v["featured_image"] or p["featured_image"] or {}).get("src", "")
        opts = [{"name": o["name"], "value": v["options"][k]} for k, o in enumerate(p["options_with_values"])]
        items.append({"key": l["key"], "id": v["id"], "variant_id": v["id"], "quantity": l["quantity"], "title": p["title"] + " - " + v["title"],
                      "product_title": p["title"], "variant_title": v["title"], "options_with_values": opts, "product_has_only_default_variant": p["has_only_default_variant"],
                      "price": v["price"], "original_price": v["price"], "final_price": v["price"], "line_price": line, "original_line_price": line,
                      "final_line_price": line - disc[li], "line_level_total_discount": disc[li], "total_discount": disc[li],
                      "image": img, "url": p["url"], "handle": p["handle"], "properties": l.get("props") or {}})
        total += line - disc[li]
    return {"token": "banc", "item_count": sum(l["quantity"] for l in CART["lines"]), "items": items,
            "total_price": total, "original_total_price": total + sum(disc), "items_subtotal_price": total, "total_discount": sum(disc),
            "currency": "EUR", "requires_shipping": True}

def cart_add(items):
    for it in items:
        vid, q = int(it["id"]), int(it.get("quantity", 1))
        if vid not in VARIANTS:
            return False
        props = it.get("properties") or {}
        for l in CART["lines"]:
            if l["id"] == vid and (l.get("props") or {}) == props:
                l["quantity"] += q
                break
        else:
            CART["lines"].append({"id": vid, "quantity": q, "key": f"{vid}:k{len(CART['lines'])}", "props": props})
    return True

def cart_change(key, q):
    for l in CART["lines"]:
        if l["key"] == key or str(l["id"]) == str(key):
            l["quantity"] = int(q)
    CART["lines"] = [l for l in CART["lines"] if l["quantity"] > 0]

# ---------- Liquid ----------
class ImgUrl(str):
    """URL d'image qui garde l'image d'origine (pour image_tag)."""
    def __new__(cls, s, img):
        o = super().__new__(cls, s); o.img = img; return o

def f_image_url(img, width=None, height=None, **kw):
    if not img:
        return ""
    src = img["src"] if isinstance(img, dict) else str(img)
    sep = "&" if "?" in src else "?"
    return ImgUrl(f"{src}{sep}width={width or 800}", img if isinstance(img, dict) else {"src": src})

def f_image_tag(url, **kw):
    if not url:
        return ""
    img = getattr(url, "img", {"src": str(url)})
    base = img.get("src", str(url)); sep = "&" if "?" in base else "?"
    attrs = {"src": str(url), "alt": kw.pop("alt", img.get("alt", "")) or ""}
    widths = kw.pop("widths", None)
    if widths:
        attrs["srcset"] = ", ".join(f"{base}{sep}width={w.strip()} {w.strip()}w" for w in str(widths).split(","))
    attrs["width"] = kw.pop("width", img.get("width", 800))
    attrs["height"] = kw.pop("height", img.get("height", 800))
    for k, v in kw.items():
        if k == "preload":
            continue
        attrs[k] = v
    return "<img " + " ".join(f'{k}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items() if v is not None) + ">"

def to_jsonable(o, depth=0):
    if depth > 8:
        return None
    if isinstance(o, dict):
        return {k: to_jsonable(v, depth + 1) for k, v in o.items() if k not in ("collections", "products", "metafields", "object")}
    if isinstance(o, (list, tuple)):
        return [to_jsonable(v, depth + 1) for v in o]
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    return str(o)

FILTERS = {
    "money": lambda c: money(int(c or 0)), "money_without_trailing_zeros": lambda c: money(int(c or 0)).replace(",00", ""),
    "money_without_currency": lambda c: f"{int(c or 0) / 100:.2f}".replace(".", ","),
    "asset_url": lambda f: f"/assets/{f}?v=1", "asset_img_url": lambda f, *a, **k: f"/assets/{f}",
    "stylesheet_tag": lambda u, **k: f'<link rel="stylesheet" href="{u}" media="all">',
    "script_tag": lambda u: f'<script src="{u}"></script>',
    "image_url": f_image_url, "image_tag": f_image_tag, "img_url": lambda i, *a, **k: f_image_url(i, 600),
    "json": lambda o: json.dumps(to_jsonable(o), ensure_ascii=False).replace("</", "<\\/"),
    "handleize": lambda s: re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-"), "handle": lambda s: re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-"),
    "t": lambda k, **kw: str(k).split(".")[-1].replace("_", " "),
    "link_to": lambda t, u, *a: f'<a href="{u}">{t}</a>', "within": lambda u, c: u,
    "default_pagination": lambda p, **k: "", "payment_type_svg_tag": lambda *a, **k: "", "placeholder_svg_tag": lambda *a, **k: "<svg></svg>",
    "highlight": lambda s, q: s, "time_tag": lambda d, *a, **k: str(d), "structured_data": lambda o: "{}",
    "sort_natural": lambda l, *a: sorted(l, key=lambda x: str(x).lower()),
    "url_for_vendor": lambda v: "/collections/all", "font_face": lambda *a, **k: "", "metafield_tag": lambda m, **k: str(m),
}

PREPROC = [
    (re.compile(r"\{%-?\s*schema\s*-?%\}.*?\{%-?\s*endschema\s*-?%\}", re.S), ""),
    (re.compile(r"\{%-?\s*(?:stylesheet|javascript)\s*-?%\}.*?\{%-?\s*end(?:stylesheet|javascript)\s*-?%\}", re.S), ""),
    (re.compile(r"\{%-?\s*layout\s+[^%]*%\}"), ""),
    (re.compile(r"\{%-?\s*paginate\s+[^%]*%\}"), ""), (re.compile(r"\{%-?\s*endpaginate\s*-?%\}"), ""),
    (re.compile(r"posted_successfully\?"), "posted_successfully"),
]
FORM_RE = re.compile(r"\{%-?\s*form\s+'([a-z_]+)'(?:\s*,\s*([^%]*?))?\s*-?%\}")

def preprocess(src):
    for r, s in PREPROC:
        src = r.sub(s, src)
    def form(m):
        kind, args = m.group(1), m.group(2) or ""
        attrs = dict(re.findall(r"(\w+):\s*'([^']*)'", args))
        action = {"customer": "/contact", "contact": "/contact", "customer_login": "/account/login", "create_customer": "/account", "recover_customer_password": "/account/recover", "storefront_password": "/password"}.get(kind, "/" + kind)
        extra = " ".join(f'{k}="{v}"' for k, v in attrs.items())
        return f'<form method="post" action="{action}" {extra}><input type="hidden" name="form_type" value="{kind}">'
    src = FORM_RE.sub(form, src)
    src = re.sub(r"\{%-?\s*endform\s*-?%\}", "</form>", src)
    # {% section 'x' %} → rendu de la section avec ses réglages
    src = re.sub(r"\{%-?\s*section\s+'([^']+)'\s*-?%\}", lambda m: "{% render '__section__" + m.group(1) + "', section: zz_sections['" + m.group(1) + "'] %}", src)
    return src

def schema_of(name):
    s = open(os.path.join(THEME, "sections", name + ".liquid")).read()
    m = re.search(r"\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema", s, re.S)
    return json.loads(m.group(1)) if m else {}

def section_obj(name, settings=None, blocks=None, sid=None):
    sch = schema_of(name)
    st = {x["id"]: x.get("default") for x in sch.get("settings", []) if "id" in x}
    st.update(settings or {})
    bl = []
    for k, b in (blocks or {}).items():
        bsch = next((x for x in sch.get("blocks", []) if x["type"] == b["type"]), {})
        bst = {x["id"]: x.get("default") for x in bsch.get("settings", []) if "id" in x}
        bst.update(b.get("settings", {}))
        bl.append({"id": k, "type": b["type"], "settings": bst, "shopify_attributes": ""})
    return {"id": sid or name, "settings": st, "blocks": bl, "class": sch.get("class", ""), "tag": sch.get("tag", "div")}

def build_env():
    files = {}
    for f in glob.glob(os.path.join(THEME, "snippets", "*.liquid")):
        files[os.path.basename(f)[:-7]] = preprocess(open(f).read())
    for f in glob.glob(os.path.join(THEME, "sections", "*.liquid")):
        n = os.path.basename(f)[:-7]
        sch = schema_of(n)
        tag = sch.get("tag", "div")
        files["__section__" + n] = f'<{tag} id="shopify-section-{n}" class="shopify-section {sch.get("class", "")}">' + preprocess(open(f).read()) + f"</{tag}>"
    env = Environment(loader=DictLoader(files))
    for k, v in FILTERS.items():
        env.add_filter(k, v)
    return env

def render_template(page_type, suffix, ctx):
    env = build_env()
    name = page_type + ("." + suffix if suffix else "")
    base = os.path.join(THEME, "templates", name)
    if not (os.path.exists(base + ".json") or os.path.exists(base + ".liquid")):
        name, base = page_type, os.path.join(THEME, "templates", page_type)
    if os.path.exists(base + ".json"):
        tj = json.load(open(base + ".json"))
        out = ""
        for sid in tj["order"]:
            s = tj["sections"][sid]
            if s.get("disabled"):
                continue
            sec = section_obj(s["type"], s.get("settings"), s.get("blocks"), sid)
            out += env.from_string("{% render '__section__" + s["type"] + "', section: zz_sec %}").render(**ctx, zz_sec=sec)
        content = out
        layout = tj.get("layout", "theme")
    else:
        src = open(base + ".liquid").read()
        layout = "none" if re.search(r"\{%-?\s*layout\s+none", src) else "theme"
        content = env.from_string(preprocess(src)).render(**ctx)
    if layout in (False, "none"):
        return content
    lay = preprocess(open(os.path.join(THEME, "layout", layout + ".liquid")).read())
    return env.from_string(lay).render(**ctx, content_for_layout=content)

def base_ctx(path, page_type, suffix=None, **extra):
    settings = json.load(open(os.path.join(THEME, "config/settings_data.json")))["current"]
    sections = {n: section_obj(n, settings.get("sections", {}).get(n, {}).get("settings")) for n in ("lou-header", "lou-footer")}
    ctx = {
        "shop": {"name": "Les Mots de Lou", "url": "http://localhost", "email": "contact@lesmotsdelou.fr", "description": "Bijoux personnalisés",
                 "privacy_policy": {"url": "/policies/privacy-policy", "title": "Politique de confidentialité"}, "refund_policy": {"url": "/policies/refund-policy"},
                 "terms_of_service": {"url": "/policies/terms-of-service"}, "currency": "EUR", "money_format": "{{amount_with_comma_separator}} €"},
        "settings": {k: v for k, v in settings.items() if k != "sections"},
        "routes": {"root_url": "/", "cart_url": "/cart", "cart_add_url": "/cart/add", "cart_change_url": "/cart/change", "search_url": "/search",
                   "account_url": "/account", "account_login_url": "/account/login", "account_register_url": "/account/register", "collections_url": "/collections", "all_products_collection_url": "/collections/all"},
        "request": {"locale": {"iso_code": "fr"}, "page_type": page_type, "origin": "http://localhost", "path": path, "design_mode": False},
        "template": {"name": page_type, "suffix": suffix, "directory": "customers" if page_type.startswith("customers") else None},
        "canonical_url": "http://localhost" + path, "page_title": extra.pop("page_title", "Les Mots de Lou"), "page_description": extra.pop("page_description", ""),
        "content_for_header": "", "cart": {**cart_json(), "currency": {"iso_code": "EUR"}},
        "collections": COLLECTIONS, "all_products": BY_HANDLE, "linklists": menus(), "zz_sections": {"__section__" + k: v for k, v in sections.items()},
        "form": {"posted_successfully": False, "errors": None}, "customer": None, "current_page": 1, "pages": PAGES,
        "blogs": {}, "localization": {}, "powered_by_link": "",
    }
    ctx["zz_sections"] = {k: v for k, v in sections.items()}
    ctx.update(extra)
    for link_ in ctx["linklists"]["main-menu"]["links"]:
        link_["active"] = link_["url"] == path
    return ctx

def route(path, query):
    if path in ("/", ""):
        return "index", None, base_ctx(path, "index")
    m = re.match(r"^/products/([^/]+)$", path)
    if m and urllib.parse.unquote(m.group(1)) in BY_HANDLE:
        p = BY_HANDLE[urllib.parse.unquote(m.group(1))]
        cc = (p["metafields"]["lou"]["contenu"]["value"] or {})
        return "product", (query.get("view") or [None])[0], base_ctx(path, "product", product=p, page_title=p["title"], page_description=cc.get("seo", ""), page_image=p["featured_image"])
    m = re.match(r"^/collections/([^/]+)$", path)
    if m and m.group(1) in COLLECTIONS:
        c = COLLECTIONS[m.group(1)]
        return "collection", None, base_ctx(path, "collection", collection=c, page_title=c["title"],
                                            paginate={"pages": 1, "current_page": 1, "items": c["products_count"]})
    if path == "/collections":
        return "list-collections", None, base_ctx(path, "list-collections")
    m = re.match(r"^/pages/([^/]+)$", path)
    if m:
        h = m.group(1)
        pg = PAGES.get(h, {"handle": h, "title": h.replace("-", " ").capitalize(), "content": "<p>Contenu de la page.</p>", "template_suffix": h})
        pg = {**pg, "url": path}
        return "page", pg.get("template_suffix"), base_ctx(path, "page", page=pg, page_title=pg["title"])
    if path == "/cart":
        return "cart", None, base_ctx(path, "cart", page_title="Votre panier")
    if path == "/search":
        q = (query.get("q") or [""])[0].lower()
        res = [p for p in PRODUCTS if q and q in p["title"].lower()]
        return "search", None, base_ctx(path, "search", search={"performed": bool(q), "terms": q, "results": res, "results_count": len(res)}, page_title="Recherche")
    m = re.match(r"^/policies/([^/]+)$", path)
    if m:
        f = os.path.join(ROOT, "contenu/politiques", m.group(1) + ".html")
        p = {"title": m.group(1).replace("-", " ").capitalize(), "body": open(f).read() if os.path.exists(f) else "<p>Politique Shopify</p>"}
        return "page", "politique", base_ctx(path, "page", page={"title": p["title"], "content": p["body"], "handle": m.group(1), "url": path}, page_title=p["title"])
    m = re.match(r"^/account(?:/(login|register|addresses|recover))?$", path)
    if m:
        t = {"login": "customers/login", "register": "customers/register", "addresses": "customers/addresses", None: "customers/login", "recover": "customers/login"}[m.group(1)]
        return t, None, base_ctx(path, t)
    if path == "/password":
        return "password", None, base_ctx(path, "password")
    if path.startswith("/blogs/"):
        return "blog", None, base_ctx(path, "blog", blog={"title": "Nos conseils", "articles": [], "url": "/blogs/conseils", "handle": "conseils"})
    return "404", None, base_ctx(path, "404", page_title="Page introuvable")

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass
    def send(self, code, body, ctype="text/html; charset=utf-8"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); path = urllib.parse.unquote(u.path)
        if path.startswith("/assets/"):
            f = os.path.join(THEME, "assets", os.path.basename(path))
            if not os.path.exists(f):
                return self.send(404, "")
            ct = {"css": "text/css", "js": "application/javascript", "webp": "image/webp", "png": "image/png", "svg": "image/svg+xml", "jpg": "image/jpeg"}.get(f.rsplit(".", 1)[-1], "application/octet-stream")
            return self.send(200, open(f, "rb").read(), ct)
        if path.startswith("/local/"):
            f = os.path.join(ROOT, path[7:])
            if os.path.exists(f) and os.path.realpath(f).startswith(ROOT):
                return self.send(200, open(f, "rb").read(), "image/png")
            return self.send(404, "")
        if path.startswith("/cdn/"):
            f = os.path.join(IMG_DIR, path[5:])
            return self.send(200, open(f, "rb").read(), "image/jpeg") if os.path.exists(f) else self.send(404, "")
        if path == "/cart.js":
            return self.send(200, json.dumps(cart_json()), "application/json")
        if path == "/checkout":
            return self.send(200, "<h1>Caisse Shopify (imitée)</h1>")
        try:
            t, suffix, ctx = route(path, urllib.parse.parse_qs(u.query))
            out = render_template(t, suffix, ctx)
            self.send(404 if t == "404" else 200, out)
        except Exception as e:
            import traceback
            self.send(500, "<pre>" + html.escape(traceback.format_exc()) + "</pre>")
    def do_POST(self):
        u = urllib.parse.urlparse(self.path); n = int(self.headers.get("Content-Length") or 0); raw = self.rfile.read(n)
        ctype = self.headers.get("Content-Type") or ""
        if ctype.startswith("multipart/form-data"):
            from email.parser import BytesParser
            msg = BytesParser().parsebytes(b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + raw)
            body, props = {}, {}
            for part in msg.get_payload():
                name = part.get_param("name", header="content-disposition")
                val = part.get_filename() and ("/uploads/" + part.get_filename()) or part.get_payload(decode=True).decode("utf-8", "replace")
                try:
                    name = name.encode("latin-1").decode("utf-8")
                except (UnicodeError, AttributeError):
                    pass
                m = re.match(r"properties\[(.+)\]", name or "")
                if m:
                    props[m.group(1)] = val
                else:
                    body[name] = val
            body["properties"] = props
        else:
            try:
                body = json.loads(raw or b"{}")
            except Exception:
                body = {k: v[0] for k, v in urllib.parse.parse_qs(raw.decode()).items()}
        if u.path in ("/cart/add.js", "/cart/add"):
            items = body.get("items") or [{"id": body.get("id"), "quantity": body.get("quantity", 1), "properties": body.get("properties")}]
            ok = cart_add(items)
            return self.send(200 if ok else 422, json.dumps({"items": items} if ok else {"status": 422, "description": "Variante introuvable"}), "application/json")
        if u.path in ("/cart/change.js", "/cart/update.js"):
            if "id" in body:
                cart_change(body["id"], body.get("quantity", 0))
            return self.send(200, json.dumps(cart_json()), "application/json")
        if u.path == "/cart/clear.js":
            CART["lines"] = []
            return self.send(200, json.dumps(cart_json()), "application/json")
        self.send_response(302); self.send_header("Location", (self.headers.get("Referer") or "/").split("?")[0] + "?customer_posted=true"); self.end_headers()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"Banc d'essai du thème : http://localhost:{port}/")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
