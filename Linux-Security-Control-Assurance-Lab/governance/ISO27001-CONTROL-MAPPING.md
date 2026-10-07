# ISO 27001 Control Mapping

## Project

Linux Security Control Assurance Lab

## Purpose

This document maps the technical security controls tested in the Linux Security Control Assurance Lab to relevant ISO/IEC 27001:2022 Annex A controls.

The mapping connects technical evidence, control testing, identified gaps, risks, and remediation activities.

---

## Control Mapping

| Control Area | ISO/IEC 27001:2022 Control | Evidence | Current Status | Gap / Observation |
|---|---|---|---|---|
| Access Control | A.5.15 Access control | Access control test | Partially Effective | Access permissions require periodic review and documented validation. |
| Identity Management | A.5.16 Identity management | User account evidence | Partially Effective | User account configuration was reviewed; further lifecycle testing is required. |
| Access Rights | A.5.18 Access rights | Privileged access evidence | Partially Effective | Sudo membership and privileged access require continued review. |
| Logging | A.8.15 Logging | Authentication and sudo logs | Partially Effective | System logging is available, but dedicated audit logging could not be fully validated in WSL2. |
| Monitoring Activities | A.8.16 Monitoring activities | Authentication log analysis | Partially Effective | Security events can be reviewed, but structured audit monitoring requires further validation. |

---

## Key Finding

The primary control gap identified during the assessment is the inability to successfully operate and verify the Linux Audit subsystem in the current WSL2 environment.

Auditd was installed as part of remediation. However, the service failed to start and the audit subsystem could not be successfully queried.

The failure was investigated and documented rather than treated as a successful control implementation.

---

## GRC Assessment

### Initial Condition

Dedicated Linux audit monitoring was not available.

### Evidence Collection

Evidence was collected from:

- Linux system information
- User and privileged access configuration
- Authentication and sudo activity
- Auditd installation and service status
- Auditd service logs

### Control Testing

The available evidence was reviewed to determine whether the security logging and monitoring control could be considered effective.

### Finding

The Linux system provides system journal logging and records privileged activity, but dedicated audit monitoring could not be verified in the WSL2 environment.

### Risk

Insufficient structured audit monitoring may reduce the ability to consistently detect, investigate, and demonstrate security-relevant activity.

### Risk Rating

Medium

### Treatment

Remediation was attempted by installing and configuring the Auditd package.

The remediation could not be fully validated because the WSL2 environment could not successfully start the Auditd service.

### Closure Requirement

The control should only be marked fully effective after testing on a supported Linux virtual machine or physical Linux system confirms:

1. Auditd starts successfully.
2. Audit rules are loaded.
3. Security events are generated.
4. Events can be queried.
5. Evidence is retained.
6. Control testing results are documented.

---

## Conclusion

The control is currently assessed as **Partially Effective**.

The project demonstrates an evidence-based control assurance process:

**Evidence Collection → Control Testing → Gap Identification → Risk Assessment → Remediation → Retesting → Closure Criteria**

The current WSL2 limitation is documented as an environmental constraint rather than being treated as a successful remediation.
