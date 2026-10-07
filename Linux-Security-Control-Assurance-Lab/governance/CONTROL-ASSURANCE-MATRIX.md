# Control Assurance Matrix

## Linux Security Control Assurance Lab

| ID | Control | Test Performed | Evidence | Result | Risk | Remediation | Closure Criteria |
|---|---|---|---|---|---|---|---|
| CA-001 | User Access Control | Reviewed Linux user accounts and account attributes | ACCESS-CONTROL-TEST.md | Partially Effective | Medium | Perform periodic account review | Approved users and account status documented |
| CA-002 | Privileged Access | Reviewed sudo access and privileged groups | ACCESS-CONTROL-TEST.md | Partially Effective | Medium | Review privileged memberships periodically | Privileged access approved and documented |
| CA-003 | Authentication Logging | Reviewed authentication and sudo activity | AUTHENTICATION-LOG-ANALYSIS.md | Effective with limitations | Medium | Continue log monitoring and review | Security events consistently captured and reviewed |
| CA-004 | Security Logging | Tested availability of Linux audit capability | AUDITD-CONTROL-TEST.md | Not Verified | Medium | Validate Auditd on supported Linux environment | Auditd operational and producing evidence |
| CA-005 | Security Monitoring | Reviewed security monitoring and SIEM use cases | SIEM-USE-CASES.md | Partially Effective | Medium | Implement defined monitoring use cases | Monitoring requirements mapped to alerts and evidence |
| CA-006 | Vulnerability Assessment | Reviewed Linux security posture using Lynis | LYNIS-ASSESSMENT.md | Assessment Completed | Medium | Track identified hardening opportunities | Findings reviewed and remediation tracked |

---

## Assurance Status Definitions

### Effective

Evidence demonstrates that the control is implemented and operating as expected.

### Partially Effective

The control exists or produces useful evidence, but weaknesses or limitations remain.

### Not Verified

The control could not be reliably tested or confirmed in the current environment.

### Ineffective

The control is absent or does not operate as required.

---

## Overall Assessment

**Overall Control Assurance Status: PARTIALLY EFFECTIVE**

The assessment demonstrates a structured control assurance process using technical evidence, control testing, risk assessment, remediation tracking, and defined closure criteria.

The primary outstanding issue is validation of dedicated Linux audit monitoring on a supported Linux environment.

---

## Assurance Method

The project follows this lifecycle:

1. Define the control objective.
2. Collect technical evidence.
3. Test the control.
4. Identify gaps.
5. Assess risk.
6. Define remediation.
7. Retest the control.
8. Document the result.
9. Define closure criteria.
10. Track the control until closure.

