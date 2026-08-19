# Cloud GRC Lab — one risk, followed all the way through

A learning project. I built a small compliance environment for a **fictional**
health analytics company and followed a single risk from "what could go wrong"
all the way to "here is dated, tamper-evident proof it isn't happening".

The company is invented. The method is not.

## Why one risk instead of twenty

Most GRC portfolios are a long list of controls nobody has tested. I wanted
the opposite: one risk, taken seriously, all the way through the cycle —
because that is the cycle you actually repeat in the job.

**Scope → Risk → Control → Automated enforcement → Evidence → Finding →
Remediation → Retest → Reassessment**

## The story

**The risk.** Hospital clinical data exposed publicly through a misconfigured
S3 bucket. Scored **20 out of 25 — Critical**, because at a health data
company the impact is regulatory, not just embarrassing.

The engineers said buckets were created properly through Terraform. That is
*inquiry* — the weakest kind of evidence. It did not move the score. A control
nobody has tested cannot reduce risk.

**The control.** CTL-001, in three layers, because the risk assessment
identified four separate ways a bucket goes public and no single mechanism
closes all four.

**Layer 2 — block it before it is built.** `check_public_buckets.py` reads a
Terraform plan and refuses the deployment if it would create a public bucket.
It caught four violations in the test plan: a `public-read` ACL, two Block
Public Access switches off, and a bucket policy allowing `"*"`.

Tested in both directions — the bad plan must fail, **and the good plan must
pass**. A checker that blocks everything would pass the first test and get
switched off within a week.

**Layer 3 — check what is really there.** `collect_evidence.py` looks at the
live account rather than the pipeline.

It found a bucket that Layer 2 was structurally incapable of catching:
`meridian-temp-incident-20260814`, created by hand in the console during an
incident, holding restricted clinical data, publicly readable.

That is not a coincidence I arranged. It is the reason detective controls
exist.

**The evidence.** Every run writes an evidence pack recording what was
checked, when, out of how many, and a SHA-256 fingerprint of the findings.
Change one character and the fingerprint changes completely, so quietly
deleting an inconvenient failure is detectable.

Before remediation: `c64d791494b51c60...`
After remediation: `47d53d434b8b08e4...`

**The finding.** F-2026-001. The root cause is not "an engineer made a
mistake" — it is that creating a bucket by hand during an incident was
possible, normal and unmonitored. Blaming the individual would fix nothing,
because the next incident produces the same bucket.

The most urgent action was not fixing the bucket. It was pulling the S3 access
logs to determine whether anyone read the data while it was exposed — the
difference between an internal control failure and a notifiable breach with a
72-hour reporting clock.

**The reassessment.** 20 → **10 (Moderate)**. Likelihood dropped from 4 to 2.
**Impact stayed at 5.**

Impact did not move because controls change how *often* something happens, not
how *bad* it is when it does. Reducing impact because a control exists is one
of the most common ways a risk register stops describing reality.

Likelihood did not drop to 1 either, for three reasons stated openly in the
assessment: one day of results is not a period, the check found a genuine
failure, and Layer 1 is not built yet.

## Files

| File | What it is |
|---|---|
| `CONTEXT.md` | The environment being assessed. Scope comes before everything. |
| `GLOSSARY.md` | Every term in plain English. |
| `scales.md` | How risk is measured here, including what the model cannot do. |
| `R-001-public-cloud-storage.md` | The risk assessment and its reassessment. |
| `CTL-001-no-public-storage.md` | The control, in three layers. |
| `check_public_buckets.py` | Layer 2 — blocks public buckets at deploy time. |
| `bad-plan.json` | A deliberately non-compliant Terraform plan. |
| `collect_evidence.py` | Layer 3 — checks the live account, writes the evidence pack. |
| `account-snapshot.json` | A saved snapshot standing in for a live AWS account. |
| `evidence-report.md` | The generated evidence, in a form an auditor would read. |
| `F-2026-001-public-bucket.md` | The finding, its root cause, and open actions. |

## Running it

Requires Python 3. No AWS account needed.

```
python check_public_buckets.py bad-plan.json
python collect_evidence.py
```

The first should block four violations. The second checks three buckets and
reports one failure.

## Being honest about what this is

- The company, account IDs and data are invented.
- `account-snapshot.json` is a saved file standing in for real AWS API
  responses, so this can be run without credentials. The evidence pack says
  so on its face and marks itself as not real audit evidence.
- Layer 1 (account-wide Block Public Access) is designed but not implemented.
- The risk scoring model multiplies ordinal scores, which produces a
  defensible ranking rather than a calculated probability. `scales.md` says so.

Marking the shortcuts is deliberate. An assessor will find them anyway, and
having named them first is the difference between a limitation and a gap.

## What I would build next

1. Layer 1, so a hand-created bucket cannot be public even when made in a hurry
2. The same checks in OPA/Rego, the industry-standard policy engine
3. GitHub Actions, so the checks run on every pull request instead of by hand
4. Trend reporting across evidence packs, so control effectiveness is visible
   over a period rather than at a point in time
