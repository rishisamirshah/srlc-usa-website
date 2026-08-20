"""Shared page shell + components — SRLC USA purple system (team-approved base).
Copy rules per A4: no em dashes, approved stats only, seva locked to Our Inspiration.
"""

SITE = "https://srlcusa.netlify.app"  # swap to https://srlcusa.org at DNS cutover
EMAIL = "info@srlc-usa.org"
PHONE = "1.551.775.2872"
PHONE_VANITY = "1.551.SRLC.USA"
ADDRESS = "500 Paterson Plank Rd #33685<br>Union City, NJ 07087, USA"
EIN_LINE = ("Shrimad Rajchandra Love and Care USA is a registered 501(c)(3) nonprofit "
            "organization. EIN 81-5162502. Contributions are tax deductible to the "
            "extent permitted by law.")
IG = "https://www.instagram.com/srlc_usa/"
FB = "https://www.facebook.com/SRLCUSA/"

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..700&"
         "family=DM+Sans:ital,opsz,wght@0,9..40,300..700;1,9..40,300..700&display=swap")

SOCIAL_SVG = {
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2m0 4.8a5 5 0 1 1 0 10 5 5 0 0 1 0-10m0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4m5.2-3a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12"/></svg>',
}

ICON_SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="vu-i-heart-hand" viewBox="0 0 24 24"><path d="M12 21s-7-4.6-7-10.3a4.7 4.7 0 0 1 8-3.3 4.7 4.7 0 0 1 8 3.3C21 16.4 14 21 12 21Z"/></symbol>
<symbol id="vu-i-people" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9" r="2.6"/><path d="M3 19c.5-3 3-5 6-5s5.5 2 6 5"/><path d="M14 18c.5-2.4 2.3-4 4-4 1.5 0 3 1.2 3.5 3"/></symbol>
<symbol id="vu-i-medical-cross" viewBox="0 0 24 24"><path d="M10 3h4v6h6v4h-6v6h-4v-6H4V9h6z"/></symbol>
<symbol id="vu-i-graduation-cap" viewBox="0 0 24 24"><path d="M3 9 12 4l9 5-9 5L3 9Z"/><path d="M7 11v4c0 1 2.2 2.5 5 2.5s5-1.5 5-2.5v-4"/><path d="M21 9v5"/></symbol>
<symbol id="vu-i-shield" viewBox="0 0 24 24"><path d="M12 3 4 6v6c0 5 3.5 8.5 8 9 4.5-.5 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></symbol>
<symbol id="vu-i-check" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/></symbol>
<symbol id="vu-i-doc" viewBox="0 0 24 24"><path d="M6 3h9l5 5v13H6z"/><path d="M14 3v6h6"/><path d="M9 13h7M9 17h7"/></symbol>
<symbol id="vu-i-chart" viewBox="0 0 24 24"><rect x="4" y="12" width="3" height="8"/><rect x="10" y="8" width="3" height="12"/><rect x="16" y="4" width="3" height="16"/></symbol>
<symbol id="vu-i-calendar" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></symbol>
<symbol id="vu-i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
</defs></svg>"""


def head(title, desc, path):
    canonical = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/photos/school-children-hero.jpg">
<link rel="icon" type="image/png" href="/assets/img/srlc-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site.css?v=5">
<script src="/assets/js/site.js?v=5" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{ICON_SPRITE}
"""


def nav_panel_link(href, label, desc):
    return (f'<a class="primary-nav__sublink" role="menuitem" href="{href}">'
            f'<span class="primary-nav__sublabel">{label}</span>'
            f'<span class="primary-nav__subdesc">{desc}</span></a>')


def nav():
    return f"""<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Shrimad Rajchandra Love and Care USA home">
      <img class="brand__flame" src="/assets/img/srlc-mark.png" alt="" width="44" height="38" loading="eager">
      <span class="brand__lockup-h"><span class="brand__name-h">SHRIMAD RAJCHANDRA</span><span class="brand__tag-h">Love and Care</span></span>
    </a>
    <nav class="primary-nav" aria-label="Primary">
      <ul class="primary-nav__list">
        <li class="primary-nav__item"><button class="primary-nav__trigger" type="button" aria-expanded="false" aria-haspopup="true" aria-controls="navpanel-about">About Us</button>
          <div class="primary-nav__panel" id="navpanel-about" role="menu" aria-label="About Us submenu">
            {nav_panel_link("/about/our-inspiration/", "Our Inspiration", "The spiritual lineage that inspires SRLC&rsquo;s mission.")}
            {nav_panel_link("/about/who-we-are/", "Who We Are", "A modern overview of SRLC USA. Who, what, and how.")}
            {nav_panel_link("/about/our-impact/", "Our Impact", "Program outcomes, impact stories, aggregate numbers.")}
            {nav_panel_link("/about/management/", "Management Team", "Board, leadership, and team profiles.")}
            {nav_panel_link("/about/financials/", "Financials", "Annual reports and Form 990 filings.")}
          </div>
        </li>
        <li class="primary-nav__item"><button class="primary-nav__trigger" type="button" aria-expanded="false" aria-haspopup="true" aria-controls="navpanel-work">Our Work</button>
          <div class="primary-nav__panel" id="navpanel-work" role="menu" aria-label="Our Work submenu">
            {nav_panel_link("/our-work/10-care-program/", "10 Care Program", "The 10 focus areas that frame SRLC&rsquo;s work globally.")}
            {nav_panel_link("/our-work/united-states/", "Where We Serve", "The three places SRLC operates.")}
            <div class="primary-nav__subnest">
              <a class="primary-nav__sublink--nested" role="menuitem" href="/our-work/united-states/">United States</a>
              <a class="primary-nav__sublink--nested" role="menuitem" href="/our-work/india/">India</a>
              <a class="primary-nav__sublink--nested" role="menuitem" href="/our-work/mission-africa/">Mission Africa</a>
            </div>
          </div>
        </li>
        <li class="primary-nav__item"><button class="primary-nav__trigger" type="button" aria-expanded="false" aria-haspopup="true" aria-controls="navpanel-involved">Get Involved</button>
          <div class="primary-nav__panel" id="navpanel-involved" role="menu" aria-label="Get Involved submenu">
            {nav_panel_link("/donate/", "Donate", "One-time or recurring giving, matching gifts, DAF grants.")}
            {nav_panel_link("/volunteer/", "Volunteer", "Sign up for SRLC volunteer opportunities across U.S. cities.")}
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
    return f"""</main><footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="site-footer__cols">
      <div>
        <p class="site-footer__brand"><img class="brand__logo-img" src="/assets/img/srlc-logo-color.png" alt="Shrimad Rajchandra Love and Care" loading="lazy"></p>
        <p class="site-footer__legal">SRLC USA is a registered 501(c)(3).</p>
        <p class="site-footer__legal">EIN: 81-5162502</p>
        <p class="site-footer__legal"><a href="mailto:{EMAIL}" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor">{EMAIL}</a></p>
        <p class="site-footer__legal">{ADDRESS}<br>{PHONE_VANITY}</p>
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
          <li><a href="/about/management/">Management Team</a></li>
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
          <li><a href="/volunteer/">Volunteer</a></li>
          <li><a href="/donate/#matching">Corporate Matching</a></li>
        </ul>
      </div>
      <div>
        <h4>Connect</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">Contact Us</a></li>
          <li><a href="/#final-newsletter">Newsletter Signup</a></li>
          <li><a href="tel:+15517752872">{PHONE}</a></li>
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


def page(title, desc, path, body):
    return head(title, desc, path) + nav() + body + footer()


# ---------- Components ----------

def ph(label, cls="", style=""):
    s = f' style="{style}"' if style else ""
    return (f'<div class="ph-media {cls}"{s}><span><img class="ph-mark" src="/assets/img/srlc-mark.png" alt="">'
            f'<br>{label}</span></div>')


def img(src, alt, cls="", style=""):
    s = f' style="{style}"' if style else ""
    return f'<div class="vu-split__photo {cls}"{s}><img src="{src}" alt="{alt}" loading="lazy"></div>'


def hero_purple(crumb_html, title_html, sub=None, chips=None, ctas=None):
    sub_html = f'<p class="hero__sub">{sub}</p>' if sub else ""
    chips_html = ""
    if chips:
        chips_html = '<div class="chip-row">' + "".join(f"<span>{c}</span>" for c in chips) + "</div>"
    ctas_html = f'<div class="hero__ctas">{ctas}</div>' if ctas else ""
    return f"""<section class="hero hero--purple">
  <div class="container hero__inner">
    <p class="hero__crumb">{crumb_html}</p>
    <h1 class="hero__title">{title_html}</h1>
    {sub_html}
    {chips_html}
    {ctas_html}
  </div>
</section>"""


def vu_section(title_html, lead=None, body="", shell="lav", first=False, extra_head=""):
    cls = {"lav": "vu-shell--lav", "cream": "vu-shell--cream", "ink": "vu-shell--ink", "purple": "vu-shell--purple"}[shell]
    first_cls = " vu-shell--first" if first else ""
    lead_html = f'<p class="vu-lead">{lead}</p>' if lead else ""
    return f"""<section class="vu-shell {cls}{first_cls}">
  <div class="container">
    <h2 class="vu-h reveal">{title_html}</h2>
    {lead_html}{extra_head}
    {body}
  </div>
</section>"""


def actionbar(title, body, cta_label, cta_href="/donate/", second=None):
    second_html = f'<a class="btn btn--ghost" href="{second[1]}">{second[0]}</a>' if second else ""
    return f"""<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-actionbar reveal">
      <div class="vu-actionbar__copy">
        <h3>{title}</h3>
        <p>{body}</p>
      </div>
      <div class="vu-actionbar__ctas">
        <a class="btn btn--primary" href="{cta_href}">{cta_label}</a>
        {second_html}
      </div>
    </div>
  </div>
</section>"""


def impact_stats(stats, cols=None):
    n = cols or (3 if len(stats) == 3 else 4)
    grid_cls = "impact-grid impact-grid--3" if n == 3 else "impact-grid"
    cells = "".join(
        f'<div class="impact-stat reveal" data-stagger="{i % 4 + 1}"><p class="impact-stat__n count-up">{v}</p><p class="impact-stat__l">{l}</p></div>'
        for i, (v, l) in enumerate(stats))
    return f'<div class="{grid_cls}">{cells}</div>'


def recognition_chips():
    chips = [
        ("UN ECOSOC", "Special Consultative Status, 2020"),
        ("U.S. IRS", "501(c)(3) &middot; EIN 81-5162502"),
        ("NABH", "Hospital Accreditation"),
        ("GreatNonprofits", "Top-Rated"),
        ("Candid", "Gold Transparency Seal, 2025"),
    ]
    items = "".join(f'<span class="recognition-chip"><strong>{a}</strong> &middot; {b}</span>' for a, b in chips)
    return f'<div class="recognition-cluster__items">{items}</div>'


def trust_bar(items):
    cells = "".join(
        f'<div class="trust-bar__item"><span class="trust-bar__label">{l}</span><span class="trust-bar__value">{v}</span></div>'
        for l, v in items)
    return f'<section class="trust-bar"><div class="container trust-bar__inner">{cells}</div></section>'
