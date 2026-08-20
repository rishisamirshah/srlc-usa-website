"""Renderers: homepage (approved-base port), donate, volunteer, about cluster, 404."""
import os
from shell import (page, ph, hero_purple, actionbar, impact_stats, recognition_chips, EMAIL, PHONE, EIN_LINE, IG, FB)
from data_states import STATES, CAMPAIGNS
from data_cares import CARES
from pages_work import cf_map, state_chips

GLOBAL_STATS = [
    ("33M+", "Lives", "touched globally"),
    ("8.35M+", "Patients", "treated through health initiatives"),
    ("3.28M+", "Students", "supported through educational activities"),
    ("12.24M+", "People", "reached through Humanitarian Care"),
    ("450K+", "Animals", "cared for through Animal Care"),
    ("8.90M+", "Lives", "reached through Emergency Relief Care"),
]


def partner_marquee():
    pdir = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "partners")
    logos = sorted(f for f in os.listdir(pdir) if not f.startswith("."))
    group = "".join(
        f'<div class="marquee-logo"><img src="/assets/img/partners/{f}" alt="{f.rsplit(".", 1)[0].replace("-", " ").title()}" loading="lazy"></div>'
        for f in logos)
    group_dup = group.replace('alt="', 'alt="" data-a="', 1) if False else "".join(
        f'<div class="marquee-logo"><img src="/assets/img/partners/{f}" alt="" loading="lazy"></div>'
        for f in logos)
    return f"""<div class="partner-marquee" aria-label="Corporate matching gift partners">
  <div class="partner-marquee__track">
    <div class="partner-marquee__group">{group}</div>
    <div class="partner-marquee__group partner-marquee__group--dup" aria-hidden="true">{group_dup}</div>
  </div>
</div>"""


def care_card_media(icon):
    return (f'<div class="care-card__img" style="display:grid;place-items:center;'
            f'background:linear-gradient(135deg,#F1EAF7 0%,#E2D2F0 100%)">'
            f'<img src="/assets/img/care-icons/{icon}" alt="" style="width:46%;max-width:120px;opacity:.85"></div>')


def render_home(svg_inner):
    slides = [
        {
            "img": "/assets/img/photos/school-children-hero.jpg",
            "eyebrow": "Educational Care &middot; Classroom of Change",
            "title": "The classroom comes to every child.",
            "sub": "A year-round educational care campaign that brings learning to underserved children, from Title I schools across the United States to 238 villages in South Gujarat. Every learner gets a real shot, no matter where they&rsquo;re born.",
            "cta1": ("Fund a classroom", "/donate/"), "cta2": ("See the program", "/our-work/10-care-program/educational-care/"),
        },
        {
            "img": "/assets/img/photos/event-recent.jpg",
            "eyebrow": "Our Impact",
            "title": "33M+ lives. Care for those who need it most.",
            "sub": "Our impact spans the hospital, the schools, the animal sanctuary, Mission Africa, and the community work happening right where you live. Every program carries a story, built around the people it serves.",
            "cta1": ("See the impact", "/about/our-impact/"), "cta2": ("Who we are", "/about/who-we-are/"),
        },
        {
            "img": "/assets/img/photos/love-care-walk.jpg",
            "eyebrow": "Get Involved",
            "title": "Your nearest chapter is closer than you think.",
            "sub": "25+ U.S. cities from Boston to Seattle, Atlanta to Phoenix. Monthly meetings, local volunteer drives, and university partnerships. Meet like-minded people who want to bring joy and impact through global initiatives.",
            "cta1": ("Find your chapter", "/our-work/united-states/"), "cta2": ("How to volunteer", "/volunteer/"),
        },
    ]
    slides_html = "".join(f"""<article class="hero-carousel__slide{' is-active' if i == 0 else ''}" data-slide="{i}" style="--bg:url('{s["img"]}')">
      <div class="hero-carousel__overlay"></div>
      <div class="container hero-carousel__content">
        <p class="hero-carousel__eyebrow">{s["eyebrow"]}</p>
        <h1 class="hero-carousel__title">{s["title"]}</h1>
        <p class="hero-carousel__sub">{s["sub"]}</p>
        <div class="hero-carousel__ctas">
          <a class="btn btn--primary" href="{s["cta1"][1]}">{s["cta1"][0]}</a>
          <a class="btn btn--ghost" href="{s["cta2"][1]}">{s["cta2"][0]}</a>
        </div>
      </div>
    </article>""" for i, s in enumerate(slides))
    dots = "".join(f'<button class="dot{" is-active" if i == 0 else ""}" data-go="{i}" role="tab" aria-label="Slide {i + 1}"></button>' for i in range(3))

    mstats = "".join(f"""<div class="mstat">
        <p class="mstat__n">{n}</p>
        <p class="mstat__label">{l}</p>
        <p class="mstat__desc">{d}</p>
      </div>""" for n, l, d in GLOBAL_STATS)

    care_cards = "".join(f"""<a class="care-card reveal" data-stagger="{i % 5 + 1}" href="/our-work/10-care-program/{c["slug"]}/">
        {care_card_media(c["icon"])}
        <div class="care-card__label">
          <span class="care-card__num">{c["num"]}</span>
          <h3>{c["name"]}</h3>
        </div>
      </a>""" for i, c in enumerate(CARES))

    institutes_cards = ""
    from data_india import INSTITUTES
    for inst in INSTITUTES:
        institutes_cards += f"""<a class="institute-card reveal" href="/our-work/india/{inst["slug"]}/">
        <div class="institute-card__media">{ph(inst["tag"], cls="ph-media--tint", style="min-height:0;height:100%")}</div>
        <div class="institute-card__body"><h3 class="institute-card__h">{inst["name"]}</h3><p class="institute-card__d">{inst["desc"]}</p><span class="institute-card__more" aria-label="Learn more"></span></div>
      </a>"""

    campaigns_cards = "".join(f"""<a class="news-card reveal" data-stagger="{i + 1}" href="/our-work/united-states/#campaigns">
        <div class="news-card__media">{ph(c["img_label"], cls="ph-media--tint", style="min-height:0;height:100%")}</div>
        <div class="news-card__meta"><span class="news-card__tag">National Campaign</span></div>
        <h3 class="news-card__h">{c["name"]}</h3>
        <p class="news-card__d">{c["body"][:170]}&hellip;</p>
        <span class="news-card__cta">{c["cta"]}</span>
      </a>""" for i, c in enumerate(CAMPAIGNS))

    activity = """<aside class="chapter-activity reveal" aria-label="Recent chapter activity">
        <header class="chapter-activity__head">
          <p class="chapter-activity__title">From the chapters</p>
          <span class="chapter-activity__count">22 centers</span>
        </header>
        <ul class="chapter-activity__list">
          <li class="chapter-activity__item">
            <span class="chapter-activity__city">Boston</span>
            <span class="chapter-activity__body">Meal kits assembled and delivered through Open Table<span class="chapter-activity__time">Ongoing</span></span>
          </li>
          <li class="chapter-activity__item">
            <span class="chapter-activity__city">Chicago</span>
            <span class="chapter-activity__body">500+ PB&amp;J sandwiches packed and 1,000+ pounds of food donated<span class="chapter-activity__time">Recent drive</span></span>
          </li>
          <li class="chapter-activity__item">
            <span class="chapter-activity__city">Phoenix</span>
            <span class="chapter-activity__body">Hot meals and breakfast packs with TCAA and Andre House<span class="chapter-activity__time">Year-round</span></span>
          </li>
        </ul>
      </aside>"""

    body = f"""
<div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>
<div class="sticky-donate" id="stickyDonate" aria-hidden="true">
  <div class="container sticky-donate__inner">
    <p class="sticky-donate__msg"><strong>33M+</strong> lives touched globally. Your gift adds to that.</p>
    <div class="sticky-donate__actions">
      <a class="btn btn--primary" href="/donate/">Donate now</a>
      <button type="button" class="sticky-donate__close" id="stickyDonateClose" aria-label="Dismiss">&times;</button>
    </div>
  </div>
</div>

<div class="newsletter-modal" id="newsletterModal" role="dialog" aria-modal="true" aria-labelledby="newsletterTitle" hidden>
  <div class="newsletter-modal__backdrop" data-newsletter-close></div>
  <div class="newsletter-modal__panel">
    <button class="newsletter-modal__close" data-newsletter-close aria-label="Close">&times;</button>
    <h3 id="newsletterTitle">Stay informed. Be inspired.</h3>
    <p>Get updates on the impact of our programs and the initiatives we&rsquo;re running across the U.S. and abroad.</p>
    <form class="newsletter-modal__form" name="updates" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="updates">
      <input type="hidden" name="source" value="modal">
      <p class="hp-field"><input name="bot-field" tabindex="-1"></p>
      <input type="email" name="email" required placeholder="you@example.com" aria-label="Email address" class="form-hidewrap">
      <button type="submit" class="btn btn--primary form-hidewrap">Subscribe</button>
      <span class="form-success" style="color:var(--color-srlc-purple);font-weight:600">Thank you. Check your inbox to confirm.</span>
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
      <h2 class="mission-split__h">Love and Care. <em>Compassion in action.</em></h2>
      <p class="mission-split__body">Shrimad Rajchandra Love and Care USA is the United States chapter of Shrimad Rajchandra Love and Care, a global humanitarian organization holding Special Consultative Status with the United Nations Economic and Social Council. SRLC USA is a 501(c)(3) public charity raising funds across 25+ U.S. cities for global health, education, and humanitarian work.</p>
      <div class="mission-split__actions">
        <a class="btn btn--primary btn--lg" href="/donate/">Donate</a>
        <a class="btn btn--secondary" href="/about/who-we-are/">See what your gift funds</a>
      </div>
      <p class="mission-split__micro">Registered 501(c)(3) &middot; EIN 81-5162502</p>
    </div>
    <div class="mission-split__stats">{mstats}</div>
  </div>
</section>

<section class="care-section" id="ten-care">
  <div class="container">
    <div class="care-section__head reveal">
      <p class="care-section__eyebrow">The 10 Care Program</p>
      <h2 class="care-section__h">Our Unique Global Approach</h2>
      <p class="care-section__sub">From rural hospitals to U.S. chapter food drives, every initiative comes back to the same idea: love and care, delivered in person, with measured outcomes.</p>
    </div>
    <div class="care-grid">{care_cards}</div>
    <div class="care-section__cta reveal"><a class="btn btn--secondary" href="/our-work/10-care-program/">Explore all 10 programs</a></div>
  </div>
</section>

<section class="named-story" aria-label="Impact story">
  <div class="named-story__grid">
    <div class="named-story__media"><div class="named-story__placeholder">Laxmibhai&rsquo;s portrait &middot; Media Bank photo pending consent</div></div>
    <div class="named-story__copy-wrap">
      <div class="named-story__copy reveal" data-stagger="1">
        <p class="named-story__eyebrow">Impact story &middot; Laxmibhai</p>
        <p class="named-story__quote">A 52-year-old farmer received the region&rsquo;s first-ever cardiothoracic bypass surgery, performed entirely free of charge. Today he is back on his feet.</p>
        <p class="named-story__attribution">Laxmibhai&rsquo;s second chance</p>
        <p class="named-story__attribution-meta">Health Care &middot; Shrimad Rajchandra Hospital and Research Center</p>
        <a class="named-story__link" href="/our-work/10-care-program/health-care/">Read about Health Care</a>
      </div>
    </div>
  </div>
</section>

<section class="institutes-section">
  <div class="container">
    <div class="institutes-section__head">
      <p class="institutes-section__eyebrow">Where the work happens</p>
      <h2 class="institutes-section__h">The institutes you fund</h2>
      <p class="institutes-section__sub">American donations flow into a global network of institutions, each one built around a specific need. Your gift funds their day-to-day work.</p>
    </div>
    <div class="institutes-grid">{institutes_cards}</div>
  </div>
</section>

<section class="chapter-finder chapter-finder--v3">
  <div class="container chapter-finder__inner">
    <div class="chapter-finder__widget">
      <h2 class="chapter-finder__h">Find your nearest chapter.</h2>
      <p class="chapter-finder__sub">Drop in a ZIP code or click any highlighted state on the map.</p>
      <form class="chapter-finder__form" onsubmit="event.preventDefault(); window.__cfZipLookup &amp;&amp; window.__cfZipLookup();">
        <input type="text" id="zipInput" inputmode="numeric" maxlength="5" placeholder="ZIP code (e.g. 08820)" aria-label="ZIP code" pattern="\\d{{5}}">
        <button type="submit" class="btn btn--primary" id="zipBtn">Find chapter</button>
      </form>
      <div class="chapter-finder__result" id="zipResult" hidden>
        <p class="chapter-finder__city" id="zipCity"></p>
        <p class="chapter-finder__meta" id="zipMeta"></p>
        <div class="chapter-finder__actions">
          <a id="zipJoinBtn" class="btn btn--primary" href="/volunteer/">Join this chapter</a>
          <a class="btn btn--ghost" href="mailto:{EMAIL}">Email us</a>
        </div>
      </div>
      <p class="chapter-finder__link-row"><a href="/our-work/united-states/">Browse all U.S. chapters &rarr;</a></p>
      {activity}
    </div>
    <div>
      {cf_map(svg_inner)}
    </div>
  </div>
</section>

<section class="news-section">
  <div class="container">
    <div class="news-section__head">
      <div class="news-section__headcopy">
        <p class="news-section__eyebrow">Our Campaigns</p>
        <h2 class="news-section__h">Three moments the whole country shows up for</h2>
      </div>
      <a class="news-section__all" href="/our-work/united-states/#campaigns">See the campaigns</a>
    </div>
    <div class="news-grid">{campaigns_cards}</div>
  </div>
</section>

<section class="recognition-band" id="recognition" aria-label="Trust and recognition">
  <div class="container">
    <div class="recognition-band__head reveal">
      <h2 class="recognition-band__h">Globally recognized. Locally rooted.</h2>
      <p class="recognition-band__sub">Shrimad Rajchandra Love and Care holds Special Consultative Status with the United Nations Economic and Social Council, granting our humanitarian work a seat at the global table on sustainable development, health, education, and human rights.</p>
    </div>
    <div class="recognition-cluster reveal" data-stagger="1">
      <p class="recognition-cluster__label">Recognized by</p>
      {recognition_chips()}
    </div>
    <div class="recognition-cluster reveal" data-stagger="2">
      <p class="recognition-cluster__label">Corporate matching gift partners</p>
      {partner_marquee()}
    </div>
    <div class="recognition-band__cta reveal">
      <a class="btn btn--secondary" href="https://www.loveandcare.srmd.org/awards-and-accolades/" target="_blank" rel="noopener">See all awards and accolades</a>
    </div>
  </div>
</section>

<section class="final-cta" aria-label="Take the next step with SRLC USA">
  <div class="container">
    <div class="final-cta__hero">
      <span class="final-cta__eyebrow">Be part of the work</span>
      <h2 class="final-cta__h">One small step from <em>where you are</em> right now.</h2>
      <p class="final-cta__sub">Whether you have five minutes, five dollars, or five hours a month, there is a way for you to join. Pick what fits, and we will meet you there.</p>
    </div>
    <div class="fc-newsletter" id="final-newsletter">
      <div class="fc-newsletter__copy">
        <h3>Stay informed. Be inspired.</h3>
        <p>Real updates on the people we serve, the programs we run, and what your support is making possible.</p>
      </div>
      <form class="fc-newsletter__form" name="updates" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="updates">
        <input type="hidden" name="source" value="homepage">
        <p class="hp-field"><input name="bot-field" tabindex="-1"></p>
        <input type="email" name="email" required placeholder="you@example.com" aria-label="Your email address" class="form-hidewrap">
        <button type="submit" class="btn btn--primary form-hidewrap">Subscribe</button>
        <span class="form-success" style="color:var(--color-srlc-purple);font-weight:600">Thank you. Check your inbox to confirm.</span>
      </form>
    </div>
  </div>
</section>
"""
    return page(
        "SRLC USA | Shrimad Rajchandra Love and Care",
        "Volunteers across 25+ US cities serving neighbors through the 10 Care Program, institutes in India, and Mission Africa. A 501(c)(3) nonprofit. SRLC USA.",
        "/", body)


def render_donate():
    tiles = "".join(f"""<button type="button" class="donate-tile{' is-active' if amt == '100' else ''}" data-amount="{amt}">
        <span class="donate-tile__amount">${amt}</span>
      </button>""" for amt in ["25", "50", "100", "250", "500"])
    ways = [
        ("Give by ACH or check", "Bank transfer and mailed checks are our most efficient ways to receive your gift: more of every dollar reaches the programs. Write to us and we will send the details the same week.", f"mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA", "Email us to give"),
        ("Donor-advised funds and trusts", "Recommend a grant to Shrimad Rajchandra Love and Care USA through your donor-advised fund or charitable trust. EIN 81-5162502.", f"mailto:{EMAIL}?subject=DAF%20grant%20to%20SRLC%20USA", "Start a DAF grant"),
        ("Corporate matching", "Your employer may match your gift. Check if your company participates, and your impact can double before it leaves your paycheck.", f"mailto:{EMAIL}?subject=Matching%20gift%20question", "Ask about matching"),
        ("Give your time", "Volunteers carry every program we run. If this season your gift is hours instead of dollars, we will put them to work.", "/volunteer/", "Volunteer instead"),
    ]
    ways_html = "".join(f"""<div class="vu-card reveal" data-stagger="{i % 4 + 1}" style="grid-template-columns:1fr">
      <h3 class="vu-card__h">{t}</h3>
      <div class="vu-card__body"><p>{b}</p><p><a href="{h}">{cta}</a></p></div>
    </div>""" for i, (t, b, h, cta) in enumerate(ways))

    body = hero_purple(
        '<a href="/">Home</a> &middot; Get Involved',
        "Every gift becomes <em>someone&rsquo;s morning</em>.",
        "A meal delivered, a backpack filled, a surgery that costs a family nothing. Choose an amount and the way of giving that fits you.",
    ) + f"""
<section class="vu-shell vu-shell--lav" id="donate-tiles">
  <div class="container" style="max-width:56rem">
    <div class="donate-tiles__head">
      <h2 class="donate-tiles__h">Choose your gift</h2>
      <p class="donate-tiles__sub">Online card giving is being set up. Until it launches, our team personally handles every gift by email or phone, usually the same day.</p>
    </div>
    <div class="donate-tiles__toggle-wrap">
      <div class="donate-tiles__toggle" role="tablist" aria-label="Giving frequency">
        <button type="button" class="is-active" data-freq="once" aria-selected="true">One time</button>
        <button type="button" data-freq="monthly" aria-selected="false">Monthly</button>
      </div>
    </div>
    <div class="donate-tiles__grid">
      {tiles}
    </div>
    <div class="donate-tiles__cta">
      <a class="btn btn--primary btn--lg" id="donate-tiles-cta" href="mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA%20(%24100)">Donate $100 now</a>
      <p class="donate-tiles__monthly-note" id="donate-tiles-monthly-note" hidden>Give monthly and provide steady, year-round support.</p>
    </div>
    <div class="donate-embed__taxline" style="margin-top:1.6rem">{EIN_LINE}</div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">Ways to give</h2>
    <p class="vu-lead">Choose what fits your season.</p>
    <div class="vu-pair-grid mt-6">{ways_html}</div>
  </div>
</section>

<section class="vu-shell vu-shell--lav" id="matching">
  <div class="container">
    <h2 class="vu-h reveal text-center" style="text-align:center">Double the love before it leaves your paycheck</h2>
    <p class="vu-lead" style="margin-inline:auto;text-align:center">Thousands of employers match charitable gifts dollar for dollar. If you see your company below, your gift can go twice as far.</p>
    <div class="mt-8">{partner_marquee()}</div>
    <p class="text-center mt-6"><a class="btn btn--secondary" href="mailto:{EMAIL}?subject=Matching%20gift%20question">Check your employer</a></p>
  </div>
</section>

<section class="vu-shell vu-shell--cream vu-shell--narrow">
  <div class="container text-center">
    <p style="font-size:.9rem;color:var(--color-ink-muted)">Looking to donate via ACH, check, corporate matching or charitable trust? Please reach out to us at <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
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
        "Give to SRLC USA by ACH, check, donor-advised fund, or corporate matching. A 501(c)(3) nonprofit, EIN 81-5162502. Every gift reaches real programs.",
        "/donate/", body)


def render_volunteer():
    cards = [
        ("Community", "SRLC USA&rsquo;s 25+ chapters are built by people who show up for each other. At every event, volunteers meet neighbors, professionals, and students who share a commitment to service. Many join for the cause and stay for the community."),
        ("Purpose", "Every event organized, every food distribution completed, every campaign supported reaches real people across the United States, India, and Africa. The effort on the ground connects directly to lives changed."),
        ("Growth", "Leadership, event management, fundraising, communications, and logistics are all part of active chapter work. The skills built through SRLC USA are practical and lasting. Many of our chapter leaders developed those skills here."),
        ("Belonging", "Service is not something SRLC USA volunteers do occasionally. For many, it becomes part of how they identify. That is why so many volunteers who start with a single event stay involved for years."),
    ]
    cards_html = "".join(
        f'<div class="cause-card reveal" data-stagger="{i + 1}"><h3>{t}</h3><p>{b}</p></div>'
        for i, (t, b) in enumerate(cards))
    steps = [
        ("01", "Sign up", "Fill out the form at the bottom of this page. Share where you are, what skills or interests you can offer, and how much time you have each month. It takes under two minutes."),
        ("02", "Meet your chapter", "A coordinator from the SRLC chapter in your area will reach out within a few days. They will introduce themselves and walk you through what the chapter is currently working on."),
        ("03", "Show up", "Attend your first event. Meet the people who make the chapter run. Most volunteers return for the next one within a month."),
    ]
    steps_html = "".join(f"""<div class="prong reveal" data-stagger="{i + 1}">
      <div class="prong__icon">{n}</div>
      <h3>{t}</h3><p>{b}</p>
    </div>""" for i, (n, t, b) in enumerate(steps))
    roles = ["Events and Logistics", "Food and Distribution", "Community Outreach", "Fundraising and Campaigns",
             "Communications and Social Media", "Healthcare Outreach", "University and Youth Programs",
             "Operations and Administration", "Chapter Leadership", "Internship", "Other"]
    role_opts = "".join(f"<option>{r}</option>" for r in roles)
    time_opts = "".join(f"<option>{t}</option>" for t in ["2 to 4 hours", "4 to 8 hours", "8+ hours", "Flexible"])

    body = hero_purple(
        '<a href="/">Home</a> &middot; Get Involved',
        "Volunteer with <em>SRLC USA</em>",
        "Thousands of people across 25+ US cities give their time, their skills, and their energy to SRLC USA. Not because they have to. Because service is who they are.",
        chips=["501(c)(3) Nonprofit", "25+ US Cities", "Parent body: UN ECOSOC Special Consultative Status"],
        ctas='<a class="btn btn--primary" href="#signup">Volunteer With Us</a> <a class="btn btn--ghost" href="/our-work/united-states/">Find My State&rsquo;s Chapter</a>',
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">More than volunteering. A community.</h2>
    <div class="card-grid mt-6">{cards_html}</div>
  </div>
</section>

<section class="three-prongs" style="padding:3.4rem 0">
  <div class="container">
    <h2 class="three-prongs__h reveal">Getting started is simple</h2>
    <div class="prongs-grid">{steps_html}</div>
  </div>
</section>

<section class="vu-shell vu-shell--purple vu-shell--narrow">
  <div class="container">
    <p style="color:#E8DDF2;max-width:70ch;margin-bottom:1.6rem">SRLC USA is the U.S. chapter of Shrimad Rajchandra Love and Care, a global humanitarian organization. Collectively, the initiatives that SRLC USA volunteers help fund and organize are part of a network that has reached 33M+ lives globally. Across medical programs alone, the parent organization has served 8.35M+ patients globally.</p>
    <div style="display:flex;gap:clamp(1.8rem,6vw,4.5rem);flex-wrap:wrap">
      {"".join(f'<div><p class="count-up" style="font-family:var(--font-display);font-weight:300;font-size:clamp(2rem,4vw,2.8rem);color:var(--color-warm-orange);margin:0 0 .3rem;line-height:1">{n}</p><p style="color:#E8DDF2;margin:0;font-size:.9rem">{l}</p></div>' for n, l in [("33M+", "lives reached globally"), ("8.35M+", "patients served globally"), ("3.28M+", "students reached globally")])}
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--cream" id="signup">
  <div class="container" style="max-width:820px">
    <h2 class="vu-h reveal">Join the mission. Sign up to volunteer.</h2>
    <p class="vu-lead">Under two minutes. A chapter coordinator from your area will follow up personally.</p>
    <form class="form mt-6" name="volunteer" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="volunteer">
      <p class="hp-field"><input name="bot-field" tabindex="-1"></p>
      <div class="form-hidewrap">
        <div class="form__row form__row--two">
          <div><label for="v-fn">First Name</label><input type="text" id="v-fn" name="first_name" required autocomplete="given-name"></div>
          <div><label for="v-ln">Last Name</label><input type="text" id="v-ln" name="last_name" required autocomplete="family-name"></div>
        </div>
        <div class="form__row form__row--two" style="margin-top:1rem">
          <div><label for="v-em">Email Address</label><input type="email" id="v-em" name="email" required autocomplete="email"></div>
          <div><label for="v-zip">City / ZIP Code</label><input type="text" id="v-zip" name="city_zip" required autocomplete="postal-code"></div>
        </div>
        <div class="form__row form__row--two" style="margin-top:1rem">
          <div><label for="v-sk">What skills or interests do you bring?</label><select id="v-sk" name="skills" required>{role_opts}</select></div>
          <div><label for="v-tm">How much time can you offer per month?</label><select id="v-tm" name="time" required>{time_opts}</select></div>
        </div>
        <div class="form__row" style="margin-top:1rem">
          <label for="v-ph">Phone Number (Optional. So your chapter coordinator can reach you directly.)</label>
          <input type="tel" id="v-ph" name="phone" autocomplete="tel">
        </div>
        <div style="margin-top:1.4rem"><button class="btn btn--primary btn--lg" type="submit">I Want to Volunteer</button></div>
      </div>
      <div class="form-success">
        <p class="vu-lead--xl">Thank you. A chapter coordinator from your area will be in touch within a few days.</p>
      </div>
    </form>
    <p style="font-size:.9rem;color:var(--color-ink-muted);margin-top:1.4rem">Not ready to sign up yet? Follow us on <a href="{IG}" rel="noopener" target="_blank">Instagram</a> and <a href="{FB}" rel="noopener" target="_blank">Facebook</a> to see what SRLC USA chapters are doing in your city.</p>
  </div>
</section>
"""
    return page(
        "Volunteer with SRLC USA | Give Your Time, Build Community",
        "Serve communities across the US with SRLC USA. A 501(c)(3) nonprofit whose work has reached 33M+ lives globally. Sign up to volunteer in two minutes.",
        "/volunteer/", body)


def render_who_we_are():
    how = [
        ("Volunteer led", "Programs are carried by volunteers who know their communities. Because they give their time, administration costs stay low and more of every dollar reaches the programs it was given to support."),
        ("Designed to scale", "We invest in models that can be replicated, so a program that works in one community can be extended to the next."),
        ("Measured against evidence", "Every initiative operates within professional frameworks and defined performance indicators. Results, not intentions, decide what continues."),
        ("Building the next generation of leaders", "Volunteers of every generation carry this work, from students to retirees, and young people lead most of the initiatives under the 10 Care Program."),
    ]
    how_html = "".join(
        f'<div class="cause-card reveal" data-stagger="{i % 4 + 1}"><h3>{t}</h3><p>{b}</p></div>'
        for i, (t, b) in enumerate(how))
    promises = [
        ("Dignity, always", "Every living being deserves compassion, dignity and respect."),
        ("Every figure verified", "Our commitment to transparency is unwavering."),
        ("Built to last", "Long standing impact, for generations to come."),
    ]
    promises_html = "".join(f"""<div class="prong reveal" data-stagger="{i + 1}">
      <div class="prong__icon"><svg width="20" height="20"><use href="#vu-i-check"/></svg></div>
      <h3>{t}</h3><p>{b}</p>
    </div>""" for i, (t, b) in enumerate(promises))

    body = hero_purple(
        '<a href="/">Home</a> &middot; About Us',
        "Love and care, <em>in action</em>.",
        "SRLC USA is what happens when physicians, engineers, teachers, and students decide their weekends belong to their neighbors. We are the US chapter of Shrimad Rajchandra Love and Care, a global nonprofit holding Special Consultative Status with the United Nations Economic and Social Council (ECOSOC), and a 501(c)(3) organization. But before we are any of that, we are people who believe care is not a profession. It is a practice.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h3>Care you can point to</h3>
        <p>We focus on immediate needs and the systems behind them. In the United States, volunteers prepare and share meals, equip students for the school year, and organize community care events with local partners. Globally, the movement builds and sustains hospitals, schools, and development programs designed to serve for generations. The programs differ; the standard does not: high-quality, sustainable work that outlasts the day we arrive.</p>
      </div>
      <div class="vu-split__photo"><img src="/assets/img/photos/event-recent.jpg" alt="SRLC USA volunteers at a community event" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="mission-band">
  <div class="container mission-band__inner">
    <p class="eyebrow eyebrow--orange">Our philosophy</p>
    <h2 class="mission-band__h">&ldquo;When there is love within, it flows naturally in the form of care.&rdquo;</h2>
    <p class="mission-band__sub">We serve and bring joy, not because we have to, or because it is our duty, but because we love to. That conviction shapes every program we run, from hospital corridors to classrooms to meal lines.</p>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">Ten ways we care</h2>
    <p class="maxw-70">Every initiative we run belongs to one of ten focus areas, together the 10 Care Program: Health Care, Educational Care, Child Care, Woman Care, Tribal Care, Community Care, Humanitarian Care, Animal Care, Environmental Care, and Emergency Relief Care. In the United States, that vision looks like service in your own city, on your own street. Globally, it stands as permanent institutions in India and Mission Africa.</p>
    <div class="mt-8">{impact_stats([("33M+", "lives touched globally"), ("3.28M+", "students reached globally"), ("12.24M+", "reached through Humanitarian Care globally")], cols=3)}</div>
    <div class="recognition-cluster mt-8">{recognition_chips()}</div>
    <div class="vu-toc--inline">
      <a href="/our-work/10-care-program/">10 Care Program</a>
      <a href="/our-work/united-states/">United States</a>
      <a href="/our-work/india/">India</a>
      <a href="/our-work/mission-africa/">Mission Africa</a>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Built to be trusted</h2>
    <div class="card-grid mt-6">{how_html}</div>
  </div>
</section>

<section class="three-prongs" style="padding:3.4rem 0">
  <div class="container">
    <h2 class="three-prongs__h reveal">Three promises we keep</h2>
    <div class="prongs-grid">{promises_html}</div>
  </div>
</section>

{actionbar("Come see for yourself.", "An about page can only introduce us; it cannot let you feel the work. The programs, the numbers, and the financials are all published for anyone to read, and the volunteers are probably closer than you think.", "Explore the 10 Care Program", "/our-work/10-care-program/")}
"""
    return page(
        "Who We Are | SRLC USA | 501(c)(3) Nonprofit",
        "Meet the volunteers bringing care and joy to communities across the US and worldwide. A 501(c)(3) nonprofit. See who we are. SRLC USA.",
        "/about/who-we-are/", body)


TIMELINE = [
    ("2006&ndash;08", "Mobile care begins", "A mobile dispensary begins carrying medical care to rural doorsteps, and a mid-day meal program gives families one more reason to send their children to school."),
    ("2009&ndash;11", "Gurukul opens", "Shrimad Rajchandra Gurukul opens in Karanjveri, Gujarat, and a new neonatal intensive care unit begins providing critical care for premature newborns."),
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
      <h4 class="ft-name">{t}</h4>
      <p class="ft-body">{b}</p>
    </li>""" for i, (y, t, b) in enumerate(TIMELINE))
    six = [(n, f"{l} {d}") for n, l, d in GLOBAL_STATS]

    body = hero_purple(
        '<a href="/">Home</a> &middot; About Us',
        "Our <em>impact</em>",
        "The work of Shrimad Rajchandra Love and Care began with volunteers bringing medicine to families in rural villages. Over two decades, it has grown into a global movement that has touched 33M+ lives globally.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Global results</h2>
    <p class="vu-lead">SRLC USA is one chapter of a global movement carried largely by volunteers. The figures below reflect the movement&rsquo;s worldwide reach and behind them are individual people whose circumstances changed because someone was in a position to help.</p>
    <div class="mt-6">{impact_stats([(n, l) for n, l in six])}</div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h3>Independent recognition and accreditation</h3>
        <p>The movement received Special Consultative Status from the United Nations Economic and Social Council in 2020, and GuideStar awarded its Platinum Seal for transparency and accountability in 2019. Independent recognition matters because it does not depend on our own account of the work. The 250-bed Shrimad Rajchandra Hospital and Research Center earned accreditation from the National Accreditation Board for Hospitals and Healthcare Providers (NABH) within its first year of operation.</p>
      </div>
      <div class="vu-split__photo"><img src="/assets/img/photos/awards.jpg" alt="SRLC recognition and accolades" loading="lazy"></div>
    </div>
    <div class="recognition-cluster mt-8">{recognition_chips()}</div>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">An operating model built for efficiency</h2>
    <p class="maxw-70">Because the programs are carried by experienced professionals and volunteers, administration costs remain low, and each initiative is managed against defined performance indicators. In practical terms, this means a greater share of every contribution reaches the programs it was intended to support.</p>
    <div class="chip-row mt-6"><span>Volunteer delivery model</span><span>Low administration costs</span><span>Defined performance indicators</span></div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <div class="vu-split vu-split--reverse">
      <div class="vu-split__copy">
        <h3>Results in the United States</h3>
        <p>In the United States, volunteers organize recurring service programs in cities from Los Angeles to New York, preparing and sharing meals, assembling school supplies, and holding community care events with established local partners. In 2024, US centers distributed 90,000+ educational items, reaching 18,000+ students.</p>
        <p><a href="/our-work/united-states/">Explore the US chapters</a></p>
      </div>
      <div>{cf_map(svg_inner)}</div>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Two decades of documented growth</h2>
    <p class="vu-lead">The milestones below are drawn from the movement&rsquo;s published record. They trace twenty years of steady growth, from volunteers delivering medicine to rural doorsteps to permanent institutions that now serve millions.</p>
    <ol class="founder-timeline vu-tl-rail">{nodes}</ol>
  </div>
</section>

<section class="vu-shell vu-shell--cream vu-shell--narrow">
  <div class="container">
    <div class="vu-card vu-card--accent reveal" style="grid-template-columns:1fr">
      <h3 class="vu-card__h">What these figures mean in practice</h3>
      <div class="vu-card__body"><p>Laxmibhai, a 52-year-old farmer, had been living with triple-vessel heart disease, and the surgery he needed was beyond his family&rsquo;s means. He received the region&rsquo;s first cardiothoracic bypass at Shrimad Rajchandra Hospital at no cost, and he has since returned home to his fields. His recovery is one outcome among millions, and it is the kind of outcome every figure on this page represents.</p>
      <p><a href="/about/financials/">Read the full record on the Financials page</a></p></div>
    </div>
  </div>
</section>

{actionbar("Support work you can verify.", "Each result presented here belongs to a program that can be examined, visited, and audited, and each of those programs welcomes new support.", "Explore the 10 Care Program", "/our-work/10-care-program/")}
"""
    return page(
        "Our Impact | Verified Global Results | SRLC USA",
        "33M+ lives touched globally. Two decades of documented growth, independently accredited and published in full. Explore the results. SRLC USA.",
        "/about/our-impact/", body)


VOICES = [
    ("No matter how much I praise Gurudev Rakeshji, it will not be enough. He walks on the path of right knowledge as well as the path of selfless action. To have the opportunity of meeting Rakeshji, I consider it my great fortune.", "Honorable Narendra Modi", "Prime Minister of India"),
    ("One of the great things that has come out of Jainism is this Mission and the great work that it is doing now as I understand, all over the world, for humanity, and may this movement go onwards and upwards.", "Honorable David John Clarke", "Member, New South Wales Legislative Council, Australia"),
    ("This is not a meet of knowledge, but a meet of love. He has such a pleasant personality. He has immense love for saints, no matter which saint it is.", "His Holiness Mahant Swami Maharaj", "Spiritual Head, BAPS Swaminarayan Sanstha"),
    ("My most beloved, most revered Rakeshji. You are invaluable to this world. May You keep spreading such light.", "Sri Sri Ravi Shankar", "Founder and Spiritual Head, The Art of Living"),
    ("We have all become confined in our pigeon holes, while this saint has broken down all walls and come out. One needs to have such magnanimity.", "Pujyashri Morari Bapu", "Renowned Ram Katha Narrator"),
    ("Each time I see Him, it&rsquo;s a special experience. So calm and quiet and so peaceful. To experience true peace, you don&rsquo;t need to listen to much talk. You just need to come closer to Gurudev Rakeshji, and just sit.", "Venerable Bhikkhu Sanghasena", "Founder, Mahabodhi International Meditation Centre, Ladakh"),
]


def render_inspiration():
    quote_cards = "".join(f"""<figure class="quote-card{' is-active' if i == 0 else ''}">
      <blockquote>&ldquo;{q}&rdquo;</blockquote>
      <span class="quote-card__name">{n}</span>
      <span class="quote-card__role" style="color:#C9B3DC">{r}</span>
    </figure>""" for i, (q, n, r) in enumerate(VOICES))
    qdots = "".join(f'<button class="qd{" is-active" if i == 0 else ""}" data-go="{i}" aria-label="Quote {i + 1}"></button>' for i in range(len(VOICES)))

    body = hero_purple(
        '<a href="/">Home</a> &middot; About Us &middot; A timeless legacy flowing through a present-day visionary',
        "Our <em>Inspiration</em>",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container prose">
    <h2 class="vu-h">Jainism and Lord Mahavir</h2>
    <p>Jainism, one of the world&rsquo;s oldest spiritual philosophies, teaches enduring, universal principles of love and kindness.</p>
    <p>Lord Mahavir, a revered spiritual leader who graced the Indian subcontinent over 2,500 years ago, illuminated a path to inner peace through understanding and kindness toward all, a message that continues to guide the modern world.</p>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container prose">
    <h2 class="vu-h">Shrimad Rajchandraji</h2>
    <p>In the late 19th century, the self-realized saint and poet-philosopher Shrimad Rajchandraji illuminated the wisdom of Lord Mahavir with remarkable clarity, shaping a spiritual path for a new era.</p>
    <p>Grounded in direct inner experience, He articulated the subtle truths of spirituality through His own life, valuable teachings, and influential writings, including Shri Atmasiddhi Shastra, blending deep philosophical insights with practical steps for inner transformation.</p>
    <p>Shrimad Rajchandraji&rsquo;s formative influence on Mahatma Gandhi&rsquo;s philosophy of truth and non-violence stands as a testament to the enduring impact of His message, which continues to resonate today.</p>
    <blockquote>Standing at the foot of a hill, all that is visible are your immediate surroundings. Upon ascending the peak, you can see all of existence.<br><br>Shrimad Rajchandraji was at that vantage point. Every word emerged from inner experience, every expression from universal vision, and every message from limitless compassion.</blockquote>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container prose">
    <h2 class="vu-h">Pujya Gurudevshri Rakeshji</h2>
    <h3>Legacy of Wisdom</h3>
    <p>Pujya Gurudevshri Rakeshji is an enlightened visionary, global ambassador of peace, and the founder of Shrimad Rajchandra Mission Dharampur (SRMD). Following the revered footsteps of Shrimad Rajchandraji, Pujya Gurudevshri carries forward a legacy of timeless wisdom, translating profound spiritual truths into transformative teachings that make spirituality accessible to all.</p>
    <h3>Steady Force of Compassion</h3>
    <p>Through Shrimad Rajchandra Love and Care (SRLC), Pujya Gurudevshri translates compassion into action. Guided by His philosophy of empathy and universal harmony, SRLC is a comprehensive program that addresses critical needs in healthcare, education, environmental sustainability, and social welfare, earning Special Consultative Status with the United Nations Economic and Social Council (ECOSOC) for its far-reaching impact.</p>
    <h3>A Movement Reaching America</h3>
    <p>That vision now lives across the United States. Through SRLC USA, volunteers in communities nationwide carry this spirit of seva, selfless service, into action: serving their neighborhoods through the 10 Care Program and supporting institutions in India and initiatives around the world.</p>
    <blockquote>Spearheading a global movement, while remaining steady in universal peace and untethered compassion.<br><br>Pujya Gurudevshri is the unmoved mover.</blockquote>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container prose text-center">
    <h2 class="vu-h">Inner Awakening and Compassionate Action</h2>
    <p class="vu-lead" style="margin-inline:auto">Pujya Gurudevshri teaches a simple and complete path. Inner awakening brings clarity and harmony within, and love naturally flows outward as kindness in action. This path leads toward lasting peace and compassionate living in the world.</p>
  </div>
</section>

<section class="quote-wall">
  <div class="container text-center">
    <h2 class="quote-wall__h">Voices of Respect</h2>
    <div class="quote-wall__track">{quote_cards}</div>
    <div class="quote-wall__controls">
      <button class="quote-wall__btn" data-dir="prev" aria-label="Previous quote">&larr;</button>
      <div class="quote-wall__dots">{qdots}</div>
      <button class="quote-wall__btn" data-dir="next" aria-label="Next quote">&rarr;</button>
    </div>
    <p style="color:#C9B3DC;font-size:.9rem;max-width:56ch;margin:0 auto">A beacon of unity that transcends faiths and boundaries, Pujya Gurudevshri&rsquo;s message and Mission resonate across traditions and communities.</p>
  </div>
</section>

{actionbar("That is the inspiration.", "The rest of this site is what it looks like in practice: ten Care programs, institutions in India, medical camps in Africa, and volunteers across the United States.", "Explore the 10 Care Program", "/our-work/10-care-program/")}
"""
    return page(
        "Our Inspiration | Shrimad Rajchandraji | SRLC USA",
        "The story and philosophy behind SRLC&rsquo;s work: Shrimad Rajchandraji, Pujya Gurudevshri Rakeshji, and the movement of selfless service they inspire. SRLC USA.",
        "/about/our-inspiration/", body)


MANAGEMENT = [
    ("Snehal Shah", "Trustee, President", "President of a small electronic distribution firm, with BSEE, MSEE, and MBA degrees. Leading the organization since 2017."),
    ("Dr. Chintan Mehta", "Trustee, Secretary", "Internal medicine specialist in Phoenix, AZ, leading the operations team of SRLC USA. Engaged for over 10 years."),
    ("Kirti Desai", "Trustee, Treasurer", "Certified Public Accountant, serving as Chief Financial Officer at Tevogen Bio Holdings Inc and SRLC USA Treasurer since 2024."),
    ("Kamini Shah", "Trustee", "Dedicated Special Education teacher with over 20 years of experience and former president of the Jain Sangh of Austin."),
    ("Payal Kamdar", "Trustee", "CEO of VSolvit LLC, an award-winning technology solutions provider, involved across SRLC activities and strategic direction."),
    ("Mitesh Lakhani", "Trustee", "Managing Partner at Raisol Capital, focusing on private aviation, digital marketing, and healthcare. Active for nearly 10 years."),
    ("Biren Mehta", "Trustee", "Vice President of Venture Investments at Johnson &amp; Johnson, with degrees from UCLA and USC. Engaged for over a decade."),
    ("Chirag Shah", "Trustee", "Global Marketing Manager at Microchip Technology, active in the Phoenix community for over 10 years."),
    ("Ravi Shah", "Grants and Partnerships Lead", "Product leader at Google, with previous roles at Global Traffic Technologies and IBM."),
    ("Devang Jhaveri", "Programs and Partnerships Lead", "Associate Director at Cognizant Technology with 26 years of experience. Volunteer for over 10 years."),
    ("Parima Shah", "Youth Lead", "Engineering Manager at the ed tech startup Outschool, with 10+ years in technology including Google and Disney."),
    ("Krish Kamdar", "Social Media Lead", "Kelley School of Business graduate in Finance and Supply Chain Management. 12+ years with SRLC."),
    ("Sujay Shah", "National Planning Functions", "Senior IT Manager at Kaiser Permanente with 20+ years of leadership experience. Seven years of SRLC service."),
]


def render_management():
    people = "".join(f"""<div class="bio reveal" data-stagger="{i % 4 + 1}">
      <div class="bio__photo" style="display:grid;place-items:center;background:linear-gradient(135deg,var(--color-srlc-purple),var(--color-purple-deep))"><span style="font-family:var(--font-display);font-size:2.4rem;color:var(--color-warm-orange)">{n[0]}</span></div>
      <p class="bio__name">{n}</p>
      <p class="bio__role">{r}</p>
      <p style="font-size:.88rem;color:var(--color-ink-muted);line-height:1.55;margin-top:.5rem">{b}</p>
    </div>""" for i, (n, r, b) in enumerate(MANAGEMENT))
    body = hero_purple(
        '<a href="/">Home</a> &middot; About Us',
        "Management <em>Team</em>",
        "Physicians, engineers, educators, and finance professionals who give their leadership the way every volunteer gives their weekend: freely.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container"><div class="bio-grid">{people}</div></div>
</section>
{actionbar("Serve alongside them.", "Chapter leadership grows from volunteering. Start where you are.", "Volunteer With Us", "/volunteer/")}
"""
    return page(
        "Management Team | SRLC USA",
        "The trustees and program leads guiding SRLC USA, a 501(c)(3) nonprofit serving communities across the United States and worldwide.",
        "/about/management/", body)


F990_YEARS = ["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017"]


def render_financials():
    cards = "".join(f"""<div class="vu-card reveal" data-stagger="{i % 4 + 1}" style="grid-template-columns:44px 1fr">
      <div class="vu-card__ic"><svg width="22" height="22"><use href="#vu-i-doc"/></svg></div>
      <h3 class="vu-card__h">{y} Form 990</h3>
      <div class="vu-card__body"><p>Annual IRS filing. <a href="mailto:{EMAIL}?subject=Request%3A%20{y}%20Form%20990">Request a copy</a></p></div>
    </div>""" for i, y in enumerate(F990_YEARS))
    body = hero_purple(
        '<a href="/">Home</a> &middot; About Us',
        "<em>Financials</em>",
        "We know how much it matters to you that your gift reaches the people it&rsquo;s meant for. It matters just as much to us. That&rsquo;s why every filing, report, and financial record we produce is published here in full, for anyone to read.",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--narrow">
  <div class="container"><div class="recognition-cluster">{recognition_chips()}</div></div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">Documents by year</h2>
    <div class="vu-actionbar reveal" style="margin-bottom:1.4rem">
      <div class="vu-actionbar__copy">
        <h3>Annual Report 2024&ndash;2025</h3>
        <p>The year in programs, numbers, and people. Featured report, available the same day by email.</p>
      </div>
      <div class="vu-actionbar__ctas"><a class="btn btn--primary" href="mailto:{EMAIL}?subject=Request%3A%20Annual%20Report%202024-2025">Request a copy</a></div>
    </div>
    <div class="vu-doc-grid">{cards}</div>
    <p style="font-size:.88rem;color:var(--color-ink-muted);margin-top:1.2rem">Self-hosted PDF downloads are being prepared. Until they are live, every document is available the same day by email.</p>
  </div>
</section>

<section class="vu-shell vu-shell--lav vu-shell--narrow">
  <div class="container text-center">
    <p style="font-size:.9rem;color:var(--color-ink-muted)">{EIN_LINE}</p>
    <p style="font-size:.9rem;color:var(--color-ink-muted)">Additional financial information is available on request at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</section>
"""
    return page(
        "Financials | Form 990 and Reports | SRLC USA",
        "Annual filings, financial statements, and governing documents, published in full. SRLC USA is a 501(c)(3) nonprofit. EIN on page.",
        "/about/financials/", body)


def render_404():
    body = hero_purple(
        "Page not found",
        "This page has <em>moved on</em>.",
        "The care continues elsewhere. Start from the beginning, or head straight to the work.",
        ctas='<a class="btn btn--primary" href="/">Go home</a> <a class="btn btn--ghost" href="/our-work/10-care-program/">Explore Our Work</a>',
    )
    return page("Page Not Found | SRLC USA", "The page you were looking for has moved.", "/404.html", body)
