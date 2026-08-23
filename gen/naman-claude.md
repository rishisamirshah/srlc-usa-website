# CLAUDE.md — srlcusa.org build rules

Rules for every build session in this repo. v2, August 2026. Supersedes v1.
When anything here conflicts with a content tab, flag it to Naman; never
resolve silently. Naman approves everything.

## Source of truth

- Build pages ONLY from tabs marked FINAL at the top of the master Google
  doc, and from the approved homepage HTML. No tab, no page.
- Never write, improvise, or "improve" copy. If a tab is missing something,
  build the structure and leave the slot empty; the gap belongs to content,
  not to the build.
- Bracketed flags in tabs (FINANCE-PENDING, STORY SLOT) are unresolved
  content. Build the section, leave the flagged element out, note it in the
  build log.

## Approved statistics — the only numbers allowed anywhere

| Stat | Use |
|---|---|
| 33M+ lives touched globally | trust bar, homepage, global sections |
| 8.35M+ patients treated globally | Health Care |
| 3.28M+ students supported globally | Educational Care |
| 12.24M+ people reached globally (Humanitarian Care) | Humanitarian Care |
| 450K+ animals served globally | Animal Care |
| 8.90M+ lives supported globally (Emergency Relief) | Emergency Relief Care |

Every global figure is labeled global. NO US-specific stats are approved.
BANNED (remove on sight): 27M+, 3.1M, 300K, 25+ cities, 400+ community
partners, $110K+ aid, 3 continents, per-state stat bands.
The US footprint is stated as: chapters in 11 states and Washington, D.C.
(22 centers). Never "25+ cities."

## Trust language

- UN recognition belongs to the parent body only. Approved forms: "the
  United States chapter of Shrimad Rajchandra Love and Care, holder of UN
  ECOSOC Special Consultative Status" or a recognition item labeled
  "SRLC (Global): UN ECOSOC Special Consultative Status, 2020."
  NEVER "SRLC USA is UN-recognized."
- Recognition cluster is exactly: ECOSOC (labeled SRLC Global),
  GreatNonprofits Top-Rated (SRLC USA), Candid Gold Transparency Seal
  (SRLC USA). NABH is the hospital's accreditation: it appears only in
  hospital/institute context, never as an SRLC USA credential.
- Never "100% volunteer-powered" or any variant.
- SRET, SRST, SRJT never appear anywhere public, including alt text and
  metadata.
- The corporate logo wall label is pending verification. Until Naman
  confirms the correct label, the section ships as "Corporate matching
  gift eligibility" or holds. These are employers whose matching programs
  cover SRLC USA, not partners.

## Mission Africa positioning — locked

Mission Africa is one initiative among peers, level with the India
institutes. Never the flagship, never the primary acquisition page for
any donor segment, never given more space, stronger CTAs, or higher
placement than peer initiatives. It gets identical treatment to every
other cause page.

## Naming — exact, no variants

- Institutes, never institutions.
- Center, never Centre, in every SRLC name.
- Classroom of Change. The name Back2School never appears in new content.
- The ten Cares, exactly: Health Care, Educational Care, Child Care,
  Woman Care, Tribal Care, Community Care, Humanitarian Care, Animal Care,
  Environmental Care, Emergency Relief Care.
- Love and Care always spelled out. Never Love & Care.
- The Shrimad Rajchandra wordmark always renders on a single line.
- QC, never QA.

## Copy rules the build must preserve

- No em dashes anywhere, including metadata and alt text.
- No ellipsis truncation. If card copy is too long, the tab gets fixed,
  not truncated with "…".
- Banned CTA labels: Learn more, Click here, Read more, Discover, Find
  out how.
- Restricted words: aid, charity (as self-description), handout, pity,
  unfortunate, poor, needy.
- Person-first language always.
- Spiritual content (Gurudevshri, lineage, seva) exists only on
  /about/our-inspiration/. Anywhere else is a build-stopping error.
- American English.

## Brand tokens (Brand Guide, August 2026)

- SRLC Purple #693D84 primary; Light Purple #A387C6 links/accents;
  Warm Orange #FD954F CTAs; Lavender White #F7F4FF backgrounds;
  Maroon #5D2B29 reserved for footer/formal only.
- Cormorant Garamond for display/headings; Jost for body/UI/nav.
- CTAs: Jost 600 on Warm Orange. Impact stats display in Warm Orange.
- Contrast: verify hero overlay text at 4.5:1 minimum, measured.

## Navigation — Phase 1, exactly this

- About Us: Our Inspiration, Who We Are, Our Impact, Management Team,
  Financials. (FAQs is Phase 2: remove.)
- Our Work: 10 Care Program; Where We Serve > United States, India,
  Mission Africa.
- Get Involved: Donate, Volunteer, Events, Start a Fundraiser, Partner
  With Us. (Corporate Giving is Phase 2: remove.)
- Plus the Donate CTA button.

## URLs

- Hierarchy: /about/{page}/, /our-work/10-care-program/{care}/,
  /our-work/united-states/{state}/, /our-work/india/{institute}/,
  /our-work/mission-africa/, /get-involved/{page}/, /donate/.
- Trailing slash canonical; redirect the other form.
- Redirect map from the old site is Nikhil's deliverable; every old URL
  (/map/, /locations/*, /back-to-school/, /financials/, /annual-reports/,
  /institutes/* including the mislabeled primary-school slug) gets a
  single-hop 301 to its new home before cutover.

## Technical baselines

- Static prerendered HTML. All copy present with JavaScript disabled.
- Real heading elements, one H1 per page. Real anchors with resolvable
  hrefs.
- Images: AVIF/WebP, srcset, explicit width and height, hero preloaded,
  rest lazy. Alt text is a real description, never a filename.
- Scroll-driven sections (10 Care parallax) require a reduced-motion
  fallback that collapses to a stacked list.
- Staging carries noindex until cutover. Production sitemap and robots
  generated in the build.
- Performance: LCP under 2.5s, CLS under 0.1, page under 2MB.
- Third-party scripts: analytics and payment processor only.
- Hosting: staging anywhere with noindex is fine; production is AWS
  Amplify on the SRLC USA org account per the August decision.

## Verify before anything ships

- The footer address and phone number must be confirmed real by Naman
  before they appear on any deployed page.
- Every image with an identifiable person: consent confirmed via the
  Media Bank. Placeholder-then-swap is fine on staging.
- Donation CTAs: destination pending Naman's ruling on designated giving
  forms. Until ruled, all giving CTAs route to /donate/ with no
  designation promises in copy.

## Ownership

Content: Naman (10 Care pages, US/states/India hubs, Financials,
Our Inspiration with Millen), Millen (Who We Are, Our Impact, Mission
Africa), Riyan (Volunteer; Vidyapeeth, Gurukul, Skill Development Center),
Parshva (Management Team; Hospital and Research Center, Jivamaitridham,
Center of Excellence for Women). Build: Rishi, from FINAL tabs only.
QC: Shreya, against Document D. Approval: Naman only.
