"""Shared page shell + components — SRLC USA purple system, flat pass (Aug 23),
Aug 24 change list applied (Aug 30): Newsreader + DM Sans, official logo,
no trust bar, real filler photography in every image slot, badge images.
Sources: Naman's CLAUDE.md v2 (gen/naman-claude.md), SRLC_USA_Brand_Guide.pdf,
approved homepage HTML v2, the Aug 22 edits list and the Aug 24 change list.
No em dashes, approved stats only, spiritual content only on /about/our-inspiration/.
"""
import hashlib
import re

SITE = "https://srlcusa.netlify.app"  # staging; production per Aug decision is AWS Amplify
EMAIL = "info@srlc-usa.org"           # domain ruling pending Naman; do not mass-change
PHONE = "1.551.775.2872"
EIN_LINE = ("Shrimad Rajchandra Love and Care USA is a registered 501(c)(3) nonprofit "
            "organization. EIN 81-5162502. Contributions are tax deductible to the "
            "extent permitted by law.")
IG = "https://www.instagram.com/srlc_usa/"
FB = "https://www.facebook.com/SRLCUSA/"

CSS_FILE = "/assets/css/site.css"
JS_FILE = "/assets/js/site.js"

# Exactly the pairing the approved homepage HTML loads (gen/base-homepage-v2.html):
# Newsreader for headings, DM Sans for body. Both carry the opsz axis.
FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..700&"
         "family=DM+Sans:ital,opsz,wght@0,9..40,300..700;1,9..40,300..700&display=swap")

LOGO_DARK = "/assets/img/logo/srlc-logo-dark.svg"    # maroon artwork, light backgrounds
LOGO_LIGHT = "/assets/img/logo/srlc-logo-light.svg"  # cream artwork, dark / photo backgrounds
LOGO_ALT = "Shrimad Rajchandra Love and Care"
# Cropped viewBox is 1511 x 249; width/height attributes carry that ratio.
LOGO_W, LOGO_H = 340, 56

SOCIAL_SVG = {
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2m0 4.8a5 5 0 1 1 0 10 5 5 0 0 1 0-10m0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4m5.2-3a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12"/></svg>',
}


def head(title, desc, path, overlay=False):
    canonical = SITE + path
    body_cls = ' class="has-overlay-nav"' if overlay else ""
    preload = ('<link rel="preload" as="image" href="/assets/img/photos/school-children-hero.jpg">\n'
               if path == "/" else "")
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<!-- staging noindex: remove at srlcusa.org cutover -->
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/photos/school-children-hero.jpg">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
{preload}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{CSS_FILE}">
<script>document.documentElement.classList.replace("no-js","js")</script>
<script src="{JS_FILE}" defer></script>
</head>
<body{body_cls}>
<a class="skip-link" href="#main">Skip to content</a>
"""


def nav_panel_link(href, label, desc):
    return (f'<a class="primary-nav__sublink" role="menuitem" href="{href}">'
            f'<span class="primary-nav__sublabel">{label}</span>'
            f'<span class="primary-nav__subdesc">{desc}</span></a>')


def nav(overlay=False):
    cls = "site-header site-header--overlay" if overlay else "site-header"
    return f"""<header class="{cls}">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Shrimad Rajchandra Love and Care USA home">
      <img class="brand__logo brand__logo--dark" src="{LOGO_DARK}" alt="{LOGO_ALT}" width="{LOGO_W}" height="{LOGO_H}" loading="eager" decoding="async">
      <img class="brand__logo brand__logo--light" src="{LOGO_LIGHT}" alt="{LOGO_ALT}" width="{LOGO_W}" height="{LOGO_H}" loading="eager" decoding="async">
    </a>
    <nav class="primary-nav" aria-label="Primary">
      <ul class="primary-nav__list">
        <li class="primary-nav__item"><button class="primary-nav__trigger" type="button" aria-expanded="false" aria-haspopup="true" aria-controls="navpanel-about">About Us</button>
          <div class="primary-nav__panel" id="navpanel-about" role="menu" aria-label="About Us submenu">
            {nav_panel_link("/about/our-inspiration/", "Our Inspiration", "The spiritual lineage that inspires SRLC&rsquo;s mission.")}
            {nav_panel_link("/about/who-we-are/", "Who We Are", "A modern overview of SRLC USA. Who, what, and how.")}
            {nav_panel_link("/about/our-impact/", "Our Impact", "Program outcomes, impact stories, aggregate numbers.")}
            {nav_panel_link("/about/management-team/", "Management Team", "Board, leadership, and team profiles.")}
            {nav_panel_link("/about/financials/", "Financials", "Annual reports, audited statements, and 990s.")}
          </div>
        </li>
        <li class="primary-nav__item"><button class="primary-nav__trigger" type="button" aria-expanded="false" aria-haspopup="true" aria-controls="navpanel-work">Our Work</button>
          <div class="primary-nav__panel" id="navpanel-work" role="menu" aria-label="Our Work submenu">
            {nav_panel_link("/our-work/10-care-program/", "10 Care Program", "The 10 focus areas that frame SRLC&rsquo;s work globally.")}
            <a class="primary-nav__sublink primary-nav__sublink--has-children" role="menuitem" href="/our-work/united-states/"><span class="primary-nav__sublabel">Where We Serve</span><span class="primary-nav__subdesc">Regional hub for the three places SRLC operates.</span></a>
            <div class="primary-nav__subnest">
              <a class="primary-nav__sublink--nested" role="menuitem" href="/our-work/united-states/">United States</a>
              <a class="primary-nav__sublink--nested" role="menuitem" href="/our-work/india/">India</a>
              <a class="primary-nav__sublink--nested" role="menuitem" href="/our-work/mission-africa/">Mission Africa</a>
            </div>
          </div>
        </li>
        <li class="primary-nav__item"><button class="primary-nav__trigger" type="button" aria-expanded="false" aria-haspopup="true" aria-controls="navpanel-involved">Get Involved</button>
          <div class="primary-nav__panel" id="navpanel-involved" role="menu" aria-label="Get Involved submenu">
            {nav_panel_link("/donate/", "Donate", "One-time or recurring giving with dollar-to-outcome options.")}
            {nav_panel_link("/get-involved/volunteer/", "Volunteer", "Sign up for SRLC volunteer opportunities across U.S. cities.")}
            {nav_panel_link("/get-involved/events/", "Events", "Chapter events, galas, and community gatherings.")}
            {nav_panel_link("/get-involved/fundraise/", "Start a Fundraiser", "Birthday, memorial, wedding, run. Any moment.")}
            {nav_panel_link("/get-involved/partner-with-us/", "Partner With Us", "Strategic partnerships for organizations and NGOs.")}
          </div>
        </li>
      </ul>
      <a class="btn btn--primary primary-nav__cta" href="/donate/">Donate</a>
    </nav>
    <button class="nav-toggle" aria-expanded="false" aria-label="Open menu"><span></span></button>
  </div>
</header><main class="main" id="main">
"""


def footer():
    # Address and phone withheld pending Naman's confirmation (CLAUDE.md: must be
    # confirmed real before appearing on any deployed page).
    return f"""</main><footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="site-footer__cols">
      <div>
        <p class="site-footer__brand"><img class="brand__logo-img" src="{LOGO_LIGHT}" alt="{LOGO_ALT}" width="260" height="43" loading="lazy"></p>
        <p class="site-footer__legal">SRLC USA is a registered 501(c)(3).</p>
        <p class="site-footer__legal">EIN: 81-5162502</p>
        <p class="site-footer__legal"><a href="mailto:{EMAIL}" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">{EMAIL}</a></p>
        <div class="social">
          <a href="{IG}" aria-label="Instagram" rel="noopener" target="_blank">{SOCIAL_SVG['ig']}</a>
          <a href="{FB}" aria-label="Facebook" rel="noopener" target="_blank">{SOCIAL_SVG['fb']}</a>
        </div>
      </div>
      <div>
        <h4>About Us</h4>
        <ul>
          <li><a href="/about/our-inspiration/">Our Inspiration</a></li>
          <li><a href="/about/who-we-are/">Who We Are</a></li>
          <li><a href="/about/our-impact/">Our Impact</a></li>
          <li><a href="/about/management-team/">Management Team</a></li>
          <li><a href="/about/financials/">Financials</a></li>
        </ul>
      </div>
      <div>
        <h4>Our Work</h4>
        <ul>
          <li><a href="/our-work/10-care-program/">10 Care Program</a></li>
          <li><a href="/our-work/united-states/">United States</a></li>
          <li><a href="/our-work/india/">India</a></li>
          <li><a href="/our-work/mission-africa/">Mission Africa</a></li>
        </ul>
      </div>
      <div>
        <h4>Get Involved</h4>
        <ul>
          <li><a href="/donate/">Donate</a></li>
          <li><a href="/get-involved/volunteer/">Volunteer</a></li>
          <li><a href="/get-involved/events/">Events</a></li>
          <li><a href="/get-involved/fundraise/">Start a Fundraiser</a></li>
          <li><a href="/get-involved/partner-with-us/">Partner With Us</a></li>
        </ul>
      </div>
      <div>
        <h4>Connect</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">Contact Us</a></li>
          <li><a href="/#final-newsletter">Newsletter Signup</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__bottom">
      <p>&copy; Copyright <span data-year>2026</span> Shrimad Rajchandra Love and Care USA, All Rights Reserved</p>
      <p>{EIN_LINE}</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def page(title, desc, path, body, overlay=False):
    # Pages that open with a photo header get the transparent overlay nav with
    # the light logo automatically; callers can still pass overlay=True themselves.
    if not overlay and body.lstrip().startswith('<section class="pagehead'):
        overlay = True
    return head(title, desc, path, overlay) + nav(overlay) + body + footer()


# ---------- Filler photography ----------
# The "existing image set": the Unsplash photos the approved homepage HTML and
# Naman's donate HTML use (downloaded once into assets/img/fillers/) plus the
# four photos in assets/img/photos/. Placeholder-then-swap on staging is fine per
# CLAUDE.md; final photography replaces these slot by slot from the Media Bank.
# (path, tag, width, height) — tags judged from the actual pictures.
FILLERS = [
    ("/assets/img/fillers/children-smiling.jpg", "children", 2400, 1600),
    ("/assets/img/fillers/children-india.jpg", "children", 1600, 1142),
    ("/assets/img/fillers/child-paint.jpg", "children", 1600, 2409),
    ("/assets/img/photos/school-children-hero.jpg", "children", 1600, 1067),
    ("/assets/img/fillers/classroom-desk.jpg", "classroom", 2400, 1695),
    ("/assets/img/photos/love-care-walk.jpg", "awards", 1600, 1067),
    ("/assets/img/fillers/skills-coding.jpg", "skills", 1600, 2399),
    ("/assets/img/fillers/hospital-theatre.jpg", "hospital", 2400, 1350),
    ("/assets/img/fillers/surgeons.jpg", "hospital", 1600, 1697),
    ("/assets/img/fillers/hospital-building.jpg", "hospital", 1600, 1064),
    ("/assets/img/fillers/health-laptop.jpg", "health", 1600, 1067),
    ("/assets/img/fillers/community-gathering.jpg", "community", 2400, 1602),
    ("/assets/img/photos/event-recent.jpg", "awards", 1600, 1067),
    ("/assets/img/photos/awards.jpg", "awards", 1600, 1067),
    ("/assets/img/fillers/hands-heart.jpg", "hands", 1600, 1067),
    ("/assets/img/fillers/hands-seedling.jpg", "nature", 1600, 916),
    ("/assets/img/fillers/runner-road.jpg", "nature", 1600, 1065),
    ("/assets/img/fillers/woman-portrait.jpg", "women", 1600, 2400),
    ("/assets/img/fillers/animals-dog-cat.jpg", "animals", 1600, 941),
]

# Subject hints for ph(): first matching keyword in the slot label picks the tag.
_TAG_HINTS = [
    ("animals", ("animal", "dog", "cat", "cattle", "shelter", "veterinar", "jivamaitri")),
    ("hospital", ("hospital", "patient", "surgery", "surgical", "medical", "doctor", "camp", "clinic", "cardio", "health")),
    ("classroom", ("classroom", "school", "student", "computer", "lab", "gurukul", "vidyapeeth", "college", "kit")),
    ("skills", ("skill", "training", "vocational", "coding", "software")),
    ("women", ("woman", "women", "mother", "girl")),
    ("children", ("child", "children", "kid", "youth", "young")),
    ("awards", ("award", "plaque", "recogni", "ceremony", "felicitat")),
    ("hands", ("hands", "packing", "supply", "supplies", "kits", "meal", "food")),
    ("nature", ("field", "farm", "village", "road", "terrain", "tree", "plant", "environment", "region", "walk", "run")),
    ("community", ("volunteer", "event", "community", "chapter", "gathering", "team", "crowd", "hall", "people")),
]


def _tag_for(label):
    low = (label or "").lower()
    for tag, words in _TAG_HINTS:
        if any(w in low for w in words):
            return tag
    return None


def filler(key, tag=None):
    """Deterministic filler pick for a slot: same key always yields the same
    photo. `tag` restricts the pool to one subject; an unknown tag falls back to
    the whole set. Returns the /assets path (use filler_entry for dimensions)."""
    return filler_entry(key, tag)[0]


def filler_entry(key, tag=None):
    pool = [f for f in FILLERS if tag and f[1] == tag] or FILLERS
    h = int(hashlib.md5((key or "").encode("utf-8")).hexdigest(), 16)
    return pool[h % len(pool)]


def _attr(text):
    return (text or "").replace("&", "&amp;").replace('"', "&quot;").replace("&amp;rsquo;", "&rsquo;").replace("&amp;amp;", "&amp;")


def ph(label, cls="", style="", tag=None):
    """Image slot. Renders a real photo (a deterministic filler from the existing
    image set) with the slot's direction line as alt text; the same line rides in
    the title attribute so the team can see what final photography each slot
    wants. Keeps the ph-media class plus cls/style so every existing call site
    on every page keeps its layout."""
    path, ftag, w, h = filler_entry(label, tag or _tag_for(label))
    s = f' style="{style}"' if style else ""
    c = f"ph-media {cls}".strip()
    alt = _attr(re.sub(r"\s+", " ", label or "").strip())
    return (f'<img class="{c}" src="{path}" alt="{alt}" title="{alt}" width="{w}" height="{h}" '
            f'loading="lazy" decoding="async"{s}>')


def page_header(eyebrow, h1, sub=None, cta=None, image=None):
    """SRA-pattern page header over a real photo: one small eyebrow line, short
    single-color H1, flat dark-purple scrim for contrast. `image` is an /assets
    path; otherwise a filler chosen from the H1."""
    if image:
        src, w, h = image, 2400, 1600
        for f in FILLERS:
            if f[0] == image:
                w, h = f[2], f[3]
    else:
        src, _, w, h = filler_entry(h1, _tag_for(f"{eyebrow} {h1} {sub or ''}"))
    sub_html = f'<p class="pagehead__sub">{sub}</p>' if sub else ""
    cta_html = f'<div class="pagehead__cta">{cta}</div>' if cta else ""
    return f"""<section class="pagehead pagehead--photo">
  <img class="pagehead__img" src="{src}" alt="" width="{w}" height="{h}" loading="eager" fetchpriority="high" decoding="async">
  <div class="pagehead__scrim"></div>
  <div class="container pagehead__inner">
    <p class="pagehead__eyebrow">{eyebrow}</p>
    <h1 class="pagehead__h1">{h1}</h1>
    {sub_html}
    {cta_html}
  </div>
</section>"""


def trust_bar():
    """Retired on Naman's Aug 24 list. Kept so existing imports and call sites
    keep working; renders nothing."""
    return ""


def flat_cta(h2, body, label, href="/donate/", second=None):
    """Flat end-of-page CTA section (replaces the retired rounded banner)."""
    body_html = f'<p class="flatcta__body">{body}</p>' if body else ""
    second_html = f' <a class="btn btn--secondary" href="{second[1]}">{second[0]}</a>' if second else ""
    return f"""<section class="flatcta">
  <div class="container">
    <h2 class="flatcta__h">{h2}</h2>
    {body_html}
    <p class="flatcta__actions"><a class="btn btn--primary" href="{href}">{label}</a>{second_html}</p>
  </div>
</section>"""


def impact_stats(stats, cols=None):
    cells = "".join(
        f'<div class="impact-stat reveal" data-stagger="{i % 4 + 1}"><p class="impact-stat__n count-up">{v}</p><p class="impact-stat__l">{l}</p></div>'
        for i, (v, l) in enumerate(stats))
    return f'<div class="impact-grid{" impact-grid--3" if (cols or len(stats)) == 3 else ""}">{cells}</div>'


# Recognition marks. Candid seal is the live official widget SVG for EIN
# 81-5162502 saved locally; GreatNonprofits is the official hi-res Top-Rated
# badge from cdn.greatnonprofits.org; the UN ECOSOC lockup is built in-house
# (the UN does not license its emblem to NGOs). See the build report.
BADGES = [
    ("/assets/img/badges/un-ecosoc-consultative-status-2020.svg", 320, 108,
     "UN ECOSOC Special Consultative Status", "SRLC Global", "UN ECOSOC Special Consultative Status, 2020"),
    ("/assets/img/badges/greatnonprofits-top-rated-2025.png", 534, 400,
     "GreatNonprofits Top-Rated Nonprofit badge", "SRLC USA", "GreatNonprofits Top-Rated"),
    ("/assets/img/badges/candid-gold-seal-2025.svg", 108, 108,
     "Candid Gold Seal of Transparency 2025", "SRLC USA", "Candid Gold Transparency Seal, 2025"),
]


def recognition_chips():
    """Flat one-row band of the three official badge images with captions,
    thin dividers, no cards. Keeps the recognition-cluster__items class so
    existing wrappers keep working."""
    items = "".join(
        f'<figure class="recognition-badge">'
        f'<img class="recognition-badge__img" src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'
        f'<figcaption class="recognition-badge__cap"><strong>{a}</strong> &middot; {b}</figcaption>'
        f'</figure>'
        for src, w, h, alt, a, b in BADGES)
    return f'<div class="recognition-cluster__items recognition-badges">{items}</div>'
