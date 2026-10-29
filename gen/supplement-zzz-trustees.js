/* Management Team carousel (Naman, Oct 29): the arrows move one card at a
   time and switch off at either end; a card shows its bio on hover (CSS), and
   on tap or Enter/Space it toggles open and shut, for phones and tablets that
   have no hover. Opening one card closes the others. */
(function () {
  var vp = document.querySelector('.trustees__viewport');
  if (!vp) return;
  var cards = Array.prototype.slice.call(vp.querySelectorAll('.tcard'));
  var arrows = Array.prototype.slice.call(document.querySelectorAll('.trustees__arrow'));

  function step() {
    var a = cards[0], b = cards[1];
    return b ? b.getBoundingClientRect().left - a.getBoundingClientRect().left : vp.clientWidth;
  }
  function sync() {
    var max = vp.scrollWidth - vp.clientWidth - 2;
    arrows.forEach(function (btn) {
      var dir = Number(btn.getAttribute('data-step'));
      btn.disabled = dir < 0 ? vp.scrollLeft <= 2 : vp.scrollLeft >= max;
    });
  }
  arrows.forEach(function (btn) {
    btn.addEventListener('click', function () {
      vp.scrollBy({ left: Number(btn.getAttribute('data-step')) * step(), behavior: 'smooth' });
    });
  });
  var t;
  vp.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(sync, 60); }, { passive: true });
  window.addEventListener('resize', sync);
  sync();

  function setOpen(card, on) {
    card.classList.toggle('is-open', on);
    card.querySelector('.tcard__media').setAttribute('aria-expanded', on ? 'true' : 'false');
  }
  cards.forEach(function (card) {
    var btn = card.querySelector('.tcard__media');
    var bio = card.querySelector('.tcard__bio');
    btn.addEventListener('click', function () {
      var on = !card.classList.contains('is-open');
      cards.forEach(function (c) { if (c !== card) setOpen(c, false); });
      setOpen(card, on);
    });
    // a bio taller than the photo starts at its top, so it scrolls from line one
    function fit() { bio.classList.toggle('is-tall', bio.scrollHeight > bio.clientHeight + 1); }
    fit();
    window.addEventListener('resize', fit);
  });
})();
