# Environment in scope

Every artifact in this repository assesses one specific environment. Without
that, a risk assessment is a list of things that are bad in general, and a
control is a thing that would be nice to have. Scope is what makes both of
them answerable.

## The organisation

**Meridian Health Analytics** — a fictional company, used consistently across
this repository.

A 60-person SaaS business selling a patient-outcomes analytics platform to
hospital groups in the UK and Ireland. Hospitals upload de-identified clinical
datasets; Meridian processes them and returns benchmarking reports.

Runs entirely on AWS. No on-premise infrastructure. Engineering deploys via
Terraform through GitHub Actions.

## Why the business context matters

Two facts about this business drive almost every risk decision that follows,
and they are the reason scope comes before assessment:

1. **The data is health data.** Even de-identified, it is subject to UK GDPR,
   and re-identification risk means regulators treat it as sensitive. A
   disclosure is a notifiable breach with a regulatory penalty attached, not
   an embarrassment.
2. **The customers are hospitals.** Hospital procurement runs security
   questionnaires and demands assurance reports before signing. A control
   failure does not just create a fine — it stops the sales pipeline.

An identical technical failure at a company selling restaurant booking
software would score materially lower on impact. Same infrastructure, same
misconfiguration, different consequence. That is what scope buys you.

## Technical scope

| In scope | Out of scope |
|---|---|
| AWS production account (workloads, customer data) | Corporate laptops and endpoint management |
| AWS log-archive account | Google Workspace and corporate email |
| The Terraform code and GitHub Actions pipeline that deploy to them | Marketing website (separate account, no customer data) |
| S3 buckets, RDS instances, and IAM within those accounts | Physical security (fully remote company, no offices) |

## Data classification in use

| Level | Meaning | Example |
|---|---|---|
| `public` | Published deliberately | Marketing content |
| `internal` | Routine business information | Sprint plans, internal docs |
| `confidential` | Commercially sensitive | Contracts, pricing, source code |
| `restricted` | Regulated customer data | Hospital clinical datasets, benchmarking outputs |

## Compliance drivers

- **UK GDPR** — statutory. Applies whether or not a customer asks.
- **SOC 2 Type II** — contractual. Two prospects have made it a condition of
  signing.
- **NHS Data Security and Protection Toolkit** — required by NHS customers.

These drivers are why controls exist here. A control that traces to none of
them, and to no risk, is a cost with no stated benefit.
