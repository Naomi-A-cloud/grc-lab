# Risk Register

## Linux Security Control Assurance Lab

| Risk ID | Risk Description | Asset / Process | Likelihood | Impact | Risk Rating | Existing Control | Treatment | Status |
|---|---|---|---|---|---|---|---|---|
| R-001 | Insufficient structured security audit capability may reduce visibility of security-relevant events. | Linux security logging and monitoring | Possible | Moderate | Medium | System journal and authentication logging | Validate Auditd on a supported Linux environment and implement required audit rules | Open |
| R-002 | Excessive or outdated privileged access may increase the risk of unauthorized administrative activity. | Linux privileged accounts | Possible | Moderate | Medium | Sudo group and privileged access review | Perform periodic privileged access reviews and document approvals | Open |
| R-003 | Incomplete account review may result in unauthorized or unnecessary user accounts remaining active. | Linux user accounts | Possible | Moderate | Medium | Local account review | Establish periodic account review and account lifecycle procedures | Open |
| R-004 | Security events may not be consistently monitored or escalated without defined monitoring use cases. | Security monitoring | Possible | Moderate | Medium | System logs and monitoring use cases | Define monitoring requirements and establish alert review procedures | Open |

---

## Risk Treatment Approach

The project uses the following risk treatment process:

**Identify → Assess → Treat → Monitor → Retest → Close**

### R-001 Treatment

Auditd was installed as a remediation action for the security logging gap.

The installation completed successfully, but the Auditd service failed to start in the WSL2 environment.

The failure was investigated and documented.

The risk remains **Open** because the control has not been successfully validated.

### Required Closure Evidence

R-001 can be closed when:

- Auditd starts successfully on a supported Linux environment.
- Required audit rules are loaded.
- Security events are generated.
- Events can be queried.
- Evidence is retained.
- Control testing confirms the control is operating effectively.

---

## Risk Ownership

| Risk Area | Suggested Owner |
|---|---|
| Access Control | IT / Security |
| Privileged Access | IT / Security |
| Security Logging | Security |
| Security Monitoring | Security / GRC |
| Risk Tracking | GRC / Information Security |

---

## Overall Risk Position

The assessment identified several medium-level risks related to access management, logging, and monitoring.

The most significant outstanding technical limitation is the inability to validate Auditd successfully in the current WSL2 environment.

The risk has been documented rather than incorrectly marked as resolved.
