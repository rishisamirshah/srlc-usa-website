"""Renderers: homepage (approved v2 base), donate, about cluster, 404 — flat pass."""
import os
import re
from shell import (page, ph, page_header, flat_cta, trust_bar, impact_stats, pinned,
                   recognition_chips, filler, photo, img_tag, story_split, EMAIL, PHONE, EIN_LINE, IG, FB)
import data_naman as NAMAN
from data_states import STATES, CAMPAIGNS
from data_cares import CARES
from data_media import slot
from pages_work import cf_map, editorial_map, flipcard, inst_photo, state_chips

US_FOOTPRINT = "chapters in 11 states and Washington, D.C."

# Homepage stat row: live order and wording from the Homepage tab, as on Sept 7
HOME_STATS = [
    ("33M+", "Lives", "touched globally through various initiatives"),
    ("8.90M+", "Lives", "benefitted globally through Emergency Relief initiatives"),
    ("12.24M+", "People", "benefitted globally through humanitarian initiatives"),
    ("3.28M+", "Students", "supported globally by educational activities"),
    ("8.35M+", "Patients", "treated at Shrimad Rajchandra Hospital"),
    ("450K+", "Animals", "saved, treated, and rehabilitated globally"),
]

# Homepage 10 Care tiles: one photo per Care (placeholders from the filler set
# until Naman points to Media Bank candidates per Care).
CARE_PHOTOS = {
    "health-care": "/assets/img/fillers/hospital-theatre.jpg",
    "educational-care": "/assets/img/fillers/classroom-desk.jpg",
    "child-care": "/assets/img/fillers/children-smiling.jpg",
    "woman-care": "/assets/img/fillers/woman-portrait.jpg",
    "tribal-care": "/assets/img/fillers/children-india.jpg",
    "community-care": "/assets/img/fillers/community-gathering.jpg",
    "humanitarian-care": "/assets/img/fillers/hands-heart.jpg",
    "animal-care": "/assets/img/fillers/animals-dog-cat.jpg",
    "environmental-care": "/assets/img/fillers/hands-seedling.jpg",
    "emergency-relief-care": "/assets/img/fillers/hospital-building.jpg",
}

INSTITUTE_HOME_TAGS = {
    "hospital-and-research-center": "hospital", "vidyapeeth": "classroom", "gurukul": "children",
    "skill-development-center": "skills", "jivamaitridham": "animals", "center-of-excellence-for-women": "women",
}

MATCH_QUALIFIER = ("These are examples of companies with employee matching-gift programs. "
                   "Logos are the property of their respective owners and do not imply "
                   "partnership with or endorsement of SRLC USA.")


def partner_marquee():
    pdir = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "partners")
    logos = sorted(f for f in os.listdir(pdir) if not f.startswith("."))
    def group(hidden):
        alt = (lambda f: "") if hidden else (lambda f: f.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title())
        return "".join(
            f'<div class="marquee-logo"><img src="/assets/img/partners/{f}" alt="{alt(f)}" width="150" height="56" loading="lazy"></div>'
            for f in logos)
    return f"""<div class="partner-marquee" aria-label="Employers with matching gift programs">
  <div class="partner-marquee__track">
    <div class="partner-marquee__group">{group(False)}</div>
    <div class="partner-marquee__group partner-marquee__group--dup" aria-hidden="true">{group(True)}</div>
  </div>
</div>"""


def prose_photo(items, photo_key, tag=None, alt="", numbered=False, reverse=False):
    """Prose block beside one photo (SRA two-col pattern). items = [(title, body)].
    Copy is passed through unchanged; no cards, no grid of equal boxes."""
    blocks = []
    for i, (t, b) in enumerate(items):
        num = f'<span class="prosephoto__num" aria-hidden="true">{i + 1:02d}</span>' if numbered else ""
        blocks.append(f"<h3>{num}{t}</h3><p>{b}</p>")
    src = photo_key if photo_key.startswith("/assets/") else filler(photo_key, tag=tag)
    cls = "prosephoto prosephoto--reverse" if reverse else "prosephoto"
    return (f'<div class="{cls}"><div class="prosephoto__copy">{"".join(blocks)}</div>'
            f'<div class="prosephoto__photo"><img src="{src}" alt="{alt}" width="1200" height="900" loading="lazy"></div></div>')


def care_card_media(icon, name):
    return (f'<div class="care-card__img" style="display:grid;place-items:center;background:#E7E3EC">'
            f'<img src="/assets/img/care-icons/{icon}" alt="" width="110" height="110" style="width:44%;max-width:110px;opacity:.85"></div>')


# Interim photos for slots Naman supplies later ("image to follow"); Media Bank
# picks from data_media win over these.
HOME_FALLBACK = {
    "home-hero-1": ("/assets/img/photos/school-children-hero.jpg", 1600, 1067, "Students gathered outside a school"),
    "home-hero-2": ("/assets/img/fillers/community-gathering.jpg", 2400, 1602, "Community volunteers gathered together"),
    "home-hero-3": ("/assets/img/fillers/children-india.jpg", 1600, 1142, "Children smiling together"),
    "home-impact-story": ("/assets/img/fillers/hospital-building.jpg", 1600, 1064, "Hospital building"),
    "card-donate": ("/assets/img/fillers/children-smiling.jpg", 2400, 1600, "Children smiling"),
    "card-volunteer": ("/assets/img/fillers/hands-heart.jpg", 1600, 1067, "Volunteers' hands together"),
}


def home_img(name):
    return slot(name, HOME_FALLBACK.get(name))


def chapter_finder(svg_inner, activity_html="", tone=""):
    """Homepage chapter finder: ZIP search, optional chapter feed, dark
    editorial map. Shared with the Volunteer page."""
    mod = f" chapter-finder--{tone}" if tone else ""
    return f"""<section class="chapter-finder chapter-finder--v3{mod}" id="find-chapter">
  <div class="container chapter-finder__inner">
    <div class="chapter-finder__intro">
      <h2 class="chapter-finder__h">Find your nearest chapter.</h2>
      <p class="chapter-finder__sub">Enter a ZIP code or click any pin on the map.</p>
    </div>
    <div class="chapter-finder__cols">
      <div class="chapter-finder__search">
        <p class="chapter-finder__search-title">Search by ZIP</p>
        <form class="chapter-finder__form" onsubmit="event.preventDefault(); window.__cfZipLookup &amp;&amp; window.__cfZipLookup();">
          <input type="text" id="zipInput" inputmode="numeric" maxlength="5" placeholder="ZIP code (e.g. 08820)" aria-label="ZIP code" pattern="\\d{{5}}">
          <button type="submit" class="btn btn--primary" id="zipBtn">Find Chapter</button>
        </form>
        <div class="chapter-finder__result" id="zipResult" hidden>
          <p class="chapter-finder__city" id="zipCity"></p>
          <p class="chapter-finder__meta" id="zipMeta"></p>
          <div class="chapter-finder__actions">
            <a id="zipJoinBtn" class="btn btn--primary" href="/get-involved/volunteer/">Join This Chapter</a>
            <a class="btn btn--secondary" href="mailto:{EMAIL}">Email the Lead</a>
          </div>
          <div class="chapter-finder__chips" id="zipChips" hidden>
            <p class="chapter-finder__chips-label">Other chapters in this area</p>
            <div class="chapter-finder__chips-list" id="zipChipsList"></div>
          </div>
        </div>
        <p class="chapter-finder__search-hint">We&rsquo;ll point you to your nearest SRLC USA chapter.</p>
      </div>
      {activity_html}
    </div>
    <div class="chapter-finder__map-wrap edmap--dark">
      {editorial_map(svg_inner)}
      <p class="edmap-legend" aria-hidden="true"><svg viewBox="0 0 14 14"><circle cx="7" cy="7" r="6" fill="#2A1C36"/><circle cx="7" cy="7" r="3" fill="#FFFFFF"/></svg>Active SRLC USA chapter</p>
    </div>
    <p class="chapter-finder__link-row"><a class="btn btn--secondary" href="/our-work/united-states/">Browse All US Chapters</a></p>
  </div>
</section>"""


def nobreak(text):
    """Keep hyphenated words (life-changing, 250-bed) on one line."""
    return re.sub(r"[\w.,+]+(?:-\w+)+", lambda m: f'<span class="nowrap">{m.group(0)}</span>', text)


# Homepage 10 Care tile crops (Naman, Oct 18): the boy stays in frame on Child
# Care; Humanitarian Care zooms in so the two people fill the tile.
CARE_TILE_CROP = {
    "child-care": "background-position:100% 50%",
    "humanitarian-care": "background-size:150%;background-position:50% 47%",
}


def render_home(svg_inner):
    # Naman, Oct 18: the Sept 7 homepage plus only the items he asked for in the
    # refinement doc (Oct 16, revised Oct 17) and on WhatsApp Oct 18. Slides:
    # the organization-level slide leads, the United States slide is second,
    # Classroom of Change third with its CTA on the campaign itself (Venezuela
    # relief retired). Eyebrow, headline, one CTA per slide, no body copy.
    slides = [
        {
            "img": NAMAN.SLIDE_1,
            "eyebrow": "Compassion in Action",
            "title": 'One gift. <span class="nowrap">Ten ways to care.</span>',
            "cta": ("Donate Now", "/donate/"),
        },
        {
            "img": NAMAN.SLIDES[2],
            "eyebrow": "Across the United States",
            "title": "Care and joy, close to home.",
            "cta": ("Get Involved Locally", "/our-work/united-states/"),
        },
        {
            "img": NAMAN.SLIDES[3],
            "eyebrow": "Classroom of Change",
            "title": "Turning the key to brighter futures.",
            "cta": ("See the Initiative", "/our-work/united-states/#classroom-of-change"),
        },
    ]
    slides_html = "".join(f"""<article class="hero-carousel__slide{' is-active' if i == 0 else ''}" data-slide="{i}" role="group" aria-roledescription="slide" aria-label="{i + 1} of 3" style="--bg:url('{s["img"][0]}')">
      <div class="hero-carousel__overlay"></div>
      <div class="container hero-carousel__content">
        <p class="hero-carousel__eyebrow">{s["eyebrow"]}</p>
        {"<h1" if i == 0 else "<p"} class="hero-carousel__title">{s["title"]}{"</h1>" if i == 0 else "</p>"}
        <div class="hero-carousel__ctas">
          <a class="btn btn--primary" href="{s["cta"][1]}">{s["cta"][0]}</a>
        </div>
      </div>
    </article>""" for i, s in enumerate(slides))
    dots = "".join(f'<button class="dot{" is-active" if i == 0 else ""}" data-go="{i}" role="tab" aria-label="Slide {i + 1}"></button>' for i in range(3))

    story_img = NAMAN.STORY
    donate_img = NAMAN.CARDS["donate"]
    volunteer_img = NAMAN.CARDS["volunteer"]

    mstats = "".join(f"""<div class="mstat">
        <p class="mstat__n">{n}</p>
        <p class="mstat__label">{l}</p>
        <p class="mstat__desc">{d}</p>
      </div>""" for n, l, d in HOME_STATS)

    # SRA "Our Unique Approach" tile: photo, flat veil, chip (number + name),
    # hover layer with the one-liner. Below 1024 the same markup collapses to
    # the SRA accordion rows (tap reveals the one-liner, tap again to open).
    care_tiles = "".join(f"""<a class="caretile" href="/our-work/10-care-program/{c["slug"]}/" style="background-image:url('{NAMAN.CARE_TILES[c["slug"]]}'){";" + CARE_TILE_CROP[c["slug"]] if c["slug"] in CARE_TILE_CROP else ""}">
        <span class="caretile__overlay" aria-hidden="true"></span>
        <span class="caretile__chip"><span class="caretile__num">{c["num"]}</span><span class="caretile__name">{c["name"]}</span></span>
        <span class="caretile__hover"><span class="caretile__hover-h">{c["num"]}<br>{c["name"]}</span><span class="caretile__hover-p">{nobreak(c["one"])}</span></span>
      </a>""" for c in CARES)

    from data_india import INSTITUTES
    # charity:water "Ready to take action" row (Naman, Oct 16): edge-to-edge
    # scroller of square photo cards, dark label bar with an icon, flipping to
    # a purple back with the one-liner on hover / tap / keyboard focus.
    institutes_cards = "".join(flipcard(inst, nobreak(inst["home_desc"]), f'/our-work/india/{inst["slug"]}/', link_label="Learn More")
                               for inst in sorted(INSTITUTES, key=lambda i: NAMAN.INSTITUTE_ORDER.index(i["slug"])))

    # Section 7, Latest Articles: hidden until three articles are published
    # (Naman 7.0). Markup kept verbatim inside the comment so it returns as is.
    articles = "".join(f"""<div class="news-card reveal" data-stagger="{i + 1}">
        <div class="news-card__media">{ph("Article image, Media Bank", style="min-height:0;height:100%")}</div>
        <div class="news-card__meta"><span class="news-card__tag">Article slot</span></div>
        <h3 class="news-card__h" style="color:var(--color-ink-muted)">Article pending from the content team</h3>
      </div>""" for i in range(3))

    activity = """<div class="chapter-activity reveal" aria-label="Recent chapter activity">
        <header class="chapter-activity__head">
          <p class="chapter-activity__title">From the chapters</p>
          <span class="chapter-activity__count">22 centers</span>
        </header>
        <ul class="chapter-activity__list">
          <li class="chapter-activity__item">
            <span class="chapter-activity__city">Boston</span>
            <span class="chapter-activity__body">Meal kits assembled and delivered through Open&nbsp;Table<span class="chapter-activity__time">Ongoing</span></span>
          </li>
          <li class="chapter-activity__item">
            <span class="chapter-activity__city">Chicago</span>
            <span class="chapter-activity__body">500+ PB&amp;J sandwiches packed and 1,000+ pounds of food&nbsp;donated<span class="chapter-activity__time">Recent drive</span></span>
          </li>
          <li class="chapter-activity__item">
            <span class="chapter-activity__city">Phoenix</span>
            <span class="chapter-activity__body">Hot meals and breakfast packs with TCAA and Andre&nbsp;House<span class="chapter-activity__time">Year-round</span></span>
          </li>
        </ul>
      </div>"""

    body = f"""
<div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>

<div class="newsletter-modal" id="newsletterModal" role="dialog" aria-modal="true" aria-labelledby="newsletterTitle" hidden>
  <div class="newsletter-modal__backdrop" data-newsletter-close></div>
  <div class="newsletter-modal__panel">
    <button class="newsletter-modal__close" data-newsletter-close aria-label="Close">&times;</button>
    <h3 id="newsletterTitle">Stay informed. Be inspired.</h3>
    <p>Updates on who we serve, the programs we run, and what your support makes possible.</p>
    <form class="newsletter-modal__form" name="updates" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="updates">
      <input type="hidden" name="source" value="modal">
      <p class="hp-field"><input name="bot-field" tabindex="-1"></p>
      <input type="email" name="email" required placeholder="Email address" aria-label="Email address" class="form-hidewrap">
      <button type="submit" class="btn btn--primary form-hidewrap">Subscribe</button>
      <span class="form-success" style="color:var(--color-srlc-purple);font-weight:600">Thank you for subscribing. Please check your inbox to confirm your email.</span>
    </form>
  </div>
</div>

<section class="hero-carousel" id="heroCarousel" aria-roledescription="carousel" aria-label="SRLC USA featured stories">
  <div class="hero-carousel__track">{slides_html}</div>
  <button class="hero-carousel__arrow hero-carousel__arrow--prev" data-dir="prev" aria-label="Previous slide"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg></button>
  <button class="hero-carousel__arrow hero-carousel__arrow--next" data-dir="next" aria-label="Next slide"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg></button>
  <div class="hero-carousel__controls"><div class="hero-carousel__dots" role="tablist" aria-label="Choose slide">{dots}</div></div>
</section>

<section class="mission-split">
  <div class="mission-split__grid">
    <div class="mission-split__copy">
      <p class="mission-split__eyebrow">Our Mission</p>
      <h2 class="mission-split__h">A global initiative to offer service and bring joy to the lives of underserved sections of society.</h2>
      <p class="mission-split__body">Shrimad Rajchandra Love and Care (SRLC) USA is the US chapter of a global nonprofit organization that has been recognized by the United Nations for its humanitarian efforts. A 501(c)(3) organization, SRLC USA supports community development projects across India and Africa, and brings holistic care and joy to local communities throughout the US. With a presence in 25+ cities, SRLC USA focuses on raising funds and awareness in <span class="nowrap">high-impact</span> areas, while putting compassion in action.</p>
      <div class="mission-split__actions">
        <a class="btn btn--primary btn--lg" href="/about/our-impact/">See Our Impact</a>
      </div>
      <p class="mission-split__micro">Registered 501(c)(3) &middot; EIN 81-5162502</p>
    </div>
    <div class="mission-split__stats">{mstats}</div>
  </div>
</section>

<section class="care-section" id="ten-care">
  <div class="container">
    <div class="care-section__head reveal">
      <p class="care-section__eyebrow">Our Work</p>
      <h2 class="care-section__h">The 10 Care Program</h2>
    </div>
    <div class="caregrid">{care_tiles}</div>
    <div class="care-section__cta reveal"><a class="btn btn--secondary" href="/our-work/10-care-program/">Explore the 10 Care Program</a></div>
  </div>
</section>

<section class="named-story" aria-label="Impact story">
  <div class="named-story__grid">
    <div class="named-story__media named-story__media--photo" role="img" aria-label="{story_img[3]}" data-parallax-bg="57 30" style="background-image:url('{story_img[0]}');background-position:57% 30%"></div>
    <div class="named-story__copy-wrap">
      <div class="named-story__copy reveal" data-stagger="1">
        <p class="named-story__eyebrow">Impact Story &middot; Laxibhai</p>
        <p class="named-story__quote">A 52-year-old farmer received the region&rsquo;s <span class="nowrap">first-ever</span> cardiothoracic bypass surgery, performed entirely free of charge. Today he is back on his feet.</p>
        <p class="named-story__attribution">Laxibhai&rsquo;s second chance</p>
        <p class="named-story__attribution-meta">Health Care &middot; Shrimad Rajchandra Hospital and Research Center</p>
        <a class="btn btn--primary named-story__btn" href="/our-work/10-care-program/health-care/">Explore Health Care</a>
      </div>
    </div>
  </div>
</section>

<section class="institutes-section instrow" aria-labelledby="instrow-h">
  <div class="container">
    <div class="institutes-section__head">
      <p class="institutes-section__eyebrow">Where the work happens</p>
      <h2 class="institutes-section__h" id="instrow-h">Our Institutes</h2>
      <p class="institutes-section__sub">Six institutes in South Gujarat, India, each built around a specific need. Your gift supports their <span class="nowrap">day-to-day</span> work.</p>
    </div>
  </div>
  <div class="instrow__viewport">
    <ul class="instrow__track" id="instrowTrack">{institutes_cards}</ul>
  </div>
  <div class="instrow__arrows">
    <button type="button" class="instrow__arrow" data-dir="-1" aria-controls="instrowTrack" aria-label="Previous institutes"><svg viewBox="0 0 44 16" aria-hidden="true"><path d="M43 8H2M9 1L2 8l7 7"/></svg></button>
    <button type="button" class="instrow__arrow" data-dir="1" aria-controls="instrowTrack" aria-label="Next institutes"><svg viewBox="0 0 44 16" aria-hidden="true"><path d="M1 8h41M35 1l7 7-7 7"/></svg></button>
  </div>
</section>

<section class="chapter-finder chapter-finder--v3">
  <div class="container chapter-finder__inner">
    <div class="chapter-finder__intro">
      <h2 class="chapter-finder__h">Find your nearest chapter.</h2>
      <p class="chapter-finder__sub">Enter a ZIP code or click any pin on the map.</p>
    </div>
    <div class="chapter-finder__cols">
      <div class="chapter-finder__search">
        <p class="chapter-finder__search-title">Search by ZIP</p>
        <form class="chapter-finder__form" onsubmit="event.preventDefault(); window.__cfZipLookup &amp;&amp; window.__cfZipLookup();">
          <input type="text" id="zipInput" inputmode="numeric" maxlength="5" placeholder="ZIP code (e.g. 08820)" aria-label="ZIP code" pattern="\\d{{5}}">
          <button type="submit" class="btn btn--primary" id="zipBtn">Find Chapter</button>
        </form>
        <div class="chapter-finder__result" id="zipResult" hidden>
          <p class="chapter-finder__city" id="zipCity"></p>
          <p class="chapter-finder__meta" id="zipMeta"></p>
          <div class="chapter-finder__actions">
            <a id="zipJoinBtn" class="btn btn--primary" href="/get-involved/volunteer/">Join This Chapter</a>
            <a class="btn btn--secondary" href="mailto:{EMAIL}">Email the Lead</a>
          </div>
          <div class="chapter-finder__chips" id="zipChips" hidden>
            <p class="chapter-finder__chips-label">Other chapters in this area</p>
            <div class="chapter-finder__chips-list" id="zipChipsList"></div>
          </div>
        </div>
        <p class="chapter-finder__search-hint">We&rsquo;ll point you to your nearest SRLC USA chapter.</p>
      </div>
      {activity}
    </div>
    <div class="chapter-finder__map-wrap homemap">
      {editorial_map(svg_inner)}
      <div class="cf-map__legend" aria-hidden="true"><span><span class="swatch"></span>Active SRLC USA chapter</span></div>
    </div>
    <p class="chapter-finder__link-row"><a class="btn btn--secondary" href="/our-work/united-states/">Browse All US Chapters</a></p>
  </div>
</section>

<!-- Section 7, Latest Articles: hidden until at least three articles are published (Naman, Sept 3).
<section class="news-section">
  <div class="container">
    <div class="news-section__head">
      <div class="news-section__headcopy">
        <p class="news-section__eyebrow">News and Updates</p>
        <h2 class="news-section__h">Latest Articles</h2>
        <p class="news-section__sub">From our chapters and programs</p>
      </div>
      <a class="btn btn--secondary" href="/news/">View All Articles</a>
    </div>
    <div class="news-grid">{articles}</div>
  </div>
</section>
-->

<section class="takepart" id="take-part" aria-labelledby="takepart-h">
  <div class="container">
    <div class="takepart__head">
      <p class="takepart__eyebrow">Be part of the work</p>
      <h2 class="takepart__h" id="takepart-h">Two ways to make a difference.</h2>
    </div>
    <div class="takepart__cards">
      <article class="photocard">
        <div class="photocard__frame">
          <img class="photocard__img" src="{donate_img[0]}" alt="{donate_img[3]}" width="{donate_img[1]}" height="{donate_img[2]}" loading="lazy" decoding="async">
          <div class="photocard__bar">
            <h3 class="photocard__h">Donate</h3>
            <a class="btn btn--primary" href="/donate/">Donate Now</a>
          </div>
        </div>
        <p class="photocard__caption">To give without expecting anything in return is love in action.</p>
      </article>
      <article class="photocard">
        <div class="photocard__frame">
          <img class="photocard__img" src="{volunteer_img[0]}" alt="{volunteer_img[3]}" width="{volunteer_img[1]}" height="{volunteer_img[2]}" loading="lazy" decoding="async">
          <div class="photocard__bar">
            <h3 class="photocard__h">Volunteer</h3>
            <a class="btn btn--primary" href="/get-involved/volunteer/">Volunteer Near You</a>
          </div>
        </div>
        <p class="photocard__caption">Give someone your heart to understand and a hand to hold.</p>
      </article>
    </div>
    <div class="nlrow" id="final-newsletter">
      <div class="nlrow__copy">
        <p class="nlrow__eyebrow">Stay informed. Be inspired.</p>
        <p class="nlrow__line">Updates on who we serve, the programs we run, and what your support makes possible.</p>
      </div>
      <form class="nlrow__form" name="updates" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="updates">
        <input type="hidden" name="source" value="homepage">
        <p class="hp-field"><input name="bot-field" tabindex="-1"></p>
        <input type="email" name="email" required placeholder="Email address" aria-label="Email address" class="form-hidewrap">
        <button type="submit" class="btn btn--primary form-hidewrap">Subscribe</button>
        <span class="form-success">Thank you for subscribing. Please check your inbox to confirm your email.</span>
      </form>
    </div>
  </div>
</section>

<section class="lotusband" aria-label="Quote">
  <div class="lotusband__inner">
    <blockquote class="lotusband__quote">&ldquo;Selfless service is love made visible.&rdquo;</blockquote>
    <p class="lotusband__attr">Pujya Gurudevshri Rakeshji</p>
  </div>
</section>
"""
    return page(
        "Shrimad Rajchandra Love and Care USA | 501(c)(3) Nonprofit",
        "Health, education, and humanitarian care for underserved communities across India, Africa, and the US. A 501(c)(3) nonprofit. Donate today. SRLC USA.",
        "/", body, overlay=True)

def render_donate():
    tiles = "".join(f"""<button type="button" class="donate-tile{' is-active' if amt == '100' else ''}" data-amount="{amt}">
        <span class="donate-tile__amount">${amt}</span>
        {{outcome_html}}
      </button>""".replace("{{outcome_html}}", f'<span class="donate-tile__outcome">{outcome}</span>' if outcome else "") for amt, outcome in [
        ("25", ""),
        ("50", "Provides a month of nutrition support for a child"),
        ("100", ""),
        ("250", ""),
        ("500", ""),
    ])
    ways = [
        ("Give by ACH, check, or wire", "Bank transfer and mailed checks are our most efficient ways to receive your gift: more of every dollar reaches the programs. Write to us and we will send the details the same week.", f"mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA", "Email Us to Give"),
        ("Donor-advised funds and charitable trusts", "Recommend a grant to Shrimad Rajchandra Love and Care USA through your donor-advised fund or charitable trust. EIN 81-5162502.", f"mailto:{EMAIL}?subject=DAF%20grant%20to%20SRLC%20USA", "Start a DAF Grant"),
        ("Appreciated stock", "Giving appreciated stock can be one of the most tax-efficient ways to support the work. Write to us and we will coordinate the transfer with your broker.", f"mailto:{EMAIL}?subject=Stock%20gift%20to%20SRLC%20USA", "Give Stock"),
        ("Cryptocurrency", "Ask us about giving crypto. We will confirm what we can currently accept and walk you through it.", f"mailto:{EMAIL}?subject=Crypto%20gift%20to%20SRLC%20USA", "Ask About Crypto"),
        ("Corporate matching", "Your employer may match your gift. Check if your company participates, and your impact can double before it leaves your paycheck.", f"mailto:{EMAIL}?subject=Matching%20gift%20question", "Ask About Matching"),
    ]
    ways_html = "".join(f"""<details{' open' if i == 0 else ''}>
      <summary>{t}</summary>
      <p style="margin:0.4rem 0 0.6rem;color:var(--color-ink-muted)">{b}</p>
      <p style="margin:0"><a href="{h}">{cta}</a></p>
    </details>""" for i, (t, b, h, cta) in enumerate(ways))

    body = page_header(
        "Get Involved",
        "Every gift becomes someone&rsquo;s morning.",
        "A meal delivered, a backpack filled, a surgery that costs a family nothing. Choose an amount and the way of giving that fits you.",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first" id="donate-tiles">
  <div class="container" style="max-width:56rem">
    <div class="donate-tiles__head">
      <h2 class="donate-tiles__h">Choose your gift</h2>
      <p class="donate-tiles__sub">Amounts are illustrative pending finance review. Online card giving is being set up; until it launches, our team personally handles every gift by email or phone, usually the same day.</p>
    </div>
    <div class="donate-tiles__toggle-wrap">
      <div class="donate-tiles__toggle" role="tablist" aria-label="Giving frequency">
        <button type="button" class="is-active" data-freq="once" aria-selected="true">One Time</button>
        <button type="button" data-freq="monthly" aria-selected="false">Monthly</button>
      </div>
    </div>
    <div class="donate-tiles__grid">
      {tiles}
    </div>
    <div class="donate-tiles__cta">
      <a class="btn btn--primary btn--lg" id="donate-tiles-cta" href="mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA%20(%24100)">Email Us to Give</a>
      <p class="donate-tiles__monthly-note" id="donate-tiles-monthly-note" hidden>Give monthly and provide steady, year-round support.</p>
    </div>
  </div>
</section>

{trust_bar()}

<section class="vu-shell vu-shell--cream">
  <div class="container" style="max-width:820px">
    <h2 class="vu-h reveal">Ways to give</h2>
    <div class="accordion mt-6">{ways_html}</div>
  </div>
</section>

<section class="vu-shell vu-shell--lav" id="matching">
  <div class="container">
    <h2 class="vu-h reveal" style="text-align:center">Does your employer match gifts?</h2>
    <p style="text-align:center;font-size:.82rem;color:var(--color-ink-muted);max-width:62ch;margin:0.6rem auto 1.2rem">{MATCH_QUALIFIER}</p>
    <div>{partner_marquee()}</div>
    <p class="text-center mt-6" style="text-align:center"><a class="btn btn--secondary" href="mailto:{EMAIL}?subject=Matching%20gift%20question">Check Your Employer</a></p>
  </div>
</section>

<section class="vu-shell vu-shell--cream vu-shell--narrow">
  <div class="container" style="max-width:820px;text-align:center">
    <p style="font-size:.9rem;color:var(--color-ink-muted);margin-top:1.2rem">{EIN_LINE}</p>
    <p style="font-size:.9rem;color:var(--color-ink-muted)">Reach us at <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
  </div>
</section>
<script>
(function () {{
  function currentAmt() {{
    var t = document.querySelector('.donate-tile.is-active');
    return t ? t.getAttribute('data-amount') : '';
  }}
  function freq() {{
    var b = document.querySelector('.donate-tiles__toggle button.is-active');
    return b && b.getAttribute('data-freq') === 'monthly' ? ' monthly' : '';
  }}
  function sync() {{
    var cta = document.getElementById('donate-tiles-cta');
    if (!cta) return;
    var amt = currentAmt();
    var subj = 'Donation to SRLC USA' + (amt ? ' ($' + amt + freq() + ')' : '');
    cta.href = 'mailto:{EMAIL}?subject=' + encodeURIComponent(subj);
  }}
  document.addEventListener('click', function (e) {{
    if (e.target.closest('.donate-tile') || e.target.closest('.donate-tiles__toggle button')) setTimeout(sync, 20);
  }});
  sync();
}})();
</script>
"""
    return page(
        "Donate | SRLC USA | 501(c)(3) Nonprofit",
        "Give to SRLC USA by ACH, check, stock, DAF, or corporate matching. A 501(c)(3) nonprofit, EIN 81-5162502. Every gift reaches real programs.",
        "/donate/", body)


def render_who_we_are():
    # Rebuilt per Naman's Oct 16 doc: Hero, Who We Are, What We Support, Care
    # and Joy Close to Home, Why We Serve, How We Work, Continue Reading. No stat
    # row, no Donate CTA. Every body line is verbatim from the Who We Are tab;
    # the tab predates the seven-section structure, so the mapping is flagged.
    routes = {
        "wwa-hero": (["volunteers", "us-community"], 1600),
        "wwa-who": (["volunteers", "us-community"], 1200),
        "wwa-support": (["hospital+india", "india"], 1200),
        "wwa-home": (["us-community", "volunteers"], 1200),
    }
    img = lambda k: slot(k) or photo(k, routes[k][0], "community", min_w=routes[k][1])
    how = [
        ("Volunteer led", "Programs are carried by volunteers who know their communities. Because they give their time, administration costs stay low and more of every dollar reaches the programs it was given to support."),
        ("Designed to scale", "We invest in models that can be replicated, so a program that works in one community can be extended to the next."),
        ("Measured against evidence", "Every initiative operates within professional frameworks and defined performance indicators. Results, not intentions, decide what continues."),
        ("Building the next generation of leaders", "Volunteers of every generation carry this work, from students to retirees, and young people lead most of the initiatives under the 10 Care Program."),
    ]
    how_html = "".join(f'<div class="howwork__item"><h3>{t}</h3><p>{b}</p></div>' for t, b in how)
    pills = """<div class="pillrow">
      <a class="btn btn--secondary" href="/our-work/10-care-program/">10 Care Program</a>
      <a class="btn btn--secondary" href="/our-work/united-states/">United States</a>
      <a class="btn btn--secondary" href="/our-work/india/">India</a>
      <a class="btn btn--secondary" href="/our-work/mission-africa/">Mission Africa</a>
    </div>"""
    hero = img("wwa-hero")

    body = page_header("About Us", "Who We Are", "Love and care, in action", image=hero[0], size=(hero[1], hero[2]), alt=hero[3]) + f"""
{story_split("Who We Are", ["SRLC USA is what happens when physicians, engineers, teachers, and students decide their weekends belong to their neighbors. We are the US chapter of Shrimad Rajchandra Love and Care, a global nonprofit holding Special Consultative Status with the United Nations Economic and Social Council (ECOSOC), and a <span class='nowrap'>501(c)(3)</span> organization. But before we are any of that, we are people who believe care is not a profession. It is a practice."], img("wwa-who"), tone="white")}
{story_split("What We Support", ["We focus on immediate needs and the systems behind them. In the United States, volunteers prepare and share meals, equip students for the school year, and organize community care events with local partners. Globally, the movement builds and sustains hospitals, schools, and development programs designed to serve for generations. The programs differ; the standard does not: high-quality, sustainable work that outlasts the day we arrive."], img("wwa-support"), reverse=True, tone="lav")}
{story_split("Care and Joy Close to Home", ["Every initiative we run belongs to one of ten focus areas, together the 10 Care Program: Health Care, Educational Care, Child Care, Woman Care, Tribal Care, Community Care, Humanitarian Care, Animal Care, Environmental Care, and Emergency Relief Care. In the United States, that vision looks like service in your own city, on your own street. Globally, it stands as permanent institutes in India and Mission Africa."], img("wwa-home"), tone="white", extra=pills)}

<section class="lotusband lotusband--page" aria-labelledby="wwa-why">
  <div class="lotusband__inner">
    <h2 class="lotusband__eyebrow" id="wwa-why">Why We Serve</h2>
    <blockquote class="lotusband__quote">&ldquo;When there is love within, it flows naturally in the form of care.&rdquo;</blockquote>
    <p class="lotusband__line">We serve and bring joy, not because we have to, or because it is our duty, but because we love to.</p>
  </div>
</section>

<section class="howwork" aria-labelledby="wwa-how">
  <div class="container">
    <p class="howwork__eyebrow">How We Work</p>
    <h2 class="howwork__h" id="wwa-how">Built to be trusted</h2>
    <div class="howwork__grid">{how_html}</div>
    <div class="howwork__recog">{recognition_chips(holders_only=True)}</div>
    <p class="howwork__cta"><a class="btn btn--primary" href="/about/financials/">See Our Financials</a></p>
  </div>
</section>

<section class="pagenext">
  <div class="container pagenext__inner">
    <h2 class="pagenext__line">Continue Reading</h2>
    <div class="pagenext__links">
      <a class="btn btn--secondary" href="/about/our-impact/">Our Impact</a>
      <a class="btn btn--secondary" href="/about/management-team/">Management Team</a>
      <a class="btn btn--secondary" href="/about/inspiration-and-founder/">Inspiration and Founder</a>
    </div>
  </div>
</section>
"""
    return page(
        "Who We Are | SRLC USA | 501(c)(3) Nonprofit",
        "Meet the volunteers bringing care and joy to communities across the US and worldwide. A 501(c)(3) nonprofit. See who we are. SRLC USA.",
        "/about/who-we-are/", body)


TIMELINE = [
    ("2006 to 2008", "Mobile care begins", "A mobile dispensary begins carrying medical care to rural doorsteps, and a mid-day meal program gives families one more reason to send their children to school."),
    ("2009 to 2011", "Gurukul opens", "Shrimad Rajchandra Gurukul opens in Karanjveri, Gujarat, and a new neonatal intensive care unit begins providing critical care for premature newborns."),
    ("2015", "First Love and Care Walk", "New York City hosts SRLC&rsquo;s first Love and Care Walk, with more than 550 participants."),
    ("2016", "Vidyapeeth opens", "Shrimad Rajchandra Vidyapeeth opens as the first science college serving 238 villages of South Gujarat, and the Skill Development Center begins vocational training for tribal youth."),
    ("2019", "GuideStar Platinum", "GuideStar awards SRLC its Platinum Seal for the highest level of transparency and accountability."),
    ("2020", "UN recognition", "The United Nations grants SRLC Special Consultative Status. Vidyapeeth and Gurukul earn ISO 9001 and ISO 29990 certification."),
    ("2021", "Pandemic relief", "COVID-19 relief reaches 50 cities on five continents, supporting 8.85M+ lives."),
    ("2022", "The hospital opens", "The 250-bed Shrimad Rajchandra Hospital and Research Center opens, and its surgeons perform the region&rsquo;s first open-heart cardiothoracic surgery."),
    ("2023", "NABH, and Nairobi", "The hospital earns NABH accreditation within its first year. In Nairobi, Kenya, a free eye and ENT medical camp treats 7,500+ patients."),
    ("2024", "Mission Africa launches", "Mission Africa launches across 16 African nations. A mega-medical camp in Dharampur serves 25,000+ people, and US centers deliver 90,000+ educational items to 18,000+ students."),
]


def render_our_impact(svg_inner):
    nodes = "".join(f"""<li class="reveal" data-stagger="{i % 4 + 1}">
      <span class="ft-year">{y}</span>
      <h3 class="ft-name">{t}</h3>
      <p class="ft-body">{b}</p>
    </li>""" for i, (y, t, b) in enumerate(TIMELINE))
    # the Our Impact tab's own labels and order ("globally" on every figure, per A4)
    six = [("33M+", "lives touched globally"), ("8.35M+", "patients treated globally"),
           ("3.28M+", "students reached globally"), ("12.24M+", "reached through Humanitarian Care globally"),
           ("450K+", "animals saved, treated, or rehabilitated globally"),
           ("8.90M+", "supported through Emergency Relief Care globally")]

    body = page_header(
        "About Us",
        "Our impact",
        "The work of Shrimad Rajchandra Love and Care began with volunteers bringing medicine to families in rural villages. Over two decades, it has grown into a global movement that has touched 33M+ lives globally.",
        image="/assets/img/photos/awards.jpg",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first">
  <div class="container">
    <h2 class="vu-h reveal">Global results</h2>
    <p class="vu-lead">SRLC USA is one chapter of a global movement carried largely by volunteers. The figures below reflect the movement&rsquo;s worldwide reach and behind them are individual people whose circumstances changed because someone was in a position to help.</p>
    <div class="mt-6">{impact_stats(six, cols=3)}</div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h2 class="vu-h reveal">Independent recognition and accreditation</h2>
        <p>The movement received Special Consultative Status from the United Nations Economic and Social Council in 2020, and GuideStar awarded its Platinum Seal for transparency and accountability in 2019. Independent recognition matters because it does not depend on our own account of the work. The 250-bed Shrimad Rajchandra Hospital and Research Center earned accreditation from the National Accreditation Board for Hospitals and Healthcare Providers (NABH) within its first year of operation.</p>
      </div>
      <div class="vu-split__photo">{img_tag(pinned(97))}</div>
    </div>
    <div class="recognition-cluster fin-badges mt-8">{recognition_chips(links=True)}</div>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">An operating model built for efficiency</h2>
    <p class="maxw-70">Because the programs are carried by experienced professionals and volunteers, administration costs remain low, and each initiative is managed against defined performance indicators. In practical terms, this means a greater share of every contribution reaches the programs it was intended to support.</p>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h2 class="vu-h reveal">Results in the United States</h2>
        <p>In the United States, volunteers organize recurring service programs in cities from Los Angeles to New York, preparing and sharing meals, assembling school supplies, and holding community care events with established local partners. In 2024, US centers distributed 90,000+ educational items, reaching 18,000+ students.</p>
      </div>
      <div class="vu-split__photo">{img_tag(photo("impact-us", ["us-food+alt:sandwiches", "us-food+us", "volunteers+us"], "community", min_w=1200))}</div>
    </div>
    <div class="mt-8">{editorial_map(svg_inner)}</div>
    <p class="mt-6"><a class="btn btn--secondary" href="/our-work/united-states/">Explore the US chapters</a></p>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Two decades of documented growth</h2>
    <p class="vu-lead">The milestones below are drawn from the movement&rsquo;s published record. They trace twenty years of steady growth, from volunteers delivering medicine to rural doorsteps to permanent institutes that now serve millions.</p>
    <div class="tlwrap">
      <ol class="founder-timeline vu-tl-rail">{nodes}</ol>
      <figure class="tlwrap__photo">{img_tag(pinned(160))}</figure>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <div class="vu-split vu-split--story">
    <div class="vu-split__copy">
    <h2 class="vu-h reveal">What these figures mean in practice</h2>
    <p class="vu-lead">Laxibhai, a 52-year-old farmer, had been living with triple-vessel heart disease, and the surgery he needed was beyond his family&rsquo;s means. He received the region&rsquo;s first cardiothoracic bypass at Shrimad Rajchandra Hospital at no cost, and he has since returned home to his fields. His recovery is one outcome among millions, and it is the kind of outcome every figure on this page represents.</p>
    <p class="mt-6"><a class="textlink" href="/about/financials/">Read the full record on the Financials page<span aria-hidden="true"> &rarr;</span></a></p>
    </div>
    <div class="vu-split__photo vu-split__photo--portrait">{img_tag(NAMAN.STORY)}</div>
    </div>
  </div>
</section>

{flat_cta("Support work you can verify", "Each result presented here belongs to a program that can be examined, visited, and audited, and each of those programs welcomes new support. We invite you to explore the work, or to read the record for yourself.", "Explore the 10 Care Program", "/our-work/10-care-program/")}
"""
    return page(
        "Our Impact | Verified Global Results | SRLC USA",
        "33M+ lives touched globally. Two decades of documented growth, independently accredited and published in full. Explore the results. SRLC USA.",
        "/about/our-impact/", body)


IF_PATH = "/about/inspiration-and-founder/"
FOUNDER_IMG = ("if-gurudevshri.jpg", 1600, 2000)  # Naman's DSC03898_NJ4.tiff, FOGRA39 -> sRGB via its profile, 4:5 on Gurudevshri alone

# Voices of Respect (Naman's Inspiration and Founder doc, Oct 19): five
# speakers, Morari Bapu removed; quotes unchanged; each slide captions the
# speaker's name and title; Clarke has no photo, so his quote runs full width.
VOICES = [
    ("No matter how much I praise Gurudev Rakeshji, it will not be enough. He walks on the path of right knowledge as well as the path of selfless action. To have the opportunity of meeting Rakeshji, I consider it my great fortune.", "Honorable Narendra Modi", "Prime Minister of India", "voice-modi.jpg"),
    ("This is not a meet of knowledge, but a meet of love. He has such a pleasant personality. He has immense love for saints, no matter which saint it is.", "His Holiness Mahant Swami Maharaj", "Spiritual Head, BAPS Swaminarayan Sanstha", "voice-mahant-swami.jpg"),
    ("My most beloved, most revered Rakeshji. You are invaluable to this world. May You keep spreading such light.", "Sri Sri Ravi Shankar", "Founder and Spiritual Head, The Art of Living", "voice-ravi-shankar.jpg"),
    ("Each time I see Him, it&rsquo;s a special experience. So calm and quiet and so peaceful. To experience true peace, you don&rsquo;t need to listen to much talk. You just need to come closer to Gurudev Rakeshji, and just sit.", "Venerable Bhikkhu Sanghasena", "Founder, Mahabodhi International Meditation Centre, Ladakh", "voice-bhikkhu.jpg"),
    ("One of the great things that has come out of Jainism is this Mission and the great work that it is doing now as I understand, all over the world, for humanity, and may this movement go onwards and upwards.", "Honorable David John Clarke", "Member, New South Wales Legislative Council, Australia", None),
]


def render_inspiration():
    slides = [(None, "Pujya Gurudevshri Rakeshji with His Holiness the Dalai Lama",
               "at the World Alliance of Religions: Peace Summit, Seoul, South Korea, 2014.", "if-gurudevshri-dalai-lama.jpg")] + VOICES
    quote_cards = "".join(f"""<figure class="quote-card ifvoice{' is-active' if i == 0 else ''}{'' if img else ' ifvoice--text'}{'' if q else ' ifvoice--photo'}">
      {f'<img class="ifvoice__img" src="/assets/img/inspiration/{img}" alt="{n if not q else "Pujya Gurudevshri Rakeshji with " + n}" width="1400" height="930" loading="lazy" decoding="async">' if img else ''}
      <div class="ifvoice__copy">
        {f'<blockquote class="ifvoice__quote">&ldquo;{q}&rdquo;</blockquote>' if q else ''}
        <figcaption class="ifvoice__cap"><span class="ifvoice__name">{n}</span>{" " if not q else ", "}{r}</figcaption>
      </div>
    </figure>""" for i, (q, n, r, img) in enumerate(slides))
    qdots = "".join(f'<button class="qd{" is-active" if i == 0 else ""}" data-go="{i}" aria-label="Slide {i + 1}"></button>' for i in range(len(slides)))

    # Founder portrait (Naman's DSC03898_NJ4.tiff, cropped 4:5 to Pujya
    # Gurudevshri alone). Until it arrives the section keeps its text layout.
    founder_img = FOUNDER_IMG
    founder_media = (f'''<div class="ifsplit__media ifsplit__media--portrait ifsplit__media--parallax"><img src="/assets/img/inspiration/{founder_img[0]}" alt="Pujya Gurudevshri Rakeshji" width="{founder_img[1]}" height="{founder_img[2]}" loading="lazy" decoding="async"></div>'''
                     if founder_img else "")

    # Layout per Naman's Inspiration and Founder doc (Oct 19) and his Oct 20
    # notes: one container edge for every section; Jainism, Shrimad
    # Rajchandraji and Pujya Gurudevshri are two-column, text left (46rem
    # measure) and the photo filling the rest at full section height; the
    # Inner Awakening section is gone; the Dalai Lama photo is slide 1 of
    # Voices of Respect.
    body = f"""<section class="ifhero" aria-labelledby="ifHeroTitle">
  <div class="ifhero__inner">
    <p class="ifhero__kicker">A timeless legacy flowing through a present-day visionary</p>
    <h1 class="ifhero__title" id="ifHeroTitle">Inspiration and Founder</h1>
  </div>
  <img class="ifhero__figures" src="/assets/img/inspiration/if-hero-figures.png" alt="Lord Mahavir, Shrimad Rajchandraji, and Pujya Gurudevshri Rakeshji" width="833" height="903" loading="eager" fetchpriority="high" decoding="async">
</section>

<section class="ifsplit ifsplit--lav ifsplit--flip ifsplit--first" aria-labelledby="ifRoots">
  <div class="ifsplit__copy prose">
    <h2 class="vu-h" id="ifRoots">Jainism and Lord Mahavir</h2>
    <p>Jainism, one of the world&rsquo;s oldest spiritual philosophies, teaches enduring, universal principles of love and kindness. Its teachings have shaped the lives of millions across the world and remain a living source of inspiration today.</p>
    <p>Lord Mahavir, a revered spiritual leader, lived in India around 500 BCE. He illuminated a path to inner peace through understanding and kindness toward all. At the heart of that path is compassion for every living being, the root from which empathy grows. More than 2,500 years later, his message continues to guide the modern world.</p>
  </div>
  <div class="ifsplit__media ifsplit__media--temple"><img src="/assets/img/inspiration/if-mahavir-web.jpg" alt="Shrimad Rajchandra Jin Mandir, Dharampur" width="2400" height="1353" loading="lazy" decoding="async"></div>
</section>

<section class="ifsplit ifsplit--white" aria-labelledby="ifShrimadji">
  <div class="ifsplit__copy prose">
    <h2 class="vu-h" id="ifShrimadji">Shrimad Rajchandraji</h2>
    <p>In the late 19th century, the saint and poet-philosopher Shrimad Rajchandraji illuminated the wisdom of Lord Mahavir with remarkable clarity, shaping a spiritual path for a new era. He is described as self-realized: someone who had directly experienced the nature of the soul rather than only studied it.</p>
    <p>Mahatma Gandhi called Shrimad Rajchandraji his spiritual guide. Gandhi&rsquo;s philosophy of truth and non-violence took shape under His influence, and the two exchanged letters on faith and conduct for years. That influence stands as a testament to the enduring impact of His message, which continues to resonate today.</p>
    <p>Grounded in direct inner experience, He articulated the subtle truths of spirituality through His own life, valuable teachings, and influential writings. Chief among them is Shri Atmasiddhi Shastra, a verse work on the nature of the soul and the path to self-realization, which blends deep philosophical insight with practical steps for inner transformation.</p>
  </div>
  <div class="ifsplit__media ifsplit__media--parallax"><img src="/assets/img/inspiration/if-shrimadji.jpg" alt="Shrimad Rajchandraji" width="1920" height="1080" loading="lazy" decoding="async"></div>
</section>

<section class="{'ifsplit ifsplit--lav ifsplit--flip ifsplit--founder' if founder_img else 'vu-shell vu-shell--lav'}" aria-labelledby="ifFounder">
  <div class="{'ifsplit__copy' if founder_img else 'container'} prose">
    <h2 class="vu-h" id="ifFounder">Pujya Gurudevshri Rakeshji</h2>
    <h3>Legacy of Wisdom</h3>
    <p>Pujya Gurudevshri Rakeshji is an enlightened visionary, global ambassador of peace, and the founder of Shrimad Rajchandra Mission Dharampur, the spiritual organization from which this movement grew. Following the revered footsteps of Shrimad Rajchandraji, Pujya Gurudevshri carries forward a legacy of timeless wisdom, translating profound spiritual truths into transformative teachings that make spirituality accessible to all.</p>
    <h3>Steady Force of Compassion</h3>
    <p>Through Shrimad Rajchandra Love and Care (SRLC), Pujya Gurudevshri translates compassion into action. Guided by His philosophy of empathy and universal harmony, SRLC is a global organization whose initiatives address critical needs in health care, education, environmental sustainability, and social welfare across many countries. In His teaching, inner clarity and outward kindness are one path: what is understood within flows naturally into care for others.</p>
    <h3>A Movement Reaching America</h3>
    <p>That vision has taken root across the United States and continues to grow. Through SRLC USA, volunteers in communities nationwide carry this spirit of selfless service into action. They serve their own neighborhoods through the 10 Care Program, and they support institutes in India and initiatives around the world.</p>
  </div>
  {founder_media}
</section>

<section class="ifvoices" aria-labelledby="ifVoicesTitle">
  <div class="container">
    <div class="ifvoices__head">
      <h2 class="vu-h" id="ifVoicesTitle">Voices of Respect</h2>
      <h3 class="ifvoices__h3">A Movement of Interfaith and International Harmony</h3>
      <p class="ifvoices__intro">A beacon of unity that transcends faiths and boundaries, Pujya Gurudevshri&rsquo;s message and Mission resonate across traditions and communities.</p>
    </div>
    <div class="ifvoices__track">{quote_cards}</div>
    <div class="quote-wall__controls ifvoices__controls">
      <button class="quote-wall__btn" data-dir="prev" aria-label="Previous quote">&larr;</button>
      <div class="quote-wall__dots">{qdots}</div>
      <button class="quote-wall__btn" data-dir="next" aria-label="Next quote">&rarr;</button>
    </div>
  </div>
</section>

<section class="pagenext pagenext--if">
  <div class="container pagenext__inner">
    <h2 class="pagenext__line">Continue learning about the wider movement and the work it supports.</h2>
    <div class="pagenext__links">
      <a class="btn btn--primary" href="/our-work/10-care-program/">The 10 Care Program</a>
      <a class="btn btn--secondary" href="/about/who-we-are/">Who We Are</a>
    </div>
  </div>
</section>
"""
    return page(
        "Inspiration and Founder | SRLC USA",
        "The story and philosophy behind SRLC&rsquo;s work: Shrimad Rajchandraji, Pujya Gurudevshri Rakeshji, and the movement of selfless service they inspire. SRLC USA.",
        IF_PATH, body)


def render_management():
    """Document C spec build. The roster is BLOCKING (Naman-approved names,
    roles, and 45 to 70 word bios do not exist yet); the grid ships as labeled
    placeholder slots, per the build rules."""
    slots = "".join(f"""<div class="bio reveal" data-stagger="{i % 4 + 1}">
      <div class="bio__photo" style="display:grid;place-items:center;background:#E7E3EC"><span style="font-family:var(--font-body);font-size:.72rem;color:#6B6472;text-align:center;padding:.6rem">Portrait pending</span></div>
      <p class="bio__name" style="color:var(--color-ink-muted)">Roster pending approval</p>
    </div>""" for i in range(4))
    body = page_header(
        "About Us",
        "The management team leading SRLC USA&rsquo;s work",
        "We are a 501(c)(3) nonprofit. Every person who sets strategy, approves the budget, and answers for results is named here, with what they oversee.",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first">
  <div class="container">
    <div class="govrow">
      <h2 class="vu-h reveal">How we govern</h2>
      <p class="vu-lead">SRLC USA is the United States chapter of Shrimad Rajchandra Love and Care, holder of UN ECOSOC Special Consultative Status.</p>
    </div>
    <div class="govrow">
      <h2 class="vu-h reveal">The roster</h2>
      <p class="vu-lead">Leadership names, roles, and bios publish here once approved. Each person appears with a consistent portrait and a short account of what they oversee.</p>
    </div>
  </div>
</section>

{flat_cta("The record behind the roster", "Annual filings and financial statements are published in full on the Financials page.", "Read Our Annual Report", "/about/financials/#documents")}
"""
    return page(
        "Management Team | Leadership at SRLC USA",
        "Meet the people who direct the programs, finances, and compliance of SRLC USA, a 501(c)(3) nonprofit. See who is accountable and what they oversee. SRLC USA.",
        "/about/management-team/", body)


F990_YEARS = ["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017"]


def render_financials():
    cards = "".join(f"""<div class="vu-card vu-card--stack reveal" data-stagger="{i % 4 + 1}">
      <h3 class="vu-card__h">{y} Form 990</h3>
      <div class="vu-card__body"><p>Annual IRS filing.</p><p><a class="textlink" href="mailto:{EMAIL}?subject=Request%3A%20{y}%20Form%20990">Request a copy<span aria-hidden="true"> &rarr;</span></a></p></div>
    </div>""" for i, y in enumerate(F990_YEARS))
    body = page_header(
        "About Us",
        "Financials",
        "We know how much it matters to you that your gift reaches the people it&rsquo;s meant for. It matters just as much to us. That&rsquo;s why every filing, report, and financial record we produce is published here in full, for anyone to read.",
        image="/assets/img/photos/event-recent.jpg", mod="sky",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first vu-shell--narrow">
  <div class="container"><div class="recognition-cluster fin-badges">{recognition_chips(links=True)}</div></div>
</section>

<section class="vu-shell vu-shell--cream" id="documents">
  <div class="container">
    <h2 class="vu-h reveal">Documents by year</h2>
    <div class="vu-card vu-card--stack fin-report reveal">
      <h3 class="vu-card__h">Annual Report 2024&ndash;2025</h3>
      <div class="vu-card__body"><p>The year in programs, numbers, and people.</p><p><a class="btn btn--secondary" href="mailto:{EMAIL}?subject=Request%3A%20Annual%20Report%202024-2025">Request a copy</a></p></div>
    </div>
    <div class="vu-doc-grid">{cards}</div>
  </div>
</section>

<section class="vu-shell vu-shell--lav vu-shell--narrow">
  <div class="container fin-legal">
    <p>{EIN_LINE.replace("EIN 81-5162502", '<span class="nowrap">EIN 81-5162502</span>')}</p>
    <p>Additional financial information is available on request at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</section>
"""
    return page(
        "Financials | Form 990 and Reports | SRLC USA",
        "Annual filings, financial statements, and governing documents, published in full. SRLC USA is a 501(c)(3) nonprofit. EIN on page.",
        "/about/financials/", body)


def render_404():
    body = page_header(
        "Page not found",
        "This page has moved on.",
        "The care continues elsewhere. Start from the beginning, or head straight to the work.",
        cta='<a class="btn btn--primary" href="/">Go Home</a> <a class="btn btn--ghost" href="/our-work/10-care-program/">Explore Our Work</a>',
    )
    return page("Page Not Found | SRLC USA", "The page you were looking for has moved.", "/404.html", body)
