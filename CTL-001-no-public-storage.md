---
control_id: CTL-001
title: Clinical data storage is never publicly accessible
owner: Head of Engineering
treats_risk: R-001
type: Preventive and Detective
status: Designed — not yet tested
created: 2026-08-19
---

# CTL-001 — No public storage

## What this control says must be true

**No S3 bucket in the production account may be readable or writable by
anyone who is not authenticated as a Meridian principal.**

That single sentence is the control. Everything below is how we make it true
and how we prove it.

Notice it is written as a *testable statement*. "We take bucket security
seriously" cannot be tested. "No bucket may be publicly readable" can be —
you go and look, and the answer is yes or no.

## Which risk this exists for

**R-001** — public exposure of hospital clinical data through misconfigured
S3 storage. Inherent score 20 (Critical).

A control with no risk behind it is a cost nobody can justify. If someone
asks "why do we do this?", the answer is R-001, not "because ISO says so".

## Why three layers and not one

R-001 listed four ways a bucket becomes public. No single mechanism closes
all four, so the control has three layers.

### Layer 1 — Turn it off at the account level

**Cloud concept:** AWS has an account-wide setting called *Block Public
Access*. It has four switches. When all four are on, AWS refuses to serve
public requests to any bucket in the account, **even if that bucket's own
settings say public**.

This matters: it means an individual engineer cannot make one bucket public
by mistake, because the account overrules the bucket.

**Closes:** paths 1, 2 and 3 from R-001, for every bucket at once.

### Layer 2 — Refuse it before it is built

**Cloud concept:** Meridian builds infrastructure with Terraform. Before
Terraform makes a change, it produces a *plan* — a machine-readable list of
what it is about to do.

We check that plan automatically. If it describes a bucket that would be
public, the pipeline fails and nothing is built.

**Why this layer exists when Layer 1 already blocks it:** Layer 1 stops the
data being served, but the bad configuration still gets created and sits
there. If someone ever turns Layer 1 off — for one legitimate public
marketing file — every one of those buckets goes live at once. Layer 2 stops
the misconfiguration existing in the first place.

**Closes:** paths 1, 2 and 3, before they reach the account.

### Layer 3 — Keep checking what is really there

**Cloud concept:** Layers 1 and 2 only see things built through the pipeline.
A bucket created by hand in the AWS console during an incident never passes
through either.

So we also check the live account on a schedule: list every bucket, ask AWS
what its actual public-access settings are, and report anything wrong.

**Closes:** path 4, plus anything that existed before this control did.

## Preventive and detective

Layers 1 and 2 are **preventive** — they stop the bad thing happening.
Layer 3 is **detective** — it does not stop anything, it tells you it
happened.

You want both. Prevention can be switched off, worked around, or simply not
apply to something. Detection is how you find out when it did.

*The shop version: layers 1 and 2 are the lock. Layer 3 is walking round at
closing time checking every door, including the one you forgot existed.*

## Who owns it

**Head of Engineering.**

A control with no named owner does not get fixed when it breaks. "The
security team" is not an owner — it is a place blame goes to die.

## How we will know it is working

| Layer | Test | How often | Type of proof |
|---|---|---|---|
| 1 | Ask AWS for the account's Block Public Access settings; all four must be on | Daily, automated | System export |
| 2 | Run the pipeline against a deliberately public bucket; it must fail | Every change | Pipeline result |
| 3 | List every bucket and check its public-access settings | Daily, automated | System export |

Layer 2's test is worth pausing on. We do not just check the pipeline *has*
a rule — we feed it something bad and confirm it actually refuses. A rule
nobody has tried is not a control, it is an intention.

## What frameworks call this

The same control, named by three different rulebooks:

| Framework | Reference | Roughly says |
|---|---|---|
| SOC 2 | CC6.1 | Access to data is restricted to authorised users |
| ISO 27001:2022 | A.5.15, A.8.12 | Access control; prevention of data leakage |
| NIST CSF 2.0 | PR.AA-05 | Access permissions are defined and enforced |

**Why bother mapping?** Because when a hospital's questionnaire asks "how do
you meet CC6.1?", you can point at a real control instead of writing a
paragraph. The mapping turns your work into an answer.

You do not memorise these. You look them up. Nobody in this field has them
memorised.

## Current status

**Designed, not yet tested.**

Because of that, R-001 stays at 20. The score moves when Lesson 4 produces
evidence that these layers actually operate — not before.
