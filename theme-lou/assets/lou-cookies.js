/* Bandeau cookies (RGPD) relié à l'API de consentement de Shopify — repris de Corps-Confiant (cc-base.js), 05/11/2026.
   « Tout accepter / Tout refuser / Personnaliser » → Shopify.customerPrivacy.setTrackingConsent : c'est ce choix qui
   débloque (ou non) la balise Pinterest, l'API de conversion et Google Analytics installés par les applis Shopify.
   Si la bannière de cookies de Shopify est activée dans l'admin, on ne montre pas un 2e bandeau. */
(function () {
  var $ = function (s) { return document.querySelector(s); };
  var box = $("#cookie");
  if (!box) return;
  var CLE = "lou-cookies", api = null, reduit = matchMedia("(prefers-reduced-motion: reduce)").matches;
  function avecConsentement(cb) {
    if (api) return cb(api);
    if (!window.Shopify || !Shopify.loadFeatures) return cb(null);
    Shopify.loadFeatures([{ name: "consent-tracking-api", version: "0.1" }], function (err) { api = err ? null : window.Shopify.customerPrivacy; cb(api); });
  }
  function enregistrer(mesure, pub) {
    try { localStorage.setItem(CLE, JSON.stringify({ analytics: mesure, marketing: pub, at: Date.now() })); } catch (e) {}
    avecConsentement(function (a) { if (a) a.setTrackingConsent({ analytics: mesure, marketing: pub, preferences: true, sale_of_data: pub }, function () {}); });
    box.classList.remove("show");
    setTimeout(function () { box.hidden = true; }, reduit ? 0 : 400);
  }
  function ouvrir(perso) {
    box.hidden = false;
    $("#cookie-prefs").hidden = !perso;
    $("#cookie-custom").textContent = perso ? "Enregistrer mes choix" : "Personnaliser";
    requestAnimationFrame(function () { box.classList.add("show"); });
  }
  var dejaChoisi = function () { try { return !!localStorage.getItem(CLE); } catch (e) { return false; } };
  $("#cookie-accept").addEventListener("click", function () { enregistrer(true, true); });
  $("#cookie-refuse").addEventListener("click", function () { enregistrer(false, false); });
  $("#cookie-custom").addEventListener("click", function () {
    if ($("#cookie-prefs").hidden) { ouvrir(true); return; }
    enregistrer($("#ck-analytics").checked, $("#ck-marketing").checked);
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest("[data-cookie-settings]")) return;
    e.preventDefault();
    // Bannière Shopify active : on ouvre ses préférences ; sinon notre bandeau, choix détaillés
    if (window.privacyBanner && api && api.shouldShowBanner && api.shouldShowBanner()) { window.privacyBanner.showPreferences(); return; }
    ouvrir(true);
  });
  // Choix déjà fait (chez Shopify) ? Seulement si la visiteuse a vraiment dit oui ou non : toute autre réponse
  // (vide, « no_interaction », fonction absente selon la version de l'API) = pas de choix → on demande. (correctif 05/11)
  function choixFait(a) {
    try {
      if (a && a.currentVisitorConsent) {
        var c = a.currentVisitorConsent() || {};
        return ["analytics", "marketing"].some(function (k) { return c[k] === "yes" || c[k] === "no"; });
      }
      if (a && a.getTrackingConsent) { var t = a.getTrackingConsent(); return t === "yes" || t === "no"; }
    } catch (e) {}
    return false;
  }
  // 14/11 (décision utilisateur, temporaire) : réglage du thème « Afficher le bandeau automatiquement » décoché → pas d'ouverture
  // automatique ; sans choix, Shopify ne mesure rien (France = accord requis). « Gérer mes cookies » rouvre toujours le bandeau.
  if (!dejaChoisi() && box.getAttribute("data-auto") !== "false") {
    var fait = false;
    var decider = function (a) {
      if (fait) return; fait = true;
      if (choixFait(a)) return;                                                  // choix déjà fait ailleurs
      if (a && a.shouldShowBanner && a.shouldShowBanner() && window.privacyBanner) return;   // bannière Shopify active
      setTimeout(function () { ouvrir(false); }, 900);
    };
    avecConsentement(decider);
    setTimeout(function () { decider(api); }, 2500);   // Shopify ne répond pas : on demande quand même
  }
})();
