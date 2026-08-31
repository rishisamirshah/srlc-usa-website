"""Donate page, ported from Naman's donate.html (Aug 30 send).

Section order, copy, widget behaviour, FAQ, trust signals and the monthly
strip follow his file. Adaptations, each noted in the build report:
  - site shell (nav/footer/head) comes from shell.page(); his inlined shell
    CSS/nav/footer are dropped
  - giving CTAs are mailto links labelled "Email us to give" until a card
    processor exists (Naman, Aug 22); tax language is the approved
    "to the extent permitted by law" form, never "100% tax-deductible"
  - flat design rules (4px radius, no glow shadows, no gradients) win where
    his style block conflicts
  - Unsplash hotlink replaced by the local filler photo
  - the corporate matching logo wall from the current page is kept under the
    label naman-claude.md prescribes ("Corporate matching gift eligibility")
"""
import os
from shell import page, EMAIL

MATCH_QUALIFIER = ("These are examples of companies with employee matching-gift programs. "
                   "Logos are the property of their respective owners and do not imply "
                   "partnership with or endorsement of SRLC USA.")

MAIL_GIVE = f"mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA"
MAIL_MONTHLY = f"mailto:{EMAIL}?subject=Monthly%20donation%20to%20SRLC%20USA"


HERO_PATH = "/assets/img/fillers/children-smiling.jpg"  # Naman's hero photo (Unsplash 1488521787991), local copy


def _hero_img():
    """Same photo as Naman's hero. shell.FILLERS carries its dimensions."""
    try:
        from shell import FILLERS
        for f in FILLERS:
            if f[0] == HERO_PATH:
                return f[0], f[2], f[3]
    except Exception:
        pass
    return HERO_PATH, 2400, 1600


def _partner_marquee():
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


AMOUNTS = [
    ("25", "essential medicines for one child for a month", False),
    ("50", "school supplies for one student for a term", True),
    ("100", "hot meals for 50 underserved patients", False),
    ("250", "skills training for one rural woman for a month", False),
    ("custom", "the program you choose", False),
]

WAYS = [
    ("Appreciated stock", "Give stock or securities.",
     "Donating appreciated stock often avoids capital gains and gives you a deduction at fair market value. Our broker details are ready when you are.",
     f"mailto:{EMAIL}?subject=Stock%20gift%20inquiry", "Talk to our team"),
    ("Donor-advised funds", "Recommend a DAF grant.",
     "SRLC USA is grant-eligible through Fidelity Charitable, Schwab Charitable, Vanguard Charitable, and most major DAF sponsors. EIN 81-5162502.",
     f"mailto:{EMAIL}?subject=DAF%20grant%20inquiry", "Get DAF instructions"),
    ("Cryptocurrency", "Give crypto.",
     "We accept Bitcoin, Ethereum, and most major tokens through a compliant processor. You receive a fair-market-value tax receipt within 48 hours.",
     f"mailto:{EMAIL}?subject=Crypto%20gift%20inquiry", "Start a crypto gift"),
    ("Corporate matching", "Double your impact at work.",
     "Thousands of U.S. employers match nonprofit gifts at 1:1 or 2:1. Submit our EIN to your HR or matching platform; we will confirm the match.",
     "#corporate-matching", "Explore matching gifts"),
]

TRUST = [
    ('<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>',
     "Payment security",
     "Every transaction is processed by Stripe, a PCI-DSS Level 1 certified payment platform. 256-bit SSL encryption. SRLC USA never stores your card."),
    ('<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>',
     "Tax receipts in 48 hours",
     "An IRS-compliant receipt arrives in your inbox within 48 hours of every gift. Year-end summaries are emailed each January for monthly donors."),
    ('<circle cx="12" cy="12" r="9"/><path d="M9 12l2 2 4-4"/>',
     "Public Form 990",
     'Our latest Form 990 and audited financials are posted in full. Read them on the <a href="/about/financials/">Financials page</a>.'),
]

FAQ = [
    ("Is my donation tax-deductible?",
     "Yes. SRLC USA is a registered 501(c)(3) nonprofit, EIN 81-5162502. Every gift made through srlcusa.org is tax deductible to the extent permitted by law. No goods or services are exchanged in return for your gift."),
    ("When will I receive my tax receipt?",
     f'Within 48 hours of your gift, you receive an IRS-compliant receipt by email. Monthly donors also get a year-end summary in January, listing every gift from the prior calendar year. If a receipt does not arrive, email <a href="mailto:{EMAIL}">{EMAIL}</a> and we will resend it the same day.'),
    ("Can I cancel or change my monthly gift?",
     f'Anytime. There is no minimum commitment, no cancellation fee, and no phone tree. Email <a href="mailto:{EMAIL}">{EMAIL}</a> or log in to your donor portal to update the amount, change the program, pause, or cancel. Changes take effect on your next billing date.'),
    ("How is my gift used?",
     'Every gift goes to the program you designate. If you do not designate, gifts are directed to the Care with the most urgent unmet need that month. Overhead and fundraising costs are benchmarked against the most efficient U.S. nonprofits in our category. See the current ratio on the <a href="/about/financials/">Financials page</a>.'),
    ("Can I donate by check, wire, or ACH?",
     f'Yes. Checks payable to <strong>SRLC USA</strong> can be mailed to 500 Paterson Plank Rd #33685, Union City, NJ 07087. For wire or ACH instructions, or to set up a recurring bank transfer, email <a href="mailto:{EMAIL}">{EMAIL}</a> and our team will respond within one business day.'),
    ("Can international donors give to SRLC USA?",
     "Yes. Anyone with an internationally accepted credit card or DAF can give through srlcusa.org. Please note that tax-deductibility applies under U.S. law; donors outside the U.S. should consult a local tax adviser about deductibility in their country. For SRLC programs based in India, our parent organization offers separate India-domiciled giving options."),
    ("Will my contact information be shared?",
     "No. SRLC USA does not sell, rent, or trade donor data. Our full privacy policy outlines exactly what we store, how long we store it, and how to request deletion."),
]


def _amount_tiles():
    out = []
    for amt, outcome, sel in AMOUNTS:
        label = "Other" if amt == "custom" else f"${amt}"
        out.append(f'<button type="button" class="donate-amount" data-amt="{amt}" data-outcome="{outcome}" aria-pressed="{"true" if sel else "false"}">{label}</button>')
    return "\n          ".join(out)


def _ways():
    items = []
    for i, (eyebrow, h, body, href, cta) in enumerate(WAYS):
        pid = f"way-panel-{i + 1}"
        items.append(f"""<div class="faq-item">
        <h3 class="faq-item__h"><button type="button" class="faq-item__btn" aria-expanded="false" aria-controls="{pid}">
          <span class="way-summary">
            <span class="way-card__eyebrow">{eyebrow}</span>
            <span class="way-summary__h">{h}</span>
          </span>
          <span class="faq-item__icon" aria-hidden="true"></span>
        </button></h3>
        <div class="faq-item__body" id="{pid}" hidden>
          <p>{body}</p>
          <a class="way-card__cta" href="{href}">{cta}</a>
        </div>
      </div>""")
    return "\n      ".join(items)


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


def _trust():
    cards = "".join(f"""
      <article class="trust-sig">
        <svg class="trust-sig__svg" viewBox="0 0 24 24" aria-hidden="true">{svg}</svg>
        <h3 class="trust-sig__h">{h}</h3>
        <p class="trust-sig__body">{body}</p>
      </article>""" for svg, h, body in TRUST)
    cards += """
      <article class="trust-sig">
        <svg class="trust-sig__svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21V8l9-5 9 5v13"/><path d="M9 21V12h6v9"/></svg>
        <h3 class="trust-sig__h">501(c)(3) registered</h3>
        <p class="trust-sig__ein">EIN 81-5162502</p>
        <p class="trust-sig__body trust-sig__body--after-ein">Incorporated in New Jersey. Contributions are tax deductible to the extent permitted by law.</p>
      </article>"""
    return cards


def render_donate():
    hero_img, hero_w, hero_h = _hero_img()
    body = f"""<div class="donate-page">

<section class="donate-hero" id="donate-form" aria-labelledby="page-title">
  <div class="donate-hero__media" aria-hidden="true">
    <img src="{hero_img}" alt="" width="{hero_w}" height="{hero_h}" loading="eager" fetchpriority="high" decoding="async" data-photo-status="placeholder-stock">
  </div>
  <div class="container">
    <div class="donate-hero__grid">
      <div>
        <p class="donate-hero__eyebrow">Make a Gift</p>
        <h1 class="donate-hero__h" id="page-title">Every dollar funds a specific outcome.</h1>
        <p class="donate-hero__sub">Choose an amount. We'll show you exactly what it funds. Contributions are tax deductible to the extent permitted by law.</p>
        <div class="donate-hero__meta">
          <span>501(c)(3) registered</span>
          <span>EIN 81-5162502</span>
          <span>Tax-deductible</span>
        </div>
      </div>
      <aside class="donate-widget" aria-label="Donation form">
        <p class="donate-widget__head">Make a Gift</p>
        <h2 class="donate-widget__h">Start with an amount.</h2>
        <div class="donate-toggle" role="group" aria-label="Gift frequency">
          <button type="button" class="donate-toggle__btn" data-freq="one-time" aria-pressed="true">One time</button>
          <button type="button" class="donate-toggle__btn" data-freq="monthly" aria-pressed="false">Monthly</button>
        </div>
        <div class="donate-amounts" role="group" aria-label="Gift amount">
          {_amount_tiles()}
        </div>
        <div class="donate-custom">
          <span class="donate-custom__symbol" aria-hidden="true">$</span>
          <input class="donate-custom__input" type="number" min="1" inputmode="decimal" aria-label="Custom amount in U.S. dollars" placeholder="Enter amount">
        </div>
        <p class="donate-widget__outcome" id="donate-outcome" aria-live="polite">Your $50 gift funds school supplies for one student for a term.</p>
        <a class="btn btn--primary btn--lg donate-widget__cta" id="donate-cta" href="{MAIL_GIVE}%20(%2450)" data-mail="{MAIL_GIVE}">Email us to give</a>
        <p class="donate-widget__legal">Contributions are tax deductible to the extent permitted by law.</p>
      </aside>
    </div>
  </div>
</section>

<section class="section-pad section--white" id="corporate-matching" aria-label="Corporate matching gifts">
  <div class="container">
    <div class="section-head">
      <h2 class="section-h">Double Your Impact</h2>
      <p class="section-sub">Thousands of companies match the donations their employees make to nonprofits like SRLC USA. Some also match volunteer hours. Search for your employer below to see your company's matching gift policy and get the forms you need in minutes.</p>
    </div>
    <!-- DOUBLE THE DONATION EMBED: PENDING ACCOUNT SETUP
         Replace this placeholder block with the live embed snippet once
         the Double the Donation account and API key are confirmed (owner: Hardik).
         Standard embed shape:
         <script src="https://doublethedonation.com/api/js/ddplugin.js"></script>
         <div id="dd-container"></div>
         plus the DDCONF API key config snippet from the DTD dashboard. -->
    <div id="dd-container" class="dd-placeholder">
      <div class="dd-mock">
        <input class="dd-mock__input" type="text" placeholder="Search for your employer..." disabled aria-label="Employer search, launching soon">
        <button class="dd-mock__btn" type="button" disabled>Search</button>
      </div>
      <p class="dd-mock__caption">Company search launching soon.</p>
    </div>
    <p class="dd-attribution">Matching gift information provided by Double the Donation.</p>
    <p class="dd-cta"><a href="#donate-form">Make your gift now and submit your match request today.</a></p>
    <div class="dd-logos">
      <h3 class="dd-logos__h">Corporate matching gift eligibility</h3>
      <p class="dd-logos__qualifier">{MATCH_QUALIFIER}</p>
      {_partner_marquee()}
    </div>
  </div>
</section>

<section class="donate-strip" id="monthly" aria-label="Become a monthly donor">
  <div class="container">
    <p class="donate-strip__eyebrow">Sustaining gifts</p>
    <h2 class="donate-strip__h">A monthly gift sustains a Care every month of the year. <em>Not just today.</em></h2>
    <p class="donate-strip__body">Monthly donors are the backbone of SRLC USA. $25 a month is essential medicines for a different patient every month. $60 a month is one full mobile clinic day, twelve villages a year. Set it once.</p>
    <div class="donate-strip__ctas">
      <a class="btn btn--primary btn--lg" href="{MAIL_MONTHLY}%20(%2425%20monthly)">Become a monthly donor at $25</a>
      <a class="btn btn--ghost" href="#donate-form" data-select-freq="monthly">Choose another monthly amount</a>
    </div>
  </div>
</section>

<section class="section-pad section--lavender" id="other-ways" aria-label="Other ways to give">
  <div class="container">
    <div class="section-head">
      <p class="section-eyebrow">Other ways to give</p>
      <h2 class="section-h">More than a credit card. <em>Many paths, one mission.</em></h2>
      <p class="section-sub">Stock, donor-advised funds, crypto, and corporate matching can deepen your gift's impact and your tax benefit. Our team will guide you through the steps.</p>
    </div>
    <div class="faq-list ways-accordion">
      {_ways()}
    </div>
    <div class="check-wire">
      <p class="check-wire__h">Prefer to give by check or wire?</p>
      <p class="check-wire__body">Make checks payable to <strong>SRLC USA</strong>, EIN 81-5162502, and mail to 500 Paterson Plank Rd #33685, Union City, NJ 07087. For wires, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
  </div>
</section>

<section class="section-pad section--white" id="trust" aria-label="Trust signals">
  <div class="container">
    <div class="section-head">
      <p class="section-eyebrow">Trust, sourced</p>
      <h2 class="section-h">Your gift is safe, tracked, and reported.</h2>
      <p class="section-sub">SRLC USA is built for the donor who reads the fine print. Here is what we publish, encrypt, and confirm.</p>
    </div>
    <div class="trust-signals">{_trust()}
    </div>
  </div>
</section>

<section class="section-pad section--lavender" id="faq" aria-label="Donor questions">
  <div class="container">
    <div class="section-head">
      <p class="section-eyebrow">Before you give</p>
      <h2 class="section-h">Honest answers to the questions donors actually ask.</h2>
    </div>
    <div class="faq-list">
      {_faq()}
    </div>
  </div>
</section>

</div>
"""
    return page(
        "Donate | SRLC USA",
        "Give to SRLC USA. $25 funds essential medicines for one patient for a month. One-time or monthly. 501(c)(3), EIN 81-5162502. Contributions are tax deductible to the extent permitted by law.",
        "/donate/", body)
