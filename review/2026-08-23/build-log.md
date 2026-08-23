# SRLC USA build log — Aug 23 pass (violations + pending)

Applied: your Aug 22 edits list, CLAUDE.md v2, Brand Guide (Aug 2026), approved homepage HTML v2, and the current master doc export.

## Conflicts between CLAUDE.md and content tabs (flagged, not resolved silently)
1. Per-state stat bands exist in every state tab but sit on the CLAUDE.md banned list. Removed from all 12 state pages. Either the tabs update or the ban gets an exception.
2. "25+ US cities" appears in the Volunteer tab hero, the Volunteer "Community" card, and trust bar Set A in the institute specs. Banned list wins: replaced with the 11-states-and-D.C. footprint phrasing; trust bars ship as the Brand Guide 4-signal bar.
3. Institute eyebrow inconsistency ("Our work in India" vs "Our Institutes in India"): standardized to "Our Institutes in India" pending your ruling.
4. Who We Are hero said "SRLC USA's 25+ chapters": figure dropped.
5. The doc's txt export carries no tab titles, so FINAL markers are invisible to the build. Built from all drafted tabs; flag any tab that is not FINAL.

## Left out per FINANCE-PENDING / STORY SLOT / BLOCKING flags
- Dollar-to-outcome lines: only the drafted $50 nutrition line renders; other tiles show "pending finance sign-off."
- Named stories: Woman/Community/Humanitarian/Animal/Environmental/Emergency Care, Volunteer, Mission Africa, and all institute story slots stay empty.
- Hospital / Jivamaitridham / Center of Excellence for Women: built to the Document C spec with the long approved-description slot empty.
- Management Team: rebuilt to the spec; roster is placeholder slots because no Naman-approved bios exist (the live-site bios were removed for that reason).
- Vidyapeeth statistics remain 2 of the required 4 to 5.
- Donate FAQ accordion + trust-signal copy from donate.html: file never arrived; slot is placeholdered.
- Financials PDFs: request-by-email links until the self-hosted files arrive.

## Blocked on Naman
- Official logo file was never attached in the chat. Interim: the official stacked color lockup (solid nav) + official white horizontal lockup (transparent nav, footer), both single images, never rebuilt from mark + text. Swap the moment your file lands.
- Footer address + phone removed pending your confirmation. Provenance: both came from the footer of the approved homepage HTML you sent (500 Paterson Plank Rd #33685, Union City NJ + 1.551.SRLC.USA).
- Email domain: everything stays info@srlc-usa.org until your DNS/workspace ruling.
- Logo wall: kept, labeled "Corporate matching gift eligibility" with your qualifier line; duplicate marquee render is aria-hidden; logo.jpg and 21st Century Fox removed. Kill the wall entirely if counsel rules against it.
- Donate hero: headline constrained left in the site-wide header pattern rather than centered; say the word if you want it centered instead.

## Notes
- Staging is noindex (meta + X-Robots-Tag + robots.txt disallow) until cutover.
- URL hierarchy moved to /get-involved/{page}/ and /about/management-team/ per CLAUDE.md, with 301s from every old path.
- Impact-story parallax is wired (background-attachment engine from the original); it reads flat until a consented portrait replaces the grey slot.
- FAQs and Corporate Giving removed from nav, footer, and the build (Phase 2); old URLs 301 home and to /donate/.
