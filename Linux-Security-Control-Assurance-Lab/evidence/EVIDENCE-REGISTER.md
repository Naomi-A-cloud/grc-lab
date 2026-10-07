# Evidence Register

## Linux Security Control Assurance Lab

This register identifies the evidence used to support control testing and GRC assessment activities.

| Evidence ID | Evidence | Purpose | Control Area | Status |
|---|---|---|---|---|
| EV-001 | ACCESS-CONTROL-TEST.md | Review Linux user and access configuration | Access Control | Collected |
| EV-002 | AUTHENTICATION-LOG-ANALYSIS.md | Review authentication and privileged activity | Logging / Monitoring | Collected |
| EV-003 | AUDITD-CONTROL-TEST.md | Assess Linux Auditd capability | Security Logging | Tested |
| EV-004 | SIEM-USE-CASES.md | Define security monitoring use cases | Monitoring | Documented |
| EV-005 | LYNIS-ASSESSMENT.md | Assess Linux security posture and hardening | Security Hardening | Assessed |
| EV-006 | EVIDENCE-MANAGEMENT.md | Define evidence handling approach | GRC / Assurance | Documented |

---

## Evidence Lifecycle

Evidence is managed using the following process:

**Collect → Validate → Document → Review → Map to Control → Assess → Retain**

---

## Evidence Quality Principles

Evidence used for control assurance should be:

- Relevant to the control being tested.
- Traceable to the system or process assessed.
- Sufficient to support the assessment conclusion.
- Documented with the date and testing context.
- Retained for future review or audit.
- Clearly linked to findings and remediation activities.

---

## Evidence Limitations

The Auditd assessment has an environment limitation.

Auditd was installed successfully, but the service could not start correctly in the WSL2 environment.

Therefore, the evidence demonstrates:

- Auditd package installation.
- Service startup attempt.
- Service failure.
- Investigation of the failure.
- Documented remediation limitation.

It does **not** demonstrate a fully operational Auditd control.

Further testing is required on a supported Linux virtual machine or physical Linux system.

---

## Evidence-to-Control Traceability

| Control Area | Evidence | Assessment |
|---|---|---|
| Access Control | EV-001 | Partially Effective |
| Authentication Logging | EV-002 | Effective with limitations |
| Security Logging | EV-003 | Not Verified |
| Security Monitoring | EV-004 | Partially Effective |
| Security Hardening | EV-005 | Assessment Completed |

