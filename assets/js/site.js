/* SRLC USA — shared behavior. No dependencies. */
(function () {
  "use strict";
  var doc = document, win = window;
  var reduced = win.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Header ---------- */
  var header = doc.querySelector(".header");
  var lastY = 0;
  function onScroll() {
    var y = win.scrollY;
    if (header) {
      header.classList.toggle("header--scrolled", y > 24);
      if (y > 420 && y > lastY + 6 && !doc.body.classList.contains("nav-open")) header.classList.add("header--hidden");
      else if (y < lastY - 4 || y < 420) header.classList.remove("header--hidden");
    }
    lastY = y;
    driftTick();
  }
  win.addEventListener("scroll", onScroll, { passive: true });

  var toggle = doc.querySelector(".navtoggle");
  if (toggle) toggle.addEventListener("click", function () {
    doc.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", doc.body.classList.contains("nav-open"));
  });

  /* Dropdowns: hover on desktop, click everywhere */
  doc.querySelectorAll(".nav__item").forEach(function (item) {
    var btn = item.querySelector("button.nav__link");
    if (!btn) return;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = item.classList.contains("open");
      doc.querySelectorAll(".nav__item.open").forEach(function (o) { o.classList.remove("open"); });
      if (!was) item.classList.add("open");
      btn.setAttribute("aria-expanded", !was);
    });
    if (win.matchMedia("(hover: hover) and (min-width: 921px)").matches) {
      var closeT = null;
      item.addEventListener("mouseenter", function () {
        clearTimeout(closeT);
        doc.querySelectorAll(".nav__item.open").forEach(function (o) { if (o !== item) o.classList.remove("open"); });
        item.classList.add("open");
      });
      item.addEventListener("mouseleave", function () {
        closeT = setTimeout(function () { item.classList.remove("open"); }, 260);
      });
    }
  });
  doc.addEventListener("click", function () {
    doc.querySelectorAll(".nav__item.open").forEach(function (o) { o.classList.remove("open"); });
  });

  /* ---------- Reveals ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    });
  }, { threshold: 0.16, rootMargin: "0px 0px -6% 0px" });
  doc.querySelectorAll(".reveal, .lines").forEach(function (el) { io.observe(el); });

  /* ---------- Counters ---------- */
  function animateCounter(el) {
    var raw = el.getAttribute("data-count") || el.textContent;
    var m = raw.match(/^([^0-9]*)([0-9][0-9.,]*)(.*)$/);
    if (!m || reduced) { el.textContent = raw; return; }
    var prefix = m[1], numStr = m[2], suffix = m[3];
    var hasComma = numStr.indexOf(",") > -1;
    var decimals = (numStr.split(".")[1] || "").length;
    var target = parseFloat(numStr.replace(/,/g, ""));
    var t0 = null, dur = 1600;
    function fmt(v) {
      var s = v.toFixed(decimals);
      if (hasComma) s = Number(s).toLocaleString("en-US", { minimumFractionDigits: decimals });
      return prefix + s + suffix;
    }
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * e);
      if (p < 1) requestAnimationFrame(step); else el.textContent = raw;
    }
    requestAnimationFrame(step);
  }
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { animateCounter(en.target); cio.unobserve(en.target); }
    });
  }, { threshold: 0.5 });
  doc.querySelectorAll(".counter").forEach(function (el) {
    el.setAttribute("data-count", el.textContent.trim());
    cio.observe(el);
  });

  /* ---------- Rails: drag + arrows ---------- */
  doc.querySelectorAll(".rail, .timeline__track").forEach(function (rail) {
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
      var w = card ? card.getBoundingClientRect().width + 20 : 320;
      rail.scrollBy({ left: btn.hasAttribute("data-rail-prev") ? -w : w, behavior: "smooth" });
    });
  });

  /* ---------- Tabs ---------- */
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

  /* ---------- Parallax drift ---------- */
  var drifts = Array.prototype.slice.call(doc.querySelectorAll(".drift"));
  function driftTick() {
    if (reduced || !drifts.length) return;
    var vh = win.innerHeight;
    drifts.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var p = (r.top + r.height / 2 - vh / 2) / vh; // -0.5 .. 0.5
      el.style.setProperty("--drift", (p * -7).toFixed(2) + "%");
    });
  }
  driftTick();

  /* ---------- Progress rail (10 Care hub) ---------- */
  var rails = doc.querySelectorAll(".progressrail a");
  if (rails.length) {
    var pio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          rails.forEach(function (d) { d.classList.toggle("on", d.getAttribute("href") === "#" + en.target.id); });
        }
      });
    }, { threshold: 0.55 });
    doc.querySelectorAll(".carepanel").forEach(function (p) { pio.observe(p); });
  }

  /* ---------- US map tooltip + nav ---------- */
  doc.querySelectorAll(".mapwrap").forEach(function (wrap) {
    var tip = wrap.querySelector(".maptip");
    wrap.querySelectorAll(".usmap path.op").forEach(function (p) {
      var name = p.getAttribute("data-name"), href = p.getAttribute("data-href");
      p.setAttribute("tabindex", "0");
      p.setAttribute("role", "link");
      p.setAttribute("aria-label", name);
      p.addEventListener("mousemove", function (e) {
        if (!tip) return;
        var b = wrap.getBoundingClientRect();
        tip.textContent = name;
        tip.style.left = (e.clientX - b.left) + "px";
        tip.style.top = (e.clientY - b.top) + "px";
        tip.classList.add("show");
      });
      p.addEventListener("mouseleave", function () { tip && tip.classList.remove("show"); });
      p.addEventListener("click", function () { if (href) win.location.href = href; });
      p.addEventListener("keydown", function (e) { if (e.key === "Enter" && href) win.location.href = href; });
    });
  });
  /* Chip hover highlights its state on the map (class-based: states can be multiple paths) */
  doc.querySelectorAll("[data-state-target]").forEach(function (chip) {
    var cls = chip.getAttribute("data-state-target");
    chip.addEventListener("mouseenter", function () {
      doc.querySelectorAll(".usmap ." + cls).forEach(function (p) { p.classList.add("hot"); });
    });
    chip.addEventListener("mouseleave", function () {
      doc.querySelectorAll(".usmap ." + cls).forEach(function (p) { p.classList.remove("hot"); });
    });
  });

  /* ---------- Marquee: duplicate for seamless loop ---------- */
  doc.querySelectorAll(".marquee__track").forEach(function (t) {
    t.innerHTML += t.innerHTML;
  });

  /* ---------- Donate chips ---------- */
  doc.querySelectorAll(".chips").forEach(function (group) {
    group.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        group.querySelectorAll("button").forEach(function (x) { x.classList.remove("on"); });
        b.classList.add("on");
      });
    });
  });

  /* ---------- Netlify forms (inline success) ---------- */
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
        if (ok) { form.querySelectorAll(".form-hidewrap").forEach(function (x) { x.style.display = "none"; }); ok.style.display = "block"; }
        else form.reset();
      }).catch(function () { form.submit(); });
    });
  });

  /* ---------- Footer year ---------- */
  doc.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
