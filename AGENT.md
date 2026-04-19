# AGENT.md — 8Vitality.com

<trl>
DEFINE "8vitality_site" AS NAMESPACE.
NAMESPACE 8vitality_site CONTAINS MODULE website AND MODULE email_automation AND MODULE policies.
NAMESPACE 8vitality_site SUBJECT_TO PARTY xepayac_llc.
</trl>

## What This Repository Is

8Vitality.com is the public product site for Xepayac's acupuncture and health/wellness practice (Infinite Vitality). It is a static website — HTML, CSS, images, PDFs, and a small Python email-automation module — deployed via cPanel Git Version Control to `public_html`. Tier 3 (baseline) repo in the Xepayac portfolio. Planned as the first field deployment target for TRUGS_OS operations; see `TRUGS-DEVELOPMENT#1492` (acupuncture-automation pilot).

## How to Read This Repo as an LLM Agent

`folder.trug.json` at the repo root is structural truth — read it first. Key entry points:

| Path | Content |
|------|---------|
| `folder.trug.json` | Machine-readable repo graph (nodes + edges) |
| `index.html` | Main landing page — all visitor-facing content lives here |
| `css/style.css` | Stylesheet |
| `resources/` | Images, logos, practice-policy PDFs |
| `Policies/index.html` | Policy page (Privacy, SMS Terms, Consent forms) |
| `email_automation/` | Python scripts for monthly client email campaigns (Proton Bridge) |
| `README.md` | Quickstart + deployment instructions |
| `SEO_GUIDE.md` | SEO conventions for content updates |

This is a **product site**, not a tooling repo. Typical LLM work here is content updates (copy, images, SEO), not refactors or framework migration. No build step — edits to HTML/CSS ship on merge + pull.

## Editorial Gate — Health Claims

Any edit that adds, removes, or modifies a claim about health outcomes, treatment efficacy, medical conditions, diagnostic language, or practitioner credentials **SHALL** be reviewed by a licensed medical practitioner before merge. LLM agents MAY draft copy but MUST flag health-claim diffs explicitly in the PR body.

<trl>
AGENT SHALL_NOT WRITE ANY DATA 'that CONTAINS RECORD health_claim UNLESS PARTY medical_practitioner SHALL APPROVE.
AGENT SHALL FLAG EACH RECORD health_claim 'in RESOURCE pull_request THEN SEND RESULT TO PARTY human.
AGENT MAY WRITE DATA 'for RECORD seo OR RECORD layout OR RECORD image OR RECORD typo WITHOUT PARTY medical_practitioner.
</trl>

## Rules

<trl>
AGENT SHALL READ FILE folder.trug.json 'at ENTRY session.
AGENT SHALL_NOT WRITE ANY DATA TO ENDPOINT main.
AGENT SHALL DEFINE RESOURCE branch THEN DEFINE RESOURCE pull_request THEN SEND RESULT TO PARTY human.
AGENT SHALL_NOT MERGE ANY RESOURCE TO ENDPOINT main.
PARTY human SHALL APPROVE ALL RESOURCE THEN MERGE RESULT TO ENDPOINT main.
</trl>

## Companion Repositories

- [Xepayac/XEPAYAC_LLC](https://github.com/Xepayac/XEPAYAC_LLC) — parent entity operations
- [Xepayac/TRUGS-DEVELOPMENT](https://github.com/Xepayac/TRUGS-DEVELOPMENT) — development portfolio + EPIC
- [TRUGS-LLC/TRUGS](https://github.com/TRUGS-LLC/TRUGS) — TRUG specification (CORE + TRL + BRANCHES)
- TRUGS_OS (future) — orchestrator for which this site is the first deployment target

## License + Status

Proprietary (Xepayac LLC, all rights reserved) — see `LICENSE`. Status: **production**; deployed to https://8Vitality.com via cPanel Git Version Control.
