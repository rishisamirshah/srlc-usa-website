/* Subtle scroll parallax (Naman, Oct 20): the homepage Laxibhai story photo
   (a background image whose vertical position drifts around its crop,
   data-parallax-bg="x y"); .ifsplit__media--parallax imgs drift too (none on
   the site since Naman took it off the Inspiration photos). Desktop only,
   off for reduced motion. */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.ifsplit__media--parallax img'));
  var bgs = Array.prototype.slice.call(document.querySelectorAll('[data-parallax-bg]'));
  if ((!imgs.length && !bgs.length) || !window.matchMedia) return;
  var mq = window.matchMedia('(min-width: 900px) and (prefers-reduced-motion: no-preference)');
  var queued = false;
  // -1 when the box's centre is at the top of the viewport, 1 at the bottom
  function progress(r, vh) { return (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2); }
  function update() {
    queued = false;
    var vh = window.innerHeight, on = mq.matches;
    imgs.forEach(function (img) {
      if (!on) { img.style.transform = ''; return; }
      var r = img.parentNode.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      img.style.transform = 'translate3d(0,' + (progress(r, vh) * -0.06 * r.height).toFixed(1) + 'px,0)';
    });
    bgs.forEach(function (el) {
      var xy = el.getAttribute('data-parallax-bg').split(' ');
      if (!on) { el.style.backgroundPosition = xy[0] + '% ' + xy[1] + '%'; return; }
      var r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var y = Math.max(0, Math.min(100, +xy[1] + progress(r, vh) * 12));
      el.style.backgroundPosition = xy[0] + '% ' + y.toFixed(2) + '%';
    });
  }
  function queue() { if (!queued) { queued = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', queue, { passive: true });
  window.addEventListener('resize', queue);
  if (mq.addEventListener) mq.addEventListener('change', queue);
  update();
})();
