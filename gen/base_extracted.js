(function(){
  if (typeof window === 'undefined') return;
  function reveal(){
    if (!('IntersectionObserver' in window)) {
      document.querySelectorAll('[data-vu-reveal]').forEach(function(n){ n.classList.add('vu-in'); });
      return;
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('vu-in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -32px 0px' });
    document.querySelectorAll('[data-vu-reveal]').forEach(function(n){ io.observe(n); });
  }
  if (document.readyState !== 'loading') reveal();
  else document.addEventListener('DOMContentLoaded', reveal);


  /* ===== Scroll progress bar ===== */
  var sp = document.getElementById('scrollProgress');
  if (sp && !reducedMotion) {
    var spUpdate = function() {
      var docH = document.documentElement.scrollHeight - window.innerHeight;
      var pct = docH > 0 ? (window.scrollY / docH) * 100 : 0;
      sp.style.width = pct + '%';
    };
    window.addEventListener('scroll', spUpdate, { passive: true });
    spUpdate();
  }
})();

(function(){
  var cards = document.querySelectorAll('.quote-card');
  var dots = document.querySelectorAll('.quote-wall__dots .qd');
  var idx = 0; var timer;
  function go(n) {
    cards[idx].classList.remove('is-active'); dots[idx].classList.remove('is-active');
    idx = (n + cards.length) % cards.length;
    cards[idx].classList.add('is-active'); dots[idx].classList.add('is-active');
  }
  function start(){ stop(); timer = setInterval(function(){go(idx+1);}, 6500); }
  function stop(){ if(timer){clearInterval(timer); timer=null;} }
  document.querySelectorAll('.quote-wall__btn').forEach(function(b){
    b.addEventListener('click', function(){ go(idx + (b.dataset.dir==='next'?1:-1)); start(); });
  });
  dots.forEach(function(d){ d.addEventListener('click', function(){ go(parseInt(d.dataset.go,10)); start(); }); });
  start();
})();

(function(){
  // Hero carousel logic — keyboard, dots, prev/next, auto-rotate
  var carousel = document.getElementById('heroCarousel');
  if (carousel) {
    var slides = carousel.querySelectorAll('.hero-carousel__slide');
    var dots = carousel.querySelectorAll('.dot');
    var idx = 0;
    var timer;
    function go(n){
      slides[idx].classList.remove('is-active');
      dots[idx].classList.remove('is-active');
      idx = (n + slides.length) % slides.length;
      slides[idx].classList.add('is-active');
      dots[idx].classList.add('is-active');
    }
    function start(){ stop(); timer = setInterval(function(){go(idx+1);}, 7000); }
    function stop(){ if(timer){ clearInterval(timer); timer=null; } }
    carousel.querySelector('[data-dir="prev"]').addEventListener('click', function(){go(idx-1); start();});
    carousel.querySelector('[data-dir="next"]').addEventListener('click', function(){go(idx+1); start();});
    dots.forEach(function(d){ d.addEventListener('click', function(){go(parseInt(d.dataset.go,10)); start();}); });
    carousel.addEventListener('mouseenter', stop);
    carousel.addEventListener('mouseleave', start);
    start();
  }
  // Newsletter popup — open after 8s the first session, suppress after dismiss for the session
  try {
    var m = document.getElementById('newsletterModal');
    if (m && !sessionStorage.getItem('newsletterDismissed')) {
      setTimeout(function(){ m.removeAttribute('hidden'); }, 8000);
    }
    document.querySelectorAll('[data-newsletter-close]').forEach(function(el){
      el.addEventListener('click', function(){
        m.setAttribute('hidden','');
        try { sessionStorage.setItem('newsletterDismissed','1'); } catch(e){}
      });
    });
  } catch(e){}
})();

(function(){
  // Tag the existing stat numbers for animation
  var stats = document.querySelectorAll('.impact-stat__n');
  var targets = ['27', '25', '250', '350'];
  stats.forEach(function(el, i){
    el.setAttribute('data-target', el.textContent.replace(/[^0-9]/g,'') || targets[i]);
    el.setAttribute('data-suffix', /\+/.test(el.textContent) ? '+' : (/M/.test(el.textContent)?'M+':''));
    el.textContent = '0';
  });
  var animated = new WeakSet();
  function animate(el) {
    if (animated.has(el)) return;
    animated.add(el);
    var target = parseInt(el.dataset.target, 10);
    var suffix = el.dataset.suffix || '';
    var dur = 1400, start = performance.now();
    function tick(now) {
      var p = Math.min(1, (now-start)/dur);
      var v = Math.round(target * (1 - Math.pow(1-p, 3)));
      el.textContent = v.toLocaleString() + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){ if (en.isIntersecting) animate(en.target); });
  }, {threshold:.5});
  stats.forEach(function(el){ io.observe(el); });
})();

(function(){
  if (typeof window === 'undefined') return;
  function init() {
    var triggers = document.querySelectorAll('.primary-nav__trigger');
    function closeAll(except){
      triggers.forEach(function(b){
        if (b !== except) b.setAttribute('aria-expanded', 'false');
      });
    }
    triggers.forEach(function(btn){
      btn.addEventListener('click', function(e){
        e.preventDefault();
        var expanded = btn.getAttribute('aria-expanded') === 'true';
        closeAll(btn);
        btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      });
    });
    document.addEventListener('click', function(e){
      if (!e.target.closest('.primary-nav__item')) closeAll(null);
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape') closeAll(null);
    });
    // Mobile drawer toggle
    document.querySelectorAll('.nav-toggle').forEach(function(btn){
      btn.addEventListener('click', function(){
        var nav = btn.closest('.site-header') &&
                  btn.closest('.site-header').querySelector('.primary-nav');
        if (!nav) return;
        var open = nav.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();

/* Newsletter modal: exit-intent OR 45s scroll trigger (was auto-open on load) */
(function () {
  var modal = document.getElementById("newsletterModal");
  if (!modal) return;
  var shown = false;
  var SCROLL_DELAY_MS = 45000;
  function showModal() {
    if (shown) return;
    shown = true;
    try { modal.removeAttribute("hidden"); } catch (e) {}
  }
  // Exit-intent: cursor leaves top of viewport
  document.addEventListener("mouseleave", function (e) {
    if (e.clientY <= 0 && !shown) showModal();
  });
  // 45s scrolling: user has been on page and engaged
  var scrolled = false;
  window.addEventListener("scroll", function () { scrolled = true; }, { passive: true });
  setTimeout(function () { if (scrolled) showModal(); }, SCROLL_DELAY_MS);
  // Suppress on session repeat
  if (sessionStorage.getItem("nl-modal-shown") === "1") shown = true;
  modal.addEventListener("close", function () { sessionStorage.setItem("nl-modal-shown", "1"); });
})();

(function(){
  var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ===== 1) IntersectionObserver fade-up reveal ===== */
  if ('IntersectionObserver' in window) {
    var reveals = document.querySelectorAll('.reveal');
    if (reveals.length) {
      var revealObs = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      reveals.forEach(function(el){ revealObs.observe(el); });
    }

    /* ===== 1b) Stat counter animation ===== */
    var statEls = document.querySelectorAll('.mstat__n, .count-up');
    if (statEls.length && !reducedMotion) {
      var counted = new WeakSet();
      var counterObs = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if (!entry.isIntersecting || counted.has(entry.target)) return;
          counted.add(entry.target);
          var el = entry.target;
          var raw = el.textContent.trim();
          var match = raw.match(/^([0-9]+\.?[0-9]*)\s*([A-Za-z+]*)/);
          if (!match) return;
          var target = parseFloat(match[1]);
          var suffix = match[2] || '';
          var duration = 1600;
          var start = performance.now();
          function step(now) {
            var p = Math.min(1, (now - start) / duration);
            var eased = 1 - Math.pow(1 - p, 3);
            var current = target * eased;
            var formatted = (target >= 100) ? Math.round(current) : current.toFixed(target >= 10 ? 1 : 2);
            el.textContent = formatted + suffix;
            if (p < 1) requestAnimationFrame(step);
            else el.textContent = raw;
          }
          requestAnimationFrame(step);
        });
      }, { threshold: 0.5 });
      statEls.forEach(function(el){ counterObs.observe(el); });
    }
  }

  /* ===== 2) Donate amount tiles ===== */
  var tiles = document.querySelectorAll('.donate-tile[data-amount]');
  var cta = document.getElementById('donate-tiles-cta');
  var monthlyNote = document.getElementById('donate-tiles-monthly-note');
  var toggleButtons = document.querySelectorAll('.donate-tiles__toggle button');
  var customInput = document.getElementById('custom-amount-input');
  var freq = 'once';
  function updateCTA() {
    var active = document.querySelector('.donate-tile.is-active');
    if (!active) return;
    var amount = active.dataset.amount;
    if (active.querySelector('input')) {
      amount = active.querySelector('input').value || '';
    }
    if (cta) {
      cta.textContent = amount ? 'Donate $' + amount + (freq === 'monthly' ? '/month now' : ' now') : 'Donate now';
    }
    if (monthlyNote) {
      monthlyNote.hidden = (freq !== 'monthly');
    }
    // Update outcome label if applicable
    var outcomeEl = active.querySelector('.donate-tile__outcome');
    if (outcomeEl && active.dataset.outcomeOnce) {
      outcomeEl.textContent = freq === 'monthly'
        ? (active.dataset.outcomeMonthly || active.dataset.outcomeOnce)
        : active.dataset.outcomeOnce;
    }
  }
  tiles.forEach(function(tile){
    tile.addEventListener('click', function(){
      document.querySelectorAll('.donate-tile').forEach(function(t){ t.classList.remove('is-active'); });
      tile.classList.add('is-active');
      updateCTA();
    });
  });
  if (customInput) {
    customInput.addEventListener('input', function(){
      document.querySelectorAll('.donate-tile').forEach(function(t){ t.classList.remove('is-active'); });
      customInput.closest('.donate-tile').classList.add('is-active');
      updateCTA();
    });
    customInput.addEventListener('click', function(e){ e.preventDefault(); });
  }
  toggleButtons.forEach(function(btn){
    btn.addEventListener('click', function(){
      toggleButtons.forEach(function(b){ b.classList.remove('is-active'); b.setAttribute('aria-selected','false'); });
      btn.classList.add('is-active');
      btn.setAttribute('aria-selected','true');
      freq = btn.dataset.freq;
      // Reset outcomes on all tiles to monthly/once variants
      document.querySelectorAll('.donate-tile').forEach(function(tile){
        var outcomeEl = tile.querySelector('.donate-tile__outcome');
        if (outcomeEl && tile.dataset.outcomeOnce) {
          outcomeEl.textContent = freq === 'monthly'
            ? (tile.dataset.outcomeMonthly || tile.dataset.outcomeOnce)
            : tile.dataset.outcomeOnce;
        }
      });
      updateCTA();
    });
  });

  /* ===== 3) Sticky donate bar — appears after hero leaves viewport ===== */
  var sticky = document.getElementById('stickyDonate');
  var stickyClose = document.getElementById('stickyDonateClose');
  if (sticky) {
    var dismissed = sessionStorage.getItem('sticky-donate-dismissed') === '1';
    if (!dismissed) {
      // Detect when hero is past
      var hero = document.querySelector('.hero-carousel, .hero, #heroCarousel');
      if (hero && 'IntersectionObserver' in window) {
        var heroObs = new IntersectionObserver(function(entries){
          entries.forEach(function(entry){
            if (!entry.isIntersecting) {
              sticky.classList.add('is-visible');
              sticky.setAttribute('aria-hidden','false');
            } else {
              sticky.classList.remove('is-visible');
              sticky.setAttribute('aria-hidden','true');
            }
          });
        }, { threshold: 0, rootMargin: '-80px 0px 0px 0px' });
        heroObs.observe(hero);
      }
    }
    if (stickyClose) {
      stickyClose.addEventListener('click', function(){
        sticky.classList.remove('is-visible');
        sticky.setAttribute('aria-hidden','true');
        sessionStorage.setItem('sticky-donate-dismissed','1');
      });
    }
  }

  /* ===== 5) Chapter activity rotation (subtle) ===== */
  var actList = document.getElementById('activity-list');
  if (actList) {
    var items = Array.from(actList.children);
    var idx = 0;
    // Soft visual shimmer on a rotating item every 6s
    if (!reducedMotion) {
      setInterval(function(){
        items.forEach(function(li){ li.style.transition = 'opacity 600ms'; li.style.opacity = '1'; });
        var target = items[idx % items.length];
        target.style.opacity = '0.55';
        setTimeout(function(){ target.style.opacity = '1'; }, 500);
        idx++;
      }, 6000);
    }
  }
})();

/* Subtle hero parallax: image lags scroll by 12%, capped at 50px. Desktop only, reduced-motion safe.
   NOTE: exceeds Brand Guide v3.1 motion spec (max 8px) per Naman's direction 2026-06-03; set MAX_SHIFT=8 and FACTOR=0.05 to restore strict compliance. */
(function () {
  var MAX_SHIFT = 50;
  var FACTOR = 0.12;
  var hero = document.getElementById('heroCarousel');
  if (!hero) return;
  var mqDesktop = window.matchMedia('(min-width: 900px)');
  var mqMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var ticking = false;
  function apply() {
    ticking = false;
    if (!mqDesktop.matches || mqMotion.matches) { hero.style.removeProperty('--hero-par'); return; }
    var y = Math.min(window.scrollY * FACTOR, MAX_SHIFT);
    hero.style.setProperty('--hero-par', y.toFixed(2) + 'px');
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(apply); }
  }, { passive: true });
  apply();
})();