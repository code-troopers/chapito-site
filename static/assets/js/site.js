// Accessibilité clavier des interactions Webflow (déclenchées au clic) et de la fiche client de /realisations.
(function () {
  // Entrée / Espace sur un élément role="button" qui n'est pas un vrai bouton : même effet qu'un clic
  document.addEventListener('keydown', function (e) {
    var el = e.target;
    if ((e.key === 'Enter' || e.key === ' ') && el.getAttribute && el.getAttribute('role') === 'button' && el.tagName !== 'BUTTON') {
      e.preventDefault();
      el.click();
    }
  });

  // FAQ (/pricing) : état ouvert/fermé annoncé aux lecteurs d'écran
  document.querySelectorAll('.faq3_question[aria-expanded]').forEach(function (q) {
    q.addEventListener('click', function () {
      q.setAttribute('aria-expanded', q.getAttribute('aria-expanded') === 'true' ? 'false' : 'true');
    });
  });

  // Fiche client (/realisations) : focus dans la fiche, Échap pour fermer, retour sur la carte d'origine
  var popup = document.querySelector('.clients-popup');
  var close = document.getElementById('popup-close');
  if (!popup || !close) return;
  var opener = null;
  var isOpen = function () { return getComputedStyle(popup).display !== 'none'; };
  document.querySelectorAll('.client-card').forEach(function (card) {
    card.addEventListener('click', function () {
      opener = card;
      // l'animation Webflow affiche la fiche juste après le clic
      setTimeout(function () { if (isOpen()) close.focus(); }, 350);
    });
  });
  close.addEventListener('click', function () {
    if (opener) { var o = opener; opener = null; setTimeout(function () { o.focus(); }, 350); }
  });
  document.addEventListener('keydown', function (e) {
    if (!isOpen()) return;
    if (e.key === 'Escape') { e.preventDefault(); close.click(); return; }
    if (e.key !== 'Tab') return;
    var items = Array.prototype.filter.call(
      popup.querySelectorAll('a[href], button, [tabindex="0"], input, select, textarea'),
      function (el) { return el.offsetParent !== null; }
    );
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (!popup.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    else if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
})();
