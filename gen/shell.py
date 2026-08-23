"""Shared page shell + components — SRLC USA purple system, flat pass (Aug 23).
Sources: Naman's CLAUDE.md v2 (gen/naman-claude.md), SRLC_USA_Brand_Guide.pdf,
approved homepage HTML v2, and the Aug 22 edits list. No em dashes, approved
stats only, spiritual content only on /about/our-inspiration/.
"""

SITE = "https://srlcusa.netlify.app"  # staging; production per Aug decision is AWS Amplify
EMAIL = "info@srlc-usa.org"           # domain ruling pending Naman; do not mass-change
PHONE = "1.551.775.2872"
EIN_LINE = ("Shrimad Rajchandra Love and Care USA is a registered 501(c)(3) nonprofit "
            "organization. EIN 81-5162502. Contributions are tax deductible to the "
            "extent permitted by law.")
IG = "https://www.instagram.com/srlc_usa/"
FB = "https://www.facebook.com/SRLCUSA/"

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&"
         "family=Jost:ital,wght@0,300..700;1,300..700&display=swap")

SOCIAL_SVG = {
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2m0 4.8a5 5 0 1 1 0 10 5 5 0 0 1 0-10m0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4m5.2-3a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12"/></svg>',
}


def head(title, desc, path, overlay=False):
    canonical = SITE + path
    body_cls = ' class="has-overlay-nav"' if overlay else ""
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
<link rel="icon" type="image/png" href="/assets/img/srlc-logo.png">
<link rel="preload" as="image" href="/assets/img/photos/school-children-hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site.css?v=6">
<script>document.documentElement.classList.replace("no-js","js")</script>
<script src="/assets/js/site.js?v=6" defer></script>
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
      <img class="brand__logo brand__logo--dark" src="/assets/img/srlc-logo.png" alt="Shrimad Rajchandra Love and Care" width="98" height="52" loading="eager">
      <img class="brand__logo brand__logo--light" src="/assets/img/srlc-logo-white.png" alt="Shrimad Rajchandra Love and Care" width="225" height="36" loading="eager">
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
        <p class="site-footer__brand"><img class="brand__logo-img" src="/assets/img/srlc-logo-white.png" alt="Shrimad Rajchandra Love and Care" width="263" height="42" loading="lazy"></p>
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
    return head(title, desc, path, overlay) + nav(overlay) + body + footer()


# ---------- Components ----------

def ph(label, cls="", style=""):
    """Grey placeholder block with a one-line label from the tab's visual
    direction line. Swapped for Media Bank photography as consent clears."""
    s = f' style="{style}"' if style else ""
    return f'<div class="ph-media {cls}"{s}><span>{label}</span></div>'


def page_header(eyebrow, h1, sub=None, cta=None):
    """SRA-pattern page header: one small eyebrow line, short single-color H1."""
    sub_html = f'<p class="pagehead__sub">{sub}</p>' if sub else ""
    cta_html = f'<div class="pagehead__cta">{cta}</div>' if cta else ""
    return f"""<section class="pagehead">
  <div class="container">
    <p class="pagehead__eyebrow">{eyebrow}</p>
    <h1 class="pagehead__h1">{h1}</h1>
    {sub_html}
    {cta_html}
  </div>
</section>"""


def trust_bar():
    """Brand Guide trust bar: exactly these 4 signals, no more."""
    items = [
        "U.S. Chapter of a UN-Recognized Nonprofit",
        "501(c)(3) Tax-Deductible",
        "Chapters in 11 States + D.C.",
        "33M+ Lives Touched Globally",
    ]
    cells = "".join(f'<div class="trust-bar__item"><span class="trust-bar__value">{t}</span></div>' for t in items)
    return f'<section class="trust-bar"><div class="container trust-bar__inner">{cells}</div></section>'


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


def recognition_chips():
    chips = [
        ("SRLC Global", "UN ECOSOC Special Consultative Status, 2020"),
        ("SRLC USA", "GreatNonprofits Top-Rated"),
        ("SRLC USA", "Candid Gold Transparency Seal, 2025"),
    ]
    items = "".join(f'<span class="recognition-chip"><strong>{a}</strong> &middot; {b}</span>' for a, b in chips)
    return f'<div class="recognition-cluster__items">{items}</div>'
