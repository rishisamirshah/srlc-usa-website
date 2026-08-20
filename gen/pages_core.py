"""Renderers: homepage, donate, volunteer, about cluster, 404."""
from shell import page, ph, img, stats_row, badges_row, cta_band, sect_head, EMAIL, PHONE, EIN_LINE
from data_states import STATES, CAMPAIGNS
from data_cares import CARES
from pages_work import usmap_component, state_chips

GLOBAL_STATS = [
    ("33M+", "lives touched globally"),
    ("8.35M+", "patients treated globally"),
    ("3.28M+", "students reached globally"),
    ("12.24M+", "reached through Humanitarian Care globally"),
    ("450K+", "animals saved, treated, or rehabilitated globally"),
    ("8.90M+", "supported through Emergency Relief Care globally"),
]


def partner_marquee():
    import os
    pdir = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "partners")
    logos = sorted(f for f in os.listdir(pdir) if not f.startswith("."))
    imgs = "".join(f'<img src="/assets/img/partners/{f}" alt="{f.rsplit(".", 1)[0].replace("-", " ").title()}" loading="lazy">' for f in logos)
    return f'<div class="marquee marquee__fade"><div class="marquee__track">{imgs}</div></div>'


def render_home(svg_paths):
    care_cards = "".join(
        f'''<a class="card" href="/our-work/10-care-program/{c["slug"]}/">
      <img class="icon" src="/assets/img/care-icons/{c["icon"]}" alt="">
      <div class="card__kick">{c["num"]}</div>
      <h3>{c["name"]}</h3>
      <p style="font-size:var(--fs-sm);color:var(--ink-soft)">{c["one"]}</p>
    </a>''' for c in CARES)

    campaign_cards = "".join(
        f'''<a class="card reveal" data-d="{i}" href="/our-work/united-states/#campaigns">
      {ph(c["img_label"], style="min-height:220px;margin:-0.6rem -0.6rem 1rem;border-radius:var(--r-md)")}
      <h3>{c["name"]}</h3>
      <p style="font-size:var(--fs-sm);color:var(--ink-soft)">{c["body"][:150]}&hellip;</p>
      <span class="textlink" style="font-size:var(--fs-sm)">{c["cta"]} &rarr;</span>
    </a>''' for i, c in enumerate(CAMPAIGNS))

    body = f"""
<section class="hero">
  <div class="hero__media kenburns"><img src="/assets/img/photos/school-children-hero.jpg" alt="Students receiving school supplies at an SRLC USA distribution"></div>
  <div class="hero__scrim"></div>
  <div class="container hero__inner">
    <div class="eyebrow reveal in">Shrimad Rajchandra Love and Care USA</div>
    <h1 class="hero__title lines in">
      <span class="ln"><span>Serving with</span></span>
      <span class="ln"><span><em>love and care,</em></span></span>
      <span class="ln"><span>across America.</span></span>
    </h1>
    <p class="hero__sub reveal in" data-d="2">The US chapter of a global humanitarian movement that has touched 33M+ lives globally. Volunteers across 25+ US cities carry it forward, one neighborhood at a time.</p>
    <div class="hero__cta reveal in" data-d="3">
      <a class="btn btn--gold" href="/donate/">Donate <span class="arr">&rarr;</span></a>
      <a class="btn btn--line-light" href="/our-work/10-care-program/">Explore Our Work</a>
    </div>
    <div class="hero__foot reveal in" data-d="4"><span class="rule"></span><span>An initiative of Shrimad Rajchandra Mission Dharampur</span></div>
  </div>
</section>

<section class="sect grain">
  <div class="container container--narrow center">
    <div class="eyebrow reveal">Why we serve</div>
    <p class="pullquote reveal" data-d="1" style="margin-inline:auto">&ldquo;When there is love within, it flows naturally in the form of <mark>care</mark>.&rdquo;</p>
    <div class="goldrule reveal" data-d="2"></div>
    <p class="lead reveal" data-d="2" style="margin-inline:auto">We serve and bring joy, not because we have to, or because it is our duty, but because we love to.</p>
    <div class="reveal" data-d="3" style="margin-top:var(--sp-6)"><a class="textlink" href="/about/who-we-are/">Who we are</a></div>
  </div>
</section>

<section class="sect sect--dark grain">
  <div class="container">
    {sect_head("A global movement", "The numbers behind the <em style='color:var(--gold);font-style:italic'>love</em>", "SRLC USA is one chapter of a worldwide volunteer movement. Every figure below is part of its verified global record.")}
    <div style="margin-top:var(--sp-10)">{stats_row(GLOBAL_STATS)}</div>
  </div>
</section>

<section class="sect">
  <div class="container container--wide">
    <div class="sechead">
      {sect_head("The 10 Care Program", "Ten ways to care")}
      <div class="railnav reveal"><button data-rail-prev="#carerail" aria-label="Previous">&larr;</button><button data-rail-next="#carerail" aria-label="Next">&rarr;</button></div>
    </div>
  </div>
  <div class="container container--wide"><div class="rail" id="carerail">{care_cards}</div></div>
  <div class="container center" style="margin-top:var(--sp-4)"><a class="textlink reveal" href="/our-work/10-care-program/">Explore all ten Care programs</a></div>
</section>

<section class="sect sect--band grain">
  <div class="container"><div class="split split--wideL">
    <div>{usmap_component(svg_paths)}</div>
    <div>
      {sect_head("Find your chapter", "Care, close to <em style='color:var(--flame);font-style:italic'>home</em>", "Twelve states, twenty-two centers. Select yours to meet the volunteers already serving there.")}
      <div class="reveal" data-d="2" style="margin-top:var(--sp-6)">{state_chips()}</div>
      <div class="reveal" data-d="3" style="margin-top:var(--sp-8);display:flex;gap:1.6rem;flex-wrap:wrap">
        <a class="textlink" href="/our-work/india/">Our institutes in India</a>
        <a class="textlink" href="/our-work/mission-africa/">Mission Africa</a>
      </div>
    </div>
  </div></div>
</section>

<section class="sect">
  <div class="container">
    <div class="sechead">{sect_head("National campaigns", "Three moments the whole country shows up for")}</div>
    <div class="grid grid--3">{campaign_cards}</div>
  </div>
</section>

<section class="sect sect--sm" style="border-top:1px solid var(--line)">
  <div class="container">
    {sect_head("Recognition", "Trusted, verified, accountable", center=True)}
    <div style="margin-top:var(--sp-8)">{badges_row()}</div>
  </div>
  <div style="margin-top:var(--sp-10)">
    <p class="center reveal" style="font-size:var(--fs-eyebrow);letter-spacing:0.18em;text-transform:uppercase;color:var(--ink-soft);font-weight:600">Corporate matching gift partners</p>
    {partner_marquee()}
  </div>
</section>

<section class="sect sect--dark grain">
  <div class="container container--narrow center">
    <div class="eyebrow reveal">Stay close to the work</div>
    <h2 class="reveal">What your support builds,<br>delivered to your inbox.</h2>
    <form class="newsband reveal" data-d="1" style="margin:var(--sp-8) auto 0" name="updates" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="updates">
      <input type="hidden" name="source" value="homepage">
      <p style="display:none"><input name="bot-field"></p>
      <input type="email" name="email" required placeholder="Your email" aria-label="Email address" class="form-hidewrap">
      <button class="btn btn--gold form-hidewrap" type="submit">Subscribe</button>
      <div class="form-success" style="display:none;color:var(--gold);font-weight:600">Thank you. You are on the list.</div>
    </form>
  </div>
</section>

{cta_band("Be part of what <em>care</em> can do.", "Give once, give monthly, or give your Saturday morning. All of it reaches real people.", "Donate", "/donate/", ("Volunteer With Us", "/volunteer/"))}
"""
    return page(
        "SRLC USA | Shrimad Rajchandra Love and Care",
        "Volunteers across 25+ US cities serving neighbors through the 10 Care Program, institutes in India, and Mission Africa. A 501(c)(3) nonprofit. SRLC USA.",
        "/", body, overlay=True)


def render_donate():
    ways = [
        ("Give by ACH or check", "Bank transfer and mailed checks are our most efficient ways to receive your gift: more of every dollar reaches the programs. Write to us and we will send the details the same week.", f"mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA", "Email us to give"),
        ("Donor-advised funds &amp; trusts", "Recommend a grant to Shrimad Rajchandra Love and Care USA through your donor-advised fund or charitable trust. EIN 81-5162502.", f"mailto:{EMAIL}?subject=DAF%20grant%20to%20SRLC%20USA", "Start a DAF grant"),
        ("Corporate matching", "Your employer may match your gift. Check if your company participates, and your impact can double before it leaves your paycheck.", f"mailto:{EMAIL}?subject=Matching%20gift%20question", "Ask about matching"),
        ("Give your time", "Volunteers carry every program we run. If this season your gift is hours instead of dollars, we will put them to work.", "/volunteer/", "Volunteer instead"),
    ]
    ways_html = "".join(
        f'''<div class="card reveal" data-d="{i % 4}">
      <div class="stepnum">0{i + 1}</div>
      <h3>{t}</h3><p style="color:var(--ink-soft)">{b}</p>
      <a class="textlink" href="{h}">{cta}</a>
    </div>''' for i, (t, b, h, cta) in enumerate(ways))

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">Donate</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Every gift becomes</span></span><span class="ln"><span><em>someone&rsquo;s morning.</em></span></span></h1>
    <p class="lead reveal" data-d="1">A meal delivered, a backpack filled, a surgery that costs a family nothing. Choose an amount and the way of giving that fits you.</p>
    <div class="reveal" data-d="2" style="margin-top:var(--sp-8)">
      <div class="chips" id="amounts">
        <button type="button" data-amt="25">$25</button>
        <button type="button" data-amt="50">$50</button>
        <button type="button" class="on" data-amt="100">$100</button>
        <button type="button" data-amt="250">$250</button>
        <button type="button" data-amt="500">$500</button>
        <button type="button" data-amt="">Other</button>
      </div>
      <div style="margin-top:var(--sp-6);display:flex;gap:0.9rem;flex-wrap:wrap">
        <a class="btn btn--gold" id="givebtn" href="mailto:{EMAIL}?subject=Donation%20to%20SRLC%20USA%20(%24100)">Give by Email <span class="arr">&rarr;</span></a>
        <a class="btn btn--line" href="#ways">See all ways to give</a>
      </div>
      <p class="gallery-note reveal" data-d="3">Online card giving is being set up. Until it launches, our team personally handles every gift at <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
    </div>
  </div>
</section>

<section class="sect" id="ways">
  <div class="container">
    {sect_head("Ways to give", "Choose what fits your season")}
    <div class="grid grid--2" style="margin-top:var(--sp-8)">{ways_html}</div>
  </div>
</section>

<section class="sect sect--band grain">
  <div class="container center">
    {sect_head("Matching gifts", "Double the love before it leaves your paycheck", "Thousands of employers match charitable gifts dollar for dollar. If you see your company below, your gift can go twice as far.", center=True)}
  </div>
  <div style="margin-top:var(--sp-10)">{partner_marquee()}</div>
  <div class="container center" style="margin-top:var(--sp-8)">
    <a class="btn btn--fill reveal" href="mailto:{EMAIL}?subject=Matching%20gift%20question">Check your employer <span class="arr">&rarr;</span></a>
  </div>
</section>

<section class="sect--sm" style="border-top:1px solid var(--line)">
  <div class="container container--narrow center">
    <p style="font-size:var(--fs-sm);color:var(--ink-soft)">{EIN_LINE}</p>
    <p style="font-size:var(--fs-sm);color:var(--ink-soft)">Looking to donate via ACH, check, corporate matching or charitable trust? Please reach out to us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</section>
<script>
(function () {{
  var btns = document.querySelectorAll('#amounts button');
  var give = document.getElementById('givebtn');
  btns.forEach(function (b) {{
    b.addEventListener('click', function () {{
      var amt = b.getAttribute('data-amt');
      var subj = amt ? 'Donation to SRLC USA ($' + amt + ')' : 'Donation to SRLC USA';
      give.href = 'mailto:{EMAIL}?subject=' + encodeURIComponent(subj);
    }});
  }});
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
        f'<div class="card reveal" data-d="{i}"><h3>{t}</h3><p style="font-size:var(--fs-sm);color:var(--ink-soft)">{b}</p></div>'
        for i, (t, b) in enumerate(cards))
    steps = [
        ("Sign up", "Fill out the form at the bottom of this page. Share where you are, what skills or interests you can offer, and how much time you have each month. It takes under two minutes."),
        ("Meet your chapter", "A coordinator from the SRLC chapter in your area will reach out within a few days. They will introduce themselves and walk you through what the chapter is currently working on."),
        ("Show up", "Attend your first event. Meet the people who make the chapter run. Most volunteers return for the next one within a month."),
    ]
    steps_html = "".join(
        f'<div class="reveal" data-d="{i}"><div class="stepnum">0{i + 1}</div><h3>{t}</h3><p style="color:var(--ink-soft)">{b}</p></div>'
        for i, (t, b) in enumerate(steps))
    roles = ["Events and Logistics", "Food and Distribution", "Community Outreach", "Fundraising and Campaigns",
             "Communications and Social Media", "Healthcare Outreach", "University and Youth Programs",
             "Operations and Administration", "Chapter Leadership", "Internship", "Other"]
    role_opts = "".join(f'<option>{r}</option>' for r in roles)
    time_opts = "".join(f'<option>{t}</option>' for t in ["2 to 4 hours", "4 to 8 hours", "8+ hours", "Flexible"])

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">Get Involved</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Volunteer with</span></span><span class="ln"><span><em>SRLC USA</em></span></span></h1>
    <p class="lead reveal" data-d="1">Thousands of people across 25+ US cities give their time, their skills, and their energy to SRLC USA. Not because they have to. Because service is who they are.</p>
    <div style="margin-top:var(--sp-6)" class="reveal" data-d="2"><div class="statechips"><a style="pointer-events:none">501(c)(3) Nonprofit</a><a style="pointer-events:none">25+ US Cities</a><a style="pointer-events:none">Parent body: UN ECOSOC Special Consultative Status</a></div></div>
    <div style="margin-top:var(--sp-6)" class="reveal" data-d="3">
      <a class="btn btn--fill" href="#signup">Volunteer With Us <span class="arr">&rarr;</span></a>
      <div style="margin-top:var(--sp-4)"><a class="textlink" href="/our-work/united-states/">Find My State&rsquo;s Chapter</a></div>
    </div>
  </div>
</section>

<section class="sect">
  <div class="container">
    {sect_head("What volunteers build here", "More than volunteering. A community.")}
    <div class="grid grid--4" style="margin-top:var(--sp-8)">{cards_html}</div>
  </div>
</section>

<section class="sect sect--band grain">
  <div class="container">
    {sect_head("How it works", "Getting started is simple")}
    <div class="grid grid--3" style="margin-top:var(--sp-8)">{steps_html}</div>
  </div>
</section>

<section class="statbar">
  <div class="container">
    <p class="reveal" style="max-width:70ch;margin-bottom:var(--sp-8)">SRLC USA is the U.S. chapter of Shrimad Rajchandra Love and Care, a global humanitarian organization. Collectively, the initiatives that SRLC USA volunteers help fund and organize are part of a network that has reached 33M+ lives globally. Across medical programs alone, the parent organization has served 8.35M+ patients globally.</p>
    {stats_row([("33M+", "lives reached globally"), ("8.35M+", "patients served globally"), ("3.28M+", "students reached globally")])}
  </div>
</section>

<section class="sect" id="signup">
  <div class="container container--narrow">
    {sect_head("Sign up to volunteer", "Join the mission.", "Under two minutes. A chapter coordinator from your area will follow up personally.")}
    <form class="form" style="margin-top:var(--sp-8)" name="volunteer" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="volunteer">
      <p style="display:none"><input name="bot-field"></p>
      <div class="form-hidewrap">
        <div class="row">
          <div class="field"><label for="v-fn">First Name</label><input id="v-fn" name="first_name" required autocomplete="given-name"></div>
          <div class="field"><label for="v-ln">Last Name</label><input id="v-ln" name="last_name" required autocomplete="family-name"></div>
        </div>
        <div class="row" style="margin-top:1.1rem">
          <div class="field"><label for="v-em">Email Address</label><input id="v-em" type="email" name="email" required autocomplete="email"></div>
          <div class="field"><label for="v-zip">City / ZIP Code</label><input id="v-zip" name="city_zip" required autocomplete="postal-code"></div>
        </div>
        <div class="row" style="margin-top:1.1rem">
          <div class="field"><label for="v-sk">What skills or interests do you bring?</label><select id="v-sk" name="skills" required>{role_opts}</select></div>
          <div class="field"><label for="v-tm">How much time can you offer per month?</label><select id="v-tm" name="time" required>{time_opts}</select></div>
        </div>
        <div class="field" style="margin-top:1.1rem"><label for="v-ph">Phone Number <small>(Optional. So your chapter coordinator can reach you directly.)</small></label><input id="v-ph" type="tel" name="phone" autocomplete="tel"></div>
        <div style="margin-top:var(--sp-6)"><button class="btn btn--gold" type="submit">I Want to Volunteer <span class="arr">&rarr;</span></button></div>
      </div>
      <div class="form-success" style="display:none">
        <p class="pullquote" style="font-size:1.4rem">Thank you. A chapter coordinator from your area will be in touch within a few days.</p>
      </div>
    </form>
    <p class="gallery-note" style="margin-top:var(--sp-6)">Not ready to sign up yet? Follow us on <a href="https://www.instagram.com/srlc_usa/" rel="noopener" target="_blank">Instagram</a> and <a href="https://www.facebook.com/SRLCUSA/" rel="noopener" target="_blank">Facebook</a> to see what SRLC USA chapters are doing in your city.</p>
  </div>
</section>
"""
    return page(
        "Volunteer with SRLC USA | Give Your Time, Build Community",
        "Serve communities across the US with SRLC USA. A 501(c)(3) nonprofit whose work has reached 33M+ lives globally. Sign up to volunteer in two minutes.",
        "/volunteer/", body)


def render_who_we_are():
    promises = [
        ("Dignity, always", "Every living being deserves compassion, dignity and respect."),
        ("Every figure verified", "Our commitment to transparency is unwavering."),
        ("Built to last", "Long standing impact, for generations to come."),
    ]
    promises_html = "".join(
        f'<div class="card reveal" data-d="{i}"><div class="badge__medal" style="margin-bottom:1rem">&#10038;</div><h3>{t}</h3><p style="color:var(--ink-soft)">{b}</p></div>'
        for i, (t, b) in enumerate(promises))
    how = [
        ("Volunteer led", "Programs are carried by volunteers who know their communities. Because they give their time, administration costs stay low and more of every dollar reaches the programs it was given to support."),
        ("Designed to scale", "We invest in models that can be replicated, so a program that works in one community can be extended to the next."),
        ("Measured against evidence", "Every initiative operates within professional frameworks and defined performance indicators. Results, not intentions, decide what continues."),
        ("Building the next generation of leaders", "Volunteers of every generation carry this work, from students to retirees, and young people lead most of the initiatives under the 10 Care Program."),
    ]
    how_html = "".join(
        f'<div class="card reveal" data-d="{i % 4}"><h3 style="font-size:1.1rem">{t}</h3><p style="font-size:var(--fs-sm);color:var(--ink-soft)">{b}</p></div>'
        for i, (t, b) in enumerate(how))

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">About Us</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Love and care,</span></span><span class="ln"><span><em>in action.</em></span></span></h1>
    <p class="lead reveal" data-d="1">SRLC USA is what happens when physicians, engineers, teachers, and students decide their weekends belong to their neighbors. We are the US chapter of Shrimad Rajchandra Love and Care, a global nonprofit holding Special Consultative Status with the United Nations Economic and Social Council (ECOSOC), and a 501(c)(3) organization. But before we are any of that, we are people who believe care is not a profession. It is a practice.</p>
  </div>
</section>

<section class="sect">
  <div class="container"><div class="split split--wideL">
    <div>
      {sect_head("What we do", "Care you can point to")}
      <p class="reveal" data-d="1">We focus on immediate needs and the systems behind them. In the United States, volunteers prepare and share meals, equip students for the school year, and organize community care events with local partners. Globally, the movement builds and sustains hospitals, schools, and development programs designed to serve for generations. The programs differ; the standard does not: high-quality, sustainable work that outlasts the day we arrive.</p>
    </div>
    <div class="reveal" data-d="2">{img("/assets/img/photos/event-recent.jpg", "SRLC USA volunteers at a community event", cls="frame-tilt", drift=True)}</div>
  </div></div>
</section>

<section class="sect sect--band grain">
  <div class="container container--narrow center">
    <div class="eyebrow reveal">Our philosophy</div>
    <p class="pullquote reveal" data-d="1" style="margin-inline:auto">&ldquo;When there is love within, it flows naturally in the form of <mark>care</mark>.&rdquo;</p>
    <p class="lead reveal" data-d="2" style="margin-inline:auto;margin-top:var(--sp-6)">We serve and bring joy, not because we have to, or because it is our duty, but because we love to. That conviction shapes every program we run, from hospital corridors to classrooms to meal lines.</p>
  </div>
</section>

<section class="sect">
  <div class="container">
    {sect_head("Ten ways we care", "One vision, ten focus areas")}
    <p class="reveal" data-d="1" style="max-width:70ch">Every initiative we run belongs to one of ten focus areas, together the 10 Care Program: Health Care, Educational Care, Child Care, Woman Care, Tribal Care, Community Care, Humanitarian Care, Animal Care, Environmental Care, and Emergency Relief Care. In the United States, that vision looks like service in your own city, on your own street. Globally, it stands as permanent institutions in India and Mission Africa.</p>
    <div style="margin-top:var(--sp-10)">{stats_row([("33M+", "lives touched globally"), ("3.28M+", "students reached globally"), ("12.24M+", "reached through Humanitarian Care globally")])}</div>
    <div style="margin-top:var(--sp-10)">{badges_row()}</div>
    <div class="reveal" style="margin-top:var(--sp-8);display:flex;gap:1.6rem;flex-wrap:wrap">
      <a class="textlink" href="/our-work/10-care-program/">10 Care Program</a>
      <a class="textlink" href="/our-work/united-states/">United States</a>
      <a class="textlink" href="/our-work/india/">India</a>
      <a class="textlink" href="/our-work/mission-africa/">Mission Africa</a>
    </div>
  </div>
</section>

<section class="sect sect--band grain">
  <div class="container">
    {sect_head("How we work", "Built to be trusted")}
    <div class="grid grid--4" style="margin-top:var(--sp-8)">{how_html}</div>
  </div>
</section>

<section class="sect">
  <div class="container">
    {sect_head("Our commitments", "Three promises we keep", center=True)}
    <div class="grid grid--3" style="margin-top:var(--sp-8)">{promises_html}</div>
  </div>
</section>

{cta_band("Come see for <em>yourself</em>.", "An about page can only introduce us; it cannot let you feel the work. The programs, the numbers, and the financials are all published for anyone to read, and the volunteers are probably closer than you think. Come find out what care looks like when it is organized.", "Explore the 10 Care Program", "/our-work/10-care-program/")}
"""
    return page(
        "Who We Are | SRLC USA | 501(c)(3) Nonprofit",
        "Meet the volunteers bringing care and joy to communities across the US and worldwide. A 501(c)(3) nonprofit. See who we are. SRLC USA.",
        "/about/who-we-are/", body)


TIMELINE = [
    ("2006&ndash;2008", "A mobile dispensary begins carrying medical care to rural doorsteps, and a mid-day meal program gives families one more reason to send their children to school."),
    ("2009&ndash;2011", "Shrimad Rajchandra Gurukul opens in Karanjveri, Gujarat, and a new neonatal intensive care unit begins providing critical care for premature newborns."),
    ("2015", "New York City hosts SRLC&rsquo;s first Love and Care Walk, with more than 550 participants."),
    ("2016", "Shrimad Rajchandra Vidyapeeth opens as the first science college serving 238 villages of South Gujarat, and the Skill Development Center begins providing vocational training for tribal youth."),
    ("2019", "GuideStar awards SRLC its Platinum Seal for the highest level of transparency and accountability."),
    ("2020", "The United Nations grants SRLC Special Consultative Status. Vidyapeeth and Gurukul become the first science college and first secondary school under the State Board of Gujarat certified to ISO 9001 and ISO 29990."),
    ("2021", "COVID-19 relief reaches 50 cities on five continents, supporting 8.85M+ lives."),
    ("2022", "The 250-bed Shrimad Rajchandra Hospital and Research Center opens, and its surgeons perform the region&rsquo;s first open-heart cardiothoracic surgery."),
    ("2023", "The hospital earns NABH accreditation within its first year. In Nairobi, Kenya, a free eye and ear, nose, and throat (ENT) medical camp treats 7,500+ patients."),
    ("2024", "Mission Africa launches across 16 African nations. A mega-medical camp in Dharampur serves 25,000+ people, and US centers deliver 90,000+ educational items to 18,000+ students."),
]


def render_our_impact(svg_paths):
    nodes = "".join(
        f'<div class="tl-node"><div class="tl-node__year">{y}</div><p style="font-size:var(--fs-sm);color:var(--ink-soft)">{t}</p></div>'
        for y, t in TIMELINE)
    model = [
        ("Volunteer delivery model", "Programs carried by experienced professionals and volunteers."),
        ("Low administration costs", "A greater share of every contribution reaches the programs."),
        ("Defined performance indicators", "Each initiative is managed against measurable results."),
    ]
    model_html = "".join(
        f'<div class="card card--flat reveal" data-d="{i}"><div class="badge__medal" style="margin-bottom:1rem">&#10038;</div><h3 style="font-size:1.05rem">{t}</h3><p style="font-size:var(--fs-sm);color:var(--ink-soft)">{b}</p></div>'
        for i, (t, b) in enumerate(model))

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">About Us</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Our <em>impact</em></span></span></h1>
    <p class="lead reveal" data-d="1">The work of Shrimad Rajchandra Love and Care began with volunteers bringing medicine to families in rural villages. Over two decades, it has grown into a global movement that has touched 33M+ lives globally.</p>
  </div>
</section>

<section class="sect sect--dark grain">
  <div class="container">
    {sect_head("A global movement, by the numbers", "Global results", "SRLC USA is one chapter of a global movement carried largely by volunteers. The figures below reflect the movement&rsquo;s worldwide reach and behind them are individual people whose circumstances changed because someone was in a position to help.")}
    <div style="margin-top:var(--sp-10)">{stats_row(GLOBAL_STATS)}</div>
  </div>
</section>

<section class="sect">
  <div class="container"><div class="split">
    <div>
      {sect_head("Quality you can verify", "Independent recognition and accreditation")}
      <p class="reveal" data-d="1">The movement received Special Consultative Status from the United Nations Economic and Social Council in 2020, and GuideStar awarded its Platinum Seal for transparency and accountability in 2019. Independent recognition matters because it does not depend on our own account of the work. The 250-bed Shrimad Rajchandra Hospital and Research Center earned accreditation from the National Accreditation Board for Hospitals and Healthcare Providers (NABH) within its first year of operation.</p>
    </div>
    <div class="reveal" data-d="2">{img("/assets/img/photos/awards.jpg", "SRLC recognition and accolades", cls="frame-tilt--r")}</div>
  </div>
  <div class="container" style="margin-top:var(--sp-10)">{badges_row()}</div>
</section>

<section class="sect sect--band grain">
  <div class="container">
    {sect_head("Why a dollar goes further here", "An operating model built for efficiency", "Because the programs are carried by experienced professionals and volunteers, administration costs remain low, and each initiative is managed against defined performance indicators. In practical terms, this means a greater share of every contribution reaches the programs it was intended to support.")}
    <div class="grid grid--3" style="margin-top:var(--sp-8)">{model_html}</div>
  </div>
</section>

<section class="sect">
  <div class="container"><div class="split split--wideR">
    <div>{usmap_component(svg_paths)}</div>
    <div>
      {sect_head("Close to home", "Results in the United States")}
      <p class="reveal" data-d="1">In the United States, volunteers organize recurring service programs in cities from Los Angeles to New York, preparing and sharing meals, assembling school supplies, and holding community care events with established local partners. In 2024, US centers distributed 90,000+ educational items, reaching 18,000+ students.</p>
      <div class="reveal" data-d="2" style="margin-top:var(--sp-5)"><a class="textlink" href="/our-work/united-states/">Explore the US chapters</a></div>
    </div>
  </div></div>
</section>

<section class="sect sect--band grain">
  <div class="container container--wide">
    <div class="sechead">
      {sect_head("Two decades of documented growth", "Twenty years, one steady direction")}
      <div class="railnav reveal"><button data-rail-prev="#tl" aria-label="Earlier">&larr;</button><button data-rail-next="#tl" aria-label="Later">&rarr;</button></div>
    </div>
  </div>
  <div class="container container--wide"><div class="timeline__track" id="tl">{nodes}</div></div>
</section>

<section class="sect">
  <div class="container container--narrow">
    {sect_head("What these figures mean in practice", "One recovery among millions")}
    <div class="quotecard reveal" data-d="1"><p class="lead" style="max-width:none">Laxmibhai, a 52-year-old farmer, had been living with triple-vessel heart disease, and the surgery he needed was beyond his family&rsquo;s means. He received the region&rsquo;s first cardiothoracic bypass at Shrimad Rajchandra Hospital at no cost, and he has since returned home to his fields. His recovery is one outcome among millions, and it is the kind of outcome every figure on this page represents.</p></div>
  </div>
</section>

<section class="sect sect--sm" style="border-top:1px solid var(--line)">
  <div class="container container--narrow">
    {sect_head("Primary documents", "Read the full record", "Our annual reports and Forms 990 are published in full, so that supporters, grantmakers, and researchers can review the record directly rather than rely on summaries.")}
    <div class="reveal" style="margin-top:var(--sp-6)"><a class="textlink" href="/about/financials/">Visit the Financials page</a></div>
  </div>
</section>

{cta_band("Support work you can <em>verify</em>.", "Each result presented here belongs to a program that can be examined, visited, and audited, and each of those programs welcomes new support.", "Explore the 10 Care Program", "/our-work/10-care-program/")}
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
    voices = "".join(
        f'''<div class="card card--flat quotecard" style="border:0;border-left:3px solid;border-image:var(--grad-flame) 1;border-radius:0;background:var(--paper);box-shadow:var(--shadow-sm)">
      <p style="font-family:var(--serif);font-style:italic;font-size:1.08rem">&ldquo;{q}&rdquo;</p>
      <cite><b>{n}</b>{r}</cite>
    </div>''' for q, n, r in VOICES)

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">A timeless legacy flowing through a present-day visionary</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Our <em>Inspiration</em></span></span></h1>
  </div>
</section>

<section class="sect">
  <div class="container container--narrow">
    <div class="eyebrow reveal">Our Roots</div>
    <h2 class="reveal">Jainism and Lord Mahavir</h2>
    <p class="reveal" data-d="1">Jainism, one of the world&rsquo;s oldest spiritual philosophies, teaches enduring, universal principles of love and kindness.</p>
    <p class="reveal" data-d="1">Lord Mahavir, a revered spiritual leader who graced the Indian subcontinent over 2,500 years ago, illuminated a path to inner peace through understanding and kindness toward all, a message that continues to guide the modern world.</p>
  </div>
</section>

<section class="sect sect--band grain">
  <div class="container container--narrow">
    <div class="eyebrow reveal">Our Inspiration</div>
    <h2 class="reveal">Shrimad Rajchandraji</h2>
    <p class="reveal" data-d="1">In the late 19th century, the self-realized saint and poet-philosopher Shrimad Rajchandraji illuminated the wisdom of Lord Mahavir with remarkable clarity, shaping a spiritual path for a new era.</p>
    <p class="reveal" data-d="1">Grounded in direct inner experience, He articulated the subtle truths of spirituality through His own life, valuable teachings, and influential writings, including Shri Atmasiddhi Shastra, blending deep philosophical insights with practical steps for inner transformation.</p>
    <p class="reveal" data-d="1">Shrimad Rajchandraji&rsquo;s formative influence on Mahatma Gandhi&rsquo;s philosophy of truth and non-violence stands as a testament to the enduring impact of His message, which continues to resonate today.</p>
    <div class="quotecard reveal" data-d="2" style="margin-top:var(--sp-8)">
      <p class="pullquote" style="font-size:clamp(1.25rem,2.4vw,1.7rem);max-width:none">Standing at the foot of a hill, all that is visible are your immediate surroundings. Upon ascending the peak, you can see all of existence.<br><br>Shrimad Rajchandraji was at that vantage point.</p>
      <cite>Every word emerged from inner experience, every expression from universal vision, and every message from limitless compassion.</cite>
    </div>
  </div>
</section>

<section class="sect">
  <div class="container container--narrow">
    <div class="eyebrow reveal">Our Founder</div>
    <h2 class="reveal">Pujya Gurudevshri Rakeshji</h2>
    <h3 class="reveal" style="margin-top:var(--sp-6)">Legacy of Wisdom</h3>
    <p class="reveal" data-d="1">Pujya Gurudevshri Rakeshji is an enlightened visionary, global ambassador of peace, and the founder of Shrimad Rajchandra Mission Dharampur (SRMD). Following the revered footsteps of Shrimad Rajchandraji, Pujya Gurudevshri carries forward a legacy of timeless wisdom, translating profound spiritual truths into transformative teachings that make spirituality accessible to all.</p>
    <h3 class="reveal" style="margin-top:var(--sp-6)">Steady Force of Compassion</h3>
    <p class="reveal" data-d="1">Through Shrimad Rajchandra Love and Care (SRLC), Pujya Gurudevshri translates compassion into action. Guided by His philosophy of empathy and universal harmony, SRLC is a comprehensive program that addresses critical needs in healthcare, education, environmental sustainability, and social welfare, earning Special Consultative Status with the United Nations Economic and Social Council (ECOSOC) for its far-reaching impact.</p>
    <h3 class="reveal" style="margin-top:var(--sp-6)">A Movement Reaching America</h3>
    <p class="reveal" data-d="1">That vision now lives across the United States. Through SRLC USA, volunteers in communities nationwide carry this spirit of seva, selfless service, into action: serving their neighborhoods through the 10 Care Program and supporting institutions in India and initiatives around the world.</p>
    <div class="quotecard reveal" data-d="2" style="margin-top:var(--sp-8)">
      <p class="pullquote" style="font-size:clamp(1.25rem,2.4vw,1.7rem);max-width:none">Spearheading a global movement, while remaining steady in universal peace and untethered compassion.<br><br>Pujya Gurudevshri is the unmoved mover.</p>
    </div>
  </div>
</section>

<section class="sect sect--band grain">
  <div class="container container--narrow center">
    <div class="eyebrow reveal">Our Philosophy</div>
    <h2 class="reveal">Inner Awakening and Compassionate Action</h2>
    <p class="lead reveal" data-d="1" style="margin-inline:auto">Pujya Gurudevshri teaches a simple and complete path. Inner awakening brings clarity and harmony within, and love naturally flows outward as kindness in action. This path leads toward lasting peace and compassionate living in the world.</p>
  </div>
</section>

<section class="sect">
  <div class="container container--wide">
    <div class="sechead">
      <div>
        <div class="eyebrow reveal">Voices of Respect</div>
        <h2 class="reveal">A movement of interfaith and international harmony</h2>
        <p class="lead reveal" data-d="1">A beacon of unity that transcends faiths and boundaries, Pujya Gurudevshri&rsquo;s message and Mission resonate across traditions and communities.</p>
      </div>
      <div class="railnav reveal"><button data-rail-prev="#voices" aria-label="Previous">&larr;</button><button data-rail-next="#voices" aria-label="Next">&rarr;</button></div>
    </div>
  </div>
  <div class="container container--wide"><div class="rail" id="voices" style="grid-auto-columns:min(84vw,430px)">{voices}</div></div>
</section>

<section class="sect sect--sm" style="border-top:1px solid var(--line)">
  <div class="container container--narrow center">
    <p class="lead reveal" style="margin-inline:auto">That is the inspiration. The rest of this site is what it looks like in practice: ten Care programs, institutions in India, medical camps in Africa, and volunteers across the United States.</p>
    <div class="reveal" data-d="1" style="margin-top:var(--sp-6)"><a class="btn btn--fill" href="/our-work/10-care-program/">Explore the 10 Care Program <span class="arr">&rarr;</span></a></div>
  </div>
</section>
"""
    return page(
        "Our Inspiration | Shrimad Rajchandraji | SRLC USA",
        "The story and philosophy behind SRLC&rsquo;s work: Shrimad Rajchandraji, Pujya Gurudevshri Rakeshji, and the movement of selfless service they inspire. SRLC USA.",
        "/about/our-inspiration/", body)


MANAGEMENT = [
    ("Snehal Shah", "Trustee, President", "President of a small electronic distribution firm, with BSEE, MSEE, and MBA degrees. Leading the organization since 2017."),
    ("Dr. Chintan Mehta", "Trustee, Secretary &middot; Core Operations Lead", "Internal medicine specialist in Phoenix, AZ, leading the operations team of SRLC USA. Engaged for over 10 years."),
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
    people = "".join(
        f'''<div class="card reveal" data-d="{i % 3}">
      <div class="contactcard" style="margin:0 0 1rem;background:none;border:0;padding:0"><div class="dot">{n[0]}</div><div><b style="font-size:1.08rem">{n}</b><span class="card__kick" style="margin:0">{r}</span></div></div>
      <p style="font-size:var(--fs-sm);color:var(--ink-soft)">{b}</p>
    </div>''' for i, (n, r, b) in enumerate(MANAGEMENT))
    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">About Us</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Management</span></span><span class="ln"><span><em>Team</em></span></span></h1>
    <p class="lead reveal" data-d="1">Physicians, engineers, educators, and finance professionals who give their leadership the way every volunteer gives their weekend: freely.</p>
  </div>
</section>
<section class="sect">
  <div class="container"><div class="grid grid--3">{people}</div></div>
</section>
{cta_band("Serve alongside <em>them</em>.", "Chapter leadership grows from volunteering. Start where you are.", "Volunteer With Us", "/volunteer/")}
"""
    return page(
        "Management Team | SRLC USA",
        "The trustees and program leads guiding SRLC USA, a 501(c)(3) nonprofit serving communities across the United States and worldwide.",
        "/about/management/", body)


F990_YEARS = ["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017"]


def render_financials():
    cards = "".join(
        f'''<div class="card card--flat doccard reveal" data-d="{i % 4}">
      <div><b style="color:var(--maroon)">{y} Form 990</b><br><span style="font-size:var(--fs-sm);color:var(--ink-soft)">Annual IRS filing</span></div>
      <a class="textlink" style="font-size:var(--fs-sm)" href="mailto:info@srlc-usa.org?subject=Request%3A%20{y}%20Form%20990">Request</a>
    </div>''' for i, y in enumerate(F990_YEARS))
    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">About Us</div>
    <h1 class="pagehero__title lines"><span class="ln"><span><em>Financials</em></span></span></h1>
    <p class="lead reveal" data-d="1">We know how much it matters to you that your gift reaches the people it&rsquo;s meant for. It matters just as much to us. That&rsquo;s why every filing, report, and financial record we produce is published here in full, for anyone to read.</p>
  </div>
</section>

<section class="sect--sm sect">
  <div class="container">{badges_row()}</div>
</section>

<section class="sect sect--band grain">
  <div class="container">
    {sect_head("Documents by year", "The full record, newest first")}
    <div class="card reveal" style="margin-top:var(--sp-8);display:flex;align-items:center;justify-content:space-between;gap:1.5rem;flex-wrap:wrap">
      <div><div class="card__kick">Featured</div><h3>Annual Report 2024&ndash;2025</h3><p style="font-size:var(--fs-sm);color:var(--ink-soft);margin:0">The year in programs, numbers, and people.</p></div>
      <a class="btn btn--fill" href="mailto:info@srlc-usa.org?subject=Request%3A%20Annual%20Report%202024-2025">Request a copy</a>
    </div>
    <div class="grid grid--4" style="margin-top:var(--sp-6)">{cards}</div>
    <p class="gallery-note reveal">Self-hosted PDF downloads are being prepared. Until they are live, every document is available the same day by email.</p>
  </div>
</section>

<section class="sect--sm" style="border-top:1px solid var(--line)">
  <div class="container container--narrow center">
    <p style="font-size:var(--fs-sm);color:var(--ink-soft)">{EIN_LINE}</p>
    <p style="font-size:var(--fs-sm);color:var(--ink-soft)">Additional financial information is available on request at <a href="mailto:info@srlc-usa.org">info@srlc-usa.org</a>.</p>
  </div>
</section>
"""
    return page(
        "Financials | Form 990 and Reports | SRLC USA",
        "Annual filings, financial statements, and governing documents, published in full. SRLC USA is a 501(c)(3) nonprofit. EIN on page.",
        "/about/financials/", body)


def render_404():
    body = """
<section class="pagehero pagehero--band grain" style="min-height:70vh;display:flex;align-items:center">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container center">
    <div class="eyebrow reveal in" style="justify-content:center">Page not found</div>
    <h1 class="pagehero__title" style="margin-inline:auto">This page has <em>moved on</em>.</h1>
    <p class="lead" style="margin-inline:auto">The care continues elsewhere. Start from the beginning, or head straight to the work.</p>
    <div class="hero__cta" style="justify-content:center">
      <a class="btn btn--fill" href="/">Go home</a>
      <a class="btn btn--line" href="/our-work/10-care-program/">Explore Our Work</a>
    </div>
  </div>
</section>
"""
    return page("Page Not Found | SRLC USA", "The page you were looking for has moved.", "/404.html", body)
