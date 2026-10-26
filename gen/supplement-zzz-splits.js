/* Every photo-and-text split on a page is as tall as the tallest one
   (Naman, Oct 24). Side by side only (861px and up); stacked splits keep
   their own height. Who We Are's three adjacent splits use their own grid. */
(function () {
  var splits = Array.prototype.slice.call(document.querySelectorAll('.storysplit:not(.storysplit--text):not(.storysplit--wwa)'));
  if (splits.length < 2) return;
  var root = document.documentElement;
  function size() {
    if (window.innerWidth < 861) { root.style.removeProperty('--split-h'); return; }
    root.style.setProperty('--split-h', '0px');
    var max = 0;
    splits.forEach(function (s) { max = Math.max(max, s.getBoundingClientRect().height); });
    root.style.setProperty('--split-h', Math.ceil(max) + 'px');
  }
  size();
  window.addEventListener('load', size);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(size);
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(size, 120); });
})();
