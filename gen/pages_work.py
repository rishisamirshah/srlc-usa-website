"""Renderers: Our Work — flat pass. Copy verbatim from the master doc tabs.
Per-state stat bands are omitted (CLAUDE.md banned list) and flagged in the
build log. End-of-page CTAs render as flat sections, never banners."""
from shell import page, ph, page_header, flat_cta, trust_bar
from data_states import STATES, CAMPAIGNS, US_HERO_BODY
from data_cares import CARES, TEN_CARE_INTRO
from data_india import INSTITUTES, INDIA_INTRO, SRV


def cf_map(svg_inner, aria="Map of the United States highlighting SRLC chapter states"):
    return f"""<div class="cf-map reveal">
  <svg viewBox="0 0 959 593" xmlns="http://www.w3.org/2000/svg" class="cf-map__svg" aria-label="{aria}" preserveAspectRatio="xMidYMid meet">{svg_inner}</svg>
</div>
<div class="cf-map__legend" aria-hidden="true"><span><span class="swatch"></span>Active SRLC USA chapter</span></div>"""


def state_chips():
    return '<div class="chip-row reveal">' + "".join(
        f'<a href="/our-work/united-states/{s["slug"]}/" data-state-target="{s["svg"].lower()}">{s["name"]}</a>'
        for s in STATES) + "</div>"


def render_us_hub(svg_inner):
    campaigns = ""
    for i, c in enumerate(CAMPAIGNS):
        split_cls = "vu-split" if i % 2 == 0 else "vu-split vu-split--reverse"
        campaigns += f"""<div class="{split_cls} reveal" style="margin-bottom:2.4rem">
      <div class="vu-split__copy">
        <h3>{c["name"]}</h3>
        <p>{c["body"]}</p>
        <a class="btn btn--primary" href="/donate/">{c["cta"]}</a>
      </div>
      <div class="vu-split__photo">{ph(c["img_label"])}</div>
    </div>"""

    body = page_header(
        "Our Work &middot; Where We Serve",
        "SRLC&rsquo;s Nationwide Presence",
        US_HERO_BODY,
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first">
  <div class="container">
    {cf_map(svg_inner)}
    <div class="mt-6">{state_chips()}</div>
  </div>
</section>

<section class="vu-shell vu-shell--cream" id="campaigns">
  <div class="container">
    <h2 class="vu-h reveal">Our Campaigns</h2>
    <div class="mt-6">{campaigns}</div>
  </div>
</section>

{flat_cta("Find your chapter, or start where you are.", "Every highlighted state is an active SRLC USA chapter.", "Volunteer With Us", "/get-involved/volunteer/", ("Ways to Give", "/donate/"))}
"""
    return page(
        "SRLC in the United States | Local Programs and Chapters",
        "SRLC volunteers serve communities in eleven states and D.C. Find your state, see local programs, and join a chapter near you. SRLC USA.",
        "/our-work/united-states/", body)


def render_state(s, idx):
    gallery_slots = "".join(
        ph(s.get("gallery_note", f'{s["name"]} chapter photography, Media Bank'))
        for i in range(min(s["gallery"], 6)))
    gallery = f"""<section class="vu-shell vu-shell--cream vu-shell--narrow">
  <div class="container">
    <div class="sechead">
      <h2 class="vu-h reveal" style="margin:0">Photo gallery</h2>
      <div class="railnav"><button data-rail-prev="#gal" aria-label="Previous">&larr;</button><button data-rail-next="#gal" aria-label="Next">&rarr;</button></div>
    </div>
    <div class="rail" id="gal">{gallery_slots}</div>
  </div>
</section>""" if s["gallery"] else ""

    tab_btns, tab_panels = "", ""
    for i, c in enumerate(s["centers"]):
        sel = "true" if i == 0 else "false"
        tab_btns += f'<button role="tab" aria-selected="{sel}">{c["name"]}</button>'
        secs = "".join(f"<h3>{h}</h3><p>{b}</p>" for h, b in c["sections"])
        contact = ""
        if c["contact"]:
            name, addr, kind = c["contact"]
            link = (f'<a href="mailto:{addr}">{addr}</a>' if kind == "email"
                    else f'<a href="tel:{addr.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")}">{addr}</a>')
            contact = f'<div class="lead-card"><div><b>{name}</b>{link}</div></div>'
        partners = f'<p class="partnerline"><b>Serving alongside:</b> {c["partners"]}</p>' if c["partners"] else ""
        active = " active" if i == 0 else ""
        tab_panels += f'<div class="tabs__panel{active}" role="tabpanel">{secs}{contact}{partners}</div>'

    prev_s = STATES[(idx - 1) % len(STATES)]
    next_s = STATES[(idx + 1) % len(STATES)]

    body = page_header(
        '<a href="/our-work/united-states/">Where We Serve</a> &middot; United States',
        s["name"],
        s["hero"],
    ) + f"""
{gallery}

<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Constantly Serving Communities</h2>
    <div data-tabs class="mt-6 reveal">
      <div class="tabs__list" role="tablist">{tab_btns}</div>
      {tab_panels}
    </div>
  </div>
</section>

{flat_cta(f'Serve with us in {s["name"]}.', "Reach out to your local SRLC leaders, or sign up and your chapter coordinator will be in touch.", "Volunteer With Us", "/get-involved/volunteer/", ("Ways to Give", "/donate/"))}

<section class="pagenav-strip">
  <div class="container">
    <a href="/our-work/united-states/{prev_s["slug"]}/">&larr; {prev_s["name"]}</a>
    <a href="/our-work/united-states/">All states</a>
    <a href="/our-work/united-states/{next_s["slug"]}/">{next_s["name"]} &rarr;</a>
  </div>
</section>
"""
    return page(s["meta_title"], s["meta_desc"], f'/our-work/united-states/{s["slug"]}/', body)


def render_tencare_hub():
    chips = '<div class="chip-row reveal">' + "".join(
        f'<a href="#{c["slug"]}"><img src="/assets/img/care-icons/{c["icon"]}" alt="" width="20" height="20" style="height:20px;width:auto;vertical-align:-4px;margin-right:5px">{c["num"]} {c["name"]}</a>'
        for c in CARES) + "</div>"
    rail_dots = "".join(f'<a href="#{c["slug"]}" aria-label="{c["name"]}"></a>' for c in CARES)
    panels = ""
    for c in CARES:
        stat = ""
        if c["stat"]:
            stat = f'<div class="carepanel__stat"><div class="n count-up">{c["stat"][0]}</div><div class="l">{c["stat"][1]}</div></div>'
        panels += f"""<section class="carepanel" id="{c["slug"]}">
  <div class="carepanel__num" aria-hidden="true">{c["num"]}</div>
  <div class="container">
    <div class="carepanel__body">
      <img class="care-icon reveal" src="/assets/img/care-icons/{c["icon"]}" alt="" width="52" height="52">
      <h2 class="reveal">{c["name"]}</h2>
      <p class="vu-lead reveal" data-stagger="1" style="max-width:none">{c["one"]}</p>
      {stat}
      <div class="mt-6 reveal" data-stagger="2"><a class="btn btn--secondary" href="/our-work/10-care-program/{c["slug"]}/">Explore {c["name"]}</a></div>
    </div>
  </div>
</section>"""

    body = page_header(
        "Our Work",
        "10 Care Program",
        TEN_CARE_INTRO,
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--narrow">
  <div class="container">{chips}</div>
</section>
<nav class="progressrail" aria-label="Care programs">{rail_dots}</nav>
{panels}
{flat_cta("Every Care welcomes support.", "Your gift and your hours both count.", "Support the 10 Care Program", "/donate/", ("Volunteer", "/get-involved/volunteer/"))}
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
            inner = f"<h3>{name}</h3><p>{desc}</p>"
            if href:
                cells += f'<a class="cause-card reveal" href="{href}" style="display:block;text-decoration:none;color:inherit">{inner}<span class="card__cta">Visit the institute</span></a>'
            else:
                cells += f'<div class="cause-card reveal">{inner}</div>'
        cards = f'<div class="card-grid mt-6">{cells}</div>'

    us = ""
    if c["us"]:
        us = f"""<section class="vu-shell vu-shell--cream">
  <div class="container">
    <div class="vu-split vu-split--reverse">
      <div class="vu-split__copy">
        <h3>In the United States</h3>
        <p>{c["us"]}</p>
      </div>
      <div class="vu-split__photo">{ph(c["us_img"])}</div>
    </div>
  </div>
</section>"""

    story = ""
    if c["story"]:
        h, b = c["story"]
        story = f"""<section class="vu-shell vu-shell--lav vu-shell--narrow">
  <div class="container">
    <div class="vu-card vu-card--accent reveal" style="grid-template-columns:1fr">
      <h3 class="vu-card__h" style="grid-column:1">{h}</h3>
      <div class="vu-card__body"><p>{b}</p></div>
    </div>
  </div>
</section>"""

    impact = ""
    if c["stat"]:
        impact = f"""<section class="vu-shell vu-shell--purple vu-shell--narrow">
  <div class="container text-center">
    <p class="impact-stat__n count-up" style="color:var(--color-warm-orange);font-size:clamp(2.4rem,5.5vw,3.6rem);margin:0 0 .3rem">{c["stat"][0]}</p>
    <p style="color:#E8DDF2;margin:0">{c["stat"][1]}</p>
  </div>
</section>"""

    body = page_header(
        f'<a href="/our-work/10-care-program/">10 Care Program</a> &middot; {c["num"]}',
        c["name"],
        c["opening"],
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h3>The Work in India</h3>
        <p>{c["india"]}</p>
      </div>
      <div class="vu-split__photo">{ph(c["hero_img"])}</div>
    </div>
    {cards}
  </div>
</section>
{us}
{story}
{impact}
{flat_cta(f'{c["name"]} continues with you.', "Your employer may match your gift. Check if your company participates.", c["cta"], "/donate/")}
"""
    return page(c["title"], c["desc"], f'/our-work/10-care-program/{c["slug"]}/', body)


def render_india_hub():
    """Rebuilt like the 10 Care concept: small header, intro, jump grid of six
    institutes, one full-screen scroll panel per institute. Reduced motion
    collapses to a stacked list via the shared .carepanel media queries."""
    chips = '<div class="chip-row reveal">' + "".join(
        f'<a href="#{inst["slug"]}">{inst["name"]}</a>' for inst in INSTITUTES) + "</div>"
    rail_dots = "".join(f'<a href="#{inst["slug"]}" aria-label="{inst["name"]}"></a>' for inst in INSTITUTES)
    panels = ""
    for i, inst in enumerate(INSTITUTES, start=1):
        panels += f"""<section class="carepanel" id="{inst["slug"]}">
  <div class="carepanel__num" aria-hidden="true">{i:02d}</div>
  <div class="container">
    <div class="carepanel__body">
      <p class="vu-eyebrow" style="display:inline-flex">{inst["tag"]}</p>
      <h2 class="reveal">{inst["name"]}</h2>
      <p class="vu-lead reveal" data-stagger="1" style="max-width:none">{inst["desc"]}</p>
      <div class="mt-6 reveal" data-stagger="2"><a class="btn btn--secondary" href="/our-work/india/{inst["slug"]}/">Visit the institute</a></div>
    </div>
  </div>
</section>"""

    body = page_header(
        "Our Work &middot; Where We Serve",
        "Our Institutes in India",
        INDIA_INTRO,
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--narrow">
  <div class="container">{chips}</div>
</section>
<nav class="progressrail" aria-label="Institutes">{rail_dots}</nav>
{panels}
{flat_cta("Institutes built to serve for generations.", "Every institute welcomes support from across the world.", "Support Our Institutes", "/donate/")}
"""
    return page(
        "Our Institutes in India | SRLC USA",
        "Six permanent institutes in India: a hospital, schools, skill training, women's livelihoods, and animal care. See the work. SRLC USA.",
        "/our-work/india/", body)


def peer_cards(current_slug):
    cells = "".join(
        f'<a class="cause-card reveal" href="/our-work/india/{i["slug"]}/" style="display:block;text-decoration:none;color:inherit"><h3 style="font-size:1.05rem">{i["name"]}</h3><p style="margin:0;font-size:.9rem;color:var(--color-ink-muted)">{i["tag"]}</p></a>'
        for i in INSTITUTES if i["slug"] != current_slug)
    return f"""<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">More Institutes in India</h2>
    <div class="card-grid mt-6">{cells}</div>
    <p class="mt-6"><a href="/our-work/india/">Our Institutes in India</a></p>
  </div>
</section>"""


def render_institute(inst):
    """Spec-pattern institute page (Document C): hero with the selected intro
    sentence, description slot (empty where the approved description is
    pending), peer-institute exit path. Blocking sections stay out."""
    desc_section = ""
    if inst.get("desc_full"):
        desc_section = f"""<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h3>What This Institution Does</h3>
        <p class="vu-lead--xl" style="margin-top:0">{inst["desc"]}</p>
        {"<p>" + inst["extra"] + "</p>" if inst.get("extra") else ""}
      </div>
      <div class="vu-split__photo">{ph(inst["img"])}</div>
    </div>
  </div>
</section>"""
    else:
        desc_section = f"""<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h3>What This Institution Does</h3>
        {ph("Approved description pending. Placed verbatim once supplied.", style="min-height:140px")}
      </div>
      <div class="vu-split__photo">{ph(inst["img"])}</div>
    </div>
  </div>
</section>"""

    body = page_header(
        '<a href="/our-work/india/">Our Institutes in India</a>',
        inst["name"],
        inst["intro"],
        cta=f'<a class="btn btn--primary" href="/donate/">{inst.get("cta", "Give to This Work")}</a>',
    ) + f"""
{desc_section}
{peer_cards(inst["slug"])}
{flat_cta("Ways to Support", "", inst.get("cta", "Give to This Work"), "/donate/")}
"""
    return page(inst["meta_title"], inst["meta_desc"], f'/our-work/india/{inst["slug"]}/', body)


def render_vidyapeeth():
    programs = "".join(
        f'<div class="cause-card reveal" data-stagger="{i % 4 + 1}"><h3>{n}</h3><p>{d}</p></div>'
        for i, (n, d) in enumerate(SRV["programs"]))
    pillars = "".join(
        f'<div class="cause-card reveal" data-stagger="{i + 1}"><h3>{n}</h3><p>{d}</p></div>'
        for i, (n, d) in enumerate(SRV["pillars"]))
    need = "".join(f"<p>{p}</p>" for p in SRV["need"])
    body = page_header(
        '<a href="/our-work/india/">Our Institutes in India</a> &middot; Science College',
        SRV["h1"],
        SRV["sub"],
        cta=f'<a class="btn btn--primary" href="/donate/">{SRV["cta"]}</a>',
    ) + trust_bar() + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h3>{SRV["need_h2"]}</h3>
        {need}
      </div>
      <div class="vu-split__photo">{ph("The Dharampur region: fields, village roads, the terrain between communities and the nearest city. Media Bank.")}</div>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">{SRV["programs_h2"]}</h2>
    <p class="vu-lead">{SRV["programs_intro"]}</p>
    <div class="card-grid mt-6">{programs}</div>
    <p class="mt-8 maxw-70">{SRV["support_intro"]}</p>
    <div class="card-grid mt-6">{pillars}</div>
  </div>
</section>

<section class="vu-shell vu-shell--purple vu-shell--narrow">
  <div class="container text-center">
    <h2 class="vu-h reveal" style="color:#fff">{SRV["impact_h2"]}</h2>
    <div style="display:flex;justify-content:center;gap:clamp(2rem,8vw,6rem);flex-wrap:wrap;margin-top:1.4rem">
      {"".join(f'<div class="reveal" data-stagger="{i + 1}"><p class="impact-stat__n count-up" style="color:var(--color-warm-orange);margin:0 0 .3rem">{n}</p><p style="color:#E8DDF2;margin:0;max-width:24ch">{l}</p></div>' for i, (n, l) in enumerate(SRV["impact"]))}
    </div>
  </div>
</section>
{peer_cards("vidyapeeth")}
{flat_cta(SRV["close_h2"], SRV["close"], SRV["cta"])}
"""
    return page(SRV["title"], SRV["desc"], "/our-work/india/vidyapeeth/", body)


def render_africa():
    body = page_header(
        "Our Work &middot; Where We Serve",
        "Mission Africa",
        "Mission Africa brings doctors, medicine, and follow-up care to communities where the nearest clinic can be hours away, at no cost to patients. We work with local health workers and community partners across 16 countries in Africa.",
        cta='<a class="btn btn--primary" href="/donate/">Stand With Mission Africa</a>',
    ) + trust_bar() + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-split">
      <div class="vu-split__copy">
        <h3>Distance should not decide who gets care</h3>
        <p>In much of the region Mission Africa serves, the barrier to health is not the treatment. It is the miles between a family and anyone who can provide it, the distance where a curable illness quietly becomes a permanent one. Launched in 2024 by Shrimad Rajchandra Love and Care (SRLC), Mission Africa now works across 16 countries in Africa to close that distance.</p>
        <div style="display:flex;gap:clamp(1.6rem,5vw,3.4rem);flex-wrap:wrap;margin-top:1.2rem">
          <div><p class="impact-stat__n count-up" style="margin:0 0 .3rem">16</p><p style="margin:0;font-size:.92rem;color:var(--color-ink-muted)">countries reached</p></div>
          <div><p class="impact-stat__n count-up" style="margin:0 0 .3rem">7,500+</p><p style="margin:0;font-size:.92rem;color:var(--color-ink-muted);max-width:26ch">patients treated at a free eye and ENT medical camp in Nairobi, Kenya</p></div>
        </div>
      </div>
      <div class="vu-split__photo">{ph("A patient queue that reads as order and hope, morning light. Mission Africa team photos pending with consent records.")}</div>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">A clinic that comes to you</h2>
    <p class="vu-lead">Mission Africa brings the full spectrum of care to the community. Full medical camps staged inside the community, with doctors, diagnostics, and medicine in one place, free to every patient who walks in. And when the camp packs up, the care does not leave. Community programs carry it between visits.</p>
    <div class="vu-pair-grid mt-6">
      <div class="vu-card reveal" style="grid-template-columns:1fr"><h3 class="vu-card__h">Healthcare access</h3><div class="vu-card__body"><p>Medical camps, medicine placed directly into waiting hands, and training for community health workers, so care remains long after the visiting doctors have gone.</p></div></div>
      <div class="vu-card reveal" data-stagger="1" style="grid-template-columns:1fr"><h3 class="vu-card__h">Community development</h3><div class="vu-card__body"><p>Education, nutrition, and livelihood programs built with local communities rather than for them, so the change outlasts the camp.</p></div></div>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container container--narrow" style="max-width:820px">
    <h2 class="vu-h reveal">Proven far from here</h2>
    <p>Mission Africa did not start from zero and your gift does not land on an experiment. It extends a healthcare model refined over decades in Dharampur, India, where a 250-bed hospital accredited by the National Accreditation Board for Hospitals and Healthcare Providers (NABH) treats patients regardless of their ability to pay. The movement behind it has touched 33M+ lives globally, and volunteers across the United States help fund and power the work.</p>
    <div class="vu-toc--inline">
      <a href="/our-work/10-care-program/">Our Causes</a>
      <a href="/our-work/india/">India</a>
      <a href="/our-work/united-states/">United States</a>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--cream vu-shell--narrow">
  <div class="container">
    <div class="fc-newsletter reveal">
      <div class="fc-newsletter__copy">
        <h3>Stay close to the work</h3>
        <p>Camps are episodic; your connection to them does not have to be. Leave your email and we will send you what your support built: photos with consent, numbers with verification, and the occasional story worth your inbox.</p>
      </div>
      <form class="fc-newsletter__form" name="updates" method="POST" data-netlify="true" data-netlify-inline netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="updates">
        <input type="hidden" name="source" value="mission-africa">
        <p class="hp-field"><input name="bot-field" tabindex="-1"></p>
        <input type="email" name="email" required placeholder="you@example.com" aria-label="Email address" class="form-hidewrap">
        <button type="submit" class="btn btn--primary form-hidewrap">Get Camp Updates</button>
        <span class="form-success" style="color:var(--color-srlc-purple);font-weight:600">Thank you. You are on the list.</span>
      </form>
    </div>
  </div>
</section>

{flat_cta("Help the next camp happen", "Somewhere right now, a mother is measuring the distance between her child and a doctor. Your gift shortens it. Put medicine on the road, and hope alongside it.", "Stand With Mission Africa")}
"""
    return page(
        "Mission Africa | Free Medical Camps | SRLC USA",
        "Doctors, medicine, and follow-up care reach 16 African nations through Mission Africa. Send care the last mile. SRLC USA, a 501(c)(3) nonprofit.",
        "/our-work/mission-africa/", body)
