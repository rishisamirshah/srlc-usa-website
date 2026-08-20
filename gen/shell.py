"""Shared page shell + components for the SRLC USA site generator.
All copy rules follow the content doc's A4 standing rules: no em dashes,
approved stats only, 'seva'/spiritual framing locked to Our Inspiration.
"""

SITE = "https://srlcusa.netlify.app"  # swap to https://srlcusa.org at DNS cutover
EMAIL = "info@srlc-usa.org"
PHONE = "1.551.775.2872"
EIN_LINE = ("Shrimad Rajchandra Love and Care USA is a registered 501(c)(3) nonprofit "
            "organization. EIN 81-5162502. Contributions are tax deductible to the "
            "extent permitted by law.")
IG = "https://www.instagram.com/srlc_usa/"
FB = "https://www.facebook.com/SRLCUSA/"

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Fraunces:ital,opsz,wght@0,9..144,300..640;1,9..144,300..640&"
         "family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap")


def head(title, desc, path, overlay=False):
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
<link rel="stylesheet" href="/assets/css/site.css?v=3">
<script src="/assets/js/site.js?v=3" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def nav(overlay=False):
    mode = "header--overlay" if overlay else "header--solid"
    return f"""<header class="header {mode}">
  <div class="header__inner">
    <a class="brand" href="/" aria-label="SRLC USA home">
      <img class="brand__mark" src="/assets/img/srlc-logo-color.png" alt="Shrimad Rajchandra Love and Care">
      <img class="brand__mark--light" src="/assets/img/srlc-logo-white.png" alt="Shrimad Rajchandra Love and Care">
    </a>
    <button class="navtoggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav" aria-label="Primary">
      <div class="nav__item">
        <button class="nav__link" aria-expanded="false">Our Work <span class="caret"></span></button>
        <div class="dropdown">
          <div class="dd-label">Where We Serve</div>
          <a href="/our-work/united-states/">United States</a>
          <a href="/our-work/india/">India</a>
          <a href="/our-work/mission-africa/">Mission Africa</a>
          <hr>
          <a href="/our-work/10-care-program/">The 10 Care Program</a>
        </div>
      </div>
      <div class="nav__item">
        <button class="nav__link" aria-expanded="false">About <span class="caret"></span></button>
        <div class="dropdown">
          <a href="/about/who-we-are/">Who We Are</a>
          <a href="/about/our-impact/">Our Impact</a>
          <a href="/about/our-inspiration/">Our Inspiration</a>
          <a href="/about/management/">Management Team</a>
          <a href="/about/financials/">Financials</a>
        </div>
      </div>
      <div class="nav__item"><a class="nav__link" href="/volunteer/">Volunteer</a></div>
      <a class="btn btn--fill mobile-only" href="/donate/">Donate</a>
    </nav>
    <a class="btn btn--fill" href="/donate/">Donate</a>
  </div>
</header>
<main id="main">
"""


SOCIAL_SVG = {
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2m0 1.8c-3.1 0-3.5 0-4.8.1-1.1.1-1.5.2-1.8.3-.5.2-.8.4-1.1.7-.3.3-.5.6-.7 1.1-.1.3-.3.8-.3 1.8-.1 1.2-.1 1.6-.1 4.8s0 3.5.1 4.8c.1 1.1.2 1.5.3 1.8.2.5.4.8.7 1.1.3.3.6.5 1.1.7.3.1.8.3 1.8.3 1.2.1 1.6.1 4.8.1s3.5 0 4.8-.1c1.1-.1 1.5-.2 1.8-.3.5-.2.8-.4 1.1-.7.3-.3.5-.6.7-1.1.1-.3.3-.8.3-1.8.1-1.2.1-1.6.1-4.8s0-3.5-.1-4.8c-.1-1.1-.2-1.5-.3-1.8-.2-.5-.4-.8-.7-1.1-.3-.3-.6-.5-1.1-.7-.3-.1-.8-.3-1.8-.3-1.2-.1-1.6-.1-4.8-.1M12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10m0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4m5.2-3a1.2 1.2 0 1 1 0 2.4 1.2 1.2 0 0 1 0-2.4"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12"/></svg>',
}


def footer():
    return f"""</main>
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="/assets/img/srlc-logo-white.png" alt="Shrimad Rajchandra Love and Care">
        <p>An initiative of Shrimad Rajchandra Mission Dharampur, serving communities across the United States and around the world.</p>
        <div class="social">
          <a href="{IG}" aria-label="Instagram" rel="noopener" target="_blank">{SOCIAL_SVG['ig']}</a>
          <a href="{FB}" aria-label="Facebook" rel="noopener" target="_blank">{SOCIAL_SVG['fb']}</a>
        </div>
      </div>
      <div>
        <h4>Our Work</h4>
        <ul>
          <li><a href="/our-work/united-states/">United States</a></li>
          <li><a href="/our-work/india/">India</a></li>
          <li><a href="/our-work/mission-africa/">Mission Africa</a></li>
          <li><a href="/our-work/10-care-program/">10 Care Program</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="/about/who-we-are/">Who We Are</a></li>
          <li><a href="/about/our-impact/">Our Impact</a></li>
          <li><a href="/about/our-inspiration/">Our Inspiration</a></li>
          <li><a href="/about/management/">Management Team</a></li>
          <li><a href="/about/financials/">Financials</a></li>
        </ul>
      </div>
      <div>
        <h4>Connect</h4>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="tel:+15517752872">{PHONE}</a></li>
          <li><a href="/volunteer/">Volunteer with us</a></li>
          <li><a href="/donate/">Ways to give</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__legal">
      <span>{EIN_LINE}</span>
      <span>&copy; <span data-year>2026</span> SRLC USA</span>
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
    """Intentional media placeholder until the Media Bank photo is placed."""
    s = f' style="{style}"' if style else ""
    return (f'<div class="media media--plain {cls}"{s}><div class="ph">'
            f'<img class="ph__mark" src="/assets/img/srlc-mark.png" alt="">'
            f'<span>{label}</span></div></div>')


def img(src, alt, cls="", drift=False, style=""):
    d = " drift" if drift else ""
    s = f' style="{style}"' if style else ""
    return f'<div class="media{" " + cls if cls else ""}{d}"{s}><img src="{src}" alt="{alt}" loading="lazy"></div>'


def stats_row(stats, cls=""):
    cells = "".join(
        f'<div class="reveal" data-d="{i}"><div class="stat__num counter">{n}</div>'
        f'<div class="stat__label">{l}</div></div>'
        for i, (n, l) in enumerate(stats)
    )
    return f'<div class="stats {cls}">{cells}</div>'


def badges_row():
    items = [
        ("SRLC Global", "UN ECOSOC Special Consultative Status, 2020"),
        ("SRLC USA", "Top-Rated on GreatNonprofits"),
        ("SRLC USA", "Candid Gold Transparency Seal, 2025"),
    ]
    cells = "".join(
        f'<div class="badge reveal" data-d="{i}"><div class="badge__medal">&#10038;</div>'
        f'<div><b>{t}</b><span>{s}</span></div></div>'
        for i, (t, s) in enumerate(items)
    )
    return f'<div class="badges">{cells}</div>'


def cta_band(title_html, body, cta_label, cta_href="/donate/", second=None):
    second_html = f'<a class="btn btn--line-light" href="{second[1]}">{second[0]}</a>' if second else ""
    return f"""<section class="sect sect--dark ctaband grain">
  <div class="flamewash"></div>
  <div class="container center" style="position:relative">
    <h2 class="reveal">{title_html}</h2>
    <p class="lead reveal" data-d="1" style="margin-inline:auto">{body}</p>
    <div class="hero__cta reveal" data-d="2" style="justify-content:center">
      <a class="btn btn--gold" href="{cta_href}">{cta_label} <span class="arr">&rarr;</span></a>
      {second_html}
    </div>
  </div>
</section>"""


def sect_head(eyebrow, title_html, lead=None, center=False):
    c = " center" if center else ""
    lead_html = f'<p class="lead reveal" data-d="1">{lead}</p>' if lead else ""
    return (f'<div class="{c.strip()}"><div class="eyebrow reveal">{eyebrow}</div>'
            f'<h2 class="reveal">{title_html}</h2>{lead_html}</div>')
