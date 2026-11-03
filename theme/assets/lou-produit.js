/* Fiche produit (v0.2, 02/11/2026) : aperçus réalistes en direct sur photo (jonc gravé, prénom accroché à la chaîne,
   photo dans la bulle du collier, bracelet Morse), galerie à glisser, mini-aperçu flottant sur téléphone,
   barre d'achat, livraison estimée, conseils de Lou, ajout au panier animé. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fiche = $("#fiche"); if (!fiche) return;
  var LOU = window.LOU || {};
  var type = fiche.getAttribute("data-apercu") || "jonc";
  var scene = $("#scene"), vue = $("#vue-apercu"), galerie = $("#galerie"), form = $("#form-produit");
  var texte = $(".perso-texte[data-principal='1']") || $(".perso-texte");
  var police = $("#police"), photoURL = "";
  var fb = $(".finition.is-on:not(.police-btn)");
  var finition = fb ? fb.getAttribute("data-nom") : "Argentée";
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var qs = new URLSearchParams(location.search);
  var reduit = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var son = LOU.son || function () {};
  var IMG = { "Argentée": fiche.getAttribute("data-img-base"), "Dorée": fiche.getAttribute("data-img-doree") || fiche.getAttribute("data-img-base"), "Rosée": fiche.getAttribute("data-img-rosee") || fiche.getAttribute("data-img-base") };

  /* --- Scène : photo + calque de dessin --- */
  var photo = null, toile = null;
  if (type === "jonc" || type === "prenom" || type === "photo") {
    photo = new Image(); photo.alt = ""; photo.decoding = "async"; photo.src = IMG[finition] || IMG["Argentée"];
    scene.appendChild(photo);
    if (type !== "photo") { toile = document.createElement("canvas"); toile.setAttribute("aria-hidden", "true"); scene.appendChild(toile); }
  }
  var bullePhoto = null;
  if (type === "photo") {
    bullePhoto = document.createElement("div"); bullePhoto.className = "bulle-photo";
    // Bulle mesurée sur la photo (1200 px) : centre (888,5 ; 438,5), rayon 176
    bullePhoto.style.cssText = "left:59.37%;top:21.87%;width:29.34%;height:29.34%";
    scene.appendChild(bullePhoto);
  }

  /* --- Collier prénom : prénom en métal, la chaîne s'accroche aux deux bords du prénom ---
     Sur assets/collier-vierge*.webp (1200 px), le bas des deux brins est effacé (sous y ≈ 630, cf. scripts/assets_theme.py) :
     les brins sont redessinés depuis la vraie chaîne jusqu'à la première et la dernière lettre. Prénom court : la chaîne se
     resserre ; prénom long : elle s'ouvre. La taille des lettres ne dépend pas de la longueur du prénom. */
  function dessinerPrenom(nom, pol) { LOU.dessinerPrenom(toile, photo, nom, pol, finition); }

  /* --- Bracelet Morse : cordon et perles métalliques le long d'une courbe --- */
  var MORSE = { A: ".-", B: "-...", C: "-.-.", D: "-..", E: ".", F: "..-.", G: "--.", H: "....", I: "..", J: ".---", K: "-.-", L: ".-..", M: "--", N: "-.", O: "---", P: ".--.", Q: "--.-", R: ".-.", S: "...", T: "-", U: "..-", V: "...-", W: ".--", X: "-..-", Y: "-.--", Z: "--.." };
  function dessinerMorse(mot) {
    mot = (mot || "TOUJOURS").toUpperCase().replace(/[^A-Z]/g, "") || "TOUJOURS";
    var P0 = [40, 250], P1 = [300, 420], P2 = [560, 250];
    var pt = function (t) { var u = 1 - t; return [u * u * P0[0] + 2 * u * t * P1[0] + t * t * P2[0], u * u * P0[1] + 2 * u * t * P1[1] + t * t * P2[1]]; };
    var tab = [0], N = 400, prev = pt(0);
    for (var i = 1; i <= N; i++) { var p = pt(i / N); tab.push(tab[i - 1] + Math.hypot(p[0] - prev[0], p[1] - prev[1])); prev = p; }
    var Ltot = tab[N];
    var aLong = function (l) { var i = 0; while (i < N && tab[i + 1] < l) i++; var t = (i + (l - tab[i]) / ((tab[i + 1] - tab[i]) || 1)) / N; var a = pt(Math.max(0, t - .002)), b = pt(Math.min(1, t + .002)); var q = pt(t); return { x: q[0], y: q[1], ang: Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI }; };
    var elems = [], k = 1;
    mot.split("").forEach(function (l, li) {
      (MORSE[l] || "").split("").forEach(function (sym, si) { elems.push({ t: sym === "." ? "p" : "t" }); if (si < MORSE[l].length - 1) elems.push({ t: "g" }); });
      if (li < mot.length - 1) elems.push({ t: "s" });
    });
    var taille = function (e) { return e.t === "p" ? 28 : e.t === "t" ? 60 : e.t === "g" ? 7 : 26; };
    var total = elems.reduce(function (a, e) { return a + taille(e); }, 0);
    k = Math.min(1, Ltot * .8 / total);
    var l = (Ltot - total * k) / 2, html = "";
    elems.forEach(function (e) {
      var w = taille(e) * k, c = aLong(l + w / 2);
      if (e.t === "p") html += '<g transform="translate(' + c.x.toFixed(1) + " " + c.y.toFixed(1) + ') rotate(' + c.ang.toFixed(1) + ')"><circle r="' + (13 * k).toFixed(1) + '" fill="url(#perle)"/><ellipse cx="' + (-4 * k).toFixed(1) + '" cy="' + (-4.5 * k).toFixed(1) + '" rx="' + (4.5 * k).toFixed(1) + '" ry="' + (3 * k).toFixed(1) + '" fill="#fff" opacity=".8"/></g>';
      if (e.t === "t") html += '<g transform="translate(' + c.x.toFixed(1) + " " + c.y.toFixed(1) + ') rotate(' + c.ang.toFixed(1) + ')"><rect x="' + (-w / 2 + 1).toFixed(1) + '" y="' + (-11 * k).toFixed(1) + '" width="' + (w - 2).toFixed(1) + '" height="' + (22 * k).toFixed(1) + '" rx="' + (11 * k).toFixed(1) + '" fill="url(#barre)"/><rect x="' + (-w / 2 + 4).toFixed(1) + '" y="' + (-7.5 * k).toFixed(1) + '" width="' + (w - 10).toFixed(1) + '" height="' + (3.5 * k).toFixed(1) + '" rx="1.7" fill="#fff" opacity=".75"/></g>';
      l += w;
    });
    var legende = mot.split("").map(function (x) { return '<tspan font-weight="800">' + x + '</tspan> ' + (MORSE[x] || "").replace(/\./g, "•").replace(/-/g, "—"); }).join("   ");
    return '<svg class="morse-svg" viewBox="0 0 600 600" role="img" aria-label="Aperçu du bracelet : ' + esc(mot) + ' en code Morse"><defs>' +
      '<radialGradient id="fondm" cx="50%" cy="40%" r="70%"><stop offset="0" stop-color="#fff7f9"/><stop offset="1" stop-color="#f6d3dd"/></radialGradient>' +
      '<radialGradient id="perle" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#cfd2da"/><stop offset="1" stop-color="#6f7380"/></radialGradient>' +
      '<linearGradient id="barre" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f5f8"/><stop offset=".45" stop-color="#c3c6cf"/><stop offset=".55" stop-color="#9da1ad"/><stop offset="1" stop-color="#e4e6ec"/></linearGradient>' +
      '<filter id="ombrem" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#5a2a3a" flood-opacity=".28"/></filter></defs>' +
      '<rect width="600" height="600" fill="url(#fondm)"/>' +
      '<g filter="url(#ombrem)"><path d="M' + P0 + " Q" + P1 + " " + P2 + '" fill="none" stroke="#1d1d22" stroke-width="8" stroke-linecap="round"/>' +
      '<path d="M' + P0 + " Q" + P1 + " " + P2 + '" fill="none" stroke="#4a4a55" stroke-width="2" stroke-dasharray="3 4"/>' +
      '<path d="M40,250 C 20,230 18,200 30,180 M560,250 C 580,230 582,200 570,180" fill="none" stroke="#1d1d22" stroke-width="6" stroke-linecap="round"/>' +
      '<circle cx="30" cy="178" r="7" fill="url(#perle)"/><circle cx="570" cy="178" r="7" fill="url(#perle)"/>' + html + "</g>" +
      '<text x="300" y="530" text-anchor="middle" font-family="Nunito, Arial" font-size="19" fill="#3b1f2b">' + legende + "</text>" +
      '<text x="300" y="565" text-anchor="middle" font-family="Caveat, cursive" font-size="26" fill="#c62f63">• = point   — = trait</text></svg>';
  }

  /* --- Dessin de l'aperçu selon le produit --- */
  function dessiner() {
    var t = texte ? texte.value : "";
    var pol = police ? police.value : "Manuscrite";
    if (type === "jonc" && toile) {
      LOU.graverJonc(toile, photo, t || "Tu es ma personne", { vue: "carre", police: pol, encre: finition === "Argentée" ? "#55494f" : "#5a3f2a", fond: false });
    } else if (type === "prenom") dessinerPrenom(t || "Emma", pol);
    else if (type === "photo") {
      if (photoURL) { bullePhoto.style.backgroundImage = 'url("' + photoURL + '")'; bullePhoto.hidden = false; }
      else bullePhoto.hidden = true;
    } else if (type === "morse") scene.innerHTML = '<div class="svg-centre" style="padding:0">' + dessinerMorse(t) + "</div>";
    recap(t);
    miniMaj();
  }
  function recap(t) {
    var r = $("#recap"); if (!r || !texte) return;
    r.hidden = !t; $("#recap-texte").textContent = t ? "« " + t + " »" : "";
  }

  /* --- Mini-aperçu flottant (téléphone) : visible pendant qu'on écrit, quand la grande image n'est plus à l'écran --- */
  var mini = $("#mini-apercu"), miniVue = $("#mini-vue"), galerieVisible = true, enSaisie = false;
  function miniMaj() {
    if (!mini || !miniVue) return;
    if (type === "morse") { var svg = $("svg", scene); miniVue.innerHTML = svg ? '<img alt="" src="data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg.outerHTML) + '">' : ""; return; }
    if (type === "photo") { miniVue.innerHTML = photoURL ? '<div style="width:100%;height:100%;background:center/cover url(&quot;' + photoURL + '&quot;);border-radius:50%"></div>' : ""; return; }
    if (!photo || !photo.complete) return;
    var c = miniVue.querySelector("canvas"); if (!c) { c = document.createElement("canvas"); miniVue.innerHTML = ""; miniVue.appendChild(c); }
    var w = miniVue.clientWidth || 200, dpr = Math.min(window.devicePixelRatio || 1, 2.5); c.width = Math.round(w * dpr); c.height = Math.round(w * dpr);
    var x = c.getContext("2d"), z = type === "jonc" ? 1.6 : 2.1, fx = type === "jonc" ? .5 : .517, fy = type === "jonc" ? .645 : .72;   // zoom sur la gravure / le prénom
    var sw = c.width * z, sh = c.height * z, dx = c.width / 2 - sw * fx, dy = c.height / 2 - sh * fy;
    x.drawImage(photo, dx, dy, sw, sh); if (toile && toile.width) x.drawImage(toile, dx, dy, sw, sh);
  }
  function miniEtat() { if (mini) mini.classList.toggle("on", enSaisie && !galerieVisible && matchMedia("(max-width: 959px)").matches); }
  if (mini && "IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { galerieVisible = es[0].isIntersecting; miniEtat(); }, { threshold: .25 }).observe(galerie);
    mini.addEventListener("click", function () { galerie.scrollIntoView({ behavior: "smooth", block: "center" }); });
  }
  $$("input, button", form).forEach(function (el) { el.addEventListener("focus", function () { enSaisie = true; miniEtat(); }); });
  addEventListener("scroll", function () { if (!form) return; var r = form.getBoundingClientRect(); if (r.bottom < 80 || r.top > innerHeight) { enSaisie = false; miniEtat(); } }, { passive: true });

  /* --- Galerie à glisser --- */
  var slides = $$(".slide", galerie);
  function montrer(i, doux) {
    var cible = slides.filter(function (s) { return +s.getAttribute("data-i") === i; })[0];
    if (cible) galerie.scrollTo({ left: cible.offsetLeft, behavior: doux === false || reduit ? "auto" : "smooth" });
  }
  $$(".galerie-nav button").forEach(function (b) { b.addEventListener("click", function () { montrer(+b.getAttribute("data-vue")); son("clic"); }); });
  galerie.addEventListener("scroll", function () {
    var i = Math.round(galerie.scrollLeft / galerie.clientWidth), s = slides[i]; if (!s) return;
    var n = +s.getAttribute("data-i");
    $$(".galerie-nav button").forEach(function (b) { b.classList.toggle("is-on", +b.getAttribute("data-vue") === n); });
  }, { passive: true });

  /* --- Finitions (variantes) --- */
  function choisirFinition(b) {
    $$(".finition:not(.police-btn)").forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-checked", "false"); });
    b.classList.add("is-on"); b.setAttribute("aria-checked", "true");
    finition = b.getAttribute("data-nom");
    $("#variante").value = b.getAttribute("data-id");
    var fn = $("#finition-nom"); if (fn) fn.textContent = finition;
    ["#prix", "#prix-btn", "#prix-barre"].forEach(function (s) { var e = $(s); if (e) e.textContent = b.getAttribute("data-prix"); });
    if (photo && IMG[finition] && photo.src.indexOf(IMG[finition]) < 0) {
      var im = new Image(); im.onload = function () { photo.src = IMG[finition]; photo.decode ? photo.decode().then(dessiner, dessiner) : dessiner(); }; im.src = IMG[finition];
    } else dessiner();
    montrer(-1);
  }
  $$(".finition:not(.police-btn)").forEach(function (b) { b.addEventListener("click", function () { choisirFinition(b); son("pop"); }); });
  $$(".police-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      $$(".police-btn").forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-checked", "false"); });
      b.classList.add("is-on"); b.setAttribute("aria-checked", "true"); police.value = b.getAttribute("data-police"); son("pop"); dessiner(); montrer(-1);
    });
  });

  /* --- Texte + compteurs + idées de Lou --- */
  /* Première lettre toujours en majuscule (sans déplacer le curseur) */
  function majusculeDebut(inp) {
    var v = inp.value, i = v.search(/\S/);
    if (i < 0) return;
    var up = v.charAt(i).toLocaleUpperCase("fr-FR");
    if (up === v.charAt(i) || up.length !== 1) return;
    var a = inp.selectionStart, b = inp.selectionEnd;
    inp.value = v.slice(0, i) + up + v.slice(i + 1);
    try { inp.setSelectionRange(a, b); } catch (e) {}
  }
  $$(".perso-texte").forEach(function (inp) {
    var cpt = inp.closest(".champ").querySelector(".compteur");
    var maj = function () {
      if (inp.classList.contains("maj")) inp.value = inp.value.toUpperCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Z]/g, "");
      else majusculeDebut(inp);
      if (cpt) { cpt.textContent = inp.value.length + " / " + cpt.getAttribute("data-max"); cpt.classList.toggle("trop", inp.value.length >= +cpt.getAttribute("data-max")); }
      inp.classList.remove("erreur");
      dessiner();
    };
    inp.addEventListener("input", maj);
    inp.addEventListener("focus", function () { if (galerie.scrollLeft > 10) montrer(-1, false); });
  });
  $$(".suggestions button").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!texte) return;
      var v = b.hasAttribute("data-idee") ? LOU.idee() : b.textContent;
      texte.value = v.slice(0, +texte.maxLength || 20); texte.dispatchEvent(new Event("input")); son("pop");
      if (b.hasAttribute("data-idee") && LOU.dit) LOU.dit("« " + texte.value + " »… j'adore celle-là 💗 Regardez l'aperçu !", 3500);
      enSaisie = true; miniEtat();
    });
  });

  /* --- Photo --- */
  var fichier = $("#p-photo");
  if (fichier) fichier.addEventListener("change", function () {
    var f = fichier.files[0]; if (!f) return;
    if (f.size > 20 * 1024 * 1024) { LOU.toast && LOU.toast("Photo trop lourde (20 Mo maximum)"); fichier.value = ""; return; }
    if (photoURL) URL.revokeObjectURL(photoURL);
    photoURL = URL.createObjectURL(f);
    var d = $("#depot"); d.classList.add("ok"); d.querySelector("b").textContent = "Photo choisie ✔ (changer)";
    dessiner(); montrer(-1);
    if (bullePhoto) { bullePhoto.classList.remove("pop"); void bullePhoto.offsetWidth; bullePhoto.classList.add("pop"); }
    son("ding"); if (LOU.dit) LOU.dit("Oh, elle est belle ! 😍 Voilà ce qu'on verra dans la lentille.", 3500);
  });

  /* --- Valeurs reçues du test, de l'atelier ou de la machine à mots (?texte=…&finition=…) --- */
  if (qs.get("finition")) { var fq = $$(".finition:not(.police-btn)").filter(function (b) { return b.getAttribute("data-nom") === qs.get("finition"); })[0]; if (fq) choisirFinition(fq); }
  if (qs.get("texte") && texte) { texte.value = qs.get("texte").slice(0, +texte.maxLength || 20); texte.dispatchEvent(new Event("input")); }

  /* --- Arrivée depuis l'atelier de l'accueil (#personnaliser) : directement à l'écriture, mini-aperçu affiché --- */
  if (location.hash === "#personnaliser" && form) {
    setTimeout(function () {
      var cible = $(".bloc", form) || form;
      scrollTo({ top: cible.getBoundingClientRect().top + scrollY - 76, behavior: reduit ? "auto" : "smooth" });
      setTimeout(function () { enSaisie = true; miniEtat(); }, 1100);   // après le défilement (qui remet enSaisie à faux)
      if (LOU.dit) setTimeout(function () { LOU.dit(texte && texte.value ? "Voilà vos mots 💗 Vérifiez l'aperçu en haut à droite !" : "À vous d'écrire ✍️ Je grave en direct !", 3500); }, 1300);
    }, 450);
  }

  /* --- Premier dessin (après chargement de la photo et des polices) --- */
  if (photo) photo.addEventListener("load", dessiner);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(dessiner);
  ['40px "Allura"', '600 40px "Cormorant Garamond"', '700 40px Montserrat'].forEach(function (f) { if (document.fonts && document.fonts.load) document.fonts.load(f).then(dessiner, function () {}); });
  var att; addEventListener("resize", function () { clearTimeout(att); att = setTimeout(dessiner, 150); });
  dessiner();

  /* --- Livraison estimée --- */
  var es = $("#estim"); if (es && LOU.estimation) es.textContent = "🚚 Commandé aujourd'hui, reçu " + LOU.estimation() + " (estimation)";

  /* --- Ajout au panier --- */
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var err = $("#form-erreur"); err.textContent = "";
    var manque = $$("[required]", form).filter(function (el) { return el.type === "checkbox" ? !el.checked : el.type === "file" ? !el.files.length : !el.value.trim(); })[0];
    if (manque) {
      var msg = manque.id === "verif" ? "Une dernière chose : cochez la case pour confirmer l'orthographe 💗" : manque.type === "file" ? "Il me manque votre photo 📸" : "Écrivez vos mots d'abord, je les grave ✍️";
      err.textContent = msg; if (LOU.dit) LOU.dit(msg, 4000);
      var bloc = manque.closest(".champ") || manque.closest(".verif") || manque;
      bloc.scrollIntoView({ behavior: "smooth", block: "center" });
      if (manque.id === "verif") { var vl = $("#verif-l"); vl.classList.remove("erreur"); void vl.offsetWidth; vl.classList.add("erreur"); }
      else { manque.classList.add("erreur"); }
      if (manque.focus) setTimeout(function () { manque.focus({ preventScroll: true }); }, 350);
      return;
    }
    var btn = $("#ajouter"); btn.disabled = true;
    var source = toile && toile.width ? (function () { var c = document.createElement("canvas"); c.width = toile.width; c.height = toile.height; var x = c.getContext("2d"); x.drawImage(photo, 0, 0, c.width, c.height); x.drawImage(toile, 0, 0); c.getBoundingClientRect = function () { return galerie.getBoundingClientRect(); }; return c; })() : ($("img", scene) || $(".slide img", galerie));
    LOU.ajouter(new FormData(form), source).then(function () {
      if (LOU.dit) setTimeout(function () { LOU.dit("C'est dans le panier 💗 Le 2e bijou est à -50 %, si le cœur vous en dit !", 5000); }, 1500);
    }).catch(function (x) { err.textContent = "Oups : " + x.message; }).then(function () { btn.disabled = false; });
  });

  /* --- Barre d'achat (téléphone) : visible quand le bouton du formulaire n'est pas à l'écran --- */
  var barre = $("#barre-achat"), ajouter = $("#ajouter");
  if (barre && "IntersectionObserver" in window) new IntersectionObserver(function (es) { barre.classList.toggle("on", !es[0].isIntersecting); }).observe(ajouter);
  var bb = $("#barre-ajouter");
  if (bb) bb.addEventListener("click", function () { if (form.requestSubmit) form.requestSubmit(); else form.dispatchEvent(new Event("submit", { cancelable: true })); });
})();
