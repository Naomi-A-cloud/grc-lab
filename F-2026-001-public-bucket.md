---
finding_id: F-2026-001
title: Bucket holding restricted clinical data was publicly readable
raised: 2026-08-19
raised_by: Automated control test (CTL-001 Layer 3)
control: CTL-001
risk: R-001
severity: Critical
owner: Head of Engineering
status: Remediated — root cause open
---

# F-2026-001 — Public bucket holding clinical data

## What was found

The bucket `meridian-temp-incident-20260814` was publicly readable. All four
Block Public Access settings were off and its ACL was set to `public-read`.

It holds `restricted` data — hospital clinical datasets.

**Population:** 3 buckets checked, 1 failed.
Stating the total matters. "We found an open bucket" and "1 of our 3 buckets
was open" are very different statements, and the second is the one an auditor
can actually work with.

## How it was found

The Layer 3 detective check, on its first run.

Worth recording: **Layer 2 could not have caught this.** Layer 2 inspects
Terraform plans, and this bucket was created by hand in the AWS console. It
never passed through the pipeline.

This is the exact scenario listed as path 4 in R-001, which is why Layer 3
exists.

## Root cause

The bucket name says it: `temp-incident-20260814`. It was created during an
incident on 14 August, by hand, under time pressure, to move data somewhere
quickly. It was never cleaned up.

The root cause is not "an engineer made a mistake". The root cause is that
**creating a bucket by hand during an incident is possible, normal, and
unmonitored.** Any engineer under pressure would have done the same.

Treating this as an individual's error would fix nothing, because the next
incident would produce the same bucket.

## Immediate action taken

Block Public Access enabled on all four settings; ACL set to `private`.
Re-tested on 19 August: 3 buckets checked, 3 passed, 0 failed.

Evidence fingerprint changed from `c64d7914...` to `47d53d43...`, confirming
the re-test reflects genuinely different findings rather than a re-run of the
same result.

## Outstanding actions

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Build Layer 1 — account-wide Block Public Access, so a hand-made bucket cannot be public even if created in a hurry | Cloud Platform | 2026-09-15 |
| 2 | Determine whether this bucket's data was actually accessed while it was open, using S3 access logs | Security | 2026-08-26 |
| 3 | Decide whether this bucket should exist at all, and delete it if not | Head of Engineering | 2026-08-31 |
| 4 | Add a step to the incident process covering temporary data locations | Head of Engineering | 2026-09-30 |

**Action 2 is the urgent one.** Until we know whether anyone read the data
while it was exposed, we cannot know whether this is an internal control
failure or a **notifiable personal data breach**, which under UK GDPR must be
reported to the ICO within 72 hours.

Fixing the bucket closed the hole. It did not answer that question.

## Status

**Remediated, root cause open.**

The specific bucket is fixed. The condition that produced it is not. This
finding stays open until Actions 1 and 2 complete.

Closing it now, on the strength of the bucket being fixed, would be the
comfortable choice and the wrong one.
