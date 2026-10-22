/* Our Impact milestone timeline (Naman, Oct 22). The year rail is a tablist:
   clicking a year, the arrows, or Left/Right/Home/End on the rail shows that
   milestone; the purple line and the filled squares run up to the selected
   year. No scroll-triggered animation. On phones the rail scrolls sideways and
   keeps the selected year in view. */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('.itl'), function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('.itl__yr'));
    var panels = Array.prototype.slice.call(root.querySelectorAll('.itl__panel'));
    var scroller = root.querySelector('.itl__scroll');
    var cur = 0;

    function show(i, focusTab) {
      if (i < 0 || i >= tabs.length) return;
      cur = i;
      root.style.setProperty('--i', i);
      tabs.forEach(function (t, k) {
        t.setAttribute('aria-selected', k === i ? 'true' : 'false');
        t.tabIndex = k === i ? 0 : -1;
        t.classList.toggle('is-done', k < i);
      });
      panels.forEach(function (p, k) {
        var on = k === i;
        p.classList.toggle('is-on', on);
        if (on) { p.removeAttribute('aria-hidden'); p.inert = false; }
        else { p.setAttribute('aria-hidden', 'true'); p.inert = true; }
      });
      var t = tabs[i];
      if (scroller && scroller.scrollWidth > scroller.clientWidth) {
        scroller.scrollTo({ left: t.offsetLeft - (scroller.clientWidth - t.offsetWidth) / 2, behavior: 'smooth' });
      }
      if (focusTab) t.focus({ preventScroll: true });
    }

    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { show(k); });
      t.addEventListener('keydown', function (e) {
        var to = { ArrowRight: cur + 1, ArrowLeft: cur - 1, Home: 0, End: tabs.length - 1 }[e.key];
        if (to === undefined) return;
        e.preventDefault();
        show(Math.max(0, Math.min(tabs.length - 1, to)), true);
      });
    });
    root.addEventListener('click', function (e) {
      var b = e.target.closest('.itl__arrow');
      if (!b || b.disabled) return;
      var to = cur + Number(b.getAttribute('data-step'));
      show(to);
      // keep keyboard focus on the matching arrow of the new slide
      var next = panels[cur] && panels[cur].querySelector('.itl__arrow[data-step="' + b.getAttribute('data-step') + '"]');
      if (next && !next.disabled) next.focus({ preventScroll: true });
      else if (panels[cur]) panels[cur].querySelector('.itl__arrow:not([disabled])').focus({ preventScroll: true });
    });
  });
})();
