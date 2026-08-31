"""Get Involved pages under /get-involved/ per CLAUDE.md v2 URL hierarchy.
FAQs and Corporate Giving are Phase 2 (removed). Events / Fundraise / Partner
have no content tabs yet: structure plus functional elements only, no invented
copy. Banned figure "25+ cities" replaced with the approved footprint phrasing
(conflict with tab copy flagged in the build log)."""
from shell import page, ph, page_header, flat_cta, filler, EMAIL, PHONE, IG, FB
from pages_core import prose_photo

US_FOOTPRINT = "chapters in 11 states and Washington, D.C."


def render_volunteer():
    cards = [
        ("Community", "SRLC USA&rsquo;s chapters are built by people who show up for each other. At every event, volunteers meet neighbors, professionals, and students who share a commitment to service. Many join for the cause and stay for the community."),
        ("Purpose", "Every event organized, every food distribution completed, every campaign supported reaches real people across the United States, India, and Africa. The effort on the ground connects directly to lives changed."),
        ("Growth", "Leadership, event management, fundraising, communications, and logistics are all part of active chapter work. The skills built through SRLC USA are practical and lasting. Many of our chapter leaders developed those skills here."),
        ("Belonging", "Service is not something SRLC USA volunteers do occasionally. For many, it becomes part of how they identify. That is why so many volunteers who start with a single event stay involved for years."),
    ]
    cards_html = prose_photo(cards, "/assets/img/fillers/hands-heart.jpg",
                             alt="Volunteers in conversation at an SRLC USA chapter event")
    steps = [
        ("01", "Sign up", "Fill out the form at the bottom of this page. Share where you are, what skills or interests you can offer, and how much time you have each month. It takes under two minutes."),
        ("02", "Meet your chapter", "A coordinator from the SRLC chapter in your area will reach out within a few days. They will introduce themselves and walk you through what the chapter is currently working on."),
        ("03", "Show up", "Attend your first event. Meet the people who make the chapter run. Most volunteers return for the next one within a month."),
    ]
    steps_html = prose_photo([(t, b) for _, t, b in steps], "/assets/img/photos/event-recent.jpg",
                             alt="An SRLC USA chapter event in progress", numbered=True, reverse=True)
    roles = ["Events and Logistics", "Food and Distribution", "Community Outreach", "Fundraising and Campaigns",
             "Communications and Social Media", "Healthcare Outreach", "University and Youth Programs",
             "Operations and Administration", "Chapter Leadership", "Internship", "Other"]
    role_opts = "".join(f"<option>{r}</option>" for r in roles)
    time_opts = "".join(f"<option>{t}</option>" for t in ["2 to 4 hours", "4 to 8 hours", "8+ hours", "Flexible"])

    body = page_header(
        "Get Involved",
        "Volunteer with SRLC USA",
        "Thousands of people across 11 states and Washington, D.C. give their time, their skills, and their energy to SRLC USA. Not because they have to. Because service is who they are.",
        cta='<a class="btn btn--primary" href="#signup">Volunteer With Us</a> <a class="btn btn--ghost" href="/our-work/united-states/">Find My State&rsquo;s Chapter</a>',
        image="/assets/img/fillers/community-gathering.jpg",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first">
  <div class="container">
    <h2 class="vu-h reveal">More than volunteering. A community.</h2>
    <div class="mt-6 reveal">{cards_html}</div>
  </div>
</section>

<section class="vu-shell vu-shell--cream">
  <div class="container">
    <h2 class="vu-h reveal">Getting started is simple</h2>
    <div class="mt-6 reveal">{steps_html}</div>
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
        "Serve communities across the US with SRLC USA, a 501(c)(3) nonprofit. Sign up to volunteer in two minutes.",
        "/get-involved/volunteer/", body)


def render_events():
    body = page_header(
        "Get Involved",
        "Events",
        "Chapter events, galas, and community gatherings.",
        image="/assets/img/photos/event-recent.jpg",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first">
  <div class="container" style="max-width:820px">
    <p class="vu-lead" style="color:var(--color-ink-muted)">Events calendar pending from the content team. Chapter coordinators share upcoming dates directly with volunteers.</p>
    <p class="mt-6" style="display:flex;gap:.7rem;flex-wrap:wrap">
      <a class="btn btn--primary" href="/get-involved/volunteer/">Get Event Invites</a>
      <a class="btn btn--secondary" href="/our-work/united-states/">Find Your Chapter</a>
    </p>
  </div>
</section>
"""
    return page(
        "Events | SRLC USA",
        "Chapter events, galas, and community gatherings across SRLC USA chapters. Find the next event near you.",
        "/get-involved/events/", body)


FUND_CAUSES = ["General Fund", "Education", "Healthcare", "Humanitarian Care", "Women Empowerment",
               "Child Care", "Emergency Relief", "Environmental Care", "Community Welfare",
               "Tribal Welfare", "Animal Welfare"]


def render_fundraise():
    chips = "".join(
        f'<a href="mailto:{EMAIL}?subject={("Start a fundraiser: " + name).replace(" ", "%20")}">{name}</a>'
        for name in FUND_CAUSES)
    body = page_header(
        "Get Involved",
        "Start a Fundraiser for SRLC USA",
        "Please choose what fund you would like to start a fundraiser for.",
        image="/assets/img/fillers/community-gathering.jpg",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first">
  <div class="container" style="max-width:820px">
    <div class="chip-row reveal">{chips}</div>
    <p class="mt-6" style="font-size:.9rem;color:var(--color-ink-muted)">Questions? Reach us at <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
  </div>
</section>
"""
    return page(
        "Start a Fundraiser | SRLC USA",
        "Choose a fund and start a fundraiser for SRLC USA, a 501(c)(3) nonprofit.",
        "/get-involved/fundraise/", body)


def render_partner():
    body = page_header(
        "Get Involved",
        "Partner With Us",
        "Strategic partnerships for organizations and NGOs.",
        image="/assets/img/fillers/hands-heart.jpg",
    ) + f"""
<section class="vu-shell vu-shell--lav vu-shell--first">
  <div class="container" style="max-width:820px">
    <p class="vu-lead" style="color:var(--color-ink-muted)">Partnership program details pending from the content team.</p>
    <p class="mt-6"><a class="btn btn--primary" href="mailto:{EMAIL}?subject=Partnership%20inquiry">Start the Conversation</a></p>
  </div>
</section>
"""
    return page(
        "Partner With Us | SRLC USA",
        "Strategic partnerships for organizations and NGOs with SRLC USA, a 501(c)(3) nonprofit.",
        "/get-involved/partner-with-us/", body)
