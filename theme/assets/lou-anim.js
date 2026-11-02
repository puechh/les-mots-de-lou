/* Les Mots de Lou — animations GSAP (v0.2, 02/11/2026), inspirées de Corps-Confiant / Ciao Kombucha / Lily's Treasures.
   Tout reste lisible sans ce fichier (et si « réduire les animations » est activé sur l'appareil). */
(function () {
  "use strict";
  var reduit = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduit || !window.gsap) return;
  var g = window.gsap, ST = window.ScrollTrigger;
  if (ST) g.registerPlugin(ST);
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var un = function (sel) { $$(sel).forEach(function (e) { e.classList.remove("rv"); }); return $$(sel); };

  /* Accueil : le titre se révèle ligne par ligne, la photo de Lou entre en douceur, la bulle de Lou rebondit */
  var lignes = $$(".hero h1 .ligne > span");
  if (lignes.length) {
    g.from(lignes, { yPercent: 115, duration: 1.1, stagger: .14, ease: "power4.out", delay: .1, onComplete: function () { $$(".hero .trait").forEach(function (t) { t.classList.add("vu"); }); } });
    g.from(".hero-photo", { scale: .92, rotate: -2, opacity: 0, duration: 1.1, ease: "power3.out" });
    g.from(".hero .lou-dit", { y: 30, scale: .9, opacity: 0, duration: .8, ease: "back.out(1.8)", delay: .35 });
    g.from(".hero .sticker", { scale: 0, rotate: function (i) { return i ? 40 : -40; }, duration: .8, stagger: .15, ease: "back.out(2)", delay: .7 });
    g.from(".atelier", { y: 40, opacity: 0, duration: .9, ease: "power3.out", delay: .45 });
    g.from(".hero-cta .btn", { y: 20, opacity: 0, duration: .6, stagger: .1, ease: "back.out(1.6)", delay: .8 });
    if (ST) g.to(".hero-photo img", { yPercent: 8, scale: 1.08, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });
  }

  if (!ST) return;

  /* Ruban de mots : il se balance au défilement */
  $$(".ticker").forEach(function (t) { g.fromTo(t, { rotate: -3 }, { rotate: 1, ease: "none", scrollTrigger: { trigger: t, start: "top bottom", end: "bottom top", scrub: true } }); });

  /* Cartes produits « scrapbook » : elles tombent en place, chacune avec sa rotation */
  var cartes = un(".grille .carte");
  if (cartes.length) {
    g.set(cartes, { y: 90, opacity: 0, rotation: function () { return g.utils.random(-14, 14); } });
    ST.batch(cartes, { start: "top 92%", once: true, onEnter: function (b) { g.to(b, { y: 0, opacity: 1, rotation: 0, duration: 1, stagger: .09, ease: "back.out(1.5)" }); } });
  }
  $$(".note-lou").forEach(function (n) { g.from(n, { opacity: 0, scale: .5, rotate: -30, duration: .7, ease: "back.out(2)", scrollTrigger: { trigger: n.parentNode, start: "top 80%" }, delay: .6 }); });

  /* Cartes « problème → solution » : elles s'envolent en désordre */
  var cr = un(".carte-r");
  if (cr.length) {
    g.set(cr, { scale: .6, opacity: 0, rotation: function () { return g.utils.random(-14, 14); } });
    ST.create({ trigger: "#retourne", start: "top 85%", once: true, onEnter: function () { g.to(cr, { scale: 1, opacity: 1, rotation: 0, duration: .8, stagger: { each: .08, from: "random" }, ease: "back.out(1.7)" }); } });
  }

  /* Étapes, test, machine, Lou, Noël */
  var et = un(".etape");
  if (et.length) { g.set(et, { y: 60, opacity: 0, rotation: function (i) { return i % 2 ? 4 : -4; } }); ST.batch(et, { start: "top 90%", once: true, onEnter: function (b) { g.to(b, { y: 0, opacity: 1, rotation: 0, duration: .9, stagger: .12, ease: "back.out(1.5)" }); } }); }
  $$(".machine-boite").forEach(function (m) { m.classList.remove("rv"); g.from(m, { y: 60, rotation: 3, opacity: 0, duration: 1, ease: "back.out(1.4)", scrollTrigger: { trigger: m, start: "top 85%" } }); });
  $$(".lou-photo").forEach(function (p) { p.classList.remove("rv"); g.from(p, { x: -80, rotation: -14, opacity: 0, duration: 1.1, ease: "power3.out", scrollTrigger: { trigger: p, start: "top 85%" } }); });
  $$(".lou-infos span").forEach(function (s, i) { g.from(s, { scale: 0, opacity: 0, duration: .5, delay: i * .1, ease: "back.out(2.2)", scrollTrigger: { trigger: s, start: "top 92%" } }); });
  $$(".noel").forEach(function (n) { n.classList.remove("rv"); g.from(n, { scale: .9, opacity: 0, duration: .9, ease: "back.out(1.5)", scrollTrigger: { trigger: n, start: "top 85%" } }); });
  $$(".compte div").forEach(function (d, i) { g.from(d, { y: 30, rotationX: 90, opacity: 0, duration: .6, delay: .2 + i * .1, ease: "back.out(1.6)", scrollTrigger: { trigger: d, start: "top 92%" } }); });
  $$(".head .hand").forEach(function (h) { g.from(h, { rotate: -8, scale: .7, opacity: 0, duration: .7, ease: "back.out(2)", scrollTrigger: { trigger: h, start: "top 92%" } }); });

  /* Fiche produit : le contenu arrive en cascade */
  var fi = $$(".fiche-info > *");
  if (fi.length) {
    g.from(".fiche-galerie", { scale: .95, opacity: 0, duration: .8, ease: "power3.out" });
    g.from(fi.slice(0, 7), { y: 24, opacity: 0, duration: .6, stagger: .06, ease: "power3.out", delay: .1 });
  }

  /* Lou entre en scène (bouton en bas de l'écran) */
  var lb = document.getElementById("lou-btn");
  if (lb) g.from(lb, { scale: 0, rotation: -120, duration: .9, ease: "back.out(2)", delay: 1.2 });

  addEventListener("load", function () { ST.refresh(); });
})();
