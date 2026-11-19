// Agenda cal.com « Être rappelé » : chargé seulement quand la section contact approche de l'écran
// (le module pèse environ 2 Mo et fait plus de 80 requêtes vers app.cal.com).
(function () {
  var target = document.getElementById('my-cal-inline-chapito-camping');
  if (!target) return;
  var init = function () {
    (function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
    Cal("init", "chapito-camping", { origin: "https://app.cal.com" });
    Cal.config = Cal.config || {};
    Cal.config.forwardQueryParams = true;
    Cal.ns["chapito-camping"]("inline", {
      elementOrSelector: "#my-cal-inline-chapito-camping",
      config: { "layout": "month_view", "useSlotsViewOnSmallScreen": true },
      calLink: "nicolasdm/chapito-camping",
    });
    Cal.ns["chapito-camping"]("ui", { "hideEventTypeDetails": false, "layout": "month_view" });
  };
  if (!('IntersectionObserver' in window)) return init();
  var io = new IntersectionObserver(function (entries) {
    if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); init(); }
  }, { rootMargin: '800px 0px' });
  io.observe(target);
})();
