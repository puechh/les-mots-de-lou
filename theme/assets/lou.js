/* Les Mots de Lou — scripts communs (v0.2, 02/11/2026).
   Lou (avatar de la boutique) parle à la cliente : bulles, assistante, panier commenté. Gravure réaliste sur photo,
   machine à mots, test des mots, cartes qui se retournent, compte à rebours de Noël, sons et confettis. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var LOU = window.LOU = window.LOU || {};
  var R = LOU.reglages || { livMin: 5, livMax: 10, noel: "2026-12-10", noelTexte: "10 décembre", sons: true };
  var reduit = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var euros = function (c) { return (c / 100).toFixed(2).replace(".", ",") + " €"; };
  var stocke = function (k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } };
  var routes = LOU.routes || { root: "/", cart: "/cart" };
  var root = (routes.root || "/").replace(/\/?$/, "/");

  /* ---------- Phrases (machine à mots, test, idées de Lou) ---------- */
  var PHRASES = {
    amour: ["Tu es ma personne", "Toi, toujours", "Je choisis toi", "Pour toujours", "Mon plus beau cadeau", "Toi et moi"],
    amitie: ["Amies pour la vie", "Ma personne préférée", "Merci d'exister", "Ensemble, toujours", "Même loin, tout près", "Ma binôme de vie"],
    famille: ["Ma sœur, mon pilier", "Même sang, même cœur", "Merci maman", "Tu es ma maison", "Ma mamie d'amour", "Je t'aime gros"],
    drole: ["Supporte-moi encore", "La best, c'est toi", "Duo de choc", "Classée n°1", "Toi, en mieux ? Non", "Toi, ma préférée"],
    courage: ["Plus forte que tout", "Un pas après l'autre", "Crois en toi", "Respire, tu gères", "Je suis capable", "Après la pluie, toi"]
  };
  LOU.PHRASES = window.LOU_PHRASES = PHRASES;
  // Mots secrets (bracelet Morse) : A à Z, 8 lettres maximum
  var MOTS = {
    amour: ["JETAIME", "AMOUR", "TOUJOURS", "MONCOEUR", "TOIETMOI"],
    amitie: ["AMIES", "BFF", "COMPLICE", "BINOME", "TOUJOURS"],
    famille: ["MAMAN", "PAPA", "SOEURS", "FAMILLE", "MAMIE"],
    drole: ["BISOUS", "CHOUPI", "LOVE", "BIBOU", "PIPELET"],
    courage: ["COURAGE", "FORCE", "CROIS", "FONCE", "LIBRE"]
  };
  LOU.idee = function () { var t = Object.keys(PHRASES), l = PHRASES[t[Math.floor(Math.random() * t.length)]]; return l[Math.floor(Math.random() * l.length)]; };

  /* ---------- Sons doux (créés par le navigateur, aucun fichier) ---------- */
  var actx = null;
  function son(type) {
    if (R.sons === false || reduit) return;
    try {
      actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      if (actx.state === "suspended") actx.resume();
      var notes = type === "ding" ? [784, 988, 1319] : type === "tada" ? [659, 784, 988, 1319] : type === "clic" ? [1200] : [660, 990];
      notes.forEach(function (f, i) {
        var o = actx.createOscillator(), g = actx.createGain(), t = actx.currentTime + i * (type === "clic" ? 0 : .09);
        o.type = "sine"; o.frequency.value = f; g.gain.setValueAtTime(0, t);
        g.gain.linearRampToValueAtTime(type === "clic" ? .03 : .07, t + .015); g.gain.exponentialRampToValueAtTime(.0001, t + (type === "clic" ? .06 : .32));
        o.connect(g); g.connect(actx.destination); o.start(t); o.stop(t + .4);
      });
    } catch (e) {}
  }
  LOU.son = son;

  /* ---------- Toast, confettis, cœurs ---------- */
  var toastT;
  function toast(msg) {
    var t = $("#toast"); if (!t) return;
    t.textContent = msg; t.classList.add("on");
    clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove("on"); }, 2600);
  }
  function confettis(n, x, y) {
    if (reduit) return;
    var c = $("#confetti"); if (!c) return;
    var ctx = c.getContext("2d"), W = c.width = innerWidth, H = c.height = innerHeight;
    var ox = x == null ? W / 2 : x, oy = y == null ? H * .45 : y;
    var cols = ["#e2457a", "#f6b8cb", "#ffe79a", "#c9eedf", "#e5dcff", "#d6a466"], P = [];
    for (var i = 0; i < (n || 140); i++) P.push({ x: ox + (Math.random() - .5) * 60, y: oy, vx: (Math.random() - .5) * 16, vy: -Math.random() * 15 - 4, r: Math.random() * 6 + 4, c: cols[i % cols.length], a: Math.random() * 6, va: (Math.random() - .5) * .4, coeur: Math.random() < .3 });
    var t0 = performance.now();
    (function frame(t) {
      ctx.clearRect(0, 0, W, H);
      P.forEach(function (p) {
        p.vy += .42; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.a += p.va;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.fillStyle = p.c;
        if (p.coeur) { ctx.font = (p.r * 3) + "px serif"; ctx.fillText("♥", -p.r, p.r); } else ctx.fillRect(-p.r / 2, -p.r / 2, p.r, p.r * .6);
        ctx.restore();
      });
      if (t - t0 < 2600) requestAnimationFrame(frame); else ctx.clearRect(0, 0, W, H);
    })(t0);
  }
  function coeurs(el) {
    if (reduit || !el) return;
    var b = el.getBoundingClientRect();
    for (var i = 0; i < 9; i++) {
      var h = document.createElement("span"); h.className = "mini-coeur"; h.textContent = "♥";
      h.style.left = (b.left + b.width / 2 - 8) + "px"; h.style.top = (b.top + b.height / 2 - 10) + "px"; document.body.appendChild(h);
      var a = (i / 9) * Math.PI * 2, d = 34 + Math.random() * 26;
      h.animate([{ transform: "translate(0,0) scale(.4)", opacity: 1 }, { transform: "translate(" + Math.cos(a) * d + "px," + (Math.sin(a) * d - 14) + "px) scale(" + (.7 + Math.random() * .7) + ") rotate(" + (Math.random() * 60 - 30) + "deg)", opacity: 0 }], { duration: 750, easing: "cubic-bezier(.2,.8,.3,1)" }).onfinish = (function (x) { return function () { x.remove(); }; })(h);
    }
  }
  LOU.confettis = window.LOU_confettis = confettis;
  LOU.toast = window.LOU_toast = toast;
  LOU.coeurs = coeurs;

  /* ---------- Dates : livraison estimée, compte à rebours de Noël ---------- */
  function ajouterJours(d, n, ouvres) {
    var x = new Date(d);
    while (n > 0) { x.setDate(x.getDate() + 1); if (!ouvres || (x.getDay() !== 0 && x.getDay() !== 6)) n--; }
    return x;
  }
  var fmt = function (d) { return d.toLocaleDateString("fr-FR", { day: "numeric", month: "long" }); };
  LOU.estimation = function () {
    var now = new Date();
    var a = ajouterJours(now, R.livMin), b = ajouterJours(now, R.livMax);   // délai total, fabrication comprise
    return "entre le " + fmt(a) + " et le " + fmt(b);
  };
  function joursNoel() {
    var lim = new Date((R.noel || "2026-12-10") + "T23:59:59");
    return Math.ceil((lim - new Date()) / 864e5);
  }
  LOU.joursNoel = joursNoel;
  $$(".j-noel").forEach(function (e) { var j = joursNoel(); e.textContent = j > 0 ? "(J-" + j + ")" : ""; });

  /* ---------- Bandeau : un message à la fois sur téléphone ---------- */
  var ann = $$(".announce-track span");
  if (ann.length && matchMedia("(max-width: 899px)").matches) {
    var na = ann.length / 2, ia = 0; ann[0].classList.add("on");
    setInterval(function () { ann[ia].classList.remove("on"); ia = (ia + 1) % na; ann[ia].classList.add("on"); }, 3600);
  }

  /* ---------- En-tête flottant ---------- */
  var header = $("#header");
  if (header) {
    var flotte = function () { header.classList.toggle("flotte", scrollY > 40); };
    addEventListener("scroll", flotte, { passive: true }); flotte();
  }

  /* ---------- Menu mobile ---------- */
  var burger = $("#burger"), mnav = $("#mnav");
  if (burger && mnav) burger.addEventListener("click", function () {
    var o = burger.getAttribute("aria-expanded") !== "true";
    burger.setAttribute("aria-expanded", o); mnav.classList.toggle("open", o); son("clic");
  });

  /* ---------- Apparitions au défilement (si GSAP n'est pas là) ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("vu"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    $$(".rv, .trait").forEach(function (el) { io.observe(el); });
  } else $$(".rv, .trait").forEach(function (el) { el.classList.add("vu"); });

  /* ---------- Lou écrit (effet machine à écrire dans une bulle) ---------- */
  LOU.ecrire = function (el, texte, vitesse, fin) {
    if (!el) return;
    if (reduit) { el.textContent = texte; if (fin) fin(); return; }
    var i = 0; el.classList.add("curseur"); el.textContent = "";
    (function pas() {
      el.textContent = texte.slice(0, ++i);
      if (i < texte.length) setTimeout(pas, (vitesse || 24) + (/[.,!?…]/.test(texte[i - 1]) ? 160 : 0));
      else { el.classList.remove("curseur"); if (fin) fin(); }
    })();
  };

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
      if (on) { coeurs(b); son("pop"); }
      if (LOU.dit) LOU.dit(on ? "Ajouté à vos coups de cœur 💗 Bon goût, je note !" : "Retiré de vos coups de cœur… je ne dirai rien 🤐", 3200);
    });
  });

  /* ---------- Panier ---------- */
  var DUO = [];
  try { DUO = JSON.parse(($("#duo-produits") || {}).textContent || "[]"); } catch (e) {}
  function ouvrirPanier() { document.body.classList.add("panier-ouvert"); var d = $("#drawer"); if (d) d.setAttribute("aria-hidden", "false"); }
  function fermerPanier() { document.body.classList.remove("panier-ouvert"); var d = $("#drawer"); if (d) d.setAttribute("aria-hidden", "true"); }
  LOU.ouvrirPanier = ouvrirPanier;
  function propsHtml(p) {
    if (!p) return "";
    var out = Object.keys(p).filter(function (k) { return k.charAt(0) !== "_" && p[k]; }).map(function (k) {
      var v = String(p[k]); if (/^https?:\/\//.test(v) || v.indexOf("/uploads/") > -1) v = "photo envoyée ✔";
      return "<li><b>" + esc(k) + " :</b> " + esc(v) + "</li>";
    }).join("");
    return out ? '<ul class="props">' + out + "</ul>" : "";
  }
  var dejaDuo = false;
  function dessinerPanier(c) {
    LOU.cart = c;
    var n = $("#cart-count"); if (n) { n.textContent = c.item_count; n.classList.remove("bump"); void n.offsetWidth; n.classList.add("bump"); }
    var ul = $("#drawer-items"); if (!ul) return;
    var duo = $("#duo"), jauge = $("#jauge");
    if (!c.items.length) {
      ul.innerHTML = '<li class="vide" style="display:block;background:none"><span class="emo">💌</span>Rien pour l\'instant…<br><br><a class="btn btn-small" href="' + root + 'collections/all">Voir les bijoux</a></li>';
    } else {
      ul.innerHTML = c.items.map(function (it) {
        var img = it.image ? it.image + (it.image.indexOf("?") > -1 ? "&" : "?") + "width=300" : "";
        var prix = it.final_line_price < it.original_line_price ? '<s class="small">' + euros(it.original_line_price) + "</s> " + euros(it.final_line_price) : euros(it.final_line_price);
        return '<li><img src="' + esc(img) + '" alt="" width="76" height="76" loading="lazy"><div><div class="t">' + esc(it.product_title) + "</div>" +
          (it.variant_title ? '<div class="small">' + esc(it.variant_title) + "</div>" : "") + propsHtml(it.properties) +
          '<div class="ligne-bas"><span class="qte"><button data-k="' + esc(it.key) + '" data-q="' + (it.quantity - 1) + '" aria-label="Retirer un">−</button><span>' + it.quantity + '</span><button data-k="' + esc(it.key) + '" data-q="' + (it.quantity + 1) + '" aria-label="Ajouter un">+</button></span><b class="prix">' + prix + "</b></div></div></li>";
      }).join("");
      if (c.item_count === 1) {
        var dans = c.items.map(function (i) { return i.handle; });
        var autre = DUO.filter(function (p) { return dans.indexOf(p.handle) < 0; })[0];
        if (autre) ul.innerHTML += '<li style="display:block;background:none;padding:0"><a class="suggestion-duo" href="' + esc(autre.url) + '"><img src="' + esc(autre.image) + '" alt="" width="56" height="56" loading="lazy"><span><b>' + esc(autre.title) + '</b><span class="small">' + euros(autre.price / 2) + " au lieu de " + euros(autre.price) + '</span></span><span class="go">-50 % →</span></a></li>';
      }
    }
    var tot = $("#drawer-total"); if (tot) tot.textContent = euros(c.total_price);
    var rem = $("#drawer-discount");
    if (rem) { rem.hidden = !c.total_discount; if (c.total_discount) rem.lastElementChild.textContent = "− " + euros(c.total_discount); }
    var es = $("#drawer-estim"); if (es) es.textContent = c.item_count ? "🚚 Livraison estimée " + LOU.estimation() : "";
    if (duo) duo.textContent = !c.item_count ? "Votre panier attend encore vos mots… Je vous aide ? Le test ne prend que 30 secondes 💌" :
      c.item_count === 1 ? "Super choix 💗 Ajoutez un 2e bijou : il est à -50 %, automatiquement !" :
      "🎉 Offre débloquée ! Le 2e bijou est à -50 % (appliqué au moins cher). Relisez bien vos mots avant de commander ✍️";
    if (jauge) jauge.style.width = Math.min(100, c.item_count * 50) + "%";
    if (c.item_count >= 2 && !dejaDuo && document.body.classList.contains("panier-ouvert")) { dejaDuo = true; setTimeout(function () { confettis(120); son("tada"); }, 400); }
    if (c.item_count >= 2) dejaDuo = true;
  }
  function chargerPanier() { return fetch(root + "cart.js", { headers: { Accept: "application/json" } }).then(function (r) { return r.json(); }).then(dessinerPanier); }
  function vol(src) {
    var cible = $("#cart-btn"); if (!src || !cible || reduit) return Promise.resolve();
    var a = src.getBoundingClientRect(), b = cible.getBoundingClientRect();
    if (!a.width) return Promise.resolve();
    var im = document.createElement(src.tagName === "CANVAS" ? "canvas" : "img"); im.className = "vol";
    if (src.tagName === "CANVAS") { im.width = src.width; im.height = src.height; im.getContext("2d").drawImage(src, 0, 0); } else im.src = src.currentSrc || src.src;
    var t = Math.min(a.width, 260), h = a.height * t / a.width;
    im.style.cssText = "left:" + (a.left + (a.width - t) / 2) + "px;top:" + (a.top + (a.height - h) / 2) + "px;width:" + t + "px;height:" + h + "px";
    document.body.appendChild(im);
    var dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
    return new Promise(function (ok) {
      var an = im.animate([{ transform: "translate(0,0) scale(1) rotate(0)", opacity: 1, borderRadius: "16px" },
        { transform: "translate(" + dx * .5 + "px," + (dy * .5 - 80) + "px) scale(.55) rotate(-12deg)", opacity: 1, offset: .55 },
        { transform: "translate(" + dx + "px," + dy + "px) scale(.08) rotate(20deg)", opacity: .4, borderRadius: "50%" }], { duration: 850, easing: "cubic-bezier(.5,0,.3,1)" });
      an.onfinish = function () { im.remove(); ok(); };
    });
  }
  LOU.ajouter = window.LOU_ajouter = function (formData, source) {
    return fetch(root + "cart/add.js", { method: "POST", body: formData, headers: { Accept: "application/json" } })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.description || j.message || "Erreur"); return j; }); })
      .then(function () { son("ding"); return vol(source); })
      .then(function () { return chargerPanier(); })
      .then(function () { ouvrirPanier(); confettis(90); });
  };
  document.addEventListener("click", function (e) {
    var q = e.target.closest && e.target.closest(".qte button");
    if (q) {
      son("clic");
      fetch(root + "cart/change.js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: q.getAttribute("data-k"), quantity: +q.getAttribute("data-q") }) })
        .then(function (r) { return r.json(); }).then(dessinerPanier);
    }
  });
  var cb = $("#cart-btn"); if (cb) cb.addEventListener("click", function () { chargerPanier(); ouvrirPanier(); });
  var dc = $("#drawer-close"); if (dc) dc.addEventListener("click", fermerPanier);
  var dbg = $("#drawer-bg"); if (dbg) dbg.addEventListener("click", fermerPanier);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { fermerPanier(); if (LOU.fermerLou) LOU.fermerLou(); } });
  if (LOU.cart && LOU.cart.items) { dejaDuo = LOU.cart.item_count >= 2; dessinerPanier(LOU.cart); }

  /* ---------- Gravure réaliste sur la photo du jonc ----------
     Bords de la face avant mesurés sur la photo du jonc vierge (repère : recadrage 920×460 placé en x=90, y=360 de l'image
     1024×1024 ; un point tous les 10 px à partir de x=100). Le texte est écrit à plat sur une bande « déroulée », puis replié
     colonne par colonne entre le bord haut et le bord bas de la face (les verticales restent verticales, comme sur un cylindre) ;
     il se resserre vers les côtés (x = cx + a·sin θ). « vue » = zone de l'image 1024 affichée (accueil : bande ; fiche : carré).
     Si on change la photo : re-mesurer haut/bas/cx/a (méthode dans docs/journal.md, 02/11/2026). */
  var JONC = {
    x0: 100, pas: 10, cx: 450, a: 410, xg: 125, xd: 800, zone: 0.78, ecrase: 0.85,
    haut: [281.6,286.6,291.3,295.7,299.7,303.5,307.0,310.3,313.3,316.1,318.6,321.0,323.1,325.1,326.8,328.4,329.9,331.2,332.3,333.4,334.2,335.0,335.7,336.2,336.6,337.0,337.2,337.4,337.5,337.5,337.4,337.3,337.1,336.8,336.4,336.0,335.5,335.0,334.4,333.7,333.0,332.1,331.3,330.3,329.3,328.2,327.0,325.8,324.4,323.0,321.5,319.8,318.1,316.2,314.3,312.2,309.9,307.5,305.0,302.3,299.4,296.4,293.2,289.7,286.1,282.2,278.1,273.8,269.1,264.3,259.1,253.6,247.9,241.8],
    bas: [327.1,332.4,337.5,342.2,346.6,350.7,354.5,358.1,361.4,364.4,367.2,369.8,372.2,374.4,376.4,378.3,379.9,381.4,382.7,383.9,385.0,385.9,386.7,387.4,387.9,388.4,388.7,389.0,389.1,389.2,389.2,389.1,388.9,388.6,388.3,387.8,387.3,386.8,386.1,385.4,384.6,383.7,382.8,381.8,380.6,379.4,378.1,376.8,375.3,373.7,372.0,370.2,368.3,366.3,364.1,361.8,359.4,356.8,354.1,351.1,348.1,344.8,341.3,337.6,333.8,329.6,325.3,320.7,315.8,310.7,305.2,299.5,293.5,287.1]
  };
  var VUES = { bande: { x0: 90, y0: 360, w: 920, h: 460 }, carre: { x0: 90, y0: 104, w: 920, h: 920 }, plein: { x0: 0, y0: 0, w: 1024, h: 1024 } };
  var bordJonc = function (t, x) {
    var k = (x - JONC.x0) / JONC.pas, i = Math.max(0, Math.min(t.length - 2, Math.floor(k))), f = k - i;
    return t[i] + (t[i + 1] - t[i]) * f;
  };
  var calque = function (w, h) { var c = document.createElement("canvas"); c.width = Math.max(1, w); c.height = Math.max(1, h); return c; };
  var teinter = function (src, couleur) {
    var c = calque(src.width, src.height), x = c.getContext("2d");
    x.drawImage(src, 0, 0); x.globalCompositeOperation = "source-in"; x.fillStyle = couleur; x.fillRect(0, 0, c.width, c.height);
    return c;
  };
  var POLICES = {
    Manuscrite: { font: '"Allura", cursive', maj: false, esp: 0, ref: "Tu es ma personne", taille: 1 },
    Classique: { font: '600 {t}px "Cormorant Garamond", Georgia, serif', maj: true, esp: .16, ref: "ÉMOTION", taille: .62 },
    Moderne: { font: '500 {t}px Montserrat, Arial, sans-serif', maj: true, esp: .22, ref: "ÉMOTION", taille: .52 }
  };
  var policeCss = function (p, t) { return p.font.indexOf("{t}") > -1 ? p.font.replace("{t}", t) : t + "px " + p.font; };
  // Écrit un texte (avec espacement des lettres si besoin) ; renvoie la largeur
  function ecrireTexte(ctx, txt, x, y, esp, dessiner) {
    if (!esp) { if (dessiner) ctx.fillText(txt, x, y); return ctx.measureText(txt).width; }
    var cx = x, chars = Array.from(txt);
    chars.forEach(function (ch, i) { if (dessiner) ctx.fillText(ch, cx, y); cx += ctx.measureText(ch).width + (i < chars.length - 1 ? esp : 0); });
    return cx - x;
  }
  LOU.graverJonc = window.LOU_graverJonc = function (canvas, img, texte, opts) {
    opts = opts || {};
    var W = canvas.clientWidth, H = canvas.clientHeight;
    if (!W || !H || !img.complete || !img.naturalWidth) return null;
    var dpr = Math.min(window.devicePixelRatio || 1, 2.5), vue = VUES[opts.vue || "bande"];
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    var s = canvas.width / vue.w, ox = 90 - vue.x0, oy = 360 - vue.y0, ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (opts.fond !== false) ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    if (!texte) return null;
    var P = POLICES[opts.police] || POLICES.Manuscrite;
    if (P.maj) texte = texte.toUpperCase();
    var J = JONC, thG = Math.asin((J.xg - J.cx) / J.a), thD = Math.asin((J.xd - J.cx) / J.a), dTh = thD - thG;
    // 1. Bande déroulée (sur-échantillonnée ×2)
    var hFace = 52, SH = Math.ceil(hFace * J.zone / J.ecrase * s * 2), SW = Math.ceil(J.a * dTh * s * 2);
    var bande = calque(SW, SH), b = bande.getContext("2d");
    b.font = policeCss(P, 100); b.textBaseline = "alphabetic";
    var m = b.measureText(texte), ref = b.measureText(P.ref);
    var asc = Math.max(m.actualBoundingBoxAscent || 80, ref.actualBoundingBoxAscent || 80);
    var desc = Math.max(m.actualBoundingBoxDescent || 0, P.maj ? 4 : (ref.actualBoundingBoxDescent || 30));
    var esp100 = P.esp * 100, larg = ecrireTexte(b, texte, 0, 0, esp100, false);
    var gauche = P.esp ? 0 : (m.actualBoundingBoxLeft || 0), encre = P.esp ? larg : (m.actualBoundingBoxLeft != null ? m.actualBoundingBoxLeft + m.actualBoundingBoxRight : m.width);
    var k = Math.min(SH * 0.96 * P.taille / (asc + desc), SW * 0.94 / encre);   // l'encre tient toujours dans la bande
    b.font = policeCss(P, (100 * k).toFixed(2)); b.fillStyle = "#000"; b.textAlign = "left";
    var x0 = SW / 2 - encre * k / 2 + gauche * k;
    ecrireTexte(b, texte, x0, SH / 2 + (asc - desc) / 2 * k, esp100 * k, true);
    // 2. Repli colonne par colonne sur la face avant, avec découpe à la forme exacte de la face
    var masque = calque(canvas.width, canvas.height), mc = masque.getContext("2d"), x, X;
    mc.beginPath();
    for (x = J.xg - 15; x <= J.xd + 15; x += 5) mc.lineTo((x + ox) * s, (bordJonc(J.haut, x) + 1.5 + oy) * s);
    for (x = J.xd + 15; x >= J.xg - 15; x -= 5) mc.lineTo((x + ox) * s, (bordJonc(J.bas, x) - 1.5 + oy) * s);
    mc.closePath(); mc.clip();
    for (X = Math.floor((J.xg + ox) * s); X <= Math.ceil((J.xd + ox) * s); X++) {
      x = X / s - ox;
      var th = Math.asin(Math.max(-1, Math.min(1, (x - J.cx) / J.a)));
      var u = (th - thG) / dTh;
      if (u < 0 || u > 1) continue;
      var srcL = Math.max(1, SW / (J.a * Math.cos(th) * dTh * s));      // largeur de bande vue par 1 px d'écran
      var hb = bordJonc(J.haut, x), bb = bordJonc(J.bas, x), h = bb - hb;
      mc.drawImage(bande, Math.max(0, Math.min(SW - srcL, u * SW - srcL / 2)), 0, srcL, SH, X, (hb + oy + h * (1 - J.zone) / 2) * s, 1, h * J.zone * s);
    }
    // 3. Incrustation dans le métal : reflet clair sous le trait (bord du sillon), puis creux sombre (multiplié = suit les reflets)
    var dy = Math.max(1, 0.9 * s);
    ctx.save();
    if ("filter" in ctx) ctx.filter = "blur(" + (0.35 * dpr).toFixed(2) + "px)";
    ctx.globalCompositeOperation = "screen"; ctx.globalAlpha = 0.55; ctx.drawImage(teinter(masque, "#ffffff"), 0, dy);
    ctx.globalCompositeOperation = "multiply"; ctx.globalAlpha = 0.9; ctx.drawImage(teinter(masque, opts.encre || "#55494f"), 0, 0);
    ctx.globalAlpha = 0.35; ctx.drawImage(teinter(masque, "#3a3034"), 0, -dy * 0.5);
    ctx.restore();
    // Position de la fin du texte (pour l'étincelle du « laser »), en pixels CSS
    var uFin = (x0 + encre * k) / SW, thF = thG + uFin * dTh, xF = J.cx + J.a * Math.sin(thF);
    return { x: (xF + ox) * s / dpr, y: ((bordJonc(J.haut, xF) + bordJonc(J.bas, xF)) / 2 + oy) * s / dpr };
  };

  /* ---------- Collier prénom : prénom en métal, la chaîne s'accroche aux deux bords du prénom ----------
     Sur assets/collier-vierge*.webp (repère 1200 px), le bas des deux brins est effacé (sous y ≈ 630, cf. scripts/assets_theme.py) :
     les brins sont redessinés depuis la vraie chaîne jusqu'à la première et la dernière lettre. Prénom court : la chaîne se
     resserre ; prénom long : elle s'ouvre. La taille des lettres ne dépend pas de la longueur du prénom. */
  var METAL = { "Argentée": ["#ffffff", "#d9dbe2", "#9a9eaa", "#eef0f4", "#7c808c"], "Dorée": ["#fff6d2", "#f0cd72", "#b88a2c", "#ffe7a3", "#8a6420"], "Rosée": ["#fff0ea", "#f2bfae", "#c4806f", "#ffd9cc", "#975c4f"] };
  var BRIN = { g: { x: 361, y: 626, dx: .45 }, d: { x: 879, y: 626, dx: -.5 } };   // départ des brins redessinés + direction
  LOU.dessinerPrenom = function (toile, photo, nom, pol, finition) {
    if (!toile || !photo.complete || !photo.naturalWidth) return;
    var W = toile.clientWidth, dpr = Math.min(window.devicePixelRatio || 1, 2.5);
    toile.width = Math.round(W * dpr); toile.height = Math.round(toile.clientHeight * dpr);
    var s = toile.width / 1200, ctx = toile.getContext("2d"); ctx.clearRect(0, 0, toile.width, toile.height);
    if (!nom) return;
    var m = METAL[finition] || METAL["Argentée"];
    var script = pol !== "Moderne", font = script ? '"Allura", cursive' : '700 {t}px Montserrat, Arial, sans-serif';
    var css = function (t) { return script ? t + "px " + font : font.replace("{t}", t); };
    ctx.font = css(100);
    var mt = ctx.measureText(nom), L = mt.actualBoundingBoxLeft || 0, Rr = mt.actualBoundingBoxRight || mt.width;
    var asc = mt.actualBoundingBoxAscent || 70, desc = mt.actualBoundingBoxDescent || 20;
    var hMax = script ? 92 : 44;
    var k = Math.min(hMax / (asc + desc), script ? 1.15 : .62);
    if ((L + Rr) * k > 560) k = 560 / (L + Rr);            // garde-fou (prénom très long) : reste sur le buste
    var fs = 100 * k, encre = (L + Rr) * k, cx = 620.5;
    var base = 860 + (script ? .2 : .36) * fs;
    var xg = cx - encre / 2, yAttache = base - (script ? .22 : .36) * fs;
    var px = xg + L * k;
    // Bords réels du prénom à hauteur d'accroche (premier et dernier pixel d'encre)
    var mes = document.createElement("canvas"); mes.width = 1200; mes.height = 1200; var mx = mes.getContext("2d");
    mx.font = css(fs.toFixed(2)); mx.textBaseline = "alphabetic"; mx.lineJoin = "round"; mx.lineWidth = fs * (script ? .055 : .03);
    mx.fillStyle = mx.strokeStyle = "#000"; mx.strokeText(nom, px, base); mx.fillText(nom, px, base);
    var y0 = Math.max(0, Math.round(yAttache - fs * .16)), y1 = Math.min(1199, Math.round(yAttache + fs * .16));
    var zx0 = Math.max(0, Math.floor(xg - 20)), zw = Math.min(1200 - zx0, Math.ceil(encre + 40));
    var dat = mx.getImageData(zx0, y0, zw, y1 - y0 + 1).data, ag = null, ad = null;
    for (var yy = 0; yy <= y1 - y0; yy++) for (var xx = 0; xx < zw; xx++) if (dat[(yy * zw + xx) * 4 + 3] > 140) {
      if (!ag || xx + zx0 < ag.x) ag = { x: xx + zx0, y: yy + y0 };
      if (!ad || xx + zx0 > ad.x) ad = { x: xx + zx0, y: yy + y0 };
    }
    ag = ag || { x: xg, y: yAttache }; ad = ad || { x: xg + encre, y: yAttache };
    var rA = 6.5, RG = { x: ag.x - rA + 2, y: ag.y }, RD = { x: ad.x + rA - 2, y: ad.y };
    // calque métal (en pixels de l'image 1200, puis mis à l'échelle)
    var c = document.createElement("canvas"); c.width = toile.width; c.height = toile.height; var x = c.getContext("2d");
    x.scale(s, s);
    // un brin : courbe douce depuis la vraie chaîne jusqu'à l'anneau, maillons alternés (à plat / de profil)
    var brin = function (b, R) {
      var dl = Math.hypot(R.x - b.x, R.y - b.y), n0 = Math.hypot(b.dx, 1);
      var Q = { x: b.x + b.dx / n0 * dl * .5, y: b.y + 1 / n0 * dl * .5 };
      var pt = function (t) { var u = 1 - t; return { x: u * u * b.x + 2 * u * t * Q.x + t * t * R.x, y: u * u * b.y + 2 * u * t * Q.y + t * t * R.y }; };
      var tab = [{ t: 0, l: 0, p: pt(0) }], N = 200;
      for (var i = 1; i <= N; i++) { var q = pt(i / N); tab.push({ t: i / N, l: tab[i - 1].l + Math.hypot(q.x - tab[i - 1].p.x, q.y - tab[i - 1].p.y), p: q }); }
      var Lt = tab[N].l - rA, pas = 10.5, n = Math.max(1, Math.round(Lt / pas)); pas = Lt / n;
      var j = 0;
      for (var kk = 0; kk < n; kk++) {
        var l = (kk + .5) * pas; while (j < N && tab[j + 1].l < l) j++;
        var a = tab[j].p, bb = tab[Math.min(N, j + 1)].p, ang = Math.atan2(bb.y - a.y, bb.x - a.x);
        x.save(); x.translate(a.x, a.y); x.rotate(ang);
        var ry = kk % 2 ? 1.3 : 3.6;
        // maillon métal : contour foncé, corps clair, reflet blanc (même éclat que la chaîne de la photo)
        x.beginPath(); x.ellipse(0, 0, 6.3, ry, 0, 0, Math.PI * 2); x.lineWidth = 2.5; x.strokeStyle = m[4]; x.globalAlpha = .55; x.stroke(); x.globalAlpha = 1;
        x.beginPath(); x.ellipse(0, 0, 6.3, ry, 0, 0, Math.PI * 2); x.lineWidth = 1.6; x.strokeStyle = m[1]; x.stroke();
        x.beginPath(); x.ellipse(0, -.3, 6, Math.max(.6, ry - .3), 0, Math.PI * 1.1, Math.PI * 1.9); x.lineWidth = .9; x.strokeStyle = m[0]; x.stroke();
        x.restore();
      }
      // anneau d'accroche
      x.beginPath(); x.arc(R.x, R.y, rA, 0, Math.PI * 2); x.lineWidth = 3; x.strokeStyle = m[4]; x.globalAlpha = .55; x.stroke(); x.globalAlpha = 1;
      x.beginPath(); x.arc(R.x, R.y, rA, 0, Math.PI * 2); x.lineWidth = 2; x.strokeStyle = m[1]; x.stroke();
      x.beginPath(); x.arc(R.x, R.y - .4, rA - .2, Math.PI * 1.1, Math.PI * 1.9); x.lineWidth = 1; x.strokeStyle = m[0]; x.stroke();
    };
    brin(BRIN.g, RG); brin(BRIN.d, RD);
    x.font = css(fs.toFixed(2)); x.textBaseline = "alphabetic"; x.lineJoin = "round";
    var gr = x.createLinearGradient(0, base - asc * k, 0, base + desc * k);
    gr.addColorStop(0, m[0]); gr.addColorStop(.35, m[1]); gr.addColorStop(.6, m[3]); gr.addColorStop(1, m[2]);
    x.lineWidth = fs * (script ? .055 : .03); x.strokeStyle = gr; x.fillStyle = gr;
    x.strokeText(nom, px, base); x.fillText(nom, px, base);
    // biseau : bord haut plus clair, bas plus sombre (copie décalée en « source-atop »)
    x.globalCompositeOperation = "source-atop"; x.globalAlpha = .35; x.fillStyle = m[4];
    x.lineWidth = fs * (script ? .055 : .03); x.strokeStyle = m[4];
    x.strokeText(nom, px, base + fs * .025); x.fillText(nom, px, base + fs * .025);
    x.globalAlpha = .55; x.fillStyle = "#fff"; x.fillText(nom, px - fs * .006, base - fs * .018);
    // ombre portée sur le velours, puis le métal
    ctx.save(); ctx.shadowColor = "rgba(70,35,40,.42)"; ctx.shadowBlur = 7 * s; ctx.shadowOffsetX = 2 * s; ctx.shadowOffsetY = 5 * s;
    ctx.drawImage(c, 0, 0); ctx.restore();
  };

  /* ---------- Accueil : atelier (on tape, ça se grave) ---------- */
  var atelier = $("#atelier-texte");
  if (atelier) {
    var lien = $("#atelier-lien"), toile = $("#atelier-gravure"), boite = $("#atelier-apercu"), photo = boite && $("img", boite), etinc = $("#etincelle");
    var finA = "Argentée", dernier = "", aEcrit = false, dedans = false;
    var etincelle = function (p) {
      if (!p || !etinc || reduit) return;
      etinc.style.left = p.x + "px"; etinc.style.top = p.y + "px";
      for (var i = 0; i < 5; i++) {
        var e = document.createElement("i"); e.style.setProperty("--dx", (Math.random() * 30 - 8) + "px"); e.style.setProperty("--dy", (Math.random() * -26 + 6) + "px");
        etinc.appendChild(e); setTimeout((function (z) { return function () { z.remove(); }; })(e), 600);
      }
    };
    var maj = function (feu) {
      var v = atelier.value.slice(0, 20);
      var p = null;
      if (toile && photo && toile.getContext) p = LOU.graverJonc(toile, photo, v || (dedans ? "" : "Tu es ma personne"), { vue: "bande", encre: finA === "Argentée" ? "#55494f" : "#5a3f2a" });
      if (feu && v && v !== dernier) etincelle(p);
      dernier = v;
      // « Graver » et « Je crée mon bijou » : fiche du jonc, directement à l'écriture, avec la phrase (si la cliente l'a écrite) et la finition
      var url = lien.getAttribute("data-base") + "?" + (aEcrit && v ? "texte=" + encodeURIComponent(v) + "&" : "") + "finition=" + encodeURIComponent(finA) + "#personnaliser";
      [lien, $("#atelier-cta")].forEach(function (a) { if (a) a.href = url; });
    };
    if (photo && !photo.complete) photo.addEventListener("load", function () { maj(); });
    var attente; addEventListener("resize", function () { clearTimeout(attente); attente = setTimeout(maj, 120); });
    if (document.fonts && document.fonts.load) document.fonts.load('40px "Allura"').then(function () { maj(); });
    atelier.addEventListener("input", function () {
      var v = atelier.value, i = v.search(/\S/), up = i > -1 ? v.charAt(i).toLocaleUpperCase("fr-FR") : "";
      if (i > -1 && up !== v.charAt(i) && up.length === 1) {   // première lettre toujours en majuscule
        var a = atelier.selectionStart, b = atelier.selectionEnd;
        atelier.value = v.slice(0, i) + up + v.slice(i + 1);
        try { atelier.setSelectionRange(a, b); } catch (e) {}
      }
      aEcrit = !!atelier.value;
      maj(true); son("clic");
    });
    // Quand on touche le champ : l'exemple s'efface pour écrire ses propres mots (jonc vierge en attendant)
    atelier.addEventListener("focus", function () { dedans = true; if (!aEcrit) { atelier.value = ""; maj(); } });
    atelier.addEventListener("blur", function () { dedans = false; if (!atelier.value) maj(); });
    maj();
    $$(".pastilles button", $("#atelier")).forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".pastilles button", $("#atelier")).forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-checked", "false"); });
        b.classList.add("is-on"); b.setAttribute("aria-checked", "true"); son("pop");
        finA = b.getAttribute("aria-label");
        var src = boite.getAttribute(b.getAttribute("data-fin") === "-doree" ? "data-doree" : b.getAttribute("data-fin") === "-rosee" ? "data-rosee" : "data-base");
        var im = new Image(); im.onload = function () { photo.src = src; if (photo.complete) maj(); else photo.onload = function () { maj(); }; }; im.src = src;
      });
    });
    // Démo : le texte s'écrit tout seul tant qu'on n'a pas touché au champ
    if (!reduit) {
      var demo = ["Tu es ma personne", "Sœurs pour toujours", "Merci maman", "Toi, toujours"], di = 0, ci = 0, touche = false;
      atelier.addEventListener("focus", function () { touche = true; });
      (function tape() {
        if (touche) return;
        var mot = demo[di % demo.length];
        if (ci <= mot.length) { atelier.value = mot.slice(0, ci++); maj(ci > 1); setTimeout(tape, 95); }
        else { setTimeout(function () { ci = 0; di++; tape(); }, 2000); }
      })();
    }
  }
  // Lou se présente dans la bulle du haut
  var intro = $("#lou-intro");
  if (intro && !reduit) { var txt = intro.getAttribute("data-texte"); intro.textContent = ""; setTimeout(function () { LOU.ecrire(intro, txt, 22); }, 450); }


  /* ---------- Vignettes produits animées : l'image se « remplit » de la personnalisation ----------
     Jonc : la phrase se grave lettre par lettre ; collier : le prénom s'écrit (la chaîne suit) ; collier photo : la photo
     apparaît dans la bulle ; bracelet : le mot secret s'écrit en Morse. Seulement quand la vignette est à l'écran. */
  var MORSE_C = { A: ".-", B: "-...", C: "-.-.", D: "-..", E: ".", F: "..-.", G: "--.", H: "....", I: "..", J: ".---", K: "-.-", L: ".-..", M: "--", N: "-.", O: "---", P: ".--.", Q: "--.-", R: ".-.", S: "...", T: "-", U: "..-", V: "...-", W: ".--", X: "-..-", Y: "-.--", Z: "--.." };
  var ANIM = LOU.anim || {};
  function vignette(box) {
    var type = box.getAttribute("data-anim"), calqueA = document.createElement("div"), vu = false, t = null, i = 0, k = 0, enCours = false;
    calqueA.className = "carte-anim"; calqueA.setAttribute("aria-hidden", "true");
    var img = null, cv = null, bulleP = null, morse = null, lignes = null;
    var pause = function (f, d) { clearTimeout(t); t = setTimeout(function () { if (vu) f(); else enCours = false; }, d); };
    var pret = function () { calqueA.classList.add("on"); };
    if (type === "jonc" || type === "prenom") {
      img = new Image(); img.alt = ""; img.decoding = "async"; img.src = type === "jonc" ? ANIM.jonc : ANIM.collier;
      cv = document.createElement("canvas"); calqueA.appendChild(img); calqueA.appendChild(cv);
      lignes = type === "jonc" ? ["Tu es ma personne", "Merci maman", "Sœurs pour toujours", "Toi, toujours", "Crois en toi"] : ["Emma", "Léa", "Chloé", "Inès", "Jade", "Louise"];
    } else if (type === "photo") {
      bulleP = document.createElement("div"); bulleP.className = "bulle-photo";
      bulleP.style.cssText = "left:59.37%;top:21.87%;width:29.34%;height:29.34%";
      calqueA.appendChild(bulleP); lignes = ANIM.souvenirs || [];
    } else if (type === "morse") {
      morse = document.createElement("div"); morse.className = "carte-morse"; morse.innerHTML = "<b></b><small></small>";
      calqueA.appendChild(morse); lignes = ["NOUS", "TOUJOURS", "AMIES", "MAMAN", "JETAIME"];
    } else return;
    box.appendChild(calqueA);
    var dessine = function (txt) {
      if (type === "jonc") LOU.graverJonc(cv, img, txt, { vue: "plein", fond: false });
      else LOU.dessinerPrenom(cv, img, txt, "Manuscrite", "Argentée");
    };
    var tour = function () {
      enCours = true;
      if (type === "photo") {
        if (!lignes.length) return;
        bulleP.style.backgroundImage = 'url("' + lignes[i % lignes.length] + '")';
        bulleP.classList.remove("pop"); void bulleP.offsetWidth; bulleP.classList.add("pop"); pret();
        i++; return pause(tour, 2600);
      }
      var mot = lignes[i % lignes.length];
      if (type === "morse") {
        k++;
        var m = mot.slice(0, k);
        morse.firstChild.textContent = m;
        morse.lastChild.textContent = m.split("").map(function (l) { return (MORSE_C[l] || "").replace(/\./g, "•").replace(/-/g, "—"); }).join("  ");
        pret();
        if (k < mot.length) return pause(tour, 260);
        k = 0; i++; return pause(tour, 2000);
      }
      if (!img.complete || !img.naturalWidth) return pause(tour, 200);
      var lettres = Array.from(mot);
      k++;
      dessine(lettres.slice(0, k).join("")); pret();
      if (k < lettres.length) return pause(tour, type === "jonc" ? 95 : 190);
      k = type === "jonc" ? 0 : 0; i++;
      pause(tour, 2300);
    };
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) {
      vu = es[0].isIntersecting;
      if (vu && !enCours) pause(tour, 350);
    }, { threshold: .35 }).observe(box);
    addEventListener("resize", function () { if (cv && cv.width) { var l = Array.from(lignes[(i ? i - 1 : 0) % lignes.length]); if (type !== "photo" && type !== "morse") dessine(l.join("")); } });
  }
  if (!reduit) {
    var lancerVignettes = function () { $$(".carte-img[data-anim]").forEach(vignette); };
    if (document.fonts && document.fonts.load) Promise.all([document.fonts.load('40px "Allura"')]).then(lancerVignettes, lancerVignettes); else lancerVignettes();
  }

  /* ---------- Machine à mots (accueil : ouvre la fiche du jonc ; fiche produit : remplit le champ) ---------- */
  $$(".machine-boite").forEach(function (machine) {
    var phrase = $(".machine-phrase", machine), cat = "amour", base = machine.getAttribute("data-produit") || (root + "products/jonc-mes-mots");
    var mode = machine.getAttribute("data-mode") || "lien", banque = machine.getAttribute("data-sorte") === "mot" ? MOTS : PHRASES;
    var graver = $(".machine-graver", machine), manette = $(".manette", machine), roule = false;
    $$(".machine-cats .chip", machine).forEach(function (c) {
      c.addEventListener("click", function () {
        $$(".machine-cats .chip", machine).forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-pressed", "false"); });
        c.classList.add("is-on"); c.setAttribute("aria-pressed", "true"); cat = c.getAttribute("data-cat"); tirer();
      });
    });
    var fin = function (p) { if (graver && mode === "lien") graver.href = base + "?texte=" + encodeURIComponent(p) + "#personnaliser"; };
    var tirer = function () {
      if (roule) return;
      var liste = banque[cat], finale = liste[Math.floor(Math.random() * liste.length)];
      if (finale === phrase.textContent) finale = liste[(liste.indexOf(finale) + 1) % liste.length];
      if (manette) { manette.classList.add("tire"); setTimeout(function () { manette.classList.remove("tire"); }, 420); }
      if (reduit) { phrase.textContent = finale; return fin(finale); }
      roule = true; phrase.classList.remove("stop"); phrase.classList.add("roule"); var n = 0;
      var it = setInterval(function () {
        phrase.textContent = liste[n++ % liste.length]; if (n % 2) son("clic");
        if (n > 14) {
          clearInterval(it); phrase.classList.remove("roule"); void phrase.offsetWidth; phrase.classList.add("stop"); phrase.textContent = finale; fin(finale); roule = false; son("ding");
          var r = machine.getBoundingClientRect(); confettis(50, r.left + r.width / 2, r.top + r.height * .45);
        }
      }, 70);
    };
    var bt = $(".machine-tirer", machine); if (bt) bt.addEventListener("click", tirer);
    if (manette) manette.addEventListener("click", tirer);
    if (graver && mode === "remplir") graver.addEventListener("click", function () {
      var champ = $(".perso-texte[data-principal='1']") || $(".perso-texte"), gal = $("#galerie");
      if (!champ) return;
      champ.value = phrase.textContent.slice(0, +champ.maxLength || 20); champ.dispatchEvent(new Event("input")); son("pop");
      if (gal) { gal.scrollTo({ left: 0 }); gal.scrollIntoView({ behavior: reduit ? "auto" : "smooth", block: "center" }); }
      if (LOU.dit) setTimeout(function () { LOU.dit("« " + champ.value + " »… c'est noté ✍️ Regardez l'aperçu !", 3500); }, 700);
    });
    fin(phrase.textContent);
  });

  /* ---------- Cartes « problème → solution » : se retournent toutes seules, et au toucher ---------- */
  var cartesR = $$(".carte-r");
  if (cartesR.length) {
    cartesR.forEach(function (c) { c.addEventListener("click", function () { c.classList.toggle("flip"); c.dataset.touche = "1"; son("pop"); }); });
    if (!reduit) {
      // Une carte à la fois, lentement : on commence par la 2e (le temps de lire la 1re), puis 3e, 4e, 1re…
      var ordre = [1, 2, 3, 0], ir = 0, visible = false, lance = false;
      var suivant = function () {
        if (!visible) { lance = false; return; }
        if (cartesR.every(function (x) { return x.dataset.touche; })) return;
        var c = cartesR[ordre[ir % ordre.length] % cartesR.length]; ir++;
        if (c.dataset.touche) return setTimeout(suivant, 200);
        c.classList.add("flip");
        setTimeout(function () { if (!c.dataset.touche) c.classList.remove("flip"); }, 4000);
        setTimeout(suivant, 4000 + 1800);
      };
      if ("IntersectionObserver" in window) new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        if (visible && !lance) { lance = true; setTimeout(suivant, ir ? 1800 : 3500); }
      }, { threshold: .5 }).observe($("#retourne"));
    }
  }

  /* ---------- Compte à rebours de Noël + neige ---------- */
  var noel = $("#noel");
  if (noel) {
    var lim = new Date((noel.getAttribute("data-limite") || R.noel) + "T23:59:59");
    var u = {}; $$("[data-u]", noel).forEach(function (e) { u[e.getAttribute("data-u")] = e; });
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var tic = function () {
      var d = Math.max(0, lim - new Date()), s = Math.floor(d / 1000);
      u.j.textContent = Math.floor(s / 86400); u.h.textContent = pad(Math.floor(s / 3600) % 24); u.m.textContent = pad(Math.floor(s / 60) % 60); u.s.textContent = pad(s % 60);
      if (!d) { var p = $("p", noel); if (p) p.textContent = "Pour Noël, il est un peu tard pour la livraison… mais un bijou à mots, ça s'offre toute l'année 💗"; }
    };
    tic(); setInterval(tic, 1000);
    var ng = $(".neige", noel);
    if (ng && !reduit) for (var k = 0; k < 18; k++) { var f = document.createElement("i"); f.textContent = k % 3 ? "❄" : "♥"; f.style.left = (Math.random() * 100) + "%"; f.style.fontSize = (8 + Math.random() * 10) + "px"; f.style.animationDuration = (6 + Math.random() * 7) + "s"; f.style.animationDelay = (-Math.random() * 10) + "s"; ng.appendChild(f); }
  }

  /* ---------- FAQ : Lou « écrit » sa réponse ---------- */
  $$(".faq details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      son("pop");
      if (reduit) return;
      d.classList.add("ecrit"); setTimeout(function () { d.classList.remove("ecrit"); }, 750);
    });
  });

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
      noel: "Noël ! Il reste le temps, mais pas trop 🎄", anniv: "Joyeux anniversaire en avance 🎂", rien: "Les cadeaux sans raison sont les meilleurs 💌", pardon: "Oups… on va arranger ça 🙈", naissance: "Bienvenue au petit cœur 👶", courage: "On va lui envoyer de la force 🌈",
      Argentée: "Noté : tout en finesse 🤍", Dorée: "Un peu de soleil, j'adore 🌾", Rosée: "Glamour, j'adore 💄" };
    var PAR_QUI = { amie: PHRASES.amitie, soeur: ["Ma sœur, mon pilier", "Même sang, même cœur", "Sœurs pour toujours", "Ma première amie"], maman: ["Merci maman", "Ma maman, mon repère", "Tu es ma maison", "Je t'aime gros"], amour: PHRASES.amour, mamie: ["Ma mamie d'amour", "Mamie, mon trésor", "Tes mots me guident"], moi: ["Je suis capable", "Un pas après l'autre", "Crois en toi", "Ma vie, mes règles"] };
    var PAR_QUAND = { noel: ["Mon plus beau cadeau"], anniv: ["Un an de plus, toi"], pardon: ["Pardon, je t'aime", "On recommence ?"], naissance: ["Bienvenue petit cœur"], courage: ["Plus forte que tout", "Respire, tu gères"], rien: ["Juste parce que"] };
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
          var c = q.c[+b.getAttribute("data-i")]; rep[q.k] = c[0]; b.classList.add("is-on"); son("pop");
          if (bulle && REACT[c[0]]) LOU.ecrire(bulle, REACT[c[0]], 14);
          setTimeout(function () { etape++; poser(); }, 520);
        });
      });
      var r = $(".test-retour", zone); if (r) r.addEventListener("click", function () { etape--; poser(); });
    };
    var resultat = function () {
      var h = rep.quoi, p = PRODUITS[h] || {}, fin = rep.style || "Argentée";
      var liste = (PAR_QUAND[rep.quand] || []).concat(PAR_QUI[rep.qui] || PHRASES.amitie).filter(function (x, i, a) { return a.indexOf(x) === i && x.length <= 20; }).slice(0, 3);
      if (h === "bracelet-code-secret") liste = [MORSE[rep.qui] || "TOUJOURS", "TOUJOURS", "NOUS"].filter(function (x, i, a) { return a.indexOf(x) === i; });
      var url = (p.url || root + "products/" + h) + "?finition=" + encodeURIComponent(fin);
      var phrasesHtml = h === "collier-prenom" || h === "collier-souvenir-photo" ? "" :
        '<p class="hand" style="margin:0">Et voici les mots que je vous propose :</p><div class="phrases">' + liste.map(function (ph) {
          return '<a class="phrase-choix" href="' + esc(url + "&texte=" + encodeURIComponent(ph)) + '">' + esc(ph) + '<span class="go">Graver ça →</span></a>';
        }).join("") + "</div>";
      if (bulle) LOU.ecrire(bulle, "Tadaaa ! J'ai trouvé votre bijou idéal 🎉", 18);
      zone.innerHTML = '<div class="resultat"><h3>Votre bijou idéal</h3><div class="resultat-produit">' + (p.image ? '<img src="' + esc(p.image) + '" alt="" width="96" height="96">' : "<span></span>") +
        "<div><b>" + esc(p.title || "Votre bijou") + '</b><br><span class="small">Finition ' + esc(fin.toLowerCase()) + "</span><br><span class=\"prix\">" + esc(p.price || "") + "</span></div></div>" + phrasesHtml +
        '<div class="hero-cta" style="justify-content:center"><a class="btn" href="' + esc(url) + '"><span class="brille"></span>Je le personnalise</a><button class="btn ghost" type="button" id="test-again">Recommencer</button></div></div>';
      $("#test-again").addEventListener("click", function () { rep = {}; etape = 0; if (bulle) bulle.textContent = bulleBase; poser(); });
      confettis(160); son("tada");
    };
    poser();
  }

  /* ---------- Lou, l'assistante en bas de l'écran ---------- */
  var assist = $("#lou-assist");
  if (assist) {
    var btn = $("#lou-btn"), panel = $("#lou-panel"), fil = $("#lou-fil"), choix = $("#lou-choix"), teaser = $("#lou-teaser"), pastille = $("#lou-n");
    var ouvert = false, teaserT;
    var page = LOU.page || "";
    var MSG_PAGE = {
      index: "Psst… écrivez vos mots dans l'atelier : je vous montre le rendu gravé en direct ✨",
      product: "Besoin d'une idée de phrase ? Touchez-moi, je vous en souffle une 💡",
      collection: "Je vous aide à choisir ? 4 questions et c'est réglé 🎁",
      cart: "Le 2e bijou est à -50 %… je dis ça, je dis rien 😇",
      page: "Coucou ! Une question ? Je suis là 👋"
    };
    var dit = function (msg, duree) {
      if (ouvert || !teaser) return;
      $("p", teaser).textContent = msg; teaser.hidden = false; teaser.style.animation = "none"; void teaser.offsetWidth; teaser.style.animation = "";
      clearTimeout(teaserT); if (duree) teaserT = setTimeout(function () { teaser.hidden = true; }, duree);
    };
    LOU.dit = dit;
    var bulleMsg = function (html, qui) {
      var m = document.createElement("div"); m.className = "msg de-" + (qui || "lou"); m.innerHTML = html; fil.appendChild(m); fil.scrollTop = fil.scrollHeight; return m;
    };
    var louRepond = function (html, ensuite) {
      var t = bulleMsg('<span class="points"><i></i><i></i><i></i></span>');
      setTimeout(function () { t.innerHTML = html; t.style.animation = "none"; void t.offsetWidth; t.style.animation = ""; fil.scrollTop = fil.scrollHeight; son("pop"); if (ensuite) ensuite(); }, reduit ? 0 : 650);
    };
    var urlJonc = root + "products/jonc-mes-mots";
    var j = joursNoel();
    var REP = {
      choisir: function () { louRepond("Facile ! Répondez à mon <b>test des mots</b> : 4 questions, 30 secondes, et je vous trouve le bijou… et les mots 💌<br><a class=\"btn\" href=\"" + root + "#le-test\">Faire le test</a>", proposer); },
      idee: function () { var p = LOU.idee(); louRepond("Que diriez-vous de :<span class=\"phrase\">« " + esc(p) + " »</span><a class=\"btn\" href=\"" + urlJonc + "?texte=" + encodeURIComponent(p) + "\">La graver sur le jonc ✍️</a>", function () { proposer(["idee", "choisir", "noel"]); }); },
      noel: function () { louRepond(j > 0 ? "Pour l'avoir sous le sapin, commandez avant le <b>" + esc(R.noelTexte) + "</b> (plus que <b>" + j + " jour" + (j > 1 ? "s" : "") + "</b> ⏳). Fabrication et livraison suivie : " + R.livMin + " à " + R.livMax + " jours au total 🎄" : "Pour Noël, la date conseillée est passée… mais un bijou à mots, ça s'offre toute l'année 💗", proposer); },
      matiere: function () { louRepond("Le jonc et le collier prénom sont en <b>acier inoxydable</b> : ils ne noircissent pas. Le collier photo : chaîne en acier inoxydable, pendentif en métal plaqué. Doré et rosé sont des finitions colorées, pas de l'or (je préfère être honnête 😇).", proposer); },
      offre: function () { louRepond("Mettez <b>2 bijoux</b> dans le panier : le moins cher est automatiquement à <b>-50 %</b>. Un pour elle, un pour vous ? 🎁", proposer); },
      livraison: function () { louRepond("Livraison suivie en France et en Belgique. Commandé aujourd'hui, reçu " + esc(LOU.estimation()) + " (estimation) 🚚<br><a class=\"btn\" href=\"" + root + "pages/livraison-retours\">Livraison &amp; retours</a>", proposer); },
      qui: function () { louRepond("Je suis <b>Lou, l'avatar de la boutique</b> : un personnage virtuel, créé avec l'IA 🤖💗 Je ne fabrique pas les bijoux, je vous guide. Derrière moi, une vraie équipe répond à vos messages.", proposer); },
      equipe: function () { louRepond("Une question précise ? L'équipe vous répond par e-mail, en vrai 💌<br><a class=\"btn\" href=\"" + root + "pages/contact\">Écrire à l'équipe</a>", proposer); }
    };
    var LIB = { choisir: "🎁 Aide-moi à choisir", idee: "✍️ Une idée de phrase", noel: "🎄 Reçu pour Noël ?", matiere: "💎 C'est en quoi ?", offre: "🏷️ L'offre -50 %", livraison: "🚚 Livraison", qui: "🤖 Tu es qui ?", equipe: "💌 Parler à l'équipe" };
    var proposer = function (liste) {
      liste = liste || ["choisir", "idee", "noel", "matiere", "offre", "livraison", "qui", "equipe"];
      choix.innerHTML = liste.map(function (k) { return '<button type="button" data-k="' + k + '">' + LIB[k] + "</button>"; }).join("");
    };
    choix.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      var k = b.getAttribute("data-k"); bulleMsg(esc(LIB[k].replace(/^\S+\s/, "")), "moi"); choix.innerHTML = ""; son("clic"); REP[k]();
    });
    var ouvrir = function () {
      ouvert = true; teaser.hidden = true; if (pastille) pastille.hidden = true; stocke("lou-vu", "1");
      panel.setAttribute("aria-hidden", "false"); panel.classList.remove("ouvre"); void panel.offsetWidth; panel.classList.add("ouvre"); btn.setAttribute("aria-expanded", "true"); son("pop");
      if (!fil.children.length) {
        var bonjour = page === "product" && LOU.produit ? "Coucou ! Moi c'est Lou 👋 l'avatar de la boutique. Vous regardez « " + esc(LOU.produit) + " » : bon choix ! Je vous aide ?" : "Coucou ! Moi c'est Lou 👋 l'avatar de la boutique (un personnage virtuel). Je suis là pour vous aider à choisir… et à trouver les mots. On commence par quoi ?";
        louRepond(bonjour, function () { proposer(); });
      }
    };
    var fermer = function () { ouvert = false; panel.setAttribute("aria-hidden", "true"); btn.setAttribute("aria-expanded", "false"); };
    LOU.fermerLou = fermer;
    LOU.ouvrirLou = ouvrir;
    btn.addEventListener("click", function () { ouvert ? fermer() : ouvrir(); });
    $("#lou-fermer").addEventListener("click", fermer);
    teaser.addEventListener("click", function (e) { if (e.target.closest(".lou-teaser-x")) { teaser.hidden = true; return; } ouvrir(); });
    // Petit message selon la page, une fois par page et par visite
    var cle = "lou-teaser-" + page;
    if (!stocke(cle)) setTimeout(function () { if (!ouvert && !document.body.classList.contains("panier-ouvert")) { dit(page === "index" && scrollY > 900 ? "Vous hésitez ? Touchez-moi : je vous aide à choisir… et à trouver les mots 💬" : (MSG_PAGE[page] || MSG_PAGE.page), 9000); stocke(cle, "1"); if (pastille && !stocke("lou-vu")) pastille.hidden = false; } }, page === "index" ? 9000 : 5000);
  }
})();
