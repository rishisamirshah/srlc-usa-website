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
  var _rm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (sp && !_rm) {
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

    /* Show more / less control (June 12 review) — default shows 3, reveals the rest if present. */
    var ACT_LIMIT = 3;
    var moreBtn = document.getElementById('activity-more');
    var countEl = document.getElementById('activity-count');
    if (countEl) { countEl.textContent = items.length + ' active'; }
    if (moreBtn) {
      if (items.length > ACT_LIMIT) {
        var actCollapse = function () {
          items.forEach(function (li, i) { li.hidden = i >= ACT_LIMIT; });
          moreBtn.setAttribute('aria-expanded', 'false');
          moreBtn.textContent = 'Show more';
        };
        var actExpand = function () {
          items.forEach(function (li) { li.hidden = false; });
          moreBtn.setAttribute('aria-expanded', 'true');
          moreBtn.textContent = 'Show less';
        };
        actCollapse();
        moreBtn.hidden = false;
        moreBtn.addEventListener('click', function () {
          if (moreBtn.getAttribute('aria-expanded') === 'true') { actCollapse(); } else { actExpand(); }
        });
      } else {
        moreBtn.hidden = true;
      }
    }

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

/* Keep the slide-in donate bar offset just below the sticky header (June 12 review). */
(function () {
  var header = document.querySelector('.site-header');
  if (!header) return;
  function setHeaderHeight() {
    document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }
  setHeaderHeight();
  window.addEventListener('resize', setHeaderHeight, { passive: true });
  if (window.ResizeObserver) {
    new ResizeObserver(setHeaderHeight).observe(header);
  }
})();

/* Site supplement JS (flat pass) — header state, rails, tabs, panels, map,
   forms, ZIP finder on the confirmed 12-jurisdiction / 22-center roster. */
(function () {
  "use strict";
  var doc = document;

  /* Header: solid + shadow on scroll (transparent over hero until then) */
  var header = doc.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 24);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Rails: drag-to-scroll + arrows */
  doc.querySelectorAll(".rail").forEach(function (rail) {
    var down = false, startX = 0, startL = 0, moved = 0;
    rail.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "touch") return;
      down = true; moved = 0; startX = e.clientX; startL = rail.scrollLeft;
      rail.setPointerCapture(e.pointerId);
    });
    rail.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - startX;
      if (Math.abs(dx) > 6) { rail.classList.add("dragging"); moved = 1; }
      rail.scrollLeft = startL - dx;
    });
    ["pointerup", "pointercancel"].forEach(function (ev) {
      rail.addEventListener(ev, function () {
        down = false;
        setTimeout(function () { rail.classList.remove("dragging"); }, 30);
      });
    });
    rail.addEventListener("click", function (e) { if (moved) { e.preventDefault(); moved = 0; } }, true);
  });
  doc.querySelectorAll("[data-rail-prev],[data-rail-next]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var sel = btn.getAttribute("data-rail-prev") || btn.getAttribute("data-rail-next");
      var rail = doc.querySelector(sel);
      if (!rail) return;
      var card = rail.firstElementChild;
      var w = card ? card.getBoundingClientRect().width + 16 : 340;
      rail.scrollBy({ left: btn.hasAttribute("data-rail-prev") ? -w : w, behavior: "smooth" });
    });
  });

  /* Tabs */
  doc.querySelectorAll("[data-tabs]").forEach(function (root) {
    var btns = root.querySelectorAll(".tabs__list button");
    var panels = root.querySelectorAll(".tabs__panel");
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-selected", "false"); });
        panels.forEach(function (p) { p.classList.remove("active"); });
        b.setAttribute("aria-selected", "true");
        panels[i].classList.add("active");
      });
    });
  });

  /* Progress rail for scroll panels */
  var dots = doc.querySelectorAll(".progressrail a");
  if (dots.length && "IntersectionObserver" in window) {
    var pio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          dots.forEach(function (d) { d.classList.toggle("on", d.getAttribute("href") === "#" + en.target.id); });
        }
      });
    }, { threshold: 0.55 });
    doc.querySelectorAll(".carepanel").forEach(function (p) { pio.observe(p); });
  }

  /* Interactive US map */
  doc.querySelectorAll(".cf-map .cf-state--active, .edmap .cf-state--active, .edmap .edmap-dot").forEach(function (p) {
    var href = p.getAttribute("data-href");
    if (!href) return;
    p.setAttribute("tabindex", "0");
    p.setAttribute("role", "link");
    p.setAttribute("aria-label", p.getAttribute("data-name") || "");
    p.style.cursor = "pointer";
    p.addEventListener("click", function () { window.location.href = href; });
    p.addEventListener("keydown", function (e) { if (e.key === "Enter") window.location.href = href; });
  });
  doc.querySelectorAll("[data-state-target]").forEach(function (chip) {
    var cls = chip.getAttribute("data-state-target");
    chip.addEventListener("mouseenter", function () {
      doc.querySelectorAll(".cf-map ." + cls).forEach(function (p) { p.classList.add("is-flashed"); });
    });
    chip.addEventListener("mouseleave", function () {
      doc.querySelectorAll(".cf-map ." + cls).forEach(function (p) { p.classList.remove("is-flashed"); });
    });
  });

  /* Netlify forms with inline success (only after a real submit) */
  doc.querySelectorAll("form[data-netlify-inline]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form);
      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(data).toString()
      }).then(function () {
        var ok = form.querySelector(".form-success");
        if (ok) {
          form.querySelectorAll(".form-hidewrap").forEach(function (x) { x.style.display = "none"; });
          ok.style.display = "block";
        } else form.reset();
      }).catch(function () { form.submit(); });
    });
  });

  /* ZIP finder — confirmed roster: 11 states + D.C., 22 centers */
  var Z = {};
  function reg(prefixes, state, city, href, meta, others) {
    prefixes.forEach(function (p) { Z[p] = { state: state, city: city, href: href, meta: meta, others: others || [] }; });
  }
  var U = "/our-work/united-states/";
  reg(["85", "86"], "AZ", "Phoenix, AZ", U + "arizona/", "Arizona chapter: Phoenix. Meal services, school supply drives, and community care.");
  reg(["90", "91", "92", "93", "94", "95", "96"], "CA", "California", U + "california/", "California centers: San Francisco, Los Angeles, San Diego.", ["San Francisco", "Los Angeles", "San Diego"]);
  reg(["30", "31", "39"], "GA", "Atlanta, GA", U + "georgia/", "Georgia chapter: Atlanta. Hunger relief, school supply kits, and clothing drives.");
  reg(["60", "61", "62"], "IL", "Chicago, IL", U + "illinois/", "Illinois chapter: Chicago. Classroom of Change kits and food donations.");
  reg(["46", "47"], "IN", "Indianapolis, IN", U + "indiana/", "Indiana chapter: Indianapolis. Meals, mentoring, and Adopt-a-Street stewardship.");
  reg(["01", "02"], "MA", "Boston, MA", U + "massachusetts/", "Massachusetts chapter: Boston. Meal kits through Open Table and community support.");
  reg(["07", "08"], "NJ", "New Jersey", U + "new-jersey/", "New Jersey centers: Edison, Cherry Hill, Princeton, Parsippany.", ["Edison", "Cherry Hill", "Princeton", "Parsippany"]);
  reg(["10", "11", "12", "13", "14"], "NY", "New York", U + "new-york/", "New York centers: Long Island, Manhattan, Queens.", ["Long Island", "Manhattan", "Queens"]);
  reg(["15", "16", "17", "18", "19"], "PA", "Pennsylvania", U + "pennsylvania/", "Pennsylvania centers: East Stroudsburg, Philadelphia.", ["East Stroudsburg", "Philadelphia"]);
  reg(["75", "76", "77", "78", "79"], "TX", "Texas", U + "texas/", "Texas centers: Dallas, Austin, Houston.", ["Dallas", "Austin", "Houston"]);
  reg(["98", "99"], "WA", "Seattle, WA", U + "washington/", "Washington chapter: Seattle. Snack boxes and essentials for Eastside shelters.");
  reg(["20"], "DC", "Washington, D.C.", U + "washington-dc/", "D.C. chapter. Monthly meal service, school supply kits, and hygiene drives.");

  var input = doc.getElementById("zipInput");
  var result = doc.getElementById("zipResult");
  function hideChips() {
    var chips = doc.getElementById("zipChips");
    if (chips) chips.setAttribute("hidden", "");
  }
  function renderChips(others, href) {
    var chips = doc.getElementById("zipChips");
    var list = doc.getElementById("zipChipsList");
    if (!chips || !list) return;
    if (!others || !others.length) { hideChips(); return; }
    list.innerHTML = others.map(function (c) {
      return '<a class="cf-chip" href="' + href + '">' + c + "</a>";
    }).join("");
    chips.removeAttribute("hidden");
  }
  window.__cfZipLookup = function () {
    if (!input || !result) return;
    var z = (input.value || "").trim();
    var city = doc.getElementById("zipCity");
    var meta = doc.getElementById("zipMeta");
    var join = doc.getElementById("zipJoinBtn");
    result.removeAttribute("hidden");
    if (!/^\d{5}$/.test(z)) {
      city.textContent = "Enter a 5-digit ZIP";
      meta.textContent = "We'll match you to the closest SRLC USA chapter.";
      result.classList.remove("is-missing");
      hideChips();
      return;
    }
    var match = Z[z.substring(0, 2)];
    if (match) {
      city.textContent = "Your nearest chapter: " + match.city;
      meta.textContent = match.meta;
      if (join) { join.href = match.href; join.textContent = "Visit this chapter"; }
      result.classList.remove("is-missing");
      renderChips(match.others, match.href);
    } else {
      city.textContent = "We don't have a chapter in your area yet";
      meta.textContent = "Email " + "info@srlc-usa.org" + " to help start one, or volunteer with the nearest chapter remotely.";
      if (join) { join.href = "/get-involved/volunteer/"; join.textContent = "Volunteer anyway"; }
      result.classList.add("is-missing");
      hideChips();
    }
  };
  if (input) {
    input.addEventListener("keyup", function (e) { if (e.key === "Enter") window.__cfZipLookup(); });
    var zb = doc.getElementById("zipBtn");
    if (zb) zb.addEventListener("click", function (e) { e.preventDefault(); window.__cfZipLookup(); });
  }

  /* Footer year */
  doc.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();

/* Newsletter modal close wiring + session suppression */
(function () {
  var m = document.getElementById("newsletterModal");
  if (!m) return;
  document.querySelectorAll("[data-newsletter-close]").forEach(function (el) {
    el.addEventListener("click", function () {
      m.setAttribute("hidden", "");
      try { sessionStorage.setItem("nl-modal-shown", "1"); } catch (e) {}
    });
  });
})();
