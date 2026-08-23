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

OP_STATES = {
    s["svg"].lower(): (s["name"], f'/our-work/united-states/{s["slug"]}/', f'{s["name"]}: {s["cities"]}')
    for s in STATES
}

EXTRA_CSS = """
.scroll-progress { position: fixed; top: 0; left: 0; height: 3px; width: 0;
  background: var(--color-warm-orange); z-index: 300; pointer-events: none; }
"""

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


def assemble_assets():
    html = open(os.path.join(ROOT, "gen", "base-homepage-v2.html")).read()

    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    css = "\n\n".join(b.strip() for b in blocks)
    out_rules = []
    for chunk in css.split("}"):
        sel = chunk.split("{")[0]
        if re.search(r"\.preview-|\.nav-cat|\.nav-pages|\.nav-tag|\.page-divider|body\.preview-shell", sel):
            m = re.match(r"^(\s*@media[^{]*\{)", chunk)
            if m:
                out_rules.append(m.group(1).rstrip("{").rstrip() + "{")
            continue
        out_rules.append(chunk)
    css = "}".join(out_rules)

    # Flat-pass overrides applied at assembly:
    # 1. Brand fonts (edits list + Brand Guide): Cormorant Garamond + Jost.
    css = css.replace("'Newsreader', Georgia, serif", "'Cormorant Garamond', Georgia, serif")
    css = css.replace('"Newsreader", "Times New Roman", Georgia, serif', "'Cormorant Garamond', Georgia, serif")
    css = css.replace("'Newsreader', serif", "'Cormorant Garamond', serif")
    css = css.replace("'DM Sans', sans-serif", "'Jost', sans-serif")
    css = css.replace('"DM Sans", "Helvetica Neue", Arial, sans-serif', "'Jost', 'Helvetica Neue', Arial, sans-serif")
    css = re.sub(r"font-variation-settings:[^;]+;", "", css)  # Newsreader opsz axes do not exist in Cormorant
    # 2. One radius value site-wide, 4px max (no pills, no 16px cards).
    css = re.sub(r"border-radius:\s*(\d+)px", lambda m: "border-radius: 4px" if int(m.group(1)) > 4 else m.group(0), css)
    # 3. Drop the purple glow shadows; borders stay.
    css = re.sub(r"box-shadow:[^;}]*rgba\(105,\s*61,\s*132[^;}]*[;}]", "box-shadow: none;", css)
    css = css.replace(
        "url('https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=2400&q=85&auto=format&fit=crop')",
        "url('/assets/img/photos/event-recent.jpg')")

    supplement = open(os.path.join(ROOT, "gen", "supplement.css")).read()
    with open(os.path.join(ROOT, "assets", "css", "site.css"), "w") as f:
        f.write(css + "\n\n" + supplement + EXTRA_CSS)

    scripts = re.findall(r"<script(?:\s+id=\"[^\"]*\")?>(.*?)</script>", html, re.S)
    keep = []
    for s in scripts:
        if "zipToChapter" in s or "TABLE = [" in s or "RELATED = {" in s:
            continue  # ZIP finder regenerated for the confirmed roster
        if "targets = ['27'" in s:
            continue  # banned-number counter stub
        if "}, 8000)" in s and "newsletterDismissed" in s:
            continue  # superseded by exit-intent
        s = s.replace(
            "if (sp && !reducedMotion) {",
            "var _rm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n  if (sp && !_rm) {")
        keep.append(s.strip())
    supplement_js = open(os.path.join(ROOT, "gen", "supplement.js")).read()
    with open(os.path.join(ROOT, "assets", "js", "site.js"), "w") as f:
        f.write("\n\n".join(keep) + "\n\n" + supplement_js + EXTRA_JS)
    print(f"  assets: site.css ({(len(css) + len(supplement)) // 1024}KB), site.js assembled")


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
    emit("/donate/", C.render_donate(), "0.9")
    emit("/get-involved/volunteer/", I.render_volunteer(), "0.9")
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
    emit("/about/our-inspiration/", C.render_inspiration(), "0.8")
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
        # legacy WordPress slugs
        ("/inspiration/*", "/about/our-inspiration/"),
        ("/faqs/*", "/"),
        ("/event/*", "/get-involved/events/"),
        ("/grants/*", "/donate/"),
        ("/management/*", "/about/management-team/"),
        ("/management-team/*", "/about/management-team/"),
        ("/financials/*", "/about/financials/"),
        ("/annual-reports/*", "/about/financials/"),
        ("/10-care-program/*", "/our-work/10-care-program/"),
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
        ("/map/*", "/our-work/united-states/"),
        ("/locations/*", "/our-work/united-states/"),
    ]
    toml = "\n".join(
        f'[[redirects]]\n  from = "{f}"\n  to = "{t}"\n  status = 301\n' for f, t in redirects)
    toml += """
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"

[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "noindex"
"""
    write("/netlify.toml", toml)
    print(f"\nBuilt {len(PAGES)} pages + 404, sitemap, robots (staging noindex), netlify.toml")


if __name__ == "__main__":
    main()
