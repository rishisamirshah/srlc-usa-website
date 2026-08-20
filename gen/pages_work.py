"""Renderers: Our Work section (US hub, states, 10 Care, India, Mission Africa)."""
from shell import page, ph, img, stats_row, cta_band, sect_head
from data_states import STATES, CAMPAIGNS, US_HERO_BODY
from data_cares import CARES, TEN_CARE_INTRO
from data_india import INSTITUTES, INDIA_INTRO, SRV


def usmap_component(svg_paths, note=None):
    note_html = f'<p class="gallery-note">{note}</p>' if note else ""
    return f"""<div class="mapwrap reveal">
  <svg class="usmap" viewBox="0 0 959 593" role="img" aria-label="Map of the United States highlighting states where SRLC operates">{svg_paths}</svg>
  <div class="maptip" aria-hidden="true"></div>
  {note_html}
</div>"""


def state_chips():
    return '<div class="statechips">' + "".join(
        f'<a href="/our-work/united-states/{s["slug"]}/" data-state-target="{s["svg"].lower()}">{s["name"]}</a>'
        for s in STATES
    ) + "</div>"


def render_us_hub(svg_paths):
    campaigns = ""
    for i, c in enumerate(CAMPAIGNS):
        media = ph(c["img_label"], style="min-height:320px")
        text = f"""<div>
      <div class="card__kick">Campaign {i + 1:02d}</div>
      <h3 style="font-size:var(--fs-h2)">{c["name"]}</h3>
      <p class="lead" style="max-width:none">{c["body"]}</p>
      <div style="margin-top:var(--sp-6)"><a class="btn btn--fill" href="/donate/">{c["cta"]} <span class="arr">&rarr;</span></a></div>
    </div>"""
        left, right = (media, text) if i % 2 == 0 else (text, media)
        campaigns += f'<div class="split reveal" style="margin-bottom:var(--sect-sm)"><div>{left}</div><div>{right}</div></div>'

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">Our Work &middot; Where We Serve</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>SRLC&rsquo;s Nationwide</span></span><span class="ln"><span><em>Presence</em></span></span></h1>
    <p class="lead reveal" data-d="1">{US_HERO_BODY}</p>
  </div>
</section>

<section class="sect">
  <div class="container">
    {sect_head("Find your chapter", "Twelve states. Twenty-two centers.<br>One <em style='color:var(--flame);font-style:italic'>movement</em>.", "Every highlighted state is an active SRLC chapter. Select one to meet its centers, its people, and its work.")}
    <div style="margin-top:var(--sp-10)">{usmap_component(svg_paths)}</div>
    <div style="margin-top:var(--sp-8)" class="reveal">{state_chips()}</div>
  </div>
</section>

<section class="sect sect--band grain" id="campaigns">
  <div class="container">
    {sect_head("Our Campaigns", "Three national campaigns,<br>powered by every chapter", "Classroom of Change &middot; Giving Tuesday &middot; Meals of Love and Care")}
    <div style="margin-top:var(--sp-12)">{campaigns}</div>
  </div>
</section>

{cta_band("Your state is <em>closer</em> than you think.", "Find your chapter above, or raise your hand to volunteer wherever you are.", "Volunteer With Us", "/volunteer/", ("Ways to Give", "/donate/"))}
"""
    return page(
        "United States | Where We Serve | SRLC USA",
        "SRLC operates across 25+ US cities. Explore chapters state by state, meet the centers, and get involved near you. SRLC USA.",
        "/our-work/united-states/", body)


def render_state(s, idx):
    stats = stats_row(s["stats"])
    gallery_slots = "".join(
        ph(f'{s["name"]} chapter photo {i + 1} &middot; Media Bank', style="min-height:300px")
        for i in range(min(s["gallery"], 6))
    )
    gallery = f"""<section class="sect sect--sm">
  <div class="container container--wide">
    <div class="sechead">
      {sect_head("In the field", "Chapter life, on the ground")}
      <div class="railnav reveal"><button data-rail-prev="#gal" aria-label="Previous">&larr;</button><button data-rail-next="#gal" aria-label="Next">&rarr;</button></div>
    </div>
  </div>
  <div class="container container--wide"><div class="rail rail--photos" id="gal">{gallery_slots}</div></div>
</section>""" if s["gallery"] else ""

    tab_btns, tab_panels = "", ""
    for i, c in enumerate(s["centers"]):
        sel = "true" if i == 0 else "false"
        tab_btns += f'<button role="tab" aria-selected="{sel}">{c["name"]}</button>'
        secs = "".join(
            f'<h3 style="margin-top:var(--sp-6)">{h}</h3><p>{b}</p>'
            for h, b in c["sections"]
        )
        contact = ""
        if c["contact"]:
            name, addr, kind = c["contact"]
            link = f'<a href="mailto:{addr}">{addr}</a>' if kind == "email" else f'<a href="tel:{addr.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")}">{addr}</a>'
            initial = name[0]
            contact = f"""<div class="contactcard"><div class="dot">{initial}</div>
        <div><b>{name}</b>{link}</div></div>"""
        partners = f'<p class="partnerline"><b>Serving alongside:</b> {c["partners"]}</p>' if c["partners"] else ""
        active = " active" if i == 0 else ""
        tab_panels += f'<div class="tabs__panel{active}" role="tabpanel">{secs}{contact}{partners}</div>'

    prev_s = STATES[(idx - 1) % len(STATES)]
    next_s = STATES[(idx + 1) % len(STATES)]

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal"><a href="/our-work/united-states/" style="color:inherit">Where We Serve</a> &middot; United States</div>
    <h1 class="pagehero__title lines"><span class="ln"><span><em>{s["name"]}</em></span></span></h1>
    <p class="lead reveal" data-d="1">{s["hero"]}</p>
  </div>
</section>

<section class="statbar">
  <div class="container">{stats}</div>
</section>

{gallery}

<section class="sect sect--band grain">
  <div class="container">
    {sect_head("Constantly serving communities", "Inside the " + s["name"] + " centers")}
    <div data-tabs style="margin-top:var(--sp-8)" class="reveal">
      <div class="tabs__list" role="tablist">{tab_btns}</div>
      {tab_panels}
    </div>
  </div>
</section>

{cta_band("Serve with us in <em>" + s["name"] + "</em>.", "Reach out to your local SRLC leaders, or sign up and your chapter coordinator will be in touch.", "Volunteer With Us", "/volunteer/", ("Ways to Give", "/donate/"))}

<section class="sect--sm" style="border-top:1px solid var(--line)">
  <div class="container" style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap">
    <a class="textlink" href="/our-work/united-states/{prev_s["slug"]}/">&larr; {prev_s["name"]}</a>
    <a class="textlink" href="/our-work/united-states/">All states</a>
    <a class="textlink" href="/our-work/united-states/{next_s["slug"]}/">{next_s["name"]} &rarr;</a>
  </div>
</section>
"""
    return page(
        f'{s["name"]} | SRLC USA Chapters',
        f'SRLC {s["name"]}: volunteers in {s["cities"]} serving neighbors through hunger relief, education support, and community care. Get involved near you.',
        f'/our-work/united-states/{s["slug"]}/', body)


def render_tencare_hub():
    chips = "".join(
        f'<a href="#{c["slug"]}"><img src="/assets/img/care-icons/{c["icon"]}" alt="" style="height:22px;width:auto;vertical-align:-4px;margin-right:6px">{c["num"]} {c["name"]}</a>'
        for c in CARES
    )
    rail_dots = "".join(f'<a href="#{c["slug"]}" aria-label="{c["name"]}"></a>' for c in CARES)
    panels = ""
    for c in CARES:
        stat = ""
        if c["stat"]:
            stat = f'<div class="carepanel__stat"><div class="stat__num counter">{c["stat"][0]}</div><div class="stat__label">{c["stat"][1]}</div></div>'
        panels += f"""<section class="carepanel" id="{c["slug"]}">
  <div class="carepanel__num" aria-hidden="true">{c["num"]}</div>
  <div class="container">
    <div class="carepanel__body">
      <img class="icon reveal" src="/assets/img/care-icons/{c["icon"]}" alt="" style="width:64px">
      <h2 class="lines"><span class="ln"><span>{c["name"]}</span></span></h2>
      <p class="lead reveal" data-d="1" style="max-width:none">{c["one"]}</p>
      {stat}
      <div style="margin-top:var(--sp-6)" class="reveal" data-d="2"><a class="btn btn--line" href="/our-work/10-care-program/{c["slug"]}/">Explore {c["name"]} <span class="arr">&rarr;</span></a></div>
    </div>
  </div>
</section>"""

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">Our Work</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Ten ways</span></span><span class="ln"><span>to <em>care</em>.</span></span></h1>
    <p class="lead reveal" data-d="1">{TEN_CARE_INTRO}</p>
    <div style="margin-top:var(--sp-8)" class="reveal" data-d="2"><div class="statechips">{chips}</div></div>
  </div>
</section>
<nav class="progressrail" aria-label="Care programs">{rail_dots}</nav>
{panels}
{cta_band("Every Care needs <em>carriers</em>.", "Choose the work that moves you. Your gift and your hours both count.", "Support the 10 Care Program", "/donate/", ("Volunteer", "/volunteer/"))}
"""
    return page(
        "The 10 Care Program | Ten Ways to Care | SRLC USA",
        "Ten areas of service, one promise: care for every life. Explore the 10 Care Program, from Health Care to Emergency Relief Care. SRLC USA.",
        "/our-work/10-care-program/", body)


def render_care(c):
    cards = ""
    if c["cards"]:
        cells = ""
        for name, desc, href in c["cards"]:
            inner = f'<h3 style="font-size:1.1rem">{name}</h3><p style="font-size:var(--fs-sm);color:var(--ink-soft)">{desc}</p>'
            if href:
                cells += f'<a class="card reveal" href="{href}">{inner}<span class="textlink" style="font-size:var(--fs-sm)">Visit the institute &rarr;</span></a>'
            else:
                cells += f'<div class="card card--flat reveal">{inner}</div>'
        cols = "grid--3" if len(c["cards"]) != 4 else "grid--4"
        cards = f'<div class="grid {cols}" style="margin-top:var(--sp-8)">{cells}</div>'

    us = ""
    if c["us"]:
        us = f"""<section class="sect">
  <div class="container"><div class="split split--wideR">
    <div>{ph("US chapter volunteers &middot; Media Bank", cls="frame-tilt", style="min-height:340px")}</div>
    <div>{sect_head("In the United States", "The same care, close to home")}<p class="reveal" data-d="1">{c["us"]}</p></div>
  </div></div>
</section>"""

    story = ""
    if c["story"]:
        h, b = c["story"]
        story = f"""<section class="sect sect--band grain">
  <div class="container container--narrow">
    <div class="eyebrow reveal">One life, changed</div>
    <h2 class="reveal">{h}</h2>
    <div class="quotecard reveal" data-d="1"><p class="lead" style="max-width:none">{b}</p></div>
  </div>
</section>"""

    impact = ""
    if c["stat"]:
        impact = f"""<section class="statbar"><div class="container center">
  <div class="stat__num counter" style="font-size:clamp(3rem,7vw,5rem)">{c["stat"][0]}</div>
  <div class="stat__label" style="margin-inline:auto">{c["stat"][1]}</div>
</div></section>"""

    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container"><div class="split split--wideL">
    <div>
      <div class="eyebrow reveal"><a href="/our-work/10-care-program/" style="color:inherit">10 Care Program</a> &middot; {c["num"]}</div>
      <h1 class="pagehero__title lines"><span class="ln"><span><em>{c["name"]}</em></span></span></h1>
      <p class="lead reveal" data-d="1">{c["opening"]}</p>
    </div>
    <div class="reveal" data-d="2">{ph(c["hero_img"], style="min-height:300px")}</div>
  </div></div>
</section>

<section class="sect">
  <div class="container">
    {sect_head("The work in India", "Where this Care begins")}
    <p class="reveal" data-d="1" style="max-width:70ch">{c["india"]}</p>
    {cards}
  </div>
</section>

{us}
{story}
{impact}
{cta_band("Carry <em>" + c["name"] + "</em> further.", "Your employer may match your gift. Check if your company participates.", c["cta"], "/donate/")}
"""
    return page(c["title"], c["desc"], f'/our-work/10-care-program/{c["slug"]}/', body)


def render_india_hub():
    blocks = ""
    for i, inst in enumerate(INSTITUTES):
        blocks += f"""<a class="card reveal" data-d="{i % 3}" href="/our-work/india/{inst["slug"]}/">
  <div class="card__kick">{inst["tag"]}</div>
  <h3>{inst["name"]}</h3>
  <p style="font-size:var(--fs-sm);color:var(--ink-soft)">{inst["desc"]}</p>
  <span class="textlink" style="font-size:var(--fs-sm)">Visit the institute &rarr;</span>
</a>"""
    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">Our Work &middot; Where We Serve</div>
    <h1 class="pagehero__title lines"><span class="ln"><span>Our Institutes</span></span><span class="ln"><span>in <em>India</em></span></span></h1>
    <p class="lead reveal" data-d="1">{INDIA_INTRO}</p>
  </div>
</section>
<section class="sect">
  <div class="container"><div class="grid grid--2">{blocks}</div></div>
</section>
{cta_band("Institutions built to <em>outlast us all</em>.", "Every institute welcomes support from across the world.", "Support Our Institutes", "/donate/")}
"""
    return page(
        "India | Our Institutes | SRLC USA",
        "Permanent institutions in South Gujarat: a charitable hospital, schools and colleges, vocational training, an animal sanctuary, and a center for women. SRLC USA.",
        "/our-work/india/", body)


def render_institute(inst):
    extra = f'<p class="reveal" data-d="2">{inst["extra"]}</p>' if inst.get("extra") else ""
    title = inst.get("meta_title", f'{inst["name"].replace("&rsquo;", chr(8217))} | SRLC USA')
    desc = inst.get("meta_desc", f'{inst["desc"][:150]}')
    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal"><a href="/our-work/india/" style="color:inherit">Our Institutes in India</a> &middot; {inst["tag"]}</div>
    <h1 class="pagehero__title lines" style="font-size:var(--fs-h1)"><span class="ln"><span>{inst["name"]}</span></span></h1>
    <p class="lead reveal" data-d="1">{inst["intro"]}</p>
  </div>
</section>
<section class="sect">
  <div class="container"><div class="split split--wideL">
    <div>
      <div class="eyebrow reveal">Approved description</div>
      <p class="pullquote reveal" data-d="1" style="max-width:34ch;font-size:clamp(1.3rem,2.4vw,1.7rem)">{inst["desc"]}</p>
      {extra}
      <div style="margin-top:var(--sp-8)" class="reveal" data-d="3">
        <a class="btn btn--fill" href="/donate/">Support This Institution <span class="arr">&rarr;</span></a>
        <div style="margin-top:var(--sp-5)"><a class="textlink" href="/our-work/india/">Explore all SRLC institutes in India</a></div>
      </div>
    </div>
    <div class="reveal" data-d="2">{ph(inst["img"], cls="frame-tilt--r", style="min-height:380px")}</div>
  </div></div>
</section>
{cta_band("Part of <em>" + inst["care"] + "</em>.", "This institute anchors one of the ten Care programs.", "Explore " + inst["care"], inst["care_url"])}
"""
    return page(title, desc, f'/our-work/india/{inst["slug"]}/', body)


def render_vidyapeeth():
    trust = "".join(f'<a style="pointer-events:none">{t}</a>' for t in SRV["trust"])
    programs = "".join(
        f'<div class="card card--flat reveal" data-d="{i % 5}"><h3 style="font-size:1.05rem">{n}</h3><p style="font-size:var(--fs-sm);color:var(--ink-soft)">{d}</p></div>'
        for i, (n, d) in enumerate(SRV["programs"]))
    pillars = "".join(
        f'<div class="card card--flat reveal" data-d="{i}"><div class="stepnum">0{i + 1}</div><h3 style="font-size:1.05rem">{n}</h3><p style="font-size:var(--fs-sm);color:var(--ink-soft)">{d}</p></div>'
        for i, (n, d) in enumerate(SRV["pillars"]))
    need = "".join(f'<p class="reveal">{p}</p>' for p in SRV["need"])
    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal"><a href="/our-work/india/" style="color:inherit">Our Institutes in India</a> &middot; Science College</div>
    <h1 class="pagehero__title lines" style="max-width:20ch"><span class="ln"><span>The First Science College</span></span><span class="ln"><span>Across <em>238 Villages</em></span></span></h1>
    <p class="lead reveal" data-d="1">{SRV["sub"]}</p>
    <div style="margin-top:var(--sp-6)" class="reveal" data-d="2"><div class="statechips">{trust}</div></div>
    <div style="margin-top:var(--sp-6)" class="reveal" data-d="3"><a class="btn btn--fill" href="/donate/">{SRV["cta"]} <span class="arr">&rarr;</span></a></div>
  </div>
</section>

<section class="sect">
  <div class="container"><div class="split split--wideL">
    <div>{sect_head("The need", SRV["need_h2"])}{need}</div>
    <div class="reveal" data-d="2">{ph("The Dharampur region &middot; Media Bank", cls="frame-tilt", style="min-height:360px")}</div>
  </div></div>
</section>

<section class="sect sect--band grain">
  <div class="container">
    {sect_head("What your support funds", SRV["programs_h2"], SRV["programs_intro"])}
    <div class="grid grid--3" style="margin-top:var(--sp-8)">{programs}</div>
    <p class="reveal" style="margin-top:var(--sp-10);max-width:70ch">{SRV["support_intro"]}</p>
    <div class="grid grid--4" style="margin-top:var(--sp-8)">{pillars}</div>
  </div>
</section>

<section class="sect">
  <div class="container center">
    {sect_head("Impact", SRV["impact_h2"], center=True)}
    <div style="margin-top:var(--sp-8);display:flex;justify-content:center;gap:clamp(2rem,8vw,6rem);flex-wrap:wrap">
      {"".join(f'<div class="reveal" data-d="{i}"><div class="stat__num counter">{n}</div><div class="stat__label" style="margin-inline:auto">{l}</div></div>' for i, (n, l) in enumerate(SRV["impact"]))}
    </div>
  </div>
</section>

{cta_band(SRV["close_h2"].replace("Be the reason", "Be the <em>reason</em>"), SRV["close"], SRV["cta"])}
"""
    return page(SRV["title"], SRV["desc"], "/our-work/india/vidyapeeth/", body)


def render_africa():
    body = f"""
<section class="pagehero pagehero--band grain">
  <img class="pagehero__flame" src="/assets/img/srlc-mark.png" alt="">
  <div class="container">
    <div class="eyebrow reveal">Our Work &middot; Where We Serve</div>
    <h1 class="pagehero__title lines" style="max-width:18ch"><span class="ln"><span>Distance never decides</span></span><span class="ln"><span>who receives <em>care</em>.</span></span></h1>
    <p class="lead reveal" data-d="1">Mission Africa brings doctors, medicine, and follow-up care to communities where the nearest clinic can be hours away, at no cost to patients. We work with local health workers and community partners across 16 countries in Africa.</p>
    <div style="margin-top:var(--sp-6)" class="reveal" data-d="2"><div class="statechips"><a style="pointer-events:none">501(c)(3) Nonprofit</a><a style="pointer-events:none">33M+ Lives Touched Globally</a><a style="pointer-events:none">Parent body: UN ECOSOC Special Consultative Status</a></div></div>
    <div style="margin-top:var(--sp-6)" class="reveal" data-d="3"><a class="btn btn--fill" href="/donate/">Stand With Mission Africa <span class="arr">&rarr;</span></a></div>
  </div>
</section>

<section class="sect">
  <div class="container"><div class="split split--wideL">
    <div>
      {sect_head("The need", "Distance should not decide who gets care")}
      <p class="reveal" data-d="1">In much of the region Mission Africa serves, the barrier to health is not the treatment. It is the miles between a family and anyone who can provide it, the distance where a curable illness quietly becomes a permanent one. Launched in 2024 by Shrimad Rajchandra Love and Care (SRLC), Mission Africa now works across 16 countries in Africa to close that distance.</p>
      <div style="margin-top:var(--sp-8);display:flex;gap:clamp(2rem,6vw,4rem);flex-wrap:wrap">
        <div class="reveal"><div class="stat__num counter">16</div><div class="stat__label">countries reached</div></div>
        <div class="reveal" data-d="1"><div class="stat__num counter">7,500+</div><div class="stat__label">patients treated at a free eye and ENT medical camp in Nairobi, Kenya</div></div>
      </div>
    </div>
    <div class="reveal" data-d="2">{ph("Camp registration, morning light &middot; Mission Africa team photos pending", cls="frame-tilt--r", style="min-height:400px")}</div>
  </div></div>
</section>

<section class="sect sect--band grain">
  <div class="container">
    {sect_head("The work", "A clinic that comes to you")}
    <p class="reveal" data-d="1" style="max-width:70ch">Mission Africa brings the full spectrum of care to the community. Full medical camps staged inside the community, with doctors, diagnostics, and medicine in one place, free to every patient who walks in. And when the camp packs up, the care does not leave. Community programs carry it between visits.</p>
    <div class="grid grid--2" style="margin-top:var(--sp-8)">
      <div class="card reveal"><h3>Healthcare access</h3><p style="color:var(--ink-soft)">Medical camps, medicine placed directly into waiting hands, and training for community health workers, so care remains long after the visiting doctors have gone.</p></div>
      <div class="card reveal" data-d="1"><h3>Community development</h3><p style="color:var(--ink-soft)">Education, nutrition, and livelihood programs built with local communities rather than for them, so the change outlasts the camp.</p></div>
    </div>
  </div>
</section>

<section class="sect">
  <div class="container container--narrow">
    {sect_head("Proven far from here", "Your gift does not land on an experiment")}
    <p class="reveal" data-d="1">Mission Africa did not start from zero and your gift does not land on an experiment. It extends a healthcare model refined over decades in Dharampur, India, where a 250-bed hospital accredited by the National Accreditation Board for Hospitals and Healthcare Providers (NABH) treats patients regardless of their ability to pay. The movement behind it has touched 33M+ lives globally, and volunteers across the United States help fund and power the work.</p>
    <div class="reveal" data-d="2" style="margin-top:var(--sp-5);display:flex;gap:1.6rem;flex-wrap:wrap">
      <a class="textlink" href="/our-work/10-care-program/">Our Causes</a>
      <a class="textlink" href="/our-work/india/">India</a>
      <a class="textlink" href="/our-work/united-states/">United States</a>
    </div>
  </div>
</section>

<section class="sect sect--dark grain">
  <div class="container container--narrow center">
    <div class="eyebrow reveal">Stay close to the work</div>
    <h2 class="reveal">Camps are episodic. Your connection<br>doesn&rsquo;t have to be.</h2>
    <p class="lead reveal" data-d="1" style="margin-inline:auto">Leave your email and we will send you what your support built: photos with consent, numbers with verification, and the occasional story worth your inbox.</p>
    <form class="newsband reveal" data-d="2" style="margin:var(--sp-8) auto 0" name="updates" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="updates">
      <input type="hidden" name="source" value="mission-africa">
      <p style="display:none"><input name="bot-field"></p>
      <input type="email" name="email" required placeholder="Your email" aria-label="Email address" class="form-hidewrap">
      <button class="btn btn--gold form-hidewrap" type="submit">Get Camp Updates</button>
      <div class="form-success" style="display:none;color:var(--gold);font-weight:600">Thank you. You are on the list.</div>
    </form>
  </div>
</section>

{cta_band("Help the next camp <em>happen</em>.", "Somewhere right now, a mother is measuring the distance between her child and a doctor. Your gift shortens it. Put medicine on the road, and hope alongside it.", "Stand With Mission Africa")}
"""
    return page(
        "Mission Africa | Free Medical Camps | SRLC USA",
        "Doctors, medicine, and follow-up care reach 16 African nations through Mission Africa. Send care the last mile. SRLC USA, a 501(c)(3) nonprofit.",
        "/our-work/mission-africa/", body)
