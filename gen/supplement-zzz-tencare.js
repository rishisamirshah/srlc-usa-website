/* 10 Care Program hub (Naman's approved mock, Oct 29-30): the care bar marks
   the Care on screen, and a click eases to that panel (about 0.55s to a
   neighbor, up to 1.4s across the page). Once scrolling stops within about a
   third of a screen of a panel's top, the page eases to it. The panel photos
   drift with the site-wide parallax (supplement-zz-px.js). Reduced motion
   jumps instead of easing and never snaps. */
(function () {
  var panels = Array.prototype.slice.call(document.querySelectorAll('.panel'));
  var links = Array.prototype.slice.call(document.querySelectorAll('#carebar a'));
  if (!panels.length || !links.length) return;
  var root = document.documentElement;
  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.carebar');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // the site scrolls smoothly by default, which would fight the easing here
  root.style.scrollBehavior = 'auto';

  function hdr() { return header ? header.getBoundingClientRect().height : 72; }
  function offset() { return hdr() + (bar ? bar.getBoundingClientRect().height : 62); }
  function sync() { root.style.setProperty('--hdr', Math.round(hdr()) + 'px'); }
  function phone() { return window.innerWidth <= 768; }
  function top(i) { return panels[i].getBoundingClientRect().top + window.scrollY - offset() + 1; }

  var last = -1;
  function current() {
    var cur = 0;
    panels.forEach(function (p, i) { if (p.getBoundingClientRect().top <= window.innerHeight * 0.5) cur = i; });
    links.forEach(function (a, i) {
      var on = i === cur;
      a.classList.toggle('cur', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
    if (cur !== last && phone()) {
      var a = links[cur], ul = a.parentElement.parentElement;
      ul.scrollTo({ left: a.offsetLeft - (ul.clientWidth - a.offsetWidth) / 2, behavior: reduced ? 'auto' : 'smooth' });
    }
    last = cur;
  }

  var anim = null, snapping = false, timer = null;
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function smoothTo(y, done) {
    if (anim) cancelAnimationFrame(anim);
    if (reduced) { window.scrollTo(0, y); if (done) done(); return; }
    var s = window.scrollY, d = y - s, dur = Math.min(1400, 550 + Math.abs(d) * 0.12), t0 = performance.now();
    function step(now) {
      var t = Math.min(1, (now - t0) / dur);
      window.scrollTo(0, s + d * ease(t));
      if (t < 1) anim = requestAnimationFrame(step); else { anim = null; if (done) done(); }
    }
    anim = requestAnimationFrame(step);
  }

  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      snapping = true;
      smoothTo(top(i), function () { setTimeout(function () { snapping = false; }, 150); });
      history.replaceState(null, '', a.getAttribute('href'));
      panels[i].setAttribute('tabindex', '-1');
      panels[i].focus({ preventScroll: true });
    });
  });

  window.addEventListener('scroll', function () {
    current();
    if (reduced || snapping) return;
    clearTimeout(timer);
    timer = setTimeout(function () {
      var y = window.scrollY, H = window.innerHeight - offset(), best = null, bd = 1e9;
      panels.forEach(function (p, i) { var t = top(i), d = Math.abs(y - t); if (d < H * 0.35 && d < bd) { bd = d; best = t; } });
      if (best !== null && bd > 2) {
        snapping = true;
        smoothTo(best, function () { setTimeout(function () { snapping = false; }, 150); });
      }
    }, 160);
  }, { passive: true });
  window.addEventListener('resize', function () { sync(); current(); });
  sync();
  current();
})();
