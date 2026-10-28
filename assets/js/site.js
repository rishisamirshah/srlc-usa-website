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
  if (!cards.length) return;
  var idx = 0; var timer;
  function go(n) {
    cards[idx].classList.remove('is-active'); dots[idx].classList.remove('is-active');
    idx = (n + cards.length) % cards.length;
    cards[idx].classList.add('is-active'); dots[idx].classList.add('is-active');
  }
  function start(){ stop(); if (hold || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) return; timer = setInterval(function(){go(idx+1);}, 11000); }
  function stop(){ if(timer){clearInterval(timer); timer=null;} }
  document.querySelectorAll('.quote-wall__btn').forEach(function(b){
    b.addEventListener('click', function(){ go(idx + (b.dataset.dir==='next'?1:-1)); start(); });
  });
  dots.forEach(function(d){ d.addEventListener('click', function(){ go(parseInt(d.dataset.go,10)); start(); }); });
  var wall = document.querySelector('.quote-wall');
  var hold = false;
  if (wall) { wall.addEventListener('mouseenter', function(){ hold = true; stop(); }); wall.addEventListener('mouseleave', function(){ if (!wall.contains(document.activeElement)) { hold = false; start(); } }); wall.addEventListener('focusin', function(){ hold = true; stop(); }); wall.addEventListener('focusout', function(e){ if (!wall.contains(e.relatedTarget)) { hold = false; start(); } }); }
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
    function start(){ stop(); if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return; timer = setInterval(function(){go(idx+1);}, 7000); }
    function stop(){ if(timer){ clearInterval(timer); timer=null; } }
    carousel.querySelector('[data-dir="prev"]').addEventListener('click', function(){go(idx-1); start();});
    carousel.querySelector('[data-dir="next"]').addEventListener('click', function(){go(idx+1); start();});
    dots.forEach(function(d){ d.addEventListener('click', function(){go(parseInt(d.dataset.go,10)); start();}); });
    carousel.addEventListener('mouseenter', stop);
    carousel.addEventListener('mouseleave', start);
    carousel.addEventListener('focusin', stop);
    carousel.addEventListener('focusout', start);
    start();
  }
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
    var statEls = document.querySelectorAll('.mstat__n');
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

/* ---- supplement.js ---- */
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
    function select(i, focus) {
      btns.forEach(function (x, k) { x.setAttribute("aria-selected", k === i ? "true" : "false"); x.tabIndex = k === i ? 0 : -1; });
      panels.forEach(function (p, k) { p.classList.toggle("active", k === i); });
      if (focus) btns[i].focus();
    }
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () { select(i, false); });
      b.addEventListener("keydown", function (e) {
        var n = btns.length, to = null;
        if (e.key === "ArrowRight") to = (i + 1) % n;
        else if (e.key === "ArrowLeft") to = (i - 1 + n) % n;
        else if (e.key === "Home") to = 0;
        else if (e.key === "End") to = n - 1;
        if (to !== null) { e.preventDefault(); select(to, true); }
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
      }).then(function (res) {
        if (!res.ok) throw new Error("form post " + res.status);
        var ok = form.querySelector(".form-success");
        if (ok) {
          form.querySelectorAll(".form-hidewrap").forEach(function (x) { x.style.display = "none"; });
          ok.style.display = "block";
          var box = form.closest(".nlrow, .newsletter-modal__panel");
          if (box) box.classList.add("is-subscribed");
        } else form.reset();
      }).catch(function () {
        // never fall through to a native POST: it lands on the 404 page
        if (form.querySelector(".form-error")) return;
        var err = doc.createElement("span");
        err.className = "form-error";
        err.setAttribute("role", "alert");
        err.textContent = "Something went wrong. Please try again in a moment.";
        form.appendChild(err);
      });
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
    if (join) join.style.display = "";
    if (!/^\d{5}$/.test(z)) {
      if (join) join.style.display = "none";
      result.classList.add("is-hint");
      city.textContent = "Enter a 5-digit ZIP";
      meta.textContent = "We'll match you to the closest SRLC USA chapter.";
      meta.hidden = false;
      result.classList.remove("is-missing");
      hideChips();
      return;
    }
    result.classList.remove("is-hint");
    var match = Z[z.substring(0, 2)];
    var vol = doc.getElementById("zipVolBtn");
    var chipsOnly = result.hasAttribute("data-chips-only");
    if (vol) vol.style.display = "";
    if (match) {
      city.textContent = "Your nearest chapter: " + match.city;
      /* homepage (Naman, Oct 20): the chips already list the centers, so no centers line */
      meta.textContent = chipsOnly ? "" : match.meta;
      meta.hidden = chipsOnly;
      if (join) { join.href = match.href; join.textContent = "Visit this chapter"; }
      result.classList.remove("is-missing");
      renderChips(match.others, match.href);
    } else {
      city.textContent = "We don't have a chapter in your area yet";
      meta.textContent = "Email " + "info@srlcusa.org" + " to help start one, or volunteer with the nearest chapter remotely.";
      meta.hidden = false;
      if (join) { join.href = "/get-involved/volunteer/#signup"; join.textContent = "Volunteer anyway"; }
      if (vol) vol.style.display = "none";
      result.classList.add("is-missing");
      hideChips();
    }
  };
  if (input) {
    input.addEventListener("keyup", function (e) { if (e.key === "Enter") window.__cfZipLookup(); });
    var zb = doc.getElementById("zipBtn");
    if (zb) zb.addEventListener("click", function (e) { e.preventDefault(); window.__cfZipLookup(); });
  }

  /* Desktop nav: a clicked (aria-expanded) panel must not stay open while the
     pointer hovers a sibling item, or two panels overlap (Riyan, Sept 3). */
  var navItems = doc.querySelectorAll(".primary-nav__item");
  var canHover = window.matchMedia && window.matchMedia("(hover: hover)").matches;
  if (canHover && navItems.length) {
    function closeExpanded() {
      doc.querySelectorAll('.primary-nav__trigger[aria-expanded="true"]').forEach(function (b) {
        b.setAttribute("aria-expanded", "false");
      });
      /* the clicked trigger keeps focus, and :focus-within holds its panel open */
      var a = doc.activeElement;
      if (a && a.classList && a.classList.contains("primary-nav__trigger")) a.blur();
    }
    navItems.forEach(function (item) {
      item.addEventListener("mouseenter", closeExpanded);
      item.addEventListener("mouseleave", closeExpanded);
    });
  }

  /* 10 Care accordion below 1024 (SRA SI-r19 pattern, exclusive): a tap opens
     the row and reveals its one-liner; a second tap on the open row follows
     the link. Desktop hover is untouched. */
  var careGrid = doc.querySelector(".caregrid");
  if (careGrid && window.matchMedia) {
    var careMq = window.matchMedia("(max-width: 1023px)");
    careGrid.addEventListener("click", function (e) {
      if (!careMq.matches) return;
      var tile = e.target.closest(".caretile");
      if (!tile || !careGrid.contains(tile)) return;
      if (tile.classList.contains("is-open")) return;
      e.preventDefault();
      careGrid.querySelectorAll(".caretile.is-open").forEach(function (t) { t.classList.remove("is-open"); });
      tile.classList.add("is-open");
    });
  }

  /* Footer year */
  doc.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();


/* ---- supplement-donate.js ---- */
/* Donate page (ported from Naman's donate.html): giving widget and accordions;
   the hero drifts with the site-wide parallax (supplement-zz-px.js).
   Everything bails unless .donate-page is on the page. */
(function () {
  "use strict";
  var root = document.querySelector(".donate-page");
  if (!root) return;

  /* Giving widget: frequency toggle, amount tiles, custom amount, outcome line.
     The Donate button stays a mailto until Stripe is wired (Naman, Oct 25);
     the amount and frequency ride in the subject line. */
  (function () {
    var amounts = Array.prototype.slice.call(root.querySelectorAll(".donate-amount"));
    var toggles = Array.prototype.slice.call(root.querySelectorAll(".donate-toggle__btn"));
    var outcome = document.getElementById("donate-outcome");
    var cta = document.getElementById("donate-cta");
    var customInput = root.querySelector(".donate-custom__input");
    if (!amounts.length || !cta || !outcome) return;
    var mailBase = cta.getAttribute("data-mail") || cta.getAttribute("href").split("%20(")[0];
    var freq = "one-time";
    var sel = { amt: "50", outcome: "school supplies for one student for a term" };
    var pressed = amounts.filter(function (b) { return b.getAttribute("aria-pressed") === "true"; })[0];
    if (pressed) { sel.amt = pressed.getAttribute("data-amt"); sel.outcome = pressed.getAttribute("data-outcome") || sel.outcome; }

    function currentAmt() {
      if (sel.amt === "custom") {
        var v = customInput ? parseFloat(customInput.value) : NaN;
        if (!(v > 0)) return "";
        return v % 1 ? v.toFixed(2) : String(v);
      }
      return sel.amt;
    }
    function render() {
      var amt = currentAmt();
      var monthly = (freq === "monthly");
      if (amt) {
        var shown = Number(amt).toLocaleString("en-US", { maximumFractionDigits: 2 });
        cta.setAttribute("href", mailBase + encodeURIComponent(" ($" + shown + (monthly ? " monthly" : "") + ")"));
        outcome.textContent = "Your $" + shown + (monthly ? "/mo" : "") + " gift can fund " + sel.outcome + ".";
      } else {
        cta.setAttribute("href", mailBase + (monthly ? encodeURIComponent(" (monthly)") : ""));
        outcome.textContent = "Enter an amount to see what it can fund.";
      }
    }
    function selectFreq(f) {
      freq = f;
      toggles.forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-freq") === f ? "true" : "false"); });
      render();
    }
    amounts.forEach(function (btn) {
      btn.addEventListener("click", function () {
        amounts.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        btn.setAttribute("aria-pressed", "true");
        sel.amt = btn.getAttribute("data-amt");
        sel.outcome = btn.getAttribute("data-outcome") || sel.outcome;
        if (sel.amt === "custom" && customInput) customInput.focus();
        else if (customInput) customInput.value = "";
        render();
      });
    });
    if (customInput) {
      customInput.addEventListener("input", function () {
        var custom = root.querySelector('.donate-amount[data-amt="custom"]');
        if (custom) {
          amounts.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
          custom.setAttribute("aria-pressed", "true");
          sel.amt = "custom";
          sel.outcome = custom.getAttribute("data-outcome") || sel.outcome;
        }
        render();
      });
    }
    toggles.forEach(function (t) {
      t.addEventListener("click", function () { selectFreq(t.getAttribute("data-freq")); });
    });
    /* "Choose another monthly amount" in the strip scrolls to the widget with Monthly preselected */
    root.querySelectorAll("[data-select-freq]").forEach(function (a) {
      a.addEventListener("click", function () { selectFreq(a.getAttribute("data-select-freq")); });
    });
    render();
  })();

  /* Accordions (Other ways to give + FAQ): button + aria-expanded, panels hidden until opened */
  root.querySelectorAll(".faq-item__btn[aria-controls]").forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute("aria-controls"));
    if (!panel) return;
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", open ? "false" : "true");
      if (open) panel.setAttribute("hidden", ""); else panel.removeAttribute("hidden");
    });
  });

})();


/* ---- supplement-work.js ---- */
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


/* ---- supplement-zz-px.js ---- */
/* Site-wide parallax (Naman, Oct 27): each img.px drifts slower than the page
   inside its frame, by the --pxr the photo runs past the frame at each end
   (supplement-zz-px.css), so an edge never shows. Off where the CSS keeps the
   photo flush with its frame (phones, tablets, reduced motion). The QA audit
   sets window.__pxForce to -1 or 1 to hold every photo at the far end it can
   actually reach (a hero starts mid-drift, never at -1). */
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
      var p = Math.max(-1, Math.min(1, (vh - r.top) / (vh + r.height) * 2 - 1));
      if (force !== undefined) {
        // QA: the far end this frame can actually reach while scrolling
        var top = r.top + window.scrollY, maxS = Math.max(0, document.documentElement.scrollHeight - vh);
        var lo = Math.max(-1, Math.min(1, (vh - top) / (vh + r.height) * 2 - 1));
        var hi = Math.max(-1, Math.min(1, (vh - (top - maxS)) / (vh + r.height) * 2 - 1));
        p = Math.max(lo, Math.min(hi, force));
      }
      img.style.setProperty('--py', (p * room).toFixed(1) + 'px');
    });
  }
  function request() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  window.addEventListener('load', request);
  update();
})();


/* ---- supplement-zz-refine.js ---- */
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
    var links = card.querySelectorAll("a");
    var syncLinks = function () {
      var on = card.classList.contains("is-flipped");
      links.forEach(function (a) { a.tabIndex = on ? 0 : -1; });
    };
    if (window.MutationObserver) new MutationObserver(syncLinks).observe(card, { attributes: true, attributeFilter: ["class"] });
    card.addEventListener("focus", function () {
      card.scrollIntoView({ block: "nearest", inline: "nearest", behavior: reduce.matches ? "auto" : "smooth" });
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
    var btn = header.querySelector(".nav-toggle");
    if (btn) btn.setAttribute("aria-label", nav.classList.contains("is-open") ? "Close menu" : "Open menu");
  }
  new MutationObserver(sync).observe(nav, { attributes: true, attributeFilter: ["class"] });
  window.addEventListener("resize", sync);
})();


/* ---- supplement-zzz-facefit.js ---- */
/* Face-safe crops picked live (Naman, Oct 22: no face cut off in any photo).
   A photo with data-faces (face boxes from gen/qa, as shares of the photo)
   gets the object-position, and if needed a slight zoom, that leaves every
   face fully in or fully out of its visible crop at the size it actually has
   on screen; redone whenever the photo's frame changes size. Order of
   preference: no face cut, no face under the data-avoid text, most faces in,
   least zoom, closest to data-pos. Without JS the CSS crop stands.
   - data-avoid: a selector inside the photo's section whose text faces stay
     clear of (a headline, a story panel).
   - data-fit-min: skip widths below it, where the CSS crop for the fixed
     phone and tablet boxes applies.
   - data-pad="shoulders": the box runs out to the shoulders and down to the
     chest, and may run past the bottom of the frame.
   - data-head: room kept above the face, in face heights (default 0.6, eased
     to 0.45 where nothing fits with 0.6).
   - data-keep="x0,y0,x1,y1": an area (shares of the photo) that must stay
     whole at every scroll position, like caps and a diploma.
   - data-fill: prefer the closest crop that still keeps everything whole.
   Parallax photos (img.px, supplement-zz-px.js) drift inside a frame shorter
   than the photo, so every face must sit in the band that stays visible at
   every scroll position (Naman, Oct 27). Each photo gets the strongest drift
   that keeps every face and person whole (10% of its frame, stepping down to
   4%); one that can't drift at all holds still (data-px-hold).
   The zoom and its origin go out as --fz and --fo, so the drift and the zoom
   share one transform; the drift goes out as --pxr. */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('img[data-faces]'));
  if (!imgs.length) return;
  var ZOOMS = [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3];
  var FILL_ZOOMS = [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6];
  var ROOMS = [0.10, 0.08, 0.06, 0.04];  // drift, as a share of the frame height

  // head boxes: [left, top, right, bottom, face height, shoulders left,
  // shoulders right, prominent]. A prominent person (face at least 8% of the
  // photo's height) counts as in only with the shoulders in too, so nobody
  // in the foreground is sliced at a side edge (Naman, Oct 27); a forced cut
  // takes the smallest face.
  var BIG = 0.08;
  function heads(img, up) {
    var sh = img.getAttribute('data-pad') === 'shoulders';
    return img.getAttribute('data-faces').split(';').map(function (s) {
      var f = s.split(',').map(Number);
      var big = f[3] >= BIG;
      var box = sh
        ? [Math.max(0, f[0] - 0.9 * f[2]), Math.max(0, f[1] - up * f[3]), Math.min(1, f[0] + 1.9 * f[2]), Math.min(1, f[1] + 2.2 * f[3])]
        : [Math.max(0, f[0] - 0.2 * f[2]), Math.max(0, f[1] - up * f[3]), Math.min(1, f[0] + 1.2 * f[2]), Math.min(1, f[1] + 1.1 * f[3])];
      var wl = big ? Math.max(0, Math.min(box[0], f[0] - 0.55 * f[2])) : box[0];
      var wr = big ? Math.min(1, Math.max(box[2], f[0] + 1.55 * f[2])) : box[2];
      return box.concat([f[3], wl, wr, big]);
    });
  }

  function better(a, b) {
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] < b[i];
    return false;
  }

  // parallax runs on this photo at this width (the CSS turns it on at 861px
  // and up, never with reduced motion)
  function drifting(img) {
    return img.classList.contains('px') && window.innerWidth >= 861 &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  // the drift positions this photo can actually reach: p runs from -1 (frame
  // entering at the bottom of the screen) to +1 (leaving at the top), but a
  // frame already on screen at the top of the page, or still on screen at
  // the very bottom, never reaches the far end (a hero starts near 0)
  function reach(img) {
    var r = img.parentElement.getBoundingClientRect(), vh = window.innerHeight;
    var top = r.top + window.scrollY, h = r.height;
    var maxS = Math.max(0, document.documentElement.scrollHeight - vh);
    function p(sy) { return Math.max(-1, Math.min(1, (vh - (top - sy)) / (vh + h) * 2 - 1)); }
    return [p(0), p(maxS)];
  }

  // the text lines in the photo box's coordinates (the box sits `room` above
  // the frame), stretched over every drift position the photo can reach (it
  // moves p * room against the text). A short eyebrow counts by its words, not
  // its full-width box; a block holding other blocks (a story panel) counts whole.
  function avoidRects(img, room, pr) {
    var sel = img.getAttribute('data-avoid'), sec = img.closest('section');
    if (!sel || !sec) return [];
    var fr = img.parentElement.getBoundingClientRect();
    var out = [];
    Array.prototype.forEach.call(sec.querySelectorAll(sel), function (e) {
      var rects = [e.getBoundingClientRect()];
      if (e.textContent.trim() && !e.querySelector('div, p, h1, h2, h3, h4, ul, ol')) {
        var rg = document.createRange();
        rg.selectNodeContents(e);
        rects = Array.prototype.slice.call(rg.getClientRects());
      }
      rects.forEach(function (r) {
        if (r.width > 0 && r.height > 0)
          out.push([r.left - fr.left, r.top - fr.top + room - pr[1] * room, r.right - fr.left, r.bottom - fr.top + room - pr[0] * room]);
      });
    });
    return out;
  }

  function clear(img) {
    img.style.objectPosition = img._pos0 || '';
    img.style.removeProperty('--fz');
    img.style.removeProperty('--fo');
    img.style.removeProperty('--pxr');
    img.removeAttribute('data-px-hold');
  }

  function fit(img) {
    var min = Number(img.getAttribute('data-fit-min') || 0);
    if (min && window.innerWidth < min) { clear(img); return; }
    var frame = img.parentElement;
    var fw = frame.clientWidth, fh = frame.clientHeight;
    if (!fw || !fh || !img.naturalWidth || getComputedStyle(img).objectFit !== 'cover') return;
    var calm = settle(img, fw, fh, 0);
    img._calm = calm;  // for QA
    if (drifting(img)) {
      // the strongest drift that does as well as holding still: no more heads
      // cut, no more faces under the text, no prominent person lost
      for (var i = 0; i < ROOMS.length; i++) {
        var o = ROOMS[i] * fh, best = settle(img, fw, fh + 2 * o, o);
        if (!better([calm.key[0], calm.key[1], -calm.big], [best.key[0], best.key[1], -best.big])) {
          img._drift = best;
          img.removeAttribute('data-px-hold');
          img.style.setProperty('--pxr', ROOMS[i] * 100 + '%');
          apply(img, best);
          return;
        }
      }
      img.setAttribute('data-px-hold', '');
    }
    img.style.removeProperty('--pxr');
    apply(img, calm);
  }

  // the best crop with generous room above heads, or with the usual room when
  // the generous one can't keep every face whole
  function settle(img, bw, bh, o) {
    var set = img.getAttribute('data-head');
    var best = search(img, bw, bh, o, set ? Number(set) : 0.6);
    if (!set && (best.key[0] > 0 || best.key[1] > 0)) {
      var eased = search(img, bw, bh, o, 0.45);
      if (better(eased.key.slice(0, 2), best.key.slice(0, 2))) best = eased;
    }
    return best;
  }

  // bw x bh: the photo box (frame plus the drift room o above and below)
  function search(img, bw, bh, o, up) {
    // share of the box that can scroll out of view at the top and at the bottom
    var pr = o ? reach(img) : [0, 0];
    var mt = o ? o * (1 - pr[0]) / bh : 0, mb = o ? o * (1 + pr[1]) / bh : 0;
    var av = avoidRects(img, o, pr);
    var s = Math.max(bw / img.naturalWidth, bh / img.naturalHeight);
    var wx0 = bw / (img.naturalWidth * s), wy0 = bh / (img.naturalHeight * s);
    var hs = heads(img, up);
    var open = img.getAttribute('data-pad') === 'shoulders';
    var keep = img.getAttribute('data-keep');
    keep = keep ? keep.split(',').map(Number) : null;
    var fill = img.hasAttribute('data-fill');
    var pref = (img.getAttribute('data-pos') || '50 50').split(' ').map(Number);
    var best = null;
    (fill ? FILL_ZOOMS : ZOOMS).forEach(function (z) {
      var wx = wx0 / z, wy = wy0 / z;
      for (var px = 0; px <= 100; px += 2) {
        for (var py = 0; py <= 100; py += (wy < 0.999 ? 1 : 101)) {
          var ppy = wy < 0.999 ? py : 50;
          var l = px / 100 * (1 - wx), t = ppy / 100 * (1 - wy), r = l + wx, b = t + wy;
          var st = t + mt * wy, sb = b - mb * wy;  // always on screen
          var cut = 0, inn = 0, txt = 0, big = 0;
          if (keep && !(keep[0] >= l - 1e-4 && keep[2] <= r + 1e-4 && keep[1] >= st - 1e-4 && keep[3] <= sb + 1e-4)) cut += 1;
          for (var i = 0; i < hs.length; i++) {
            var h = hs[i];
            if (h[2] <= l || h[0] >= r || h[3] <= t || h[1] >= b) continue;
            if (h[5] >= l - 1e-4 && h[6] <= r + 1e-4 && h[1] >= st - 1e-4 && (open || h[3] <= sb + 1e-4)) {
              inn++;
              if (h[7]) big++;
              var x0 = (h[0] - l) / wx * bw, y0 = (h[1] - t) / wy * bh, x1 = (h[2] - l) / wx * bw, y1 = (h[3] - t) / wy * bh;
              for (var k = 0; k < av.length; k++) {
                if (x0 < av[k][2] && x1 > av[k][0] && y0 < av[k][3] && y1 > av[k][1]) { txt++; break; }
              }
            } else cut += h[4];
          }
          var key = [cut, txt, -inn, fill ? -z : z, Math.abs(px - pref[0]) + Math.abs(ppy - pref[1])];
          if (!best || better(key, best.key)) best = { key: key, px: px, py: ppy, z: z, big: big };
        }
      }
    });
    return best;
  }

  function apply(img, best) {
    img._fit = best;  // for QA: [cut, under text, -in, zoom, distance] of the chosen crop
    var pos = best.px + '% ' + best.py + '%';
    img.style.objectPosition = pos;
    img.style.setProperty('--fo', pos);
    if (best.z > 1) img.style.setProperty('--fz', best.z); else img.style.removeProperty('--fz');
  }

  function all() { imgs.forEach(fit); }
  imgs.forEach(function (img) {
    img._pos0 = img.style.objectPosition;  // the static crop, restored where fitting is off
    if (img.complete) fit(img); else img.addEventListener('load', function () { fit(img); });
  });
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(all, 120); });
  window.addEventListener('load', all);
  // refit whenever a photo's frame changes size (equal-height splits, fonts)
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(function (entries) {
      entries.forEach(function (e) {
        var img = e.target._fitImg;
        if (img && img.complete) fit(img);
      });
    });
    imgs.forEach(function (img) {
      if (!img.parentElement) return;
      img.parentElement._fitImg = img;
      ro.observe(img.parentElement);
    });
  }
})();


/* ---- supplement-zzz-parallax.js ---- */
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


/* ---- supplement-zzz-splits.js ---- */
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


/* ---- supplement-zzz-timeline.js ---- */
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
