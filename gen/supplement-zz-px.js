/* Site-wide parallax (Naman, Oct 27): each img.px drifts slower than the page
   inside its frame, by the 6% the photo runs past the frame at each end
   (supplement-zz-px.css), so an edge never shows. Off where the CSS keeps the
   photo flush with its frame (phones, tablets, reduced motion). The QA audit
   sets window.__pxForce to -1 or 1 to hold every photo at one end. */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('img.px'));
  if (!imgs.length) return;
  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight, force = window.__pxForce;
    imgs.forEach(function (img) {
      var frame = img.parentElement;
      var room = (img.offsetHeight - frame.clientHeight) / 2;
      if (room < 1) { img.style.removeProperty('--py'); return; }
      var r = frame.getBoundingClientRect();
      if (force === undefined && (r.bottom < -room || r.top > vh + room)) return;
      // -1 as the frame enters at the bottom of the screen, +1 as it leaves at the top
      var p = force !== undefined ? force : Math.max(-1, Math.min(1, (vh - r.top) / (vh + r.height) * 2 - 1));
      img.style.setProperty('--py', (p * room).toFixed(1) + 'px');
    });
  }
  function request() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  window.addEventListener('load', request);
  update();
})();
