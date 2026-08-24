---
document_id: ISMS-01
title: ISMS Context and Scope
iso_clauses: 4.1, 4.2, 4.3, 4.4
version: 0.1 draft
owner: Governance, Risk and Compliance Officer
status: awaiting approval
created: 20/08/2026
next_review: 25/08/2027
---

## 2. External issues (Clause 4.1)

| # | External issue | Why it matters to Meridian |
|---|---|---|
| E1 | Meridian processes clinical data about real patients, so UK GDPR applies to it | If that data is disclosed, it is a notifiable personal data breach. The ICO must be told within 72 hours, enforcement action is a realistic outcome, and affected hospitals would have to be informed — which puts customer contracts at risk |
  | E2 | Hospital customers run security reviews and demand assurance evidence before they will sign a contract | If Meridian cannot produce the evidence a hospital asks for, the sale stalls or is lost. That makes information security a revenue problem rather than a technical one, and it puts an external deadline on the ISMS that Meridian does not control |
  | E3 | NHS customer organisations require their suppliers to complete the NHS Data Security and Protection Toolkit, on top of UK GDPR and the SOC 2 report other customers ask for | Meridian must satisfy three separate assurance regimes with no dedicated security team. Each asks for similar evidence in a different format, so the same control has to be evidenced several ways. That makes reusable, automated evidence collection a practical necessity rather than a preference |

  ## 3. Internal issues (Clause 4.1)

  | # | Internal issue | Why it matters to Meridian |
|---|---|---|
| I1 | Meridian has 60 staff and no dedicated security team; security is held alongside someone's main job | There is limited capacity for controls that need regular manual attention. Any control depending on a person remembering to check will decay quietly, so controls must be automated wherever possible |
| I2 | here is no approval step to attach a control to, so the check must run inside the deployment pipeline itself. This is why CTL-001 Layer 2 evaluates the Terraform plan rather than relying on review. |
| I3 | Incidents are handled under time pressure by whoever is available, and creating infrastructure by hand in the AWS console during an incident is possible, normal and unmonitored | Because infrastructure created this way never passes through Terraform, a deploy-time check cannot see it. The gap can only be closed by a detective control that inspects the live account independently of the pipeline. This is why CTL-001 has a Layer 3 as well as a Layer 2 |

## 4. Interested parties (Clause 4.2)

| Party | What they require | How we know |
|---|---|---|
| Hospital customers | Confidentiality of the clinical data they send us; assurance evidence before signing | Contract clauses and procurement questionnaires |
| Patients | Their clinical records stay confidential and unaltered, with access limited to those authorised to have it | UK GDPR sets out data subject rights on their behalf; patients do not contact Meridian directly |
| Information Commissioner's Office (ICO) | Compliance with UK GDPR; notification of a personal data breach within 72 hours; evidence that Meridian can demonstrate its compliance | Statutory — UK GDPR applies whether or not anyone asks for it |
| Engineering staff | Security controls that do not block delivery: fast, clear failures that say what to fix, rather than approval queues or unexplained rules | Internal feedback, and the evidence of F-2026-001 — when a control is too slow in the moment, people work around it |

## 5. Scope of the ISMS (Clause 4.3)

### 5.1 Scope statement


The Information Security Management System of Meridian Health Analytics
covers the development, hosting and operation of the patient-outcomes
analytics platform sold to hospital groups in the UK and Ireland,
including the de-identified clinical datasets hospitals upload and the
benchmarking reports Meridian returns to them. It applies to all
personnel, contractors and processes supporting that platform, and to
the deployment pipeline through which changes reach it. It operates from
Meridian's AWS production, shared-services and log-archive accounts,
with no on-premise infrastructure.

| Category | In scope |
|---|---|
| Business processes | Receiving clinical datasets from hospitals; processing and analysing them; producing and delivering benchmarking reports; supporting customers on the platform |
| Information | Clinical datasets uploaded by hospitals (`restricted`); benchmarking reports returned to them (`restricted`); platform source code and infrastructure configuration (`confidential`) |
| Technology | AWS production, shared-services and log-archive accounts; GitHub repositories; the GitHub Actions deployment pipeline; Terraform infrastructure definitions |
| People | All employees and contractors with access to the systems above |
| Locations | None — Meridian is fully remote with no premises under its control |

### 5.3 Outside scope

| Marketing website | Runs in a separate AWS account, holds no customer data, and has no connectivity to the production platform | It carries the Meridian brand and domain. A defacement would damage customer trust even without any data being touched. The separation is confirmed annually to check it still holds |

## 6. The ISMS (Clause 4.4)

Meridian establishes, implements, maintains and continually improves an
Information Security Management System in accordance with ISO/IEC 27001:2022,
operated on a Plan-Do-Check-Act cycle.
| Phase | Clauses | At Meridian |
|---|---|---|
| Plan | 4, 5, 6 | This document; risk methodology (`scales.md`); risk assessment (`R-001`) |
| Do | 7, 8 | Control implementation — `CTL-001` operating in three layers |
| Check | 9 | Automated evidence collection — `collect_evidence.py`, producing dated evidence packs |
| Act | 10 | Findings and corrective action — `F-2026-001`, addressing root cause rather than symptom |