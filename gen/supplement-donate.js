/* Donate page (ported from Naman's donate.html): giving widget, accordions,
   hero parallax. Everything bails unless .donate-page is on the page. */
(function () {
  "use strict";
  var root = document.querySelector(".donate-page");
  if (!root) return;

  /* Giving widget: frequency toggle, amount tiles, custom amount, outcome line.
     The CTA stays a mailto labelled "Email us to give" (no card processor yet);
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
      if (sel.amt === "custom") return (customInput && customInput.value) ? String(customInput.value) : "";
      return sel.amt;
    }
    function render() {
      var amt = currentAmt();
      var monthly = (freq === "monthly");
      if (amt) {
        cta.setAttribute("href", mailBase + encodeURIComponent(" ($" + amt + (monthly ? " monthly" : "") + ")"));
        outcome.textContent = "Your $" + amt + (monthly ? "/mo" : "") + " gift funds " + sel.outcome + ".";
      } else {
        cta.setAttribute("href", mailBase + (monthly ? encodeURIComponent(" (monthly)") : ""));
        outcome.textContent = "Enter an amount to see exactly what it funds.";
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

  /* Subtle hero parallax: image lags scroll by 12%, capped at 50px. Desktop only, reduced-motion safe. */
  (function () {
    var MAX_SHIFT = 50, FACTOR = 0.12;
    var hero = root.querySelector(".donate-hero");
    if (!hero) return;
    var mqDesktop = window.matchMedia("(min-width: 900px)");
    var mqMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    var ticking = false;
    function apply() {
      ticking = false;
      if (!mqDesktop.matches || mqMotion.matches) { hero.style.removeProperty("--hero-par"); return; }
      hero.style.setProperty("--hero-par", Math.min(window.scrollY * FACTOR, MAX_SHIFT).toFixed(2) + "px");
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }, { passive: true });
    apply();
  })();
})();
