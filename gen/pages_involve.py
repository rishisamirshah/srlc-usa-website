"""Get Involved pages + FAQs, completing the approved base's nav structure.
FAQ copy carried from the live srlcusa.org/faqs/ page (approved published content,
pending Naman's editorial pass). Fundraiser causes mirror the live /fundraise/ page."""
from shell import page, hero_purple, actionbar, EMAIL, PHONE
from pages_core import partner_marquee

FAQS = [
    ("What is Shrimad Rajchandra Love and Care?",
     "Shrimad Rajchandra Love and Care is a holistic, multi-pronged community support and development initiative, powered by genuine empathy, love and care of highly motivated volunteers delivering high quality, charitable sustainable interventions for the welfare of mankind, animals and the environment. The organization operates the 10 Care Program across cities worldwide."),
    ("What is the concept of having these 10 care programs?",
     "The focus of Shrimad Rajchandra Love and Care is to provide a holistic solution to the social development needs spanning across the spectrum of life with dedicated projects and initiatives."),
    ("How do you ensure efficiency and effectiveness of so many projects?",
     "Four key strategies: research-backed plans (primary research, feasibility studies, detailed budgets), defined structure (dedicated coordinators and project heads), accountability through periodic audits, and regular monitoring with reports to the Core Team."),
    ("How are these projects funded?",
     "Primary funding comes from generous donations of individual donors, corporates and foundations, along with government grants, corporate sponsorships, fundraising events, and product sales from beneficiaries."),
    ("How is Shrimad Rajchandra Love and Care different from any other NGO?",
     "Volunteers are driven by values emphasizing love and non-violence; the 10 Care Program is replicable and development driven, based on sustainable models; and as a volunteer-driven organization, administrative costs remain low."),
    ("Is Shrimad Rajchandra Love and Care a religious organization?",
     "Shrimad Rajchandra Love and Care is committed to bringing about a transformation in the lives of the underprivileged, irrespective of their caste, creed, religion or geography. It is a spiritual organisation guided by the principles of Shrimad Rajchandraji."),
    ("Do you provide service only to people of your own faith or religion?",
     "Services extend to all people without discrimination. Our love and care extends to all human beings and beyond it, to the animal and plant kingdom as well."),
    ("Can we find out where exactly and for whom our donation is used?",
     "Yes. Write to us at info@srlc-usa.org and we will walk you through exactly where your gift went."),
    ("Do you help individual beneficiaries?",
     "The organization assists individuals through subsidized surgeries, educational loans, and other aid on a need basis, though the majority of the work is done for community development."),
    ("Which geographical areas do you cover?",
     "Operations are global, with presence across India, the USA, the UK, the Middle East, Africa, and Southeast Asia. Primary focus areas are Dharampur and Kaprada in Gujarat&rsquo;s Valsad district."),
    ("Will I get tax benefits if I donate?",
     "Yes. Shrimad Rajchandra Love and Care USA is a registered 501(c)(3) nonprofit organization, EIN 81-5162502. Contributions are tax deductible to the extent permitted by law."),
    ("I am not part of Shrimad Rajchandra Love and Care. Can I still be a volunteer?",
     "Any interested individual can join Shrimad Rajchandra Love and Care as a volunteer. Sign up on our Volunteer page and a chapter coordinator from your area will be in touch."),
    ("Can I get a participation certificate?",
     "Yes, volunteers can request participation certificates upon completion of service."),
    ("There is a specific cause I care about. Can I volunteer for that specific cause?",
     "Yes, individuals can volunteer for any specific cause within the 10 Care Program based on their interests."),
    ("Can we visit the beneficiaries?",
     "Yes, visits can be arranged such that their privacy and dignity is maintained."),
]


def render_faqs():
    items = "".join(f"""<details{" open" if i == 0 else ""}>
      <summary>{q}</summary>
      <p style="margin:0;color:var(--color-ink-muted)">{a}</p>
    </details>""" for i, (q, a) in enumerate(FAQS))
    body = hero_purple(
        '<a href="/">Home</a> &middot; About Us',
        "Frequently Asked <em>Questions</em>",
        "Common questions on giving, programs, and transparency. If yours is not here, write to us and a real person will answer.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container" style="max-width:820px">
    <div class="accordion">{items}</div>
    <p style="font-size:.9rem;color:var(--color-ink-muted);margin-top:1.4rem">Still curious? Reach us at <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
  </div>
</section>
{actionbar("The best answer is seeing the work.", "Explore the ten Care programs, or meet the chapter closest to you.", "Explore the 10 Care Program", "/our-work/10-care-program/", ("Find your chapter", "/our-work/united-states/"))}
"""
    return page(
        "FAQs | SRLC USA",
        "Common questions on giving, programs, volunteering, and transparency at SRLC USA, a 501(c)(3) nonprofit.",
        "/about/faqs/", body)


def render_events():
    body = hero_purple(
        '<a href="/">Home</a> &middot; Get Involved',
        "Chapter <em>events</em>, all year long.",
        "Monthly meetings, food drives, Classroom of Change packing days, community lunches, and the annual campaigns that bring every chapter together. Most events are local, hands-on, and family friendly.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">What chapter life looks like</h2>
    <div class="vu-pair-grid mt-6">
      <div class="vu-card reveal" style="grid-template-columns:1fr"><h3 class="vu-card__h">Recurring service</h3><div class="vu-card__body"><p>Chapters host monthly service events: meal preparation and delivery, pantry support, hygiene kit assembly, and neighborhood cleanups. Washington, D.C. families prepare and deliver sandwiches every month; Houston families cook together in community kitchens; Boston volunteers decorate and deliver meal kits through Open Table.</p></div></div>
      <div class="vu-card reveal" data-stagger="1" style="grid-template-columns:1fr"><h3 class="vu-card__h">Seasonal campaigns</h3><div class="vu-card__body"><p>Classroom of Change packing days before each school year, Giving Tuesday in November, and Meals of Love and Care distributions year-round. These are the biggest volunteer days on the calendar, and the easiest way to bring friends.</p></div></div>
    </div>
    <div class="vu-coming mt-8 reveal">
      <div class="vu-coming__ic"><svg width="28" height="28"><use href="#vu-i-calendar"/></svg></div>
      <div>
        <h3 class="vu-coming__title">The full events calendar is on its way</h3>
        <p class="vu-coming__body">Until it lands here, your chapter coordinator shares upcoming dates directly. Sign up to volunteer and you will hear about the next one near you.</p>
      </div>
      <div class="vu-coming__ctas">
        <a class="btn btn--primary" href="/volunteer/">Get event invites</a>
        <a class="btn btn--ghost-dark" href="/our-work/united-states/">Find your chapter</a>
      </div>
    </div>
  </div>
</section>
{actionbar("Show up once. See what happens.", "Most volunteers who attend a single event return within a month.", "Volunteer With Us", "/volunteer/")}
"""
    return page(
        "Events | SRLC USA",
        "Chapter events, seasonal campaigns, and community gatherings across 25+ US cities. Find the next SRLC USA event near you.",
        "/events/", body)


FUND_CAUSES = [
    ("General Fund", ""), ("Education", "educational-care"), ("Healthcare", "health-care"),
    ("Humanitarian Care", "humanitarian-care"), ("Women Empowerment", "woman-care"),
    ("Child Care", "child-care"), ("Emergency Relief", "emergency-relief-care"),
    ("Environmental Care", "environmental-care"), ("Community Welfare", "community-care"),
    ("Tribal Welfare", "tribal-care"), ("Animal Welfare", "animal-care"),
]


def render_fundraise():
    chips = "".join(
        f'<a href="mailto:{EMAIL}?subject={("Start a fundraiser: " + name).replace(" ", "%20")}">{name}</a>'
        for name, slug in FUND_CAUSES)
    body = hero_purple(
        '<a href="/">Home</a> &middot; Get Involved',
        "Start a Fundraiser for <em>SRLC USA</em>",
        "Birthday, memorial, wedding, run. Any moment can become a fundraiser. Choose the fund you would like to raise for, and we will set you up with everything you need.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Choose your cause</h2>
    <p class="vu-lead">Every fundraiser supports a specific fund. Pick the one that moves you and tell us about your moment.</p>
    <div class="chip-row mt-6 reveal">{chips}</div>
    <div class="vu-coming mt-8 reveal">
      <div class="vu-coming__ic"><svg width="28" height="28"><use href="#vu-i-heart-hand"/></svg></div>
      <div>
        <h3 class="vu-coming__title">Self-serve fundraiser pages are being rebuilt</h3>
        <p class="vu-coming__body">Until they launch, our team sets up each fundraiser personally. Email us the cause and the occasion, and we will have you ready within a few days.</p>
      </div>
      <div class="vu-coming__ctas">
        <a class="btn btn--primary" href="mailto:{EMAIL}?subject=Start%20a%20fundraiser">Start by email</a>
      </div>
    </div>
  </div>
</section>
{actionbar("Not sure which fund?", "The General Fund reaches whichever program needs it most, when it needs it.", "Ways to Give", "/donate/")}
"""
    return page(
        "Start a Fundraiser | SRLC USA",
        "Turn a birthday, memorial, wedding, or run into support for SRLC USA programs. Choose a fund and start a fundraiser.",
        "/fundraise/", body)


def render_corporate():
    body = hero_purple(
        '<a href="/">Home</a> &middot; Get Involved',
        "Corporate <em>Giving</em>",
        "Matching gifts, sponsorships, and employee giving. Bring your company into the work, and your team&rsquo;s generosity can go twice as far.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Three ways companies join</h2>
    <div class="card-grid mt-6">
      <div class="cause-card reveal" data-stagger="1"><h3>Matching gifts</h3><p>Your employer may match your gift. Check if your company participates, and your impact can double before it leaves your paycheck.</p></div>
      <div class="cause-card reveal" data-stagger="2"><h3>Event sponsorships</h3><p>Sponsor a Classroom of Change packing day, a chapter service event, or a national campaign, and put your team on the floor beside our volunteers.</p></div>
      <div class="cause-card reveal" data-stagger="3"><h3>Employee giving and volunteering</h3><p>Workplace giving campaigns and group volunteer days, organized with your local SRLC USA chapter. Parsippany volunteers already run large-scale food drives with corporate groups such as AIG.</p></div>
    </div>
  </div>
</section>
<section class="vu-shell vu-shell--cream" id="matching">
  <div class="container">
    <h2 class="vu-h reveal" style="text-align:center">Employers our supporters match through</h2>
    <div class="mt-6">{partner_marquee()}</div>
    <p class="text-center mt-6"><a class="btn btn--primary" href="mailto:{EMAIL}?subject=Corporate%20giving">Talk to us about your company</a></p>
  </div>
</section>
{actionbar("Your company, in the work.", "One email starts it. We will bring the program to you.", "Email us", f"mailto:{EMAIL}?subject=Corporate%20giving")}
"""
    return page(
        "Corporate Giving | SRLC USA",
        "Matching gifts, sponsorships, and employee giving with SRLC USA, a 501(c)(3) nonprofit. Bring your company into the work.",
        "/corporate-giving/", body)


def render_partner():
    body = hero_purple(
        '<a href="/">Home</a> &middot; Get Involved',
        "Partner <em>With Us</em>",
        "Strategic partnerships for organizations and NGOs. Our chapters already serve alongside food banks, shelters, schools, and community organizations in every state where we operate.",
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Who we work with</h2>
    <p class="maxw-70">From Tempe Community Action Agency in Phoenix to Open Table in Boston, RISE Food Pantry in Princeton to The Sophia Way in Seattle, SRLC USA chapters partner with established local organizations that know their communities best. Nationally, the movement collaborates with schools, hospitals, food banks, and civic offices, including coordinated support with the NYC Mayor&rsquo;s Office for newly arrived families.</p>
    <div class="vu-coming mt-8 reveal">
      <div class="vu-coming__ic"><svg width="28" height="28"><use href="#vu-i-people"/></svg></div>
      <div>
        <h3 class="vu-coming__title">Exploring a partnership?</h3>
        <p class="vu-coming__body">Whether you run a food pantry, a school, a shelter, or a national program, tell us what your community needs. A member of our operations team will follow up personally.</p>
      </div>
      <div class="vu-coming__ctas">
        <a class="btn btn--primary" href="mailto:{EMAIL}?subject=Partnership%20inquiry">Start the conversation</a>
      </div>
    </div>
  </div>
</section>
{actionbar("Stronger together.", "The best partnerships start with one shared service day.", "Meet the chapters", "/our-work/united-states/")}
"""
    return page(
        "Partner With Us | SRLC USA",
        "Strategic partnerships for organizations and NGOs. Partner with SRLC USA chapters serving communities across the United States.",
        "/partner-with-us/", body)
