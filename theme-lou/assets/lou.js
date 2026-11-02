/* Les Mots de Lou — scripts communs (menu, panier, aperçu de gravure, machine à mots, test des mots, confettis). */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var LOU = window.LOU || {};
  var reduit = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var euros = function (c) { return (c / 100).toFixed(2).replace(".", ",") + " €"; };

  /* ---------- Phrases (machine à mots, test, suggestions) ---------- */
  var PHRASES = {
    amour: ["Tu es ma personne", "Toi, toujours", "Mon endroit préféré, c'est toi", "Je choisis toi, chaque jour", "Pour toujours et un jour", "Mon plus beau cadeau : toi"],
    amitie: ["Amies pour la vie", "Ma personne préférée", "Merci d'exister", "Ensemble, toujours", "Toi + moi = les meilleures", "Même loin, tout près"],
    famille: ["Ma sœur, mon pilier", "Même sang, même cœur", "Merci pour tout, maman", "Tu es ma maison", "Ma mamie, mon trésor", "Je t'aime gros comme ça"],
    drole: ["Supporte-moi encore 50 ans", "Officiellement ma préférée", "Ma partenaire de bêtises", "Pas de chocolat, mais presque", "Classée n°1, pour toujours", "Toi, en mieux : impossible"],
    courage: ["Tu es plus forte que tu crois", "Un pas après l'autre", "Crois en toi", "Après la pluie, toi", "Je suis capable", "Respire, tu gères"]
  };
  window.LOU_PHRASES = PHRASES;

  /* ---------- Toast, confettis, son ---------- */
  var toastT;
  function toast(msg) {
    var t = $("#toast"); if (!t) return;
    t.textContent = msg; t.classList.add("on");
    clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove("on"); }, 2600);
  }
  function confettis(n) {
    if (reduit) return;
    var c = $("#confetti"); if (!c) return;
    var ctx = c.getContext("2d"), W = c.width = innerWidth, H = c.height = innerHeight;
    var cols = ["#e2457a", "#f6b8cb", "#ffe79a", "#c9eedf", "#e5dcff", "#d6a466"], P = [];
    for (var i = 0; i < (n || 140); i++) P.push({ x: W / 2 + (Math.random() - .5) * 120, y: H * .45, vx: (Math.random() - .5) * 16, vy: -Math.random() * 16 - 4, r: Math.random() * 6 + 4, c: cols[i % cols.length], a: Math.random() * 6, va: (Math.random() - .5) * .4, coeur: Math.random() < .25 });
    var t0 = performance.now();
    (function frame(t) {
      ctx.clearRect(0, 0, W, H);
      P.forEach(function (p) {
        p.vy += .45; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.a += p.va;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = p.c;
        if (p.coeur) { ctx.font = (p.r * 3) + "px serif"; ctx.fillText("♥", -p.r, p.r); } else ctx.fillRect(-p.r / 2, -p.r / 2, p.r, p.r * .6);
        ctx.restore();
      });
      if (t - t0 < 2600) requestAnimationFrame(frame); else ctx.clearRect(0, 0, W, H);
    })(t0);
  }
  window.LOU_confettis = confettis;
  window.LOU_toast = toast;

  /* ---------- Menu mobile ---------- */
  var burger = $("#burger"), mnav = $("#mnav");
  if (burger && mnav) burger.addEventListener("click", function () {
    var o = burger.getAttribute("aria-expanded") !== "true";
    burger.setAttribute("aria-expanded", o); mnav.classList.toggle("open", o);
  });

  /* ---------- Apparitions au défilement ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("vu"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else $$(".rv").forEach(function (el) { el.classList.add("vu"); });

  /* ---------- Favoris (cœurs) ---------- */
  var favs = [];
  try { favs = JSON.parse(localStorage.getItem("lou-favs") || "[]"); } catch (e) {}
  $$(".coeur").forEach(function (b) {
    var h = b.getAttribute("data-handle");
    if (favs.indexOf(h) > -1) b.classList.add("is-on");
    b.addEventListener("click", function (ev) {
      ev.preventDefault(); ev.stopPropagation();
      var on = !b.classList.contains("is-on"); b.classList.toggle("is-on", on);
      favs = favs.filter(function (x) { return x !== h; }); if (on) favs.push(h);
      try { localStorage.setItem("lou-favs", JSON.stringify(favs)); } catch (e) {}
      toast(on ? "Ajouté à vos coups de cœur 💗" : "Retiré de vos coups de cœur");
    });
  });

  /* ---------- Panier ---------- */
  var routes = LOU.routes || { root: "/", cart: "/cart" };
  var root = (routes.root || "/").replace(/\/?$/, "/");
  function ouvrirPanier() { document.body.classList.add("panier-ouvert"); var d = $("#drawer"); if (d) d.setAttribute("aria-hidden", "false"); }
  function fermerPanier() { document.body.classList.remove("panier-ouvert"); var d = $("#drawer"); if (d) d.setAttribute("aria-hidden", "true"); }
  function propsHtml(p) {
    if (!p) return "";
    var out = Object.keys(p).filter(function (k) { return k.charAt(0) !== "_" && p[k]; }).map(function (k) {
      var v = String(p[k]); if (/^https?:\/\//.test(v) || v.indexOf("/uploads/") > -1) v = "photo envoyée ✔";
      return "<li><b>" + esc(k) + " :</b> " + esc(v) + "</li>";
    }).join("");
    return out ? '<ul class="props">' + out + "</ul>" : "";
  }
  function dessinerPanier(c) {
    LOU.cart = c;
    var n = $("#cart-count"); if (n) { n.textContent = c.item_count; n.classList.remove("bump"); void n.offsetWidth; n.classList.add("bump"); }
    var ul = $("#drawer-items"); if (!ul) return;
    if (!c.items.length) {
      ul.innerHTML = '<li class="vide" style="display:block"><span class="emo">💌</span>Votre panier attend encore vos mots…<br><br><a class="btn btn-small" href="' + root + 'collections/all">Voir les bijoux</a></li>';
    } else {
      ul.innerHTML = c.items.map(function (it) {
        var img = it.image ? it.image + (it.image.indexOf("?") > -1 ? "&" : "?") + "width=160" : "";
        var prix = it.final_line_price < it.original_line_price ? '<s class="small">' + euros(it.original_line_price) + "</s> " + euros(it.final_line_price) : euros(it.final_line_price);
        return '<li><img src="' + esc(img) + '" alt="" width="72" height="72" loading="lazy"><div><div class="t">' + esc(it.product_title) + "</div>" +
          (it.variant_title ? '<div class="small">' + esc(it.variant_title) + "</div>" : "") + propsHtml(it.properties) +
          '<div class="ligne-bas"><span class="qte"><button data-k="' + esc(it.key) + '" data-q="' + (it.quantity - 1) + '" aria-label="Retirer un">−</button><span>' + it.quantity + '</span><button data-k="' + esc(it.key) + '" data-q="' + (it.quantity + 1) + '" aria-label="Ajouter un">+</button></span><b class="prix">' + prix + "</b></div></div></li>";
      }).join("");
    }
    var tot = $("#drawer-total"); if (tot) tot.textContent = euros(c.total_price);
    var rem = $("#drawer-discount");
    if (rem) { rem.hidden = !c.total_discount; if (c.total_discount) rem.lastElementChild.textContent = "− " + euros(c.total_discount); }
    var duo = $("#duo");
    if (duo) duo.textContent = !c.item_count ? "" : c.item_count === 1 ? "🎁 Ajoutez un 2e bijou : il est à -50 % !" : "🎉 Offre « 2e bijou à -50 % » : appliquée au moins cher.";
  }
  function chargerPanier() { return fetch(root + "cart.js", { headers: { Accept: "application/json" } }).then(function (r) { return r.json(); }).then(dessinerPanier); }
  window.LOU_ajouter = function (formData) {
    return fetch(root + "cart/add.js", { method: "POST", body: formData, headers: { Accept: "application/json" } })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.description || j.message || "Erreur"); return j; }); })
      .then(function () { return chargerPanier(); })
      .then(function () { ouvrirPanier(); confettis(90); });
  };
  document.addEventListener("click", function (e) {
    var q = e.target.closest && e.target.closest(".qte button");
    if (q) {
      fetch(root + "cart/change.js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: q.getAttribute("data-k"), quantity: +q.getAttribute("data-q") }) })
        .then(function (r) { return r.json(); }).then(dessinerPanier);
    }
  });
  var cb = $("#cart-btn"); if (cb) cb.addEventListener("click", function () { chargerPanier(); ouvrirPanier(); });
  var dc = $("#drawer-close"); if (dc) dc.addEventListener("click", fermerPanier);
  var dbg = $("#drawer-bg"); if (dbg) dbg.addEventListener("click", fermerPanier);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") fermerPanier(); });
  if (LOU.cart && LOU.cart.items) dessinerPanier(LOU.cart);

  /* ---------- Aperçu de gravure (jonc) — partagé accueil + fiche ---------- */
  var FINITIONS = { "Argentée": ["#fbfbfd", "#b9bcc6", "#eef0f4", "#8d909b"], "Dorée": ["#fff4d6", "#d7a647", "#f8e3a8", "#a87a2a"], "Rosée": ["#ffe9e4", "#d99a8c", "#f7d3ca", "#a8695c"] };
  var uid = 0;
  window.LOU_jonc = function (el, texte, police, finition) {
    var f = FINITIONS[finition] || FINITIONS["Argentée"], id = "j" + (++uid);
    var t = esc(texte || "Vos mots ici");
    el.innerHTML = '<svg class="jonc-svg" viewBox="0 0 520 280" role="img" aria-label="Aperçu de la gravure : ' + t + '">' +
      '<defs><linearGradient id="' + id + 'g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + f[0] + '"/><stop offset=".45" stop-color="' + f[1] + '"/><stop offset=".7" stop-color="' + f[2] + '"/><stop offset="1" stop-color="' + f[3] + '"/></linearGradient>' +
      '<path id="' + id + 'p" d="M34,128 A226,96 0 0,0 486,128"/></defs>' +
      '<ellipse cx="260" cy="248" rx="200" ry="18" fill="rgba(198,47,99,.12)"/>' +
      '<path d="M268,32 A226,96 0 0,1 486,128" fill="none" stroke="' + f[3] + '" stroke-opacity=".55" stroke-width="30" stroke-linecap="round"/>' +
      '<path d="M252,32 A226,96 0 0,0 34,128" fill="none" stroke="' + f[3] + '" stroke-opacity=".55" stroke-width="30" stroke-linecap="round"/>' +
      '<path d="M34,128 A226,96 0 0,0 486,128" fill="none" stroke="url(#' + id + 'g)" stroke-width="46" stroke-linecap="round"/>' +
      '<path d="M60,150 A220,86 0 0,0 460,150" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="3"/>' +
      '<text class="grave ' + (police || "manuscrite").toLowerCase() + '" fill="rgba(40,22,30,.72)" stroke="rgba(255,255,255,.35)" stroke-width=".6" dominant-baseline="middle" text-anchor="middle"><textPath href="#' + id + 'p" startOffset="50%">' + t + "</textPath></text>" +
      "</svg>";
  };

  /* ---------- Gravure sur la photo du jonc (accueil) ----------
     Bords de la face avant mesurés sur assets/jonc-vierge.webp (repère 920×460, un point tous les 10 px à partir de x=100).
     Le texte est écrit à plat sur une bande « déroulée », puis replié colonne par colonne entre le bord haut et le bord bas
     de la face (les verticales restent verticales, comme sur un cylindre) ; il se resserre vers les côtés (x = cx + a·sin θ).
     Si on change la photo : re-mesurer haut/bas/cx/a (méthode dans docs/journal.md, 02/11/2026). */
  var JONC = {
    x0: 100, pas: 10, cx: 450, a: 410, xg: 125, xd: 800, zone: 0.78, ecrase: 0.85,
    haut: [281.6,286.6,291.3,295.7,299.7,303.5,307.0,310.3,313.3,316.1,318.6,321.0,323.1,325.1,326.8,328.4,329.9,331.2,332.3,333.4,334.2,335.0,335.7,336.2,336.6,337.0,337.2,337.4,337.5,337.5,337.4,337.3,337.1,336.8,336.4,336.0,335.5,335.0,334.4,333.7,333.0,332.1,331.3,330.3,329.3,328.2,327.0,325.8,324.4,323.0,321.5,319.8,318.1,316.2,314.3,312.2,309.9,307.5,305.0,302.3,299.4,296.4,293.2,289.7,286.1,282.2,278.1,273.8,269.1,264.3,259.1,253.6,247.9,241.8],
    bas: [327.1,332.4,337.5,342.2,346.6,350.7,354.5,358.1,361.4,364.4,367.2,369.8,372.2,374.4,376.4,378.3,379.9,381.4,382.7,383.9,385.0,385.9,386.7,387.4,387.9,388.4,388.7,389.0,389.1,389.2,389.2,389.1,388.9,388.6,388.3,387.8,387.3,386.8,386.1,385.4,384.6,383.7,382.8,381.8,380.6,379.4,378.1,376.8,375.3,373.7,372.0,370.2,368.3,366.3,364.1,361.8,359.4,356.8,354.1,351.1,348.1,344.8,341.3,337.6,333.8,329.6,325.3,320.7,315.8,310.7,305.2,299.5,293.5,287.1]
  };
  var bordJonc = function (t, x) {
    var k = (x - JONC.x0) / JONC.pas, i = Math.max(0, Math.min(t.length - 2, Math.floor(k))), f = k - i;
    return t[i] + (t[i + 1] - t[i]) * f;
  };
  var calque = function (w, h) { var c = document.createElement("canvas"); c.width = w; c.height = h; return c; };
  var teinter = function (src, couleur) {
    var c = calque(src.width, src.height), x = c.getContext("2d");
    x.drawImage(src, 0, 0); x.globalCompositeOperation = "source-in"; x.fillStyle = couleur; x.fillRect(0, 0, c.width, c.height);
    return c;
  };
  window.LOU_graverJonc = function (canvas, img, texte) {
    var W = canvas.clientWidth, H = canvas.clientHeight;
    if (!W || !H || !img.complete || !img.naturalWidth) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2.5);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    var s = canvas.width / 920, ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    if (!texte) return;
    var J = JONC, thG = Math.asin((J.xg - J.cx) / J.a), thD = Math.asin((J.xd - J.cx) / J.a), dTh = thD - thG;
    // 1. Bande déroulée (sur-échantillonnée ×2)
    var hFace = 52, SH = Math.ceil(hFace * J.zone / J.ecrase * s * 2), SW = Math.ceil(J.a * dTh * s * 2);
    var bande = calque(SW, SH), b = bande.getContext("2d"), police = '"Great Vibes", cursive';
    b.font = "100px " + police;
    var m = b.measureText(texte), ref = b.measureText("Tu es ma personne");
    var asc = Math.max(m.actualBoundingBoxAscent || 80, ref.actualBoundingBoxAscent || 80);
    var desc = Math.max(m.actualBoundingBoxDescent || 30, ref.actualBoundingBoxDescent || 30);
    var gauche = m.actualBoundingBoxLeft, droite = m.actualBoundingBoxRight;
    var encre = (gauche != null && droite != null) ? gauche + droite : m.width;
    var k = Math.min(SH * 0.96 / (asc + desc), SW * 0.94 / encre);   // l'encre tient toujours dans la bande
    b.font = (100 * k).toFixed(2) + "px " + police;
    b.textAlign = "left"; b.fillStyle = "#000";   // mesures faites en alignement « start » : on centre l'encre à la main
    b.fillText(texte, SW / 2 - encre * k / 2 + (gauche || 0) * k, SH / 2 + (asc - desc) / 2 * k);
    // 2. Repli colonne par colonne sur la face avant, avec découpe à la forme exacte de la face
    var masque = calque(canvas.width, canvas.height), mc = masque.getContext("2d"), x, X;
    mc.beginPath();
    for (x = J.xg - 15; x <= J.xd + 15; x += 5) mc.lineTo(x * s, (bordJonc(J.haut, x) + 1.5) * s);
    for (x = J.xd + 15; x >= J.xg - 15; x -= 5) mc.lineTo(x * s, (bordJonc(J.bas, x) - 1.5) * s);
    mc.closePath(); mc.clip();
    for (X = Math.floor(J.xg * s); X <= Math.ceil(J.xd * s); X++) {
      x = X / s;
      var th = Math.asin(Math.max(-1, Math.min(1, (x - J.cx) / J.a)));
      var u = (th - thG) / dTh;
      if (u < 0 || u > 1) continue;
      var srcL = Math.max(1, SW / (J.a * Math.cos(th) * dTh * s));      // largeur de bande vue par 1 px d'écran
      var hb = bordJonc(J.haut, x), bb = bordJonc(J.bas, x), h = bb - hb;
      mc.drawImage(bande, Math.max(0, Math.min(SW - srcL, u * SW - srcL / 2)), 0, srcL, SH, X, (hb + h * (1 - J.zone) / 2) * s, 1, h * J.zone * s);
    }
    // 3. Incrustation dans le métal : reflet clair sous le trait (bord du sillon), puis creux sombre (multiplié = suit les reflets)
    var flou = "blur(" + (0.35 * dpr).toFixed(2) + "px)", dy = Math.max(1, 0.9 * s);
    ctx.save();
    if ("filter" in ctx) ctx.filter = flou;
    ctx.globalCompositeOperation = "screen"; ctx.globalAlpha = 0.55; ctx.drawImage(teinter(masque, "#ffffff"), 0, dy);
    ctx.globalCompositeOperation = "multiply"; ctx.globalAlpha = 0.9; ctx.drawImage(teinter(masque, "#55494f"), 0, 0);
    ctx.globalAlpha = 0.35; ctx.drawImage(teinter(masque, "#3a3034"), 0, -dy * 0.5);
    ctx.restore();
  };

  /* ---------- Accueil : atelier (on tape, ça se grave) ---------- */
  var atelier = $("#atelier-texte");
  if (atelier) {
    var lien = $("#atelier-lien"), toile = $("#atelier-gravure"), photo = $("#atelier-apercu img");
    var maj = function () {
      var v = atelier.value.slice(0, 30);
      if (toile && photo && toile.getContext) window.LOU_graverJonc(toile, photo, v || "Tu es ma personne");
      if (lien) lien.href = lien.getAttribute("data-base") + (v ? "?texte=" + encodeURIComponent(v) : "");
    };
    if (photo && !photo.complete) photo.addEventListener("load", function () { maj(); });
    var attente; window.addEventListener("resize", function () { clearTimeout(attente); attente = setTimeout(maj, 120); });
    if (document.fonts && document.fonts.load) document.fonts.load('40px "Great Vibes"').then(function () { maj(); });
    atelier.addEventListener("input", maj); maj();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(maj);  // re-mesure avec la vraie police
    // Démo : le texte s'écrit tout seul tant qu'on n'a pas touché au champ
    if (!reduit) {
      var demo = ["Tu es ma personne", "Sœurs pour toujours", "Merci maman", "Toi, toujours"], di = 0, ci = 0, touche = false;
      atelier.addEventListener("focus", function () { touche = true; });
      (function tape() {
        if (touche) return;
        var mot = demo[di % demo.length];
        if (ci <= mot.length) { atelier.value = mot.slice(0, ci++); maj(); setTimeout(tape, 85); }
        else { setTimeout(function () { ci = 0; di++; tape(); }, 1800); }
      })();
    }
  }

  /* ---------- Machine à mots ---------- */
  var machine = $("#machine");
  if (machine) {
    var phrase = $(".machine-phrase", machine), cat = "amour", base = machine.getAttribute("data-produit") || (root + "products/jonc-mes-mots");
    var graver = $("#machine-graver");
    $$(".machine-cats .chip", machine).forEach(function (c) {
      c.addEventListener("click", function () {
        $$(".machine-cats .chip", machine).forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-pressed", "false"); });
        c.classList.add("is-on"); c.setAttribute("aria-pressed", "true"); cat = c.getAttribute("data-cat"); tirer();
      });
    });
    var tirer = function () {
      var liste = PHRASES[cat], finale = liste[Math.floor(Math.random() * liste.length)];
      if (finale === phrase.textContent) finale = liste[(liste.indexOf(finale) + 1) % liste.length];
      if (reduit) { phrase.textContent = finale; return fin(finale); }
      phrase.classList.add("roule"); var n = 0;
      var it = setInterval(function () {
        phrase.textContent = liste[n++ % liste.length];
        if (n > 12) { clearInterval(it); phrase.classList.remove("roule"); phrase.textContent = finale; fin(finale); }
      }, 70);
    };
    var fin = function (p) { if (graver) graver.href = base + "?texte=" + encodeURIComponent(p); };
    var bt = $("#machine-tirer"); if (bt) bt.addEventListener("click", tirer);
    var cp = $("#machine-copier");
    if (cp) cp.addEventListener("click", function () {
      var txt = phrase.textContent;
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Phrase copiée ✂️"); }, function () { toast(txt); }); else toast(txt);
    });
    fin(phrase.textContent);
  }

  /* ---------- Le test des mots ---------- */
  var test = $("#test-mots");
  if (test) {
    var Q = [
      { q: "Pour qui, ce petit bijou ?", k: "qui", c: [["amie", "👯‍♀️", "Ma meilleure amie"], ["soeur", "👭", "Ma sœur"], ["maman", "🌷", "Ma maman"], ["amour", "💞", "Mon amour"], ["mamie", "🧶", "Ma mamie"], ["moi", "✨", "Moi !", "je le mérite"]] },
      { q: "Pour quelle occasion ?", k: "quand", c: [["noel", "🎄", "Noël"], ["anniv", "🎂", "Un anniversaire"], ["rien", "💌", "Juste comme ça"], ["pardon", "🙈", "Me faire pardonner"], ["naissance", "👶", "Une naissance"], ["courage", "🌈", "Lui donner du courage"]] },
      { q: "Son style, c'est plutôt…", k: "style", c: [["Argentée", "🤍", "Discrète", "tout en finesse"], ["Dorée", "🌾", "Bohème", "chaleureuse"], ["Rosée", "💄", "Glamour", "elle brille"], ["Argentée", "👟", "Sportive", "jamais sans"]] },
      { q: "Et vous avez envie de lui dire…", k: "quoi", c: [["jonc-mes-mots", "💬", "Une phrase", "qui vient du cœur"], ["collier-prenom", "🔤", "Un prénom", "le sien ou un être cher"], ["collier-souvenir-photo", "📸", "Un souvenir", "en photo cachée"], ["bracelet-code-secret", "🤫", "Un mot secret", "en code Morse"]] }
    ];
    var REACT = { amie: "Une meilleure amie ! Le genre de personne qu'on garde pour la vie 🥹", soeur: "Une sœur… attention, ça va piquer les yeux 😭", maman: "Pour maman ? Prévoyez les mouchoirs 🌷", amour: "Ohhh, de l'amour ! J'adore ça 💞", mamie: "Une mamie ! Elle va le montrer à tout le quartier 🧶", moi: "Bravo. On n'est jamais mieux servie que par soi-même ✨",
      noel: "Noël ! Il reste le temps, mais pas trop 🎄", anniv: "Joyeux anniversaire en avance 🎂", rien: "Les cadeaux sans raison sont les meilleurs 💌", pardon: "Oups… on va arranger ça 🙈", naissance: "Bienvenue au petit cœur 👶", courage: "On va lui envoyer de la force 🌈" };
    var PAR_QUI = { amie: PHRASES.amitie, soeur: ["Ma sœur, mon pilier", "Même sang, même cœur", "Sœurs pour toujours", "Ma première amie"], maman: ["Merci pour tout, maman", "Ma maman, mon repère", "Tu es ma maison", "Je t'aime gros comme ça"], amour: PHRASES.amour, mamie: ["Ma mamie, mon trésor", "Mamie d'amour", "Tes mots me guident"], moi: ["Je suis capable", "Un pas après l'autre", "Crois en toi", "Ma vie, mes règles"] };
    var PAR_QUAND = { noel: ["Mon plus beau cadeau : toi"], anniv: ["Un an de plus, et toujours toi"], pardon: ["Pardon, je t'aime", "On recommence ?"], naissance: ["Bienvenue petit cœur"], courage: ["Tu es plus forte que tu crois", "Respire, tu gères"], rien: ["Juste parce que je t'aime"] };
    var MORSE = { amie: "AMIES", soeur: "SOEURS", maman: "MAMAN", amour: "JETAIME", mamie: "MAMIE", moi: "COURAGE" };
    var PRODUITS = {};
    try { PRODUITS = JSON.parse(($("#test-produits") || {}).textContent || "{}"); } catch (e) {}
    var rep = {}, etape = 0, zone = $(".test-zone", test), bulle = $(".bulle", test), prog = $(".test-prog i", test);
    var bulleBase = bulle ? bulle.textContent : "";
    var poser = function () {
      prog.style.width = (etape / Q.length * 100) + "%";
      if (etape >= Q.length) return resultat();
      var q = Q[etape];
      zone.innerHTML = '<div class="test-q"><h3>' + esc(q.q) + '</h3><div class="test-choix">' + q.c.map(function (c, i) {
        return '<button class="choix" data-i="' + i + '"><span class="emo" aria-hidden="true">' + c[1] + "</span>" + esc(c[2]) + (c[3] ? "<small>" + esc(c[3]) + "</small>" : "") + "</button>";
      }).join("") + "</div>" + (etape ? '<button class="test-retour" type="button">← Question précédente</button>' : "") + "</div>";
      $$(".choix", zone).forEach(function (b) {
        b.addEventListener("click", function () {
          var c = q.c[+b.getAttribute("data-i")]; rep[q.k] = c[0]; b.classList.add("is-on");
          if (bulle && REACT[c[0]]) bulle.textContent = REACT[c[0]];
          setTimeout(function () { etape++; poser(); }, 380);
        });
      });
      var r = $(".test-retour", zone); if (r) r.addEventListener("click", function () { etape--; poser(); });
    };
    var resultat = function () {
      var h = rep.quoi, p = PRODUITS[h] || {}, fin = rep.style || "Argentée";
      var liste = (PAR_QUAND[rep.quand] || []).concat(PAR_QUI[rep.qui] || PHRASES.amitie).filter(function (x, i, a) { return a.indexOf(x) === i && x.length <= 30; }).slice(0, 3);
      if (h === "bracelet-code-secret") liste = [MORSE[rep.qui] || "TOUJOURS", "TOUJOURS", "NOUS"].filter(function (x, i, a) { return a.indexOf(x) === i; });
      var url = (p.url || root + "products/" + h) + "?finition=" + encodeURIComponent(fin);
      var phrasesHtml = h === "collier-prenom" || h === "collier-souvenir-photo" ? "" :
        '<p class="hand">Et voici les mots que je vous propose :</p><div class="phrases">' + liste.map(function (ph) {
          return '<a class="phrase-choix" href="' + esc(url + "&texte=" + encodeURIComponent(ph)) + '">' + esc(ph) + '<span class="go">Graver ça →</span></a>';
        }).join("") + "</div>";
      if (bulle) bulle.textContent = "Tadaaa ! J'ai trouvé 🎉";
      zone.innerHTML = '<div class="resultat"><h3>Votre bijou idéal</h3><div class="resultat-produit">' + (p.image ? '<img src="' + esc(p.image) + '" alt="" width="110" height="110">' : "<span></span>") +
        "<div><b>" + esc(p.title || "Votre bijou") + '</b><br><span class="small">Finition ' + esc(fin.toLowerCase()) + "</span><br><span class=\"prix\">" + esc(p.price || "") + "</span></div></div>" + phrasesHtml +
        '<div class="hero-cta"><a class="btn" href="' + esc(url) + '">Je le personnalise</a><button class="btn ghost" type="button" id="test-again">Recommencer</button></div></div>';
      $("#test-again").addEventListener("click", function () { rep = {}; etape = 0; if (bulle) bulle.textContent = bulleBase; poser(); });
      confettis(160);
    };
    poser();
  }
})();
