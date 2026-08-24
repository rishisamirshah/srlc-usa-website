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
