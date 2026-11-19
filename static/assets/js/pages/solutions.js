// Widget de démonstration Chapitô (5 exemples dans les onglets) : le script n'est chargé qu'une fois,
// quand la section approche de l'écran (il pèse 1,3 Mo et charge ensuite les images des exemples).
(function () {
  var target = document.querySelector('chapito-static');
  if (!target) return;
  var load = function () {
    if (document.querySelector('script[data-chapito-static]')) return;
    var s = document.createElement('script');
    s.src = 'https://static.festival.chapi.to/chapito-static.js';
    s.dataset.chapitoStatic = '';
    document.body.appendChild(s);
  };
  if (!('IntersectionObserver' in window)) return load();
  var io = new IntersectionObserver(function (entries) {
    if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); load(); }
  }, { rootMargin: '600px 0px' });
  io.observe(target.closest('.w-tabs') || target);
})();
