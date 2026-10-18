"""Renderers: Our Work — flat pass. Copy verbatim from the master doc tabs.
Per-state stat bands are omitted (CLAUDE.md banned list) and flagged in the
build log. End-of-page CTAs render as flat sections, never banners."""
from shell import (page, ph, page_header, flat_cta, filler, filler_entry, story_split, photo_alt, photo,
                   img_tag, pick_distinct, photo_src_tag, pinned)
from data_media import slot
from data_states import STATES, CAMPAIGNS, US_HERO_BODY
from data_naman import CARE_TILES
from data_cares import CARES, TEN_CARE_INTRO
from data_india import INSTITUTES, INDIA_INTRO, SRV


# Filler photo subject per page (shell.filler picks a local /assets/img/fillers
# photo deterministically for a key + tag). Header bands and hub panels only.
CARE_TAGS = {
    "health-care": "hospital", "educational-care": "classroom", "child-care": "children",
    "woman-care": "women", "tribal-care": "nature", "community-care": "community",
    "humanitarian-care": "hands", "animal-care": "animals", "environmental-care": "nature",
    "emergency-relief-care": "hands",
}
# Media Bank routes per Care: the Care's own tag first, then close relatives.
CARE_ROUTE = {
    "health-care": ["health-care", "hospital"],
    "educational-care": ["educational-care", "gurukul", "vidyapeeth"],
    "child-care": ["child-care", "educational-care"],
    "woman-care": ["woman-care", "coew"],
    "tribal-care": ["tribal-care", "health-care+india"],
    "community-care": ["community-care", "us-community"],
    "humanitarian-care": ["humanitarian-care", "global"],
    "animal-care": ["animal-care", "jivamaitridham"],
    "environmental-care": ["environmental-care", "us-environment"],
    "emergency-relief-care": ["emergency-relief-care", "humanitarian-care"],
}


# US photo per Care: matched on subject (description keywords) so a Care page
# never borrows a gala hall or a back-to-school table that belongs elsewhere.
CARE_US_ROUTE = {
    "health-care": ["us+alt:hygiene", "us+alt:health", "us+alt:medical", "us+alt:hospital"],
    "educational-care": ["us-classroom-of-change+us", "us+alt:school"],
    "child-care": ["us+alt:children", "us+alt:kids", "us-classroom-of-change+us"],
    "woman-care": ["us+alt:women", "us+alt:mother"],
    "tribal-care": ["us-community+us"],
    "community-care": ["us+alt:ice cream truck", "us+alt:serve food", "us-community+us", "us+alt:senior"],
    "humanitarian-care": ["us-food+us", "us+alt:shelter", "us+alt:meal"],
    "animal-care": ["us+alt:animal", "us+alt:cow", "us+alt:farm"],
    "environmental-care": ["us-environment+us", "us+alt:tree", "us+alt:litter", "us+alt:clean"],
    "emergency-relief-care": ["us+alt:fire", "us+alt:relief", "emergency-relief-care+us"],
}


# Description keywords that keep a Care's India photo on subject when the
# Care has no India-tagged photos left.
CARE_KEYWORDS = {
    "health-care": ["doctor", "patient", "medical"], "educational-care": ["student", "school", "class"],
    "child-care": ["child", "children"], "woman-care": ["woman", "women"], "tribal-care": ["village"],
    "community-care": ["awareness", "donation drive", "volunteers at"], "humanitarian-care": ["food", "meal", "distribut"],
    "animal-care": ["animal", "cow", "dog", "cat"], "environmental-care": ["sapling", "tree planting", "solar", "water conservation"],
    "emergency-relief-care": ["relief", "flood", "cyclone", "earthquake"],
}


# Cares whose India photos are thin get a strict route: no photo beats an
# off-subject one.
CARE_INDIA_ROUTE = {
    # organ donation, prison programs and village development: nothing on-subject in the bank yet, so text only
    "community-care": ["india+alt:organ donation", "india+alt:prison", "india+alt:pledge"],
    "environmental-care": ["environmental-care+india", "india+alt:sapling", "india+alt:tree planting"],
    "emergency-relief-care": ["emergency-relief-care+india", "india+alt:flood", "india+alt:relief kit"],
}


# Horizontal focal point for wide Care photos cut into portrait tiles and
# phone heroes, so the faces stay in frame.
FOCAL = {"/assets/img/mb/mb-208.webp": "72%", "/assets/img/mb/mb-433.webp": "88%", "/assets/img/mb/mb-92.webp": "35%",
         "/assets/img/mb/mb-432.webp": "20%"}


# US photos that must not drift with render order (a state page can claim them first)
CARE_US_PIN = {"community-care": 627, "environmental-care": 543}  # cleanups, matching each Care's US copy


def care_photo(c, min_w=1600):
    """Hero-grade photo for a Care: the curated care-<slug> pick, else its route."""
    return slot(f"care-{c['slug']}") or photo(f"care-{c['slug']}", CARE_ROUTE[c["slug"]], CARE_TAGS[c["slug"]], min_w=min_w)


INSTITUTE_TAGS = {
    "hospital-and-research-center": "hospital", "vidyapeeth": "classroom", "gurukul": "children",
    "skill-development-center": "skills", "jivamaitridham": "animals",
    "center-of-excellence-for-women": "women",
}


def jump_strip(items, aria):
    """Slim sticky strip of section names: no boxes, numbers, or icons.
    Sticks beneath the site header (offset measured in supplement-work.js)."""
    lis = "".join(f'<li><a href="#{slug}">{name}</a></li>' for slug, name in items)
    return f"""<nav class="jumpstrip" aria-label="{aria}">
  <div class="container"><ul class="jumpstrip__list">{lis}</ul></div>
</nav>"""


def photo_panel(slug, key, tag, inner, eager=False):
    """Full-bleed scroll panel with a real filler photo and a flat dark scrim."""
    src, _, w, h = filler_entry(key, tag)
    loading = "eager" if eager else "lazy"
    return f"""<section class="carepanel carepanel--photo" id="{slug}">
  <img class="carepanel__bg" src="{src}" alt="" width="{w}" height="{h}" loading="{loading}" decoding="async">
  <div class="carepanel__scrim" aria-hidden="true"></div>
  <div class="container">
    <div class="carepanel__body">{inner}</div>
  </div>
</section>"""



# One marker per state (Naman's reference). Coordinates in the 959x593 viewBox,
# labels for the NE cluster stack right of the map via leader lines.
ED_MARKERS = [
    ("Washington", "washington", 105, 48, "right"),
    ("California", "california", 68, 300, "right"),
    ("Arizona", "arizona", 192, 362, "right"),
    ("Texas", "texas", 400, 440, "right"),
    ("Illinois", "illinois", 610, 215, "right"),
    ("Indiana", "indiana", 644, 255, "right"),
    ("Georgia", "georgia", 700, 385, "right"),
    ("Massachusetts", "massachusetts", 886, 158, "stack"),
    ("New York", "new-york", 852, 185, "stack"),
    ("Pennsylvania", "pennsylvania", 790, 208, "stack"),
    ("New Jersey", "new-jersey", 836, 215, "stack"),
    ("Washington, D.C.", "washington-dc", 802, 252, "stack"),
]


def editorial_map(svg_inner):
    stack = [m for m in ED_MARKERS if m[4] == "stack"]
    stack_x = 1005
    stack_y0, stack_dy = 150, 27
    marks = []
    for name, slug, x, y, mode in ED_MARKERS:
        href = f"/our-work/united-states/{slug}/"
        marks.append(f'<circle class="edmap-ring" cx="{x}" cy="{y}" r="8"></circle>')
        marks.append(f'<circle class="edmap-dot" cx="{x}" cy="{y}" r="4.5" data-href="{href}" tabindex="0" role="link" aria-label="{name}"><title>{name}</title></circle>')
        if mode == "right":
            marks.append(f'<text class="edmap-label" x="{x + 14}" y="{y + 4}">{name}</text>')
    for i, (name, slug, x, y, mode) in enumerate(stack):
        ly = stack_y0 + i * stack_dy
        marks.append(f'<path class="edmap-leader" d="M {x + 6} {y} L {stack_x - 12} {ly - 4}"></path>')
        marks.append(f'<text class="edmap-label edmap-label--side" x="{stack_x}" y="{ly}">{name}</text>')
    chapters = "".join(f'<li><a href="/our-work/united-states/{slug}/">{name}</a></li>'
                       for name, slug, *_ in sorted(ED_MARKERS))
    return f"""<div class="edmap reveal">
  <svg viewBox="0 0 1180 593" xmlns="http://www.w3.org/2000/svg" aria-label="Editorial map of SRLC USA chapters" preserveAspectRatio="xMidYMid meet">
    <g>{svg_inner}</g>
    <g>{"".join(marks)}</g>
  </svg>
  <ul class="edmap-list" aria-label="SRLC USA chapter states">{chapters}</ul>
</div>"""


def cf_map(svg_inner, aria="Map of the United States highlighting SRLC chapter states"):
    return f"""<div class="cf-map reveal">
  <svg viewBox="0 0 959 593" xmlns="http://www.w3.org/2000/svg" class="cf-map__svg" aria-label="{aria}" preserveAspectRatio="xMidYMid meet">{svg_inner}</svg>
</div>
<div class="cf-map__legend" aria-hidden="true"><span><span class="swatch"></span>Active SRLC USA chapter</span></div>"""


def state_chips():
    return '<div class="chip-row reveal">' + "".join(
        f'<a href="/our-work/united-states/{s["slug"]}/" data-state-target="{s["svg"].lower()}">{s["name"]}</a>'
        for s in STATES) + "</div>"


# Media Bank number and crop per campaign
CAMPAIGN_PHOTO = {
    "Classroom of Change": (307, "50% 50%"),
    "Giving Tuesday": (305, "50% 50%"),
    "Meals of Love and Care": (355, "50% 50%"),
}


def render_us_hub(svg_inner):
    campaigns = ""
    for i, c in enumerate(CAMPAIGNS):
        split_cls = "vu-split" if i % 2 == 0 else "vu-split vu-split--reverse"
        n, pos = CAMPAIGN_PHOTO[c["name"]]
        img = img_tag(pinned(n), pos=pos)
        campaigns += f"""<div class="{split_cls} reveal" id="{c["name"].lower().replace(" ", "-")}">
      <div class="vu-split__copy">
        <h3>{c["name"]}</h3>
        <p>{c["body"].replace("Title 1", "Title&nbsp;1")}</p>
        <a class="btn btn--secondary" href="/donate/">{c["cta"]}</a>
      </div>
      <div class="vu-split__photo">{img}</div>
    </div>"""

    body = page_header(
        "Our Work &middot; Where We Serve",
        "SRLC&rsquo;s Nationwide Presence",
        US_HERO_BODY,
        image=filler("United States", "community"),
    ) + f"""
<section class="edmap-section vu-shell vu-shell--first" id="chapters">
  <div class="container">
    <div class="edmap-head">
      <p class="edmap-kicker">Chapter Network</p>
      <h2 class="edmap-title">SRLC USA Chapters</h2>
      <p class="edmap-meta">Chapters in 11 states and Washington, D.C. &middot; One mission</p>
    </div>
    {editorial_map(svg_inner)}
    <div class="zipline">
      <label for="zipInput">Find your chapter</label>
      <form class="chapter-finder__form" style="display:flex;gap:.6rem" onsubmit="event.preventDefault(); window.__cfZipLookup &amp;&amp; window.__cfZipLookup();">
        <input type="text" id="zipInput" inputmode="numeric" maxlength="5" placeholder="ZIP code" aria-label="ZIP code" pattern="\\d{{5}}">
        <button type="submit" class="btn btn--secondary" id="zipBtn" style="padding:.55rem 1.1rem">Find Chapter</button>
      </form>
    </div>
    <div class="chapter-finder__result" id="zipResult" hidden style="max-width:34rem;margin-top:1rem;background:#fff;border:1px solid #E2D9EF;border-radius:4px;padding:1rem 1.2rem">
      <p class="chapter-finder__city" id="zipCity" style="font-family:var(--font-display);font-weight:600;font-size:1.2rem;margin:0 0 .3rem;color:#693D84"></p>
      <p class="chapter-finder__meta" id="zipMeta" style="margin:0 0 .8rem;font-size:.92rem;color:#3D2F47"></p>
      <div class="chapter-finder__actions" style="display:flex;gap:.5rem;flex-wrap:wrap">
        <a id="zipJoinBtn" class="btn btn--primary" href="/get-involved/volunteer/">Join This Chapter</a>
      </div>
      <div class="chapter-finder__chips" id="zipChips" hidden style="margin-top:.8rem">
        <p class="chapter-finder__chips-label" style="font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:#693D84;margin:0 0 .4rem">Centers in this chapter</p>
        <div class="chapter-finder__chips-list" id="zipChipsList" style="display:flex;flex-wrap:wrap;gap:.45rem"></div>
      </div>
    </div>
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
    # Shared state template (Naman, Oct 16: one layout replicated to all twelve).
    # Photos come only from the state's own shoots; a state with fewer than two
    # gets no gallery rather than another chapter's pictures.
    route = [f"state-{s['slug']}", "us-community+us", "volunteers+us", "us-food", "us-events"]
    hero = slot(f"state-{s['slug']}-hero") or photo(f"state-{s['slug']}-hero", route, "community", min_w=1600)
    gal = pick_distinct(f"state-{s['slug']}-gallery", f"state-{s['slug']}", 3, [photo_src_tag(hero[0])])
    gallery = ""
    if len(gal) < 2:
        # one shoot for the whole state: a single wide band from it rather than nothing
        band = gal[0][:1] + gal[0][2:] if gal else photo(f"state-{s['slug']}-band", [f"state-{s['slug']}"], "community", min_w=1200, strict=True)
        if band and band[0] != hero[0]:
            gallery = f"""<section class="stategal" aria-label="{s["name"]} chapter photo">
  <div class="container"><div class="stategal__grid stategal__grid--1">{img_tag(band)}</div></div>
</section>"""
    else:
        imgs = "".join(img_tag((p[0], p[2], p[3], p[4])) for p in gal)
        gallery = f"""<section class="stategal" aria-label="{s["name"]} chapter photos">
  <div class="container"><div class="stategal__grid stategal__grid--{len(gal)}">{imgs}</div></div>
</section>"""

    multi = len(s["centers"]) > 1
    tab_btns, tab_panels = "", ""
    for i, c in enumerate(s["centers"]):
        sel = "true" if i == 0 else "false"
        tab_btns += (f'<button role="tab" id="tab-{s["slug"]}-{i}" aria-controls="panel-{s["slug"]}-{i}" '
                     f'aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{c["name"]}</button>')
        secs = "".join(f"<h3>{h}</h3><p>{b}</p>" for h, b in c["sections"])
        contact = ""
        if c["contact"]:
            name, addr, kind = c["contact"]
            link = (f'<a href="mailto:{addr}">{addr}</a>' if kind == "email"
                    else f'<a href="tel:{addr.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")}">{addr}</a>')
            contact = f'<div class="lead-card"><div><b>{name}</b>{link}</div></div>'
        partners = f'<p class="partnerline"><b>Serving alongside:</b> {c["partners"]}</p>' if c["partners"] else ""
        active = " active" if i == 0 else ""
        tab_panels += (f'<div class="tabs__panel{active}" role="tabpanel" id="panel-{s["slug"]}-{i}" '
                       f'aria-labelledby="tab-{s["slug"]}-{i}">{secs}{contact}{partners}</div>')
    tabs = (f'<div data-tabs class="mt-6"><div class="tabs__list" role="tablist">{tab_btns}</div>{tab_panels}</div>'
            if multi else f'<div class="mt-6 state-single">{tab_panels}</div>')

    prev_s = STATES[(idx - 1) % len(STATES)]
    next_s = STATES[(idx + 1) % len(STATES)]
    body = page_header(
        'Where We Serve &middot; <a href="/our-work/united-states/">United States</a>',
        s["name"],
        image=hero[0], size=(hero[1], hero[2]), alt=hero[3], focal=FOCAL.get(hero[0], ""),
    ) + f"""
<section class="leadsec" aria-label="About {s["name"]}">
  <div class="container"><p class="leadsec__lead">{s["hero"]}</p></div>
</section>
{gallery}
<section class="statework" aria-labelledby="state-work-h">
  <div class="container">
    <h2 class="statework__h" id="state-work-h">Constantly Serving Communities</h2>
    {tabs}
  </div>
</section>
<section class="statecta" aria-labelledby="state-cta-h">
  <div class="container">
    <h2 class="statecta__h" id="state-cta-h">Serve with us in {s["name"].rstrip(".")}.</h2>
    <p class="statecta__p">Reach out to your local SRLC leaders, or sign up and your chapter coordinator will be in touch.</p>
    <p class="statecta__actions"><a class="btn btn--primary" href="/get-involved/volunteer/">Volunteer With Us</a><a class="btn btn--secondary" href="/donate/">Ways to Give</a></p>
    <nav class="statenav" aria-label="More states">
      <a href="/our-work/united-states/{prev_s["slug"]}/">&larr; {prev_s["name"]}</a>
      <a href="/our-work/united-states/">All states</a>
      <a href="/our-work/united-states/{next_s["slug"]}/">{next_s["name"]} &rarr;</a>
    </nav>
  </div>
</section>
"""
    return page(s["meta_title"], s["meta_desc"], f'/our-work/united-states/{s["slug"]}/', body)


def render_tencare_hub():
    """Hero, the tab's intro as its own section, then the ten Cares as photo
    tiles in the homepage grid (no numbers, no icons; one-liner on hover,
    accordion rows below 1024). Each tile links to its Care page."""
    tiles = "".join(f"""<a class="caretile caretile--hub" href="/our-work/10-care-program/{c["slug"]}/" style="background-image:url('{CARE_TILES[c["slug"]]}')">
        <span class="caretile__overlay" aria-hidden="true"></span>
        <span class="caretile__chip"><span class="caretile__name">{c["name"]}</span></span>
        <span class="caretile__hover"><span class="caretile__hover-h">{c["name"]}</span><span class="caretile__hover-p">{c["one"]}</span><span class="caretile__more">Explore {c["name"]}<span aria-hidden="true">&rarr;</span></span></span>
      </a>""" for c in CARES)
    # a volunteer group at work, not one Care's subject (the sanctuary echoed the Animal Care tile)
    hero = pinned(334) or photo("10 Care Program hero", ["volunteers+india", "community-care+india", "educational-care+india"], "community", min_w=1600)
    body = page_header("Our Work", "10 Care Program", image=hero[0], size=(hero[1], hero[2]), alt=hero[3], pos="50% 14%") + f"""
<section class="care-section care-section--hub" aria-label="The ten Cares">
  <div class="container">
    <p class="leadsec__lead">{TEN_CARE_INTRO}</p>
    <div class="caregrid">{tiles}</div>
  </div>
</section>
<section class="pagenext">
  <div class="container pagenext__inner">
    <h2 class="pagenext__line">Continue Reading</h2>
    <div class="pagenext__links">
      <a class="btn btn--secondary" href="/our-work/united-states/">United States</a>
      <a class="btn btn--secondary" href="/our-work/india/">India</a>
      <a class="btn btn--secondary" href="/our-work/mission-africa/">Mission Africa</a>
    </div>
  </div>
</section>
"""
    return page(
        "The 10 Care Program | Ten Ways to Care | SRLC USA",
        "Ten areas of service, one promise: care for every life. Explore the 10 Care Program, from Health Care to Emergency Relief Care. SRLC USA.",
        "/our-work/10-care-program/", body)


def render_care(c):
    # One template for all ten (Naman, Oct 16): why it matters, the work in
    # India, the work in the US, one named story, your gift. Copy verbatim from
    # each Care tab; the FINANCE-PENDING dollar line stays out until finance rules.
    hero_src, hero_w, hero_h, hero_alt = care_photo(c)
    route = CARE_ROUTE[c["slug"]]
    india_route = CARE_INDIA_ROUTE.get(c["slug"]) or (
        [f"{t}+india" for t in route] + [f"india+alt:{k}" for k in CARE_KEYWORDS[c["slug"]]])
    india_img = photo(f"{c['slug']}-india", india_route, CARE_TAGS[c["slug"]], min_w=1200, strict=True)
    programs = ""
    if c["cards"]:
        rows = "".join(
            f'<li class="proglist__item"><h3 class="proglist__h">{name}</h3><p class="proglist__d">{desc}</p>'
            + (f'<a class="textlink" href="{href}">Visit the institute<span aria-hidden="true"> &rarr;</span></a>' if href else "")
            + "</li>"
            for name, desc, href in c["cards"])
        programs = f'<div class="container"><ul class="proglist">{rows}</ul></div>'

    us = ""
    if c["us"]:
        us_img = (pinned(CARE_US_PIN[c["slug"]]) if c["slug"] in CARE_US_PIN
                  else photo(f"{c['slug']}-us", CARE_US_ROUTE[c["slug"]] + ["volunteers+us"], "community", min_w=1200))
        us = story_split("In the United States", [c["us"]], us_img, reverse=True, tone="white")

    story = ""
    if c["story"]:
        h, b = c["story"]
        story = f"""<section class="storyband" aria-labelledby="story-h">
  <div class="container storyband__inner">
    <p class="storyband__eyebrow">Story</p>
    <h2 class="storyband__h" id="story-h">{h}</h2>
    <p class="storyband__body">{b}</p>
  </div>
</section>"""

    body = page_header(
        '<a href="/our-work/10-care-program/">10 Care Program</a>',
        c["name"], image=hero_src, size=(hero_w, hero_h), alt=hero_alt, focal=FOCAL.get(hero_src, ""),
    ) + f"""
<section class="leadsec" aria-labelledby="why-h">
  <div class="container">
    <h2 class="leadsec__eyebrow" id="why-h">Why It Matters</h2>
    <p class="leadsec__lead">{c["opening"]}</p>
  </div>
</section>
<div class="caresec caresec--india">
{story_split("The Work in India", [c["india"]], india_img, tone="lav")}
{programs}
</div>
{us}
{story}
<section class="giftsec" aria-labelledby="gift-h">
  <div class="container giftsec__inner">
    <h2 class="giftsec__h" id="gift-h">Your Gift</h2>
    <a class="btn btn--primary" href="/donate/">{c["cta"]}</a>
  </div>
</section>
"""
    return page(c["title"], c["desc"], f'/our-work/10-care-program/{c["slug"]}/', body)


INST_SLOTS = {
    "hospital-and-research-center": "inst-hospital", "vidyapeeth": "inst-vidyapeeth",
    "gurukul": "inst-gurukul", "skill-development-center": "inst-skills",
    "jivamaitridham": "inst-jivamaitridham", "center-of-excellence-for-women": "inst-coew",
}


INST_TAG = {
    "hospital-and-research-center": "hospital", "vidyapeeth": "vidyapeeth", "gurukul": "gurukul",
    "skill-development-center": "skills", "jivamaitridham": "jivamaitridham",
    "center-of-excellence-for-women": "coew",
}

_IC = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{}</svg>'
INST_ICONS = {
    "hospital-and-research-center": _IC.format('<path d="M12 5v14M5 12h14"/>'),
    "vidyapeeth": _IC.format('<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3M7.5 15h9"/>'),
    "gurukul": _IC.format('<path d="M3 5h6a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H3zM21 5h-6a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h7z"/>'),
    "skill-development-center": _IC.format('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>'),
    "jivamaitridham": _IC.format('<circle cx="7" cy="9" r="1.8"/><circle cx="11" cy="5.5" r="1.8"/><circle cx="16" cy="6.5" r="1.8"/><circle cx="18.5" cy="11" r="1.8"/><path d="M8.5 18.5c0-2.5 1.8-5.5 4-5.5s4 3 4 5.5c0 1.5-1.2 2-2.5 1.6-1-.3-2-.3-3 0-1.3.4-2.5-.1-2.5-1.6z"/>'),
    "center-of-excellence-for-women": _IC.format('<circle cx="12" cy="7" r="3.2"/><path d="M5.5 21v-1.5a6.5 6.5 0 0 1 13 0V21"/>'),
}


# Vertical crop for institute photos whose subject sits high in the frame
INST_POS = {"jivamaitridham": "50% 12%", "skill-development-center": "15% 50%"}


def flipcard(inst, back_desc, href, card_id="", link_label="Visit the institute"):
    """Homepage institute card: square photo with a dark label bar and icon,
    flipping to a purple back with the description and a text link. The bar
    carries the institute's official name (Naman, Oct 18)."""
    id_attr = f' id="{card_id}"' if card_id else ""
    return f"""<li class="flipcard"{id_attr} tabindex="0">
        <div class="flipcard__inner">
          <div class="flipcard__front" style="background-image:url('{inst_photo(inst)[0]}');background-position:{INST_POS.get(inst["slug"], "50% 50%")}">
            <span class="flipcard__label"><span class="flipcard__icon">{INST_ICONS[inst["slug"]]}</span><span class="flipcard__name">{inst["name"]}</span></span>
          </div>
          <div class="flipcard__back">
            <h3 class="flipcard__h"><a href="{href}" tabindex="-1">{inst["home_name"]}</a></h3>
            <p class="flipcard__d">{back_desc}</p>
            <a class="textlink" href="{href}" tabindex="-1">{link_label}<span aria-hidden="true"> &rarr;</span></a>
          </div>
        </div>
      </li>"""


def inst_photo(inst):
    """(src, w, h, alt) for an institute: Naman's pick, the named Media Bank pick, else the pool."""
    from data_naman import INSTITUTES as NAMAN_INST
    if inst["slug"] in NAMAN_INST:
        return NAMAN_INST[inst["slug"]]
    pick = slot(INST_SLOTS[inst["slug"]])
    if pick:
        return pick
    f = filler_entry(inst["name"], INSTITUTE_TAGS[inst["slug"]])
    return (f[0], f[2], f[3], photo_alt(f[0], inst["name"]))


def render_india_hub():
    """India tab: one block per institute (name, approved description, photo,
    link to the detail page) in the homepage institute card pattern."""
    cards = "".join(flipcard(inst, inst["desc"], f'/our-work/india/{inst["slug"]}/', inst["slug"]) for inst in INSTITUTES)
    hero = slot("india-hero") or photo("india-hero", ["hospital+india", "india"], "children", min_w=1600)
    body = page_header(
        "Our Work &middot; Where We Serve",
        "Our Institutes in India",
        INDIA_INTRO,
        image=hero[0], size=(hero[1], hero[2]), alt=hero[3], mod="sky",
    ) + f"""
<section class="initgrid-sec">
  <div class="container">
    <ul class="flipgrid">{cards}</ul>
  </div>
</section>
{gift_section("Ways to Support", "", "Give to This Work")}
"""
    return page(
        "Our Institutes in India | SRLC USA",
        "Six permanent institutes in India: a hospital, schools, skill training, women's livelihoods, and animal care. See the work. SRLC USA.",
        "/our-work/india/", body)


def gift_section(h2, body, cta, href="/donate/"):
    body_html = f'<p class="giftsec__p">{body}</p>' if body else ""
    return f"""<section class="giftsec" aria-labelledby="gift-h">
  <div class="container giftsec__inner">
    <div class="giftsec__copy"><h2 class="giftsec__h" id="gift-h">{h2}</h2>{body_html}</div>
    <a class="btn btn--primary" href="{href}">{cta}</a>
  </div>
</section>"""


def peer_cards(current_slug):
    """More institutes: the homepage flip-card row, minus the current one."""
    cards = "".join(flipcard(inst, inst["home_desc"], f'/our-work/india/{inst["slug"]}/')
                    for inst in INSTITUTES if inst["slug"] != current_slug)
    return f"""<section class="instrow instrow--peers" aria-labelledby="peers-h">
  <div class="container instrow__head">
    <h2 class="instrow__h" id="peers-h">More Institutes in India</h2>
  </div>
  <div class="instrow__viewport">
    <ul class="instrow__track" id="instrowTrack">{cards}</ul>
  </div>
  <div class="instrow__arrows">
    <button type="button" class="instrow__arrow" data-dir="-1" aria-controls="instrowTrack" aria-label="Previous institutes"><svg viewBox="0 0 44 16" aria-hidden="true"><path d="M43 8H2M9 1L2 8l7 7"/></svg></button>
    <button type="button" class="instrow__arrow" data-dir="1" aria-controls="instrowTrack" aria-label="Next institutes"><svg viewBox="0 0 44 16" aria-hidden="true"><path d="M1 8h41M35 1l7 7-7 7"/></svg></button>
  </div>
</section>"""


def inst_hero(inst):
    return photo(f"{inst['slug']}-hero", [INST_TAG[inst["slug"]], "india"], INSTITUTE_TAGS[inst["slug"]], min_w=1600)


def render_institute(inst):
    """One layout for the institute set: hero with the selected intro
    sentence, what the institute does (approved description beside a photo),
    the other institutes, then ways to support."""
    paras = [inst["desc"]] + ([inst["extra"]] if inst.get("extra") else [])
    hero = inst_hero(inst)
    body = page_header(
        '<a href="/our-work/india/">Our Institutes in India</a>',
        inst["name"].replace("Shrimad Rajchandra ", "Shrimad&nbsp;Rajchandra "),
        inst["intro"] or None,
        image=hero[0], size=(hero[1], hero[2]), alt=hero[3],
    ) + f"""
{story_split("What This Institute Does", paras, inst_photo(inst), tone="lav", compact=len(" ".join(paras)) < 260)}
{peer_cards(inst["slug"])}
{gift_section("Ways to Support", "", inst.get("cta", "Give to This Work"))}
"""
    return page(inst["meta_title"], inst["meta_desc"], f'/our-work/india/{inst["slug"]}/', body)


def render_vidyapeeth():
    """Vidyapeeth on the shared institute layout, with its tab's programs and
    support pillars as editorial rows."""
    inst = next(i for i in INSTITUTES if i["slug"] == "vidyapeeth")
    rows = lambda items: "".join(f'<li class="proglist__item"><h3 class="proglist__h">{n}</h3><p class="proglist__d">{d}</p></li>' for n, d in items)
    hero = inst_hero(inst)
    body = page_header(
        '<a href="/our-work/india/">Our Institutes in India</a>',
        SRV["h1"],
        SRV["sub"],
        image=hero[0], size=(hero[1], hero[2]), alt=hero[3],
    ) + f"""
{story_split(SRV["need_h2"], SRV["need"], inst_photo(inst), tone="lav")}
<section class="progsec" aria-labelledby="srv-programs">
  <div class="container">
    <h2 class="progsec__h" id="srv-programs">{SRV["programs_h2"]}</h2>
    <p class="progsec__intro">{SRV["programs_intro"]}</p>
    <ul class="proglist">{rows(SRV["programs"])}</ul>
    <p class="progsec__intro progsec__intro--gap">{SRV["support_intro"]}</p>
    <ul class="proglist">{rows(SRV["pillars"])}</ul>
  </div>
</section>
{peer_cards("vidyapeeth")}
{gift_section(SRV["close_h2"], SRV["close"], SRV["cta"])}
"""
    return page(SRV["title"], SRV["desc"], "/our-work/india/vidyapeeth/", body)


def render_africa():
    body = page_header(
        "Mission Africa",
        "Distance never decides who receives care",
        "Mission Africa brings doctors, medicine, and follow-up care to communities where the nearest clinic can be hours away, at no cost to patients. We work with local health workers and community partners across 16 countries in Africa.",
        cta='<a class="btn btn--primary" href="/donate/">Stand With Mission Africa</a>',
        image=filler("Mission Africa", "hospital"),
    ) + f"""
<section class="vu-shell vu-shell--lav">
  <div class="container">
    <div class="vu-split vu-split--even">
      <div class="vu-split__copy">
        <h2 class="vu-h">Distance should not decide who gets care</h2>
        <p>In much of the region Mission Africa serves, the barrier to health is not the treatment. It is the miles between a family and anyone who can provide it, the distance where a curable illness quietly becomes a permanent one. Launched in 2024 by Shrimad Rajchandra Love and Care (SRLC), Mission Africa now works across 16 countries in Africa to close that distance.</p>
      </div>
      <div class="vu-split__photo">{img_tag(pinned(185))}</div>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">A clinic that comes to you</h2>
    <p class="vu-lead">Mission Africa brings the full spectrum of care to the community. Full medical camps staged inside the community, with doctors, diagnostics, and medicine in one place, free to every patient who walks in. And when the camp packs up, the care does not leave. Community programs carry it between visits.</p>
    <div class="vu-pair-grid mt-6">
      <div class="vu-card vu-card--stack reveal"><h3 class="vu-card__h">Healthcare access</h3><div class="vu-card__body"><p>Medical camps, medicine placed directly into waiting hands, and training for community health workers, so care remains long after the visiting doctors have gone.</p></div></div>
      <div class="vu-card vu-card--stack reveal" data-stagger="1"><h3 class="vu-card__h">Community development</h3><div class="vu-card__body"><p>Education, nutrition, and livelihood programs built with local communities rather than for them, so the change outlasts the camp.</p></div></div>
    </div>
  </div>
</section>

<section class="vu-shell vu-shell--lav">
  <div class="container">
    <h2 class="vu-h reveal">Proven far from here</h2>
    <p class="vu-lead">Mission Africa did not start from zero and your gift does not land on an experiment. It extends a healthcare model refined over decades in Dharampur, India, where a 250-bed hospital accredited by the National Accreditation Board for Hospitals and Healthcare Providers (NABH) treats patients regardless of their ability to pay. The movement behind it has touched 33M+ lives globally, and volunteers across the United States help fund and power the work.</p>
    <p class="africa-links">
      <a class="textlink" href="/our-work/10-care-program/">Our Causes<span aria-hidden="true"> &rarr;</span></a>
      <a class="textlink" href="/our-work/india/">India<span aria-hidden="true"> &rarr;</span></a>
      <a class="textlink" href="/our-work/united-states/">United States<span aria-hidden="true"> &rarr;</span></a>
    </p>
    <div class="photopair">{img_tag(pinned(310))}{img_tag(pinned(209))}</div>
  </div>
</section>

{flat_cta("Help the next camp happen", "Somewhere right now, a mother is measuring the distance between her child and a doctor. Your gift shortens it. Put medicine on the road, and hope alongside it.", "Stand With Mission Africa")}
"""
    return page(
        "Mission Africa | Free Medical Camps | SRLC USA",
        "Doctors, medicine, and follow-up care reach 16 African nations through Mission Africa. Send care the last mile. SRLC USA, a 501(c)(3) nonprofit.",
        "/our-work/mission-africa/", body)
