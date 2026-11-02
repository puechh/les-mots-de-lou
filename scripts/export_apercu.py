#!/usr/bin/env python3
"""Exporte la bêta du thème en pages HTML statiques (aperçu cliquable, sans Shopify).

    python3 scripts/banc_theme.py 8765 &      # le banc d'essai doit tourner
    python3 scripts/export_apercu.py <dossier_sortie>

Pages rendues par le banc, CSS/JS inlinés, images converties en webp, liens réécrits vers les fichiers exportés,
panier de démonstration (en mémoire) et formulaires désactivés. La page d'accueil sort en deux exemplaires :
index.html (corps seul, pour une publication « Artifact ») et accueil.html (page complète).
"""
import os, re, sys, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "http://localhost:8765"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "apercu")
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
os.environ["NO_PROXY"] = "localhost"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

PAGES = {
    "/": "accueil.html", "/collections/all": "bijoux.html", "/collections/joncs": "joncs.html", "/collections/colliers": "colliers.html",
    "/products/jonc-mes-mots": "jonc-mes-mots.html", "/products/collier-prenom": "collier-prenom.html",
    "/products/collier-souvenir-photo": "collier-souvenir-photo.html", "/products/bracelet-code-secret": "bracelet-code-secret.html",
    "/pages/le-test": "le-test.html", "/pages/qui-est-lou": "qui-est-lou.html", "/pages/faq": "faq.html",
    "/pages/livraison-retours": "livraison-retours.html", "/pages/contact": "contact.html",
    "/policies/legal-notice": "mentions-legales.html", "/policies/terms-of-service": "cgv.html",
    "/policies/refund-policy": "retours.html", "/policies/shipping-policy": "livraison.html",
}
CSS = open(os.path.join(ROOT, "theme-lou/assets/lou.css")).read()
JS = {n: open(os.path.join(ROOT, "theme-lou/assets", n)).read() for n in ("lou.js", "lou-produit.js")}

DEMO = r"""<script>
/* Aperçu : panier de démonstration en mémoire (aucune commande possible) */
(function(){
  var lignes = [], realFetch = window.fetch.bind(window);
  function json(o){ return Promise.resolve(new Response(JSON.stringify(o), {status:200, headers:{"Content-Type":"application/json"}})); }
  function panier(){
    var unites = [];
    lignes.forEach(function(l,i){ for (var k=0;k<l.quantity;k++) unites.push([i,l.price]); });
    unites.sort(function(a,b){return b[1]-a[1];});
    var rem = lignes.map(function(){return 0;});
    unites.forEach(function(u,k){ if (k%2===1) rem[u[0]] += Math.round(u[1]/2); });
    var items = lignes.map(function(l,i){ var lp=l.price*l.quantity; return {key:l.key, quantity:l.quantity, product_title:l.title, variant_title:l.variant, properties:l.props, image:l.image, original_line_price:lp, final_line_price:lp-rem[i]}; });
    var tot = items.reduce(function(s,x){return s+x.final_line_price;},0), d = rem.reduce(function(s,x){return s+x;},0);
    return {item_count: lignes.reduce(function(s,l){return s+l.quantity;},0), items:items, total_price:tot, total_discount:d};
  }
  window.fetch = function(url, opt){
    url = String(url);
    if (/cart\.js$/.test(url)) return json(panier());
    if (/cart\/add\.js$/.test(url)) {
      var fd = opt.body, props = {}, id = fd.get("id"), f = document.querySelector('.finition.is-on:not(.police-btn)');
      fd.forEach(function(v,k){ var m = k.match(/^properties\[(.+)\]$/); if (m) props[m[1]] = (v && v.name) ? "/uploads/" + v.name : v; });
      var img = document.querySelector(".vignettes button[data-vue='0'] img");
      var prix = Math.round(parseFloat((document.getElementById("prix").textContent||"0").replace(",", ".")) * 100);
      lignes.push({key: id + ":" + lignes.length, quantity:1, title: document.querySelector("h1").textContent, variant: f ? f.getAttribute("data-nom") : "", props: props, image: img ? img.getAttribute("src").split("?")[0] : "", price: prix});
      return json({});
    }
    if (/cart\/change\.js$/.test(url)) {
      var b = JSON.parse(opt.body); lignes.forEach(function(l){ if (l.key === b.id) l.quantity = b.quantity; });
      lignes = lignes.filter(function(l){ return l.quantity > 0; }); return json(panier());
    }
    return realFetch(url, opt);
  };
  document.addEventListener("submit", function(e){ if (!e.target.closest("#form-produit")) { e.preventDefault(); window.LOU_toast && LOU_toast("Aperçu : formulaire désactivé (la boutique n'est pas encore ouverte)"); } }, true);
  document.addEventListener("click", function(e){ var a = e.target.closest && e.target.closest("#checkout, [data-demo]"); if (a) { e.preventDefault(); window.LOU_toast && LOU_toast("Aperçu : le paiement n'est pas branché"); } });
})();
</script>"""
BANDEAU = '<div style="position:fixed;left:0;right:0;bottom:0;z-index:95;background:#3b1f2b;color:#ffe6ef;font:700 13px Nunito,Arial,sans-serif;text-align:center;padding:8px max(16px,env(safe-area-inset-right,0px)) calc(8px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))">Aperçu de la bêta · boutique pas encore ouverte · panier de démonstration</div>'

images = {}


def image(url):
    """/local/… ou /assets/… → img/<nom>.webp (900 px max)."""
    chemin = url.split("?")[0]
    if chemin in images:
        return images[chemin]
    src = os.path.join(ROOT, chemin[len("/local/"):]) if chemin.startswith("/local/") else os.path.join(ROOT, "theme-lou", chemin.lstrip("/"))
    nom = os.path.splitext(os.path.basename(chemin))[0] + ".webp"
    dest = os.path.join(OUT, "img", nom)
    if not os.path.exists(dest):
        im = Image.open(src)
        im = im.convert("RGBA" if im.mode in ("RGBA", "P") else "RGB")
        im.thumbnail((900, 900))
        im.save(dest, "WEBP", quality=78)
    images[chemin] = "img/" + nom
    return images[chemin]


def lien(m):
    attr, url = m.group(1), m.group(2)
    chemin, _, reste = url.partition("?")
    chemin, _, ancre = chemin.partition("#")
    if chemin == "" and ancre:
        return m.group(0)
    if chemin in PAGES:
        cible = PAGES[chemin] + (("?" + reste) if reste else "") + (("#" + ancre) if ancre else "")
        return f'{attr}="{cible}"'
    if chemin in ("/cart", "/search", "/checkout", "/policies/privacy-policy"):
        return f'{attr}="accueil.html" data-demo'
    return m.group(0)


def transformer(html, corps_seul=False):
    html = re.sub(r'<link rel="stylesheet" href="/assets/lou\.css[^"]*"[^>]*>', "<style>" + CSS.replace("\\", "\\\\") + "</style>", html)
    scripts = []
    def garder(m):
        scripts.append(JS[m.group(1)]); return ""
    html = re.sub(r'<script src="/assets/(lou(?:-produit)?\.js)[^"]*" defer></script>', garder, html)
    html = re.sub(r'(?:src|href)="(/(?:local|assets)/[^"]+\.(?:png|webp|jpg))(?:\?[^"]*)?"',
                  lambda m: m.group(0).split("=")[0] + '="' + image(m.group(1)) + '"', html)
    html = re.sub(r'srcset="[^"]*"', "", html)
    html = re.sub(r'(href|data-base|data-produit)="(/[^"]*)"', lien, html)
    html = re.sub(r'"url": "(/products/[^"]+)"', lambda m: '"url": "' + PAGES.get(m.group(1), m.group(1)) + '"', html)
    html = re.sub(r'"image": "(/local/[^"?]+)[^"]*"', lambda m: '"image": "' + image(m.group(1)) + '"', html)
    fin = DEMO + "".join(f"<script>{s}</script>" for s in scripts) + BANDEAU
    html = html.replace("</body>", fin + "</body>")
    html = html.replace('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">', "")
    if corps_seul:
        head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
        head = re.sub(r"<meta charset[^>]*>", "", head)
        body = re.search(r"<body([^>]*)>(.*)</body>", html, re.S)
        classe = re.search(r'class="([^"]*)"', body.group(1))
        html = ('<meta name="claude:viewport-fit-sides" content="cover">\n' + head +
                f'\n<script>document.body.className = {classe.group(1)!r};</script>\n' + body.group(2))
    else:
        html = html.replace("<head>", '<head>\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">', 1)
    return html


for chemin, fichier in PAGES.items():
    html = opener.open(BASE + chemin).read().decode()
    open(os.path.join(OUT, fichier), "w").write(transformer(html))
    if chemin == "/":
        open(os.path.join(OUT, "index.html"), "w").write(transformer(html, corps_seul=True))
    print("✔", fichier)
print(len(images), "images ;", sum(os.path.getsize(os.path.join(OUT, "img", f)) for f in os.listdir(os.path.join(OUT, "img"))) // 1024, "Ko")
