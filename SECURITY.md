# SRLC USA Website — Hosting & Security Analysis

Prepared for team sign-off · Rishi Shah · August 2026

## Recommendation

**Host on GitHub Pages as a fully static site.** No WordPress, no server, no database, no admin panel. This is the same architecture as the SRA USA site (srausa.org), live since July 2026 with zero security incidents.

## Why the previous hack cannot recur on this architecture

The old site was compromised and used to serve gambling/adult content. That class of attack requires **server-side code the attacker can exploit** — a WordPress admin login, PHP plugins, a writable database. A static GitHub Pages site has none of those. There is no login page to brute-force, no plugin to exploit, no database to inject into, no server we manage to misconfigure. The only way to change what the site serves is a commit to this repository.

## Attack vectors and mitigations

| Vector | Exposure on GitHub Pages | Mitigation |
|---|---|---|
| Server compromise (the previous incident) | **Eliminated** — no server, no CMS, no database | Architecture itself |
| Repo/account takeover (the real remaining risk) | An attacker with push access could change the site | 2FA required on all GitHub accounts with write access; branch protection on `main` (PR-only merges); short collaborator list |
| DDoS | GitHub Pages sits behind Fastly (global CDN) + GitHub's own DDoS mitigation, which absorbs volumetric attacks far beyond what a nonprofit brochure site attracts | Provided by platform. Optional: Cloudflare free tier in front adds another layer + rate limiting (trade-off: occasional CAPTCHA for flagged IPs) |
| DNS spoofing / hijack | Attack happens at the registrar/DNS layer, identical for any host (Hostgator included) | Registrar account 2FA + registrar lock; enable **DNSSEC** (free via Cloudflare DNS); HTTPS enforced by Pages means a spoofed DNS answer still can't present a valid certificate |
| Payment card theft (PCI) | **We never touch card data.** The donate flow uses a hosted payment processor (current: srlcusa.org/donate) — card entry happens on the processor's PCI-DSS-certified pages | Keep it that way: the site links or embeds the processor's hosted checkout; card numbers never touch our repo, our pages, or our JavaScript. This satisfies PCI SAQ-A, the lightest compliance tier |
| Content injection via dependencies | Static HTML with no third-party JS beyond Google Fonts | Keep third-party scripts near zero; any future embed (payment, analytics) gets Subresource Integrity or comes from the processor directly |
| Defacement via CMS portal (future) | The planned lightweight edit portal writes to this repo | Portal commits to a branch → PR + human approval before production; portal login = 2FA; donate page changes always require review |

## GitHub Pages vs. Hostgator

| | GitHub Pages | Hostgator |
|---|---|---|
| Attack surface | Static only — no server we manage | Full server stack to patch and harden (the environment the old hack happened in) |
| Deploys | Seconds, versioned, every change auditable in git history | FTP/panel uploads, no audit trail |
| Cost | Free | Paid |
| DDoS/CDN | Fastly + GitHub, built in | Depends on plan; typically weaker |
| Rollback | `git revert`, instant | Manual |

## Operational checklist (the actual to-dos)

1. 2FA on every GitHub account with write access — **done for repo owner**
2. Branch protection on `main` once the team is onboarded (PR-only, 1 approval)
3. Registrar: 2FA + transfer lock on the srlcusa.org domain; enable DNSSEC when DNS moves to Cloudflare (optional but recommended)
4. Donate page: hosted processor only — never a custom card form
5. All images/copy live in this repo — single source of truth, full audit trail
