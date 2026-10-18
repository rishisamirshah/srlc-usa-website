/* Institute rows: arrows step one card and disable at the ends. Every flip
   card flips on tap on touch screens (hover and keyboard focus flip via CSS). */
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var touch = window.matchMedia("(hover: none)");

  var track = document.getElementById("instrowTrack");
  if (track) {
    var arrows = document.querySelectorAll(".instrow__arrow");
    var step = function () {
      var card = track.querySelector(".flipcard");
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return card ? card.getBoundingClientRect().width + gap : 300;
    };
    var sync = function () {
      var max = track.scrollWidth - track.clientWidth - 2;
      arrows.forEach(function (b) {
        b.disabled = Number(b.getAttribute("data-dir")) < 0 ? track.scrollLeft <= 2 : track.scrollLeft >= max;
      });
    };
    arrows.forEach(function (b) {
      b.addEventListener("click", function () {
        track.scrollBy({ left: Number(b.getAttribute("data-dir")) * step(), behavior: reduce.matches ? "auto" : "smooth" });
      });
    });
    track.addEventListener("scroll", function () { window.requestAnimationFrame(sync); }, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  }

  var cards = document.querySelectorAll(".flipcard");
  cards.forEach(function (card) {
    card.addEventListener("click", function (e) {
      if (!touch.matches) return;
      if (e.target.closest("a") && card.classList.contains("is-flipped")) return;
      cards.forEach(function (c) { if (c !== card) c.classList.remove("is-flipped"); });
      card.classList.toggle("is-flipped");
    });
    card.addEventListener("keydown", function (e) {
      if ((e.key === "Enter" || e.key === " ") && e.target === card) {
        e.preventDefault();
        card.classList.toggle("is-flipped");
      }
    });
  });
})();

/* Mobile menu: a full-height sheet under the header; the page stays put behind it */
(function () {
  var header = document.querySelector(".site-header");
  var nav = header && header.querySelector(".primary-nav");
  if (!nav || !window.MutationObserver) return;
  function sync() {
    var open = nav.classList.contains("is-open") && window.innerWidth <= 900;
    nav.style.top = open ? Math.max(0, header.getBoundingClientRect().bottom) + "px" : "";
    document.documentElement.classList.toggle("nav-locked", open);
  }
  new MutationObserver(sync).observe(nav, { attributes: true, attributeFilter: ["class"] });
  window.addEventListener("resize", sync);
})();
