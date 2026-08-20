#!/usr/bin/env python3
"""SRLC USA static site builder. Run: python3 gen/build.py
Outputs committed HTML at the repo root; Netlify serves the folder as-is."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "gen"))

from shell import SITE
from data_states import STATES
from data_cares import CARES
from data_india import INSTITUTES
import pages_work as W
import pages_core as C

OP_STATES = {s["svg"].lower(): (s["name"], f'/our-work/united-states/{s["slug"]}/') for s in STATES}


def process_map():
    raw = open(os.path.join(ROOT, "gen", "usmap_raw.svg")).read()
    inner = re.sub(r"^.*?<svg[^>]*>", "", raw, flags=re.S)
    inner = inner.replace("</svg>", "")
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    inner = re.sub(r"<defs>.*?</defs>", "", inner, flags=re.S)
    inner = re.sub(r"<style[^>]*>.*?</style>", "", inner, flags=re.S)
    missing = []
    for cls, (name, href) in OP_STATES.items():
        pat = f'class="{cls}"'
        if pat not in inner:
            missing.append(cls)
            continue
        inner = inner.replace(pat, f'class="{cls} op" data-name="{name}" data-href="{href}"')
    if missing:
        print(f"  ! map: no path for {missing} (chips still link)")
    return inner.strip()


def write(path, html):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)
    print(f"  {path} ({len(html) // 1024}KB)")


PAGES = []  # (url, priority)


def emit(url, html, pri="0.7"):
    path = url + "index.html" if url.endswith("/") else url
    write(path, html)
    PAGES.append((url, pri))


def main():
    svg = process_map()

    emit("/", C.render_home(svg), "1.0")
    emit("/donate/", C.render_donate(), "0.9")
    emit("/volunteer/", C.render_volunteer(), "0.9")

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
    emit("/about/management/", C.render_management())
    emit("/about/financials/", C.render_financials())

    write("/404.html", C.render_404())

    # sitemap + robots
    urls = "".join(f"<url><loc>{SITE}{u}</loc><priority>{p}</priority></url>" for u, p in PAGES)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")

    # netlify.toml: legacy WordPress slugs -> new architecture
    redirects = [
        ("/inspiration/*", "/about/our-inspiration/"),
        ("/management/*", "/about/management/"),
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
        ("/intern-with-us/*", "/volunteer/"),
        ("/us-chapters/*", "/our-work/united-states/"),
    ]
    toml = "\n".join(
        f'[[redirects]]\n  from = "{f}"\n  to = "{t}"\n  status = 301\n' for f, t in redirects
    )
    toml += """
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"
"""
    write("/netlify.toml", toml)
    print(f"\nBuilt {len(PAGES)} pages + 404, sitemap, robots, netlify.toml")


if __name__ == "__main__":
    main()
