---
risk_id: R-001
title: Hospital clinical data is exposed publicly through misconfigured S3 storage
category: Data Protection
owner: Head of Engineering
status: Open
assessed: 2026-08-19
next_review: 2026-11-19
---

# R-001 — Public exposure of clinical data in S3

## The scenario

An S3 bucket holding hospital clinical datasets is made readable without
authentication. The data is retrieved by someone outside Meridian — a
researcher scanning for open buckets, an automated crawler, or an attacker
who found it through a search engine index.

Discovery is typically external and delayed: Meridian learns about it from a
journalist, a security researcher, or a customer, rather than from its own
monitoring.

## Assets affected

- Hospital clinical datasets (`restricted`)
- Generated benchmarking reports derived from them (`restricted`)
- Terraform state, where it records bucket configuration (`confidential`)

## How it actually happens

Four realistic paths, and it matters that they are enumerated rather than
summarised as "misconfiguration", because each needs a different treatment:

1. **A canned ACL is set to `public-read`** when someone copies an example
   from documentation or Stack Overflow that was written for a static website.
2. **A bucket policy grants `Principal: "*"`** to make a cross-account
   integration work under deadline pressure, with the intention of tightening
   it afterwards.
3. **Account-level Block Public Access is disabled** for one legitimate case —
   a public marketing asset — and the exception is never scoped back.
4. **A bucket is created outside Terraform**, in the console, during an
   incident, and never inherits the standard configuration.

Path 4 is the one people forget, and it is the reason a deploy-time control
alone is not sufficient.

## Threat sources

| Source | Realistic? |
|---|---|
| Internal error (engineer misconfiguration) | Yes — the dominant cause |
| Opportunistic external scanning | Yes — open buckets are found in hours, not months |
| Targeted attacker | Less likely at this company size, but not excluded |
| Malicious insider | Possible, but other paths are easier for an insider |

Naming the dominant source matters, because it points the treatment. This is
primarily an *error* risk, not an *attacker* risk, and error risks are treated
by making the wrong thing hard to do rather than by detecting adversaries.

## Inherent assessment

Scored as if no controls were in place.

**Likelihood: 4 — Likely.** Meridian's engineers create S3 buckets routinely,
and public exposure through one of the four paths above is a well-documented,
frequently recurring failure across the industry. With no preventive control,
expecting this within twelve months is conservative rather than alarmist.

**Impact: 5 — Severe.** Highest applicable column, which here is regulatory
and customer:

- *Regulatory* — disclosure of health data is a notifiable personal data
  breach under UK GDPR, reportable to the ICO within 72 hours, with
  enforcement action a realistic outcome.
- *Customer* — hospital contracts contain security warranties. A public
  disclosure of their patients' data is a plausible termination event, and it
  becomes a disclosable incident in every future security questionnaire.
- *Financial* — penalty, notification costs, and lost contracts sit above the
  £2M threshold for a company of this size.
- *Operational* — comparatively minor. Nothing goes offline. This is why the
  highest column is taken rather than an average; averaging would drag a
  business-threatening risk down into the middle of the register.

**Inherent score: 4 × 5 = 20 — Critical.**

## Controls currently in place

At the time of this assessment: **none that have been tested.**

Engineering states that buckets are "created through Terraform with sensible
defaults". That statement is *inquiry* — the weakest form of evidence, and
not sufficient to reduce a score. No test has been performed, no configuration
has been inspected, and there is no mechanism preventing paths 1 through 4.

## Residual assessment

**Residual score: 20 — Critical.** Unchanged from inherent.

This is deliberate and it is the honest position. A control that has not been
tested cannot be relied upon to reduce risk, and reducing the score on the
strength of a verbal assurance is how registers come to show a comfortable
profile that does not describe reality.

The score moves when there is a tested control, and not before.

## Appetite position

**Outside appetite.** The appetite statement in `scales.md` states that no
risk to the confidentiality of `restricted` data may sit in the High or
Critical band without an executive-signed, time-bound acceptance.

This risk is Critical and affects `restricted` data. Treatment is required.

## Treatment decision

**Treat — reduce.**

Direction, given that the dominant threat source is engineer error rather
than an adversary:

1. **Prevent it at deploy time.** Make a publicly readable bucket something
   the pipeline refuses to create, so the failure is caught before it exists
   rather than after. Addresses paths 1, 2, and 3.
2. **Detect what prevention cannot reach.** Continuously check the live
   account for public buckets, covering resources created outside the
   pipeline. Addresses path 4, and anything predating the control.
3. **Remove the ability to make the mistake account-wide.** Enable Block
   Public Access at the account level so that an individual bucket's settings
   cannot override it.

Designing the specific control is the next step; this assessment stops at
stating what the treatment needs to achieve.

## What would change this assessment

- A tested preventive control operating for a full quarter → likelihood
  reduced, expected residual around 8 (Moderate).
- Ceasing to hold identifiable clinical data at all → impact reduced, and a
  more effective treatment than any control.
- A near-miss or an actual exposure → likelihood raised to 5, and the
  assessment reopened immediately rather than at the scheduled review.

---

# Reassessment — 19 August 2026

## What changed

CTL-001 has been built and tested for the first time.

- **Layer 2** (block it at deploy time) was run against a deliberately
  non-compliant Terraform plan. It correctly blocked 4 violations. It was
  then run against a compliant plan and correctly allowed it.
- **Layer 3** (check the live account) was run against the account. It checked
  3 buckets, passed 2, and **found 1 genuinely open bucket** holding
  `restricted` data.
- **Layer 1** (account-wide Block Public Access) is documented but not yet
  implemented.

Evidence reference: `evidence-pack.json`, fingerprint
`c64d791494b51c606981a614c25578dc...`, collected 19 August 2026.

## New score

| | Before | After |
|---|---|---|
| Likelihood | 4 — Likely | **2 — Unlikely** |
| Impact | 5 — Severe | **5 — Severe** (unchanged) |
| Score | 20 — Critical | **10 — Moderate** |

## Why likelihood dropped

There is now a tested control that physically prevents the three most common
paths, and a detective check that catches the fourth. This is no longer a
verbal assurance — it was run, and the output was recorded.

## Why it did not drop further

Three reasons, and each would be raised by an auditor if it were not stated
here first:

1. **One day is not a period.** We have evidence the control worked *once*, on
   19 August. Evidence that a control operates *reliably over time* requires
   repeated results across months. Until then, this is a point-in-time result.
2. **The check found a real failure.** A bucket holding restricted patient
   data was publicly readable when we looked. That is direct evidence that
   this environment still produces this failure, which is not consistent with
   a low likelihood.
3. **Layer 1 is not built.** The account-wide safety net that would catch
   anything the other two layers miss does not yet exist.

## Why impact did not change at all

Impact stays at 5.

Controls change **how often** something happens, not **how bad it is** when it
does. If clinical data does become public, the regulatory and contractual
consequences are exactly what they always were. Nothing about CTL-001 makes a
breach less serious — it makes a breach less likely.

Reducing impact because a control exists is one of the most common ways a risk
register quietly stops describing reality.

## What would move it further

| Change | New likelihood | New score |
|---|---|---|
| Layer 1 built, and three consecutive months of clean Layer 3 results | 1 — Rare | 5 — Low |
| Layer 1 built, but failures still appearing occasionally | 2 — Unlikely | 10 — Moderate |
| Control switched off or bypassed | back to 4 | back to 20 |

## Open finding

**F-2026-001** — see `F-2026-001-public-bucket.md`. Must be resolved before
this assessment can be revised again.

---

*Originally assessed 19 August 2026 · Reassessed 19 August 2026 after first
control test · Next review: 19 November 2026*
