#!/usr/bin/env python3
"""SRLC USA static site builder — flat pass. Run: python3 gen/build.py"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "gen"))

from shell import SITE
from data_states import STATES
from data_cares import CARES
from data_india import INSTITUTES
import pages_work as W
import pages_core as C
import pages_involve as I
try:
    from pages_donate import render_donate
except Exception as _e:  # pages_donate lands separately; never let the build break on it
    print(f"  ! pages_donate unavailable ({_e.__class__.__name__}: {_e}); using pages_core.render_donate")
    render_donate = C.render_donate

OP_STATES = {
    s["svg"].lower(): (s["name"], f'/our-work/united-states/{s["slug"]}/', f'{s["name"]}: {s["cities"]}')
    for s in STATES
}

EXTRA_CSS = """
.scroll-progress { position: fixed; top: 0; left: 0; height: 3px; width: 0;
  background: var(--color-warm-orange); z-index: 300; pointer-events: none; }
"""

# Homepage-only stylesheet layer; every other page loads supplement-zz-refine.css instead
HOME_ONLY_CSS = ("supplement-zz-home.css",)
# Shell rules (header, mobile menu, footer, newsletter) the homepage shares with every page
SHELL_SELECTORS = r"site-header|site-footer|nav-toggle|primary-nav|newsletter-modal|nav-locked|brand__logo|\.nowrap"

EXTRA_JS = """
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
"""


# Unsplash photo id (digits before the first hyphen) -> local filler downloaded once.
UNSPLASH_LOCAL = {
    "1450778869180": "/assets/img/fillers/animals-dog-cat.jpg",
    "1469571486292": "/assets/img/fillers/hands-heart.jpg",
    "1486218119243": "/assets/img/fillers/runner-road.jpg",
    "1488521787991": "/assets/img/fillers/children-smiling.jpg",
    "1497486751825": "/assets/img/fillers/children-india.jpg",
    "1503454537195": "/assets/img/fillers/child-paint.jpg",
    "1503676260728": "/assets/img/fillers/classroom-desk.jpg",
    "1517457373958": "/assets/img/fillers/community-gathering.jpg",
    "1542601906990": "/assets/img/fillers/hands-seedling.jpg",
    "1551076805": "/assets/img/fillers/hospital-theatre.jpg",
    "1551601651": "/assets/img/fillers/surgeons.jpg",
    "1573497019418": "/assets/img/fillers/woman-portrait.jpg",
    "1576091160550": "/assets/img/fillers/health-laptop.jpg",
    "1581094794329": "/assets/img/fillers/skills-coding.jpg",
    "1586773860418": "/assets/img/fillers/hospital-building.jpg",
    # 1488554378835 (abstract light streaks) is not a usable filler;
    # 1523050854058 and 1604335398980 are gone from Unsplash (404).
}


def _supplements(ext, skip=()):
    """All gen/supplement*.{ext} files: supplement.{ext} first, then the rest by
    name (supplement-core, supplement-donate, supplement-work, ...), minus skip."""
    import glob
    gen = os.path.join(ROOT, "gen")
    base = os.path.join(gen, f"supplement.{ext}")
    others = sorted(p for p in glob.glob(os.path.join(gen, f"supplement-*.{ext}")) if os.path.basename(p) not in skip)
    out = []
    for p in ([base] if os.path.exists(base) else []) + others:
        out.append(f"/* ---- {os.path.basename(p)} ---- */\n" + open(p).read())
    return out


def assemble_assets():
    html = open(os.path.join(ROOT, "gen", "base-homepage-v2.html")).read()

    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    css = "\n\n".join(b.strip() for b in blocks)
    out_rules = []
    for chunk in css.split("}"):
        sel = chunk.rsplit("{", 1)[0]  # selector incl. any @media opener ahead of it
        if re.search(r"\.preview-|\.nav-cat|\.nav-pages|\.nav-tag|\.page-divider|body\.preview-shell|\.trust-bar", sel):
            m = re.match(r"^(\s*@media[^{]*\{)", chunk)
            if m:
                out_rules.append(m.group(1).rstrip("{").rstrip() + "{")
            continue
        out_rules.append(chunk)
    css = "}".join(out_rules)

    # Flat-pass overrides applied at assembly:
    # 1. Typography stays exactly the approved homepage pairing (Newsreader
    #    headings, DM Sans body, opsz axes intact). Aug 24: Cormorant/Jost reverted.
    # 2. One radius value site-wide, 4px max (no pills, no 16px cards).
    css = re.sub(r"border-radius:\s*(\d+)px", lambda m: "border-radius: 4px" if int(m.group(1)) > 4 else m.group(0), css)
    # 3. Drop the purple glow shadows; borders stay.
    css = re.sub(r"box-shadow:[^;}]*rgba\(105,\s*61,\s*132[^;}]*[;}]", "box-shadow: none;", css)
    css = css.replace(
        "url('https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=2400&q=85&auto=format&fit=crop')",
        "url('/assets/img/photos/event-recent.jpg')")
    # 4. Every remaining Unsplash hotlink in the base CSS points at the same photo
    #    downloaded once into assets/img/fillers/ (see shell.FILLERS).
    css = re.sub(r"url\(['\"]?https://images\.unsplash\.com/photo-(\d+)-[^'\")]*['\"]?\)",
                 lambda m: f"url('{UNSPLASH_LOCAL.get(m.group(1), '/assets/img/fillers/children-smiling.jpg')}')", css)

    css_out = css + "\n\n" + "\n\n".join(_supplements("css", skip=HOME_ONLY_CSS)) + EXTRA_CSS
    # Homepage (Naman, Oct 18): back to the Sept 7 build plus only what he asked
    # for, so the Oct 17 critic layer stays off it. It keeps the shared header,
    # footer and newsletter rules from that layer so the shell matches every page.
    import cssx
    refine = open(os.path.join(ROOT, "gen", "supplement-zz-refine.css")).read()
    shell_css = cssx.dump(cssx.pick(cssx.parse(refine), SHELL_SELECTORS))
    css_home = (css + "\n\n" + "\n\n".join(_supplements("css", skip=("supplement-zz-refine.css", "supplement-zzz-inspiration.css")))
                + "\n\n/* ---- shared shell rules from supplement-zz-refine.css ---- */\n" + shell_css + EXTRA_CSS)

    scripts = re.findall(r"<script(?:\s+id=\"[^\"]*\")?>(.*?)</script>", html, re.S)
    keep = []
    for s in scripts:
        if "zipToChapter" in s or "TABLE = [" in s or "RELATED = {" in s:
            continue  # ZIP finder regenerated for the confirmed roster
        if "targets = ['27'" in s:
            continue  # banned-number counter stub
        if "}, 8000)" in s and "newsletterDismissed" in s:
            # 8s newsletter popup is superseded by exit-intent, but the hero
            # carousel logic shares this block and must survive
            s = s.split("// Newsletter popup")[0].rstrip() + "\n})();"
            s = s.replace(
                "function start(){ stop();",
                "function start(){ stop(); if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;")
            s = s.replace(
                "carousel.addEventListener('mouseleave', start);",
                "carousel.addEventListener('mouseleave', start);\n"
                "    carousel.addEventListener('focusin', stop);\n"
                "    carousel.addEventListener('focusout', start);")
        # Homepage mission stats count up again (Naman, Oct 18: the Sept 7 behavior);
        # inner-page stats keep rendering their final values
        s = s.replace("document.querySelectorAll('.mstat__n, .count-up')", "document.querySelectorAll('.mstat__n')")
        # quote wall left the homepage; its timer threw every 6.5s with no cards
        s = s.replace(
            "var dots = document.querySelectorAll('.quote-wall__dots .qd');\n  var idx = 0;",
            "var dots = document.querySelectorAll('.quote-wall__dots .qd');\n  if (!cards.length) return;\n  var idx = 0;")
        s = s.replace(
            "function start(){ stop(); timer = setInterval(function(){go(idx+1);}, 6500); }",
            "function start(){ stop(); if (hold || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) return; timer = setInterval(function(){go(idx+1);}, 11000); }")
        s = s.replace(
            "dots.forEach(function(d){ d.addEventListener('click', function(){ go(parseInt(d.dataset.go,10)); start(); }); });\n  start();",
            "dots.forEach(function(d){ d.addEventListener('click', function(){ go(parseInt(d.dataset.go,10)); start(); }); });\n"
            "  var wall = document.querySelector('.quote-wall');\n"
            "  var hold = false;\n"
            "  if (wall) { wall.addEventListener('mouseenter', function(){ hold = true; stop(); }); wall.addEventListener('mouseleave', function(){ if (!wall.contains(document.activeElement)) { hold = false; start(); } }); wall.addEventListener('focusin', function(){ hold = true; stop(); }); wall.addEventListener('focusout', function(e){ if (!wall.contains(e.relatedTarget)) { hold = false; start(); } }); }\n"
            "  start();")
        s = s.replace(
            "if (sp && !reducedMotion) {",
            "var _rm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n  if (sp && !_rm) {")
        keep.append(s.strip())
    js_out = "\n\n".join(keep) + "\n\n" + "\n\n".join(_supplements("js")) + EXTRA_JS

    # Content-hashed filenames: no cache layer can serve a stale bundle.
    import hashlib, glob
    ch = hashlib.md5(css_out.encode()).hexdigest()[:8]
    hh = hashlib.md5(css_home.encode()).hexdigest()[:8]
    jh = hashlib.md5(js_out.encode()).hexdigest()[:8]
    for old in (glob.glob(os.path.join(ROOT, "assets", "css", "site-*.css")) + glob.glob(os.path.join(ROOT, "assets", "css", "home-*.css"))
                + glob.glob(os.path.join(ROOT, "assets", "js", "site-*.js"))):
        os.remove(old)
    with open(os.path.join(ROOT, "assets", "css", f"site-{ch}.css"), "w") as f:
        f.write(css_out)
    with open(os.path.join(ROOT, "assets", "css", f"home-{hh}.css"), "w") as f:
        f.write(css_home)
    with open(os.path.join(ROOT, "assets", "js", f"site-{jh}.js"), "w") as f:
        f.write(js_out)
    # legacy names keep working so any stale cached HTML still picks up current styles
    with open(os.path.join(ROOT, "assets", "css", "site.css"), "w") as f:
        f.write(css_out)
    with open(os.path.join(ROOT, "assets", "js", "site.js"), "w") as f:
        f.write(js_out)
    import shell as _shell
    _shell.CSS_FILE = f"/assets/css/site-{ch}.css"
    _shell.HOME_CSS_FILE = f"/assets/css/home-{hh}.css"
    _shell.JS_FILE = f"/assets/js/site-{jh}.js"
    print(f"  assets: site-{ch}.css, home-{hh}.css, site-{jh}.js (+legacy names)")


def process_map():
    raw = open(os.path.join(ROOT, "gen", "usmap_raw.svg")).read()
    inner = re.sub(r"^.*?<svg[^>]*>", "", raw, flags=re.S)
    inner = inner.replace("</svg>", "")
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    inner = re.sub(r"<defs>.*?</defs>", "", inner, flags=re.S)
    inner = re.sub(r"<style[^>]*>.*?</style>", "", inner, flags=re.S)
    inner = re.sub(r'class="([a-z]{2})"', r'class="cf-state \1"', inner)
    missing = []
    for cls, (name, href, label) in OP_STATES.items():
        pat = f'class="cf-state {cls}"'
        if pat not in inner:
            missing.append(cls)
            continue
        inner = inner.replace(
            pat,
            f'class="cf-state cf-state--active {cls}" data-state="{cls.upper()}" data-name="{label}" data-href="{href}"')

    def add_title(m):
        tag = m.group(1)
        nm = re.search(r'data-name="([^"]+)"', tag)
        t = nm.group(1) if nm else ""
        return tag + f"><title>{t}</title></path>"

    inner = re.sub(r"(<path[^>]*cf-state--active[^>]*?)\s*/>", add_title, inner)
    if missing:
        print(f"  ! map: no path for {missing}")
    return inner.strip()


def write(path, html):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)
    print(f"  {path} ({len(html) // 1024}KB)")


PAGES = []


def emit(url, html, pri="0.7"):
    path = url + "index.html" if url.endswith("/") else url
    write(path, html)
    PAGES.append((url, pri))


def main():
    # retire moved/removed output dirs
    import shutil
    for stale in ["volunteer", "events", "fundraise", "corporate-giving", "partner-with-us",
                  "about/faqs", "about/management"]:
        p = os.path.join(ROOT, stale)
        if os.path.isdir(p):
            shutil.rmtree(p)
            print(f"  - removed stale /{stale}/")

    assemble_assets()
    svg = process_map()

    emit("/", C.render_home(svg), "1.0")
    emit("/donate/", render_donate(), "0.9")
    emit("/get-involved/volunteer/", I.render_volunteer(svg), "0.9")
    emit("/get-involved/events/", I.render_events())
    emit("/get-involved/fundraise/", I.render_fundraise())
    emit("/get-involved/partner-with-us/", I.render_partner())

    emit("/our-work/united-states/", W.render_us_hub(svg), "0.9")
    for i, s in enumerate(STATES):
        emit(f'/our-work/united-states/{s["slug"]}/', W.render_state(s, i))

    emit("/our-work/10-care-program/", W.render_tencare_hub(), "0.9")
    for c in CARES:
        emit(f'/our-work/10-care-program/{c["slug"]}/', W.render_care(c))

    emit("/our-work/india/", W.render_india_hub(), "0.8")
    for inst in INSTITUTES:
        if inst.get("full_page"):
            emit(f'/our-work/india/{inst["slug"]}/', W.render_vidyapeeth())
        else:
            emit(f'/our-work/india/{inst["slug"]}/', W.render_institute(inst))

    emit("/our-work/mission-africa/", W.render_africa(), "0.8")

    emit("/about/who-we-are/", C.render_who_we_are(), "0.8")
    emit("/about/our-impact/", C.render_our_impact(svg), "0.8")
    emit(C.IF_PATH, C.render_inspiration(), "0.8")
    emit("/about/management-team/", C.render_management())
    emit("/about/financials/", C.render_financials())

    write("/404.html", C.render_404())

    urls = "".join(f"<url><loc>{SITE}{u}</loc><priority>{p}</priority></url>" for u, p in PAGES)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    # staging: keep crawlers out entirely until cutover
    write("/robots.txt", "User-agent: *\nDisallow: /\n")

    redirects = [
        # this build's own URL moves
        ("/volunteer/*", "/get-involved/volunteer/"),
        ("/events/*", "/get-involved/events/"),
        ("/fundraise/*", "/get-involved/fundraise/"),
        ("/partner-with-us/*", "/get-involved/partner-with-us/"),
        ("/corporate-giving/*", "/donate/"),
        ("/about/faqs/*", "/"),
        ("/about/management/*", "/about/management-team/"),
        ("/about/our-inspiration/*", "/about/inspiration-and-founder/"),
        # legacy WordPress slugs
        ("/inspiration/*", "/about/inspiration-and-founder/"),
        ("/faqs/*", "/"),
        ("/event/*", "/get-involved/events/"),
        ("/grants/*", "/donate/"),
        ("/management/*", "/about/management-team/"),
        ("/management-team/*", "/about/management-team/"),
        ("/financials/*", "/about/financials/"),
        ("/annual-reports/*", "/about/financials/"),
        ("/10-care-program/*", "/our-work/10-care-program/:splat"),
        ("/causes/healthcare/*", "/our-work/10-care-program/health-care/"),
        ("/causes/education/*", "/our-work/10-care-program/educational-care/"),
        ("/causes/child-care/*", "/our-work/10-care-program/child-care/"),
        ("/causes/women-empowerment/*", "/our-work/10-care-program/woman-care/"),
        ("/causes/tribal-welfare/*", "/our-work/10-care-program/tribal-care/"),
        ("/causes/community-welfare/*", "/our-work/10-care-program/community-care/"),
        ("/causes/humanitarian-care/*", "/our-work/10-care-program/humanitarian-care/"),
        ("/causes/animal-welfare/*", "/our-work/10-care-program/animal-care/"),
        ("/causes/environmental-care/*", "/our-work/10-care-program/environmental-care/"),
        ("/causes/emergency-relief/*", "/our-work/10-care-program/emergency-relief-care/"),
        ("/causes/*", "/our-work/10-care-program/"),
        ("/institutes/hospital-and-research-center/*", "/our-work/india/hospital-and-research-center/"),
        ("/institutes/science-college/*", "/our-work/india/vidyapeeth/"),
        ("/institutes/primary-school/*", "/our-work/india/gurukul/"),
        ("/institutes/skill-development-center/*", "/our-work/india/skill-development-center/"),
        ("/institutes/animal-hospital/*", "/our-work/india/jivamaitridham/"),
        ("/institutes/*", "/our-work/india/"),
        ("/educational-care/shrimad-rajchandra-vidyapeeth/*", "/our-work/india/vidyapeeth/"),
        ("/back-to-school/*", "/our-work/united-states/"),
        ("/intern-with-us/*", "/get-involved/volunteer/"),
        ("/us-chapters/*", "/our-work/united-states/"),
        # interim Aug-23 structure shared with the team before the hierarchy move
        ("/us/*", "/our-work/united-states/:splat"),
        ("/map/*", "/our-work/united-states/"),
        ("/locations/*", "/our-work/united-states/"),
    ]
    toml = "\n".join(
        f'[[redirects]]\n  from = "{f}"\n  to = "{t}"\n  status = 301\n' for f, t in redirects)
    toml += """
[[headers]]
  for = "/assets/css/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/js/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/img/*"
  [headers.values]
    Cache-Control = "public, max-age=300"

[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "noindex"
"""
    write("/netlify.toml", toml)
    print(f"\nBuilt {len(PAGES)} pages + 404, sitemap, robots (staging noindex), netlify.toml")


if __name__ == "__main__":
    main()
