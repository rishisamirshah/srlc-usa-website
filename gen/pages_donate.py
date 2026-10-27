"""Donate page. Built from Naman's donate.html (Aug 30) and rewritten from the
Donate tab of the content doc (Oct 25): general fund only, hero form with a
Donate button (a mailto until Stripe is wired), Gillaben's story spotlight,
Give monthly, Give with confidence, More ways to give (charity:water's grid)
and the FAQ. Tax language stays in the "to the extent permitted by law" form.
"""
import os
from shell import img_tag, px_img, photo, page, story_spotlight, recognition_chips, EMAIL
import data_naman as NAMAN

MAIL_GIVE = f"mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA"


HERO_PATH = "/assets/img/fillers/children-smiling.jpg"  # Naman's hero photo (Unsplash 1488521787991), local copy


def _hero_img():
    """Media Bank donate hero when curated, else Naman's original hero photo."""
    from data_media import slot
    from shell import photo
    pick = slot("donate-hero") or photo("donate-hero", ["health-care+india", "child-care+india", "india"], "children", min_w=1600)
    if pick:
        return pick[0], pick[1], pick[2]
    try:
        from shell import FILLERS
        for f in FILLERS:
            if f[0] == HERO_PATH:
                return f[0], f[2], f[3]
    except Exception:
        pass
    return HERO_PATH, 2400, 1600


def _logo_box(path, area=2200, max_w=124, max_h=36):
    """Display size giving every logo about the same amount of ink, so a solid
    block and a thin wordmark read at one optical size."""
    from PIL import Image
    with Image.open(path) as im:
        im = im.convert("RGBA")
        ar = im.width / im.height
        im.thumbnail((400, 400))
        px = list(im.getdata())
    ink = sum(1 for r, g, b, a in px if a > 16 and min(r, g, b) < 235) / len(px)
    area *= min(1.4, max(0.5, 0.45 / max(ink, 0.05)))
    h = min(max_h, (area / ar) ** 0.5)
    w = min(max_w, h * ar)
    return round(w), round(w / ar)


LOGO_NAMES = {
    "1024px-Cisco_logo.svg.png": "Cisco", "1200px-The_Blackstone_Group_Logo.svg.png": "Blackstone",
    "1280px-Lilly-Logo.svg.png": "Lilly", "2560px-3M_wordmark.svg.png": "3M", "600px-Gap_logo.svg.png": "Gap",
    "ATT_logo_2016.png": "AT&amp;T", "Bank-of-America-logo.png": "Bank of America", "Burlington.png": "Burlington",
    "Capital-one-logo.png": "Capital One", "Ford_logo_flat.svg.png": "Ford", "Hilton.png": "Hilton",
    "Intel_logo_2006-2020.svg.png": "Intel", "Walmart-Logo.jpg": "Walmart", "adobe.png": "Adobe", "amazon.png": "Amazon",
    "cbre.png": "CBRE", "chevron-hallmark-twitter.png": "Chevron", "ebay.png": "eBay", "facebook.png": "Facebook",
    "honeywell.png": "Honeywell", "target.png": "Target",
}


def _partner_marquee():
    pdir = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "partners")
    logos = sorted(f for f in os.listdir(pdir) if not f.startswith("."))

    def group(hidden):
        alt = (lambda f: "") if hidden else (lambda f: LOGO_NAMES.get(f, f.rsplit(".", 1)[0]))
        return "".join(
            f'<div class="marquee-logo"><img src="/assets/img/partners/{f}" alt="{alt(f)}" width="{w}" height="{h}" style="--w:{w}px;--h:{h}px" loading="lazy"></div>'
            for f, (w, h) in ((f, _logo_box(os.path.join(pdir, f))) for f in logos))
    return f"""<div class="partner-marquee" aria-label="Employers with matching gift programs">
  <div class="partner-marquee__track">
    <div class="partner-marquee__group">{group(False)}</div>
    <div class="partner-marquee__group partner-marquee__group--dup" aria-hidden="true">{group(True)}</div>
  </div>
</div>"""


# Dollar-to-outcome lines are placeholders in the doc's format ("Your $25 gift
# can fund ..."); every one needs finance sign-off before launch (Donate tab flag 1).
AMOUNTS = [
    ("25", "essential medicines for one child for a month", False),
    ("50", "school supplies for one student for a term", True),
    ("100", "hot meals for 50 underserved patients", False),
    ("250", "skills training for one rural woman for a month", False),
    ("500", "care where the need is greatest", False),
    ("custom", "care where the need is greatest", False),
]

# Corporate matching (Donate tab, Oct 27). Hardik's employer search plugin
# takes the EIN line's place once it is live; the logo strip stays under it.
MATCH_H = "Find your employer&rsquo;s match"
MATCH_LINE = ("Many companies match the gifts their employees make to nonprofits. Search for your employer "
              "to see whether your gift qualifies and how to request the match.")
MATCH_EIN = "Use our <span class='nowrap'>EIN 81-5162502</span> when you submit a match request through your employer."

# More ways to give (Donate tab, Oct 25): charity:water's grid, one purple line
# illustration per item. Crypto is tabled; stock is email-only for now.
WAYS = [
    ("matching", "Corporate matching",
     "Many employers match their employees&rsquo; gifts. Use our <span class='nowrap'>EIN 81-5162502</span> with your company&rsquo;s matching program.",
     "#matching", "Find your employer&rsquo;s match"),
    ("daf", "Donor-advised funds",
     "Recommend a grant to SRLC USA from your donor-advised fund using our <span class='nowrap'>EIN 81-5162502</span>.",
     f"mailto:{EMAIL}?subject=DAF%20grant%20to%20SRLC%20USA", "Give from your DAF"),
    ("stock", "Gifts of stock",
     "Give stock or other securities. Email us and our team will share the details.",
     f"mailto:{EMAIL}?subject=Gift%20of%20stock%20to%20SRLC%20USA", "Email us to give stock"),
    ("check", "Check or wire",
     "Mail checks payable to SRLC USA to 500 Paterson Plank Rd #33685, Union City, NJ 07087.",
     f"mailto:{EMAIL}?subject=Wire%20transfer%20to%20SRLC%20USA", "Ask about a wire transfer"),
]

_INK = 'fill="none" stroke="#693D84" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
_TINT = "#EFE6F8"
WAY_ICONS = {
    # two hearts: a gift and its match
    "matching": f'''<g transform="translate(13 -5)"><path d="M24 50S8 40.5 8 29.5C8 23.7 12.2 20 17 20c3.2 0 5.6 1.7 7 4 1.4-2.3 3.8-4 7-4 4.8 0 9 3.7 9 9.5C40 40.5 24 50 24 50z" fill="#FFFFFF"/></g>
      <path d="M24 52S8 42.5 8 31.5C8 25.7 12.2 22 17 22c3.2 0 5.6 1.7 7 4 1.4-2.3 3.8-4 7-4 4.8 0 9 3.7 9 9.5C40 42.5 24 52 24 52z" fill="{_TINT}"/>
      <path d="M52 8v6M49 11h6"/>''',
    # a grant letter: envelope with a heart card
    "daf": f'''<path d="M9 30L32 15l23 15v22H9z" fill="{_TINT}"/>
      <rect x="17" y="19" width="30" height="24" rx="1.5" fill="#FFFFFF"/>
      <path d="M32 36s-6-3.6-6-7.6c0-2 1.5-3.4 3.2-3.4 1.2 0 2.2.7 2.8 1.6.6-.9 1.6-1.6 2.8-1.6 1.7 0 3.2 1.4 3.2 3.4 0 4-6 7.6-6 7.6z" fill="{_TINT}"/>
      <path d="M9 31l23 14 23-14v21H9z" fill="{_TINT}"/>
      <path d="M9 52l18-12M55 52L37 40"/>''',
    # a rising chart
    "stock": f'''<rect x="9" y="11" width="46" height="42" rx="2" fill="{_TINT}"/>
      <path d="M9 21h46M15 16h3M21 16h3"/>
      <path d="M16 45l9-9 7 6 13-14"/>
      <path d="M39 28h6v6"/>''',
    # a signed check and a pen
    "check": f'''<rect x="5" y="22" width="42" height="25" rx="2" fill="{_TINT}"/>
      <path d="M11 30h14M11 41c3-3 5 2 8-1s4 1 6-1M31 41h10"/>
      <path d="M41 36l15-19 3.5 3-15 19-5.5 2z" fill="#FFFFFF"/>
      <path d="M52.5 22l3.5 3"/>''',
}

# Give with confidence (Donate tab, Oct 25): three short items, then the seals
CONFIDENCE = [
    ("Tax-deductible", "SRLC USA is a registered 501(c)(3) nonprofit, <span class='nowrap'>EIN 81-5162502</span>. You receive a tax receipt by email for every gift."),
    ("Open financials", 'Our Form 990 and financial reports are published in full on our <a href="/about/financials/">Financials page</a>.'),
    ("Independently recognized", "SRLC USA holds the Candid Gold Seal of Transparency and is a GreatNonprofits Top-Rated nonprofit."),
]
SEAL_CAPS = {"Candid Seal of Transparency": "Candid Gold Seal of Transparency, 2025",
             "GreatNonprofits Top‑Rated, 2024": "GreatNonprofits Top‑Rated, 2024"}

FAQ = [
    ("Is my donation tax-deductible?",
     "Yes. SRLC USA is a registered <span class='nowrap'>501(c)(3)</span> nonprofit, <span class='nowrap'>EIN 81-5162502</span>. Your gift is tax-deductible to the extent permitted by law, and no goods or services are provided in return."),
    ("When will I receive my tax receipt?",
     f'You receive a tax receipt by email after your gift. If it doesn&rsquo;t arrive, email <a href="mailto:{EMAIL}">{EMAIL}</a> and we&rsquo;ll resend it.'),
    ("Can I change or cancel my monthly gift?",
     f'Yes, at any time. Email <a href="mailto:{EMAIL}">{EMAIL}</a> with the change you&rsquo;d like to make.'),
    ("How is my gift used?",
     'Gifts made on this page go to Shrimad Rajchandra Love and Care&rsquo;s general fund, so support can go where the need is greatest across the 10 Care Program. Our Form 990 and financial reports are on our <a href="/about/financials/">Financials page</a>.'),
    ("Can donors outside the US give?",
     "Yes. You can give with any internationally accepted credit card. Tax deductibility applies under US law, so donors outside the US should check how their gift is treated in their own country."),
    ("Will my information be shared?",
     "No. SRLC USA does not sell, rent, or trade donor information. Our privacy policy explains what we store and how to request deletion."),
]


def _amount_tiles():
    out = []
    for amt, outcome, sel in AMOUNTS:
        label = "Other" if amt == "custom" else f"${amt}"
        out.append(f'<button type="button" class="donate-amount" data-amt="{amt}" data-outcome="{outcome}" aria-pressed="{"true" if sel else "false"}">{label}</button>')
    return "\n          ".join(out)


def _ways():
    return "\n      ".join(f"""<div class="way">
        <svg class="way__icon" viewBox="0 0 64 64" width="72" height="72" aria-hidden="true" {_INK}>{WAY_ICONS[key]}</svg>
        <h3 class="way__h">{h}</h3>
        <p class="way__p">{body}</p>
        <a class="way__link" href="{href}">{cta}</a>
      </div>""" for key, h, body, href, cta in WAYS)


def _faq():
    items = []
    for i, (q, a) in enumerate(FAQ):
        pid = f"faq-panel-{i + 1}"
        items.append(f"""<div class="faq-item">
        <h3 class="faq-item__h"><button type="button" class="faq-item__btn" aria-expanded="false" aria-controls="{pid}">{q}<span class="faq-item__icon" aria-hidden="true"></span></button></h3>
        <div class="faq-item__body" id="{pid}" hidden>
          <p>{a}</p>
        </div>
      </div>""")
    return "\n      ".join(items)


def render_donate():
    # Donate tab rewrite (Naman, Oct 25): general fund only, no cause or center
    # picker; six sections; site-wide rules (plain headings, centered text).
    hero_img, hero_w, hero_h = _hero_img()
    story_img = NAMAN.TIMELINE_PHOTOS["2022"]  # the hospital, until her photo arrives
    confidence = "".join(f"""
      <div class="confidence-item">
        <h3 class="confidence-item__h">{h}</h3>
        <p class="confidence-item__p">{p}</p>
      </div>""" for h, p in CONFIDENCE)
    body = f"""<div class="donate-page">

<section class="donate-hero" aria-labelledby="page-title">
  <div class="donate-hero__media" aria-hidden="true">
    {px_img((hero_img, hero_w, hero_h, ""), avoid=".donate-widget, .donate-hero__h, .donate-hero__sub", loading="eager")}
  </div>
  <div class="container">
    <div class="donate-hero__grid">
      <div class="donate-hero__copy">
        <div class="donate-hero__title">
          <h1 class="donate-hero__h" id="page-title">Give care where it&rsquo;s needed most</h1>
        </div>
        <div class="donate-hero__detail">
          <p class="donate-hero__sub">Your gift supports <span class="nowrap">Shrimad Rajchandra Love and Care&rsquo;s</span> work across the 10 Care Program, directed to the programs where the need is greatest.</p>
          <div class="donate-hero__meta">
            <span class="nowrap">501(c)(3) nonprofit</span>
            <span class="nowrap">EIN 81-5162502</span>
            <span>Tax-deductible to the extent permitted by law</span>
          </div>
        </div>
      </div>
      <aside class="donate-widget" id="donate-form" aria-label="Donation form">
        <div class="donate-toggle" role="group" aria-label="Gift frequency">
          <button type="button" class="donate-toggle__btn" data-freq="one-time" aria-pressed="true">One time</button>
          <button type="button" class="donate-toggle__btn" data-freq="monthly" aria-pressed="false">Monthly</button>
        </div>
        <div class="donate-amounts" role="group" aria-label="Gift amount">
          {_amount_tiles()}
        </div>
        <div class="donate-custom">
          <span class="donate-custom__symbol" aria-hidden="true">$</span>
          <input class="donate-custom__input" type="number" min="1" inputmode="decimal" aria-label="Custom amount in US dollars" placeholder="Enter amount">
        </div>
        <p class="donate-widget__outcome" id="donate-outcome" aria-live="polite">Your $50 gift can fund school supplies for one student for a term.</p>
        <!-- placeholder until Stripe is wired (Hardik and the CRM team): still opens an email -->
        <a class="btn btn--primary btn--lg donate-widget__cta" id="donate-cta" href="{MAIL_GIVE}%20(%2450)" data-mail="{MAIL_GIVE}">Donate</a>
        <p class="donate-widget__larger">Planning a larger gift? Email <a href="mailto:{EMAIL}?subject=Planning%20a%20larger%20gift">{EMAIL}</a> and our team will reach out.</p>
      </aside>
    </div>
  </div>
</section>

<section class="section-pad section--white donate-matching" id="matching" aria-labelledby="matching-h">
  <div class="container">
    <h2 class="section-h" id="matching-h">{MATCH_H}</h2>
    <p class="donate-matching__line">{MATCH_LINE}</p>
    <!-- Hardik's employer search plugin replaces the EIN line once it is live -->
    <p class="donate-matching__ein">{MATCH_EIN}</p>
    <div class="ways-logos" id="matching-logos">
      <p class="ways-logos__cap">Companies with employee matching-gift programs include:</p>
      {_partner_marquee()}
    </div>
  </div>
</section>

<section class="donate-strip donate-strip--split" id="monthly" aria-label="Give monthly">
  <div class="donate-strip__media">{px_img(photo("donate-monthly", ["child-care+india", "health-care+india", "educational-care+india"], "children", min_w=1200))}</div>
  <div class="donate-strip__copy">
    <h2 class="donate-strip__h">Give monthly</h2>
    <p class="donate-strip__body">A monthly gift gives our programs steady support they can plan around. You can change or cancel it at any time by emailing {EMAIL}.</p>
    <div class="donate-strip__ctas">
      <a class="btn btn--primary" href="#donate-form" data-select-freq="monthly">Give monthly</a>
    </div>
  </div>
</section>

<section class="section-pad section--white donate-ways" id="more-ways" aria-labelledby="ways-h">
  <div class="container">
    <h2 class="section-h" id="ways-h">More ways to give</h2>
    <div class="ways-grid">
      {_ways()}
    </div>
  </div>
</section>

{story_spotlight("Back to being a child", [
    "She loved to run and play, until breathing became hard. Doctors found a hole between the upper chambers of her heart and closed it surgically, using her own heart tissue. For her family, the cost could have been impossible. Her treatment was free. Today she is back to running, playing, and being a child."],
    story_img, cta=("Donate today", "#donate-form"), eyebrow="Impact Story", pos="70 50", bg="#F7F4FF", sid="donate-story")}

<section class="section-pad section--white donate-confidence" id="confidence" aria-labelledby="confidence-h">
  <div class="container">
    <h2 class="section-h" id="confidence-h">Give with confidence</h2>
    <div class="confidence-items">{confidence}
    </div>
    <div class="recognition-cluster fin-badges">{recognition_chips(links=True, caps=SEAL_CAPS, ecosoc=False)}</div>
    <p class="confidence-cta"><a class="btn btn--primary" href="/about/financials/">See Our Financials</a></p>
  </div>
</section>

<section class="section-pad section--lavender donate-faq" id="faq" aria-labelledby="faq-h">
  <div class="container">
    <h2 class="section-h" id="faq-h">Questions about giving</h2>
    <div class="faq-list">
      {_faq()}
    </div>
  </div>
</section>

</div>
"""
    return page(
        "Donate | SRLC USA",
        "Give to SRLC USA, a 501(c)(3) nonprofit. Your gift supports the 10 Care Program where the need is greatest. One-time and monthly giving.",
        "/donate/", body)
