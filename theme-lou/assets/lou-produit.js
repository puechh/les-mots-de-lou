/* Fiche produit : aperçu en direct, finitions, police, photo, ajout au panier. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fiche = $("#fiche"); if (!fiche) return;
  var type = fiche.getAttribute("data-apercu") || "jonc";
  var vue = $("#vue-apercu"), imgs = $$(".vue-img"), form = $("#form-produit");
  var texte = $(".perso-texte[data-principal='1']") || $(".perso-texte");
  var police = $("#police"), photoURL = "";
  var finition = ($(".finition.is-on:not(.police-btn)") || {}).getAttribute ? $(".finition.is-on:not(.police-btn)").getAttribute("data-nom") : "Argentée";
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var qs = new URLSearchParams(location.search);

  /* --- Morse --- */
  var M = { A: ".-", B: "-...", C: "-.-.", D: "-..", E: ".", F: "..-.", G: "--.", H: "....", I: "..", J: ".---", K: "-.-", L: ".-..", M: "--", N: "-.", O: "---", P: ".--.", Q: "--.-", R: ".-.", S: "...", T: "-", U: "..-", V: "...-", W: ".--", X: "-..-", Y: "-.--", Z: "--.." };
  var COULEUR_FIL = { "Noir": "#222", "Rose poudré": "#e9a3b5", "Beige": "#cbb08a" };
  var METAL = { "Argentée": ["#ffffff", "#b9bcc6", "#7f828c"], "Dorée": ["#fff4d6", "#d7a647", "#9b7027"], "Rosée": ["#ffece6", "#d99a8c", "#9b5f53"] };

  function dessiner() {
    var t = texte ? texte.value : "";
    var pol = police ? police.value : "Manuscrite";
    if (type === "jonc") return window.LOU_jonc(vue, t || (texte && texte.placeholder.replace("Ex. : ", "")), pol, finition);
    if (type === "prenom") {
      var m = METAL[finition] || METAL["Argentée"], n = esc(t || "Emma");
      vue.innerHTML = '<svg class="prenom-svg" viewBox="0 0 520 360" role="img" aria-label="Aperçu du collier : ' + n + '"><defs><linearGradient id="pm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + m[0] + '"/><stop offset=".55" stop-color="' + m[1] + '"/><stop offset="1" stop-color="' + m[2] + '"/></linearGradient></defs>' +
        '<path d="M20,10 Q140,210 200,214 M320,214 Q380,210 500,10" fill="none" stroke="' + m[1] + '" stroke-width="3" stroke-dasharray="7 4"/>' +
        '<text x="260" y="240" text-anchor="middle" fill="url(#pm)" stroke="' + m[2] + '" stroke-width="1.2" style="font-family:' + (pol === "Moderne" ? "Montserrat,Arial;font-weight:700;font-size:62px;letter-spacing:4px" : "\'Great Vibes\',cursive;font-size:96px") + '">' + n + "</text></svg>";
      return;
    }
    if (type === "photo") {
      var mm = METAL[finition] || METAL["Argentée"];
      vue.innerHTML = '<svg viewBox="0 0 400 400" style="width:100%;max-width:420px" role="img" aria-label="Aperçu du pendentif avec votre photo"><defs><linearGradient id="hm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="' + mm[0] + '"/><stop offset=".6" stop-color="' + mm[1] + '"/><stop offset="1" stop-color="' + mm[2] + '"/></linearGradient><clipPath id="hc"><circle cx="200" cy="218" r="70"/></clipPath></defs>' +
        '<path d="M120,10 Q170,90 200,92 Q230,90 280,10" fill="none" stroke="' + mm[1] + '" stroke-width="3" stroke-dasharray="7 4"/>' +
        '<path d="M200,350 C110,290 60,240 70,170 C80,110 150,95 200,140 C250,95 320,110 330,170 C340,240 290,290 200,350Z" fill="url(#hm)" stroke="' + mm[2] + '" stroke-width="2"/>' +
        '<circle cx="200" cy="218" r="74" fill="#fff" opacity=".8"/>' +
        (photoURL ? '<image href="' + photoURL + '" x="130" y="148" width="140" height="140" preserveAspectRatio="xMidYMid slice" clip-path="url(#hc)"/>' : '<text x="200" y="226" text-anchor="middle" style="font:700 18px Nunito,Arial" fill="#7d5a69">Votre photo ici</text>') +
        '<circle cx="200" cy="218" r="70" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/></svg>';
      return;
    }
    if (type === "morse") {
      var mot = (t || "TOUJOURS").toUpperCase().replace(/[^A-Z]/g, "");
      var fil = COULEUR_FIL[finition] || "#222";
      var html = '<div style="display:grid;gap:18px;justify-items:center;width:100%"><div class="morse" style="--fil:' + fil + '"><i class="sep"></i>';
      mot.split("").forEach(function (l, i) {
        (M[l] || "").split("").forEach(function (s) { html += '<i class="' + (s === "." ? "p" : "t") + '"></i>'; });
        html += '<i class="sep"></i>' + (i < mot.length - 1 ? '<i class="sep"></i>' : "");
      });
      html += '</div><p class="hand" style="margin:0;text-align:center">' + esc(mot.split("").join(" ")) + '<br><span class="small" style="font-family:Nunito">' + esc(mot.split("").map(function (l) { return (M[l] || "").replace(/\./g, "•").replace(/-/g, "—"); }).join("  ")) + "</span></p></div>";
      vue.innerHTML = html;
    }
  }

  /* --- Galerie --- */
  function montrer(i) {
    vue.style.opacity = i < 0 ? 1 : 0;
    imgs.forEach(function (im, k) { im.style.opacity = k === i ? 1 : 0; });
    $$(".vignettes button").forEach(function (b) { b.classList.toggle("is-on", +b.getAttribute("data-vue") === i); });
  }
  $$(".vignettes button").forEach(function (b) { b.addEventListener("click", function () { montrer(+b.getAttribute("data-vue")); }); });

  /* --- Finitions (variantes) --- */
  function choisirFinition(b) {
    $$(".finition:not(.police-btn)").forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-checked", "false"); });
    b.classList.add("is-on"); b.setAttribute("aria-checked", "true");
    finition = b.getAttribute("data-nom");
    $("#variante").value = b.getAttribute("data-id");
    var fn = $("#finition-nom"); if (fn) fn.textContent = finition;
    ["#prix", "#prix-btn"].forEach(function (s) { var e = $(s); if (e) e.textContent = b.getAttribute("data-prix"); });
    dessiner(); montrer(-1);
  }
  $$(".finition:not(.police-btn)").forEach(function (b) { b.addEventListener("click", function () { choisirFinition(b); }); });
  $$(".police-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      $$(".police-btn").forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-checked", "false"); });
      b.classList.add("is-on"); b.setAttribute("aria-checked", "true"); police.value = b.getAttribute("data-police"); dessiner(); montrer(-1);
    });
  });

  /* --- Texte + compteurs + suggestions --- */
  $$(".perso-texte").forEach(function (inp) {
    var cpt = inp.closest(".champ").querySelector(".compteur");
    var maj = function () {
      if (inp.classList.contains("maj")) inp.value = inp.value.toUpperCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^A-Z]/g, "");
      if (cpt) { cpt.textContent = inp.value.length + " / " + cpt.getAttribute("data-max"); cpt.classList.toggle("trop", inp.value.length >= +cpt.getAttribute("data-max")); }
      dessiner(); montrer(-1);
    };
    inp.addEventListener("input", maj);
  });
  $$(".suggestions button").forEach(function (b) {
    b.addEventListener("click", function () { if (!texte) return; texte.value = b.textContent.slice(0, +texte.maxLength || 30); texte.dispatchEvent(new Event("input")); });
  });

  /* --- Photo --- */
  var fichier = $("#p-photo");
  if (fichier) fichier.addEventListener("change", function () {
    var f = fichier.files[0]; if (!f) return;
    if (f.size > 20 * 1024 * 1024) { window.LOU_toast && LOU_toast("Photo trop lourde (20 Mo maximum)"); fichier.value = ""; return; }
    if (photoURL) URL.revokeObjectURL(photoURL);
    photoURL = URL.createObjectURL(f);
    var d = $("#depot"); d.classList.add("ok"); d.querySelector("b").textContent = "Photo choisie ✔ (changer)";
    dessiner(); montrer(-1);
  });

  /* --- Valeurs reçues du test ou de la machine à mots (?texte=…&finition=…) --- */
  if (qs.get("finition")) { var fb = $$(".finition:not(.police-btn)").filter(function (b) { return b.getAttribute("data-nom") === qs.get("finition"); })[0]; if (fb) choisirFinition(fb); }
  if (qs.get("texte") && texte) { texte.value = qs.get("texte").slice(0, +texte.maxLength || 30); texte.dispatchEvent(new Event("input")); }

  dessiner(); montrer(-1);

  /* --- Ajout au panier --- */
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var err = $("#form-erreur"); err.textContent = "";
    var manque = $$("[required]", form).filter(function (el) { return el.type === "checkbox" ? !el.checked : el.type === "file" ? !el.files.length : !el.value.trim(); })[0];
    if (manque) {
      err.textContent = manque.id === "verif" ? "Cochez la case pour confirmer l'orthographe 💗" : manque.type === "file" ? "Ajoutez votre photo 📸" : "Écrivez vos mots avant d'ajouter au panier ✍️";
      (manque.closest(".champ") || manque.closest(".verif") || manque).scrollIntoView({ behavior: "smooth", block: "center" });
      if (manque.focus) manque.focus({ preventScroll: true });
      return;
    }
    var btn = $("#ajouter"); btn.disabled = true;
    window.LOU_ajouter(new FormData(form)).catch(function (x) { err.textContent = "Oups : " + x.message; }).then(function () { btn.disabled = false; });
  });

  /* --- Barre d'achat mobile --- */
  var barre = $("#barre-achat");
  if (barre && "IntersectionObserver" in window) new IntersectionObserver(function (es) { barre.classList.toggle("on", !es[0].isIntersecting && es[0].boundingClientRect.top < 0); }).observe(form);
})();
