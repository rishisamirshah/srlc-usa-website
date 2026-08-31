/* Our Work supplement (Aug 30): sticky jump strip on the 10 Care + India hubs.
   Measures the fixed site header so the strip sits flush beneath it, keeps
   anchor scrolling clear of both, and underlines the panel in view. */
(function () {
  var doc = document;
  var strip = doc.querySelector(".jumpstrip");
  if (!strip) return;
  var header = doc.querySelector(".site-header");
  var links = Array.prototype.slice.call(strip.querySelectorAll("a[href^='#']"));
  var list = strip.querySelector(".jumpstrip__list");

  function measure() {
    var h = header ? header.offsetHeight : 72;
    strip.style.setProperty("--jumpstrip-top", h + "px");
    doc.documentElement.style.scrollPaddingTop = (h + strip.offsetHeight + 8) + "px";
  }
  measure();
  window.addEventListener("resize", measure);
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(measure);

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function setActive(id) {
    links.forEach(function (a) {
      var on = a.getAttribute("href") === "#" + id;
      a.classList.toggle("on", on);
      if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      if (on && list && list.scrollWidth > list.clientWidth) {
        var left = a.offsetLeft - (list.clientWidth - a.offsetWidth) / 2;
        if (reduced) list.scrollLeft = left;
        else list.scrollTo({ left: left, behavior: "smooth" });
      }
    });
  }

  var panels = links.map(function (a) { return doc.getElementById(a.getAttribute("href").slice(1)); })
                    .filter(Boolean);
  if (!panels.length) return;

  if ("IntersectionObserver" in window) {
    var ratios = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { ratios[en.target.id] = en.isIntersecting ? en.intersectionRatio : 0; });
      var best = null, bestR = 0;
      panels.forEach(function (p) {
        var r = ratios[p.id] || 0;
        if (r > bestR) { bestR = r; best = p; }
      });
      if (best) setActive(best.id);
      else if (window.scrollY < panels[0].offsetTop) links.forEach(function (a) { a.classList.remove("on"); a.removeAttribute("aria-current"); });
    }, { rootMargin: "-40% 0px -40% 0px", threshold: [0, 0.1, 0.25, 0.5, 0.75, 1] });
    panels.forEach(function (p) { io.observe(p); });
  } else {
    setActive(panels[0].id);
  }

  links.forEach(function (a) {
    a.addEventListener("click", function () { setActive(a.getAttribute("href").slice(1)); });
  });
})();
