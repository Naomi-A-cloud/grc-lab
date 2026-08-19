# How risk is measured here

Two questions, scored 1 to 5 each: **how likely is it**, and **how bad if it
happens**. Multiply them for a score out of 25.

The numbers are not the point. The point is that everyone uses the same
definitions, so that when two people score the same risk differently, the
disagreement is about the *facts* rather than about what "medium" means.

## Likelihood

| Score | Label | Definition |
|---|---|---|
| 1 | Rare | Not expected within 5 years. No known occurrence in similar organisations. |
| 2 | Unlikely | Plausible within 3–5 years. Occasional occurrences in the industry. |
| 3 | Possible | Expected within 1–3 years. Happens regularly in the industry. |
| 4 | Likely | Expected within 12 months. Has occurred here, or at close peers. |
| 5 | Almost certain | Expected within 3 months, or may already be happening undetected. |

Anchoring likelihood to **time** rather than to words like "medium" is what
makes it arguable. "Is this expected within twelve months?" is a question two
people can actually disagree about with reasons.

## Impact

Score on the **highest** applicable column, not an average. A risk that is
catastrophic in one dimension and trivial in the others is still catastrophic.

| Score | Label | Financial | Regulatory | Customer | Operational |
|---|---|---|---|---|---|
| 1 | Negligible | < £10k | None | Nobody notices | < 1 hour, one team |
| 2 | Minor | £10k–£50k | Internal finding | Isolated complaints | < 4 hours, one service |
| 3 | Moderate | £50k–£250k | Reportable to the ICO | Contractual SLA breach | < 24 hours, several services |
| 4 | Major | £250k–£2M | Regulatory penalty; ICO enforcement | Notifiable data breach; customer churn | Multi-day outage |
| 5 | Severe | > £2M | Enforcement action threatening the business | Mass breach of patient data; contract termination | Extended outage, recovery uncertain |

The financial bands are set relative to **this** company. £2M would be an
inconvenience to a bank and an extinction event for a 60-person business.
Copying bands from a template company is the most common way a risk register
becomes meaningless.

## Inherent and residual

**Inherent risk** is the score *before* considering the controls in place —
what the exposure would be if nothing were being done about it.

**Residual risk** is the score *after* accounting for controls that are
actually working.

Both are recorded, because the gap between them is the argument for what the
controls are worth. A register showing only residual risk cannot answer "what
are we getting for the money we spend on security?"

Residual risk is estimated by reducing **likelihood**, not impact. Most
controls change how often something happens, not how bad it is when it does.
Where a control genuinely limits the damage rather than the frequency —
encryption limiting what a stolen backup discloses, tested backups limiting
outage length — that is noted explicitly in the assessment rather than
quietly applied.

## Appetite

What the organisation will and will not tolerate, decided in advance so that
the answer is not negotiated under pressure after something has gone wrong.

| Residual score | Band | What must happen |
|---|---|---|
| 1–5 | Low | Accept. Review annually. |
| 6–11 | Moderate | Accept with monitoring. Named owner, reviewed quarterly. |
| 12–17 | High | Treatment plan with a funded target date. Reviewed monthly. |
| 18–25 | Critical | Escalate to the founders. Treat immediately or formally accept in writing. |

**Appetite statement.** Meridian accepts Low and Moderate residual risk
without escalation. Given that the data is regulated health data and that
customer contracts depend on demonstrable security, **no risk affecting the
confidentiality of `restricted` data may sit in the High or Critical band
without an executive-signed, time-bound acceptance.**

## What this model cannot do

Worth stating plainly, because it is a fair challenge and having an answer is
better than being caught by it:

- Multiplying two 1–5 ordinal scores is not mathematically sound. It produces
  a defensible **ranking**, not a calculated probability or a currency figure.
- Related risks are scored separately, which understates the total exposure
  when several share one root cause.
- The scores are informed judgement. They are reproducible only because the
  definitions above are written down.

For a company of this size, a defensible ranking is the right tool. Moving to
quantitative analysis becomes worthwhile when decisions start turning on how
much to spend rather than on what to do first.
