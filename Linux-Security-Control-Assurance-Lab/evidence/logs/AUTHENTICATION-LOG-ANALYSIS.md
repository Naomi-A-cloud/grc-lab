# Authentication Log Analysis

## Control Area

Authentication Monitoring and Security Logging

## Control Objective

Detect and review authentication and privileged activity to support security monitoring and investigation.

## Evidence Reviewed

The Linux system journal was reviewed for:

- Authentication activity
- Sudo activity
- Privilege escalation
- Session activity
- System authentication events

## Key Observation

The system journal contained sudo activity showing privileged commands executed by the assessment user.

Examples included administrative package management commands executed through sudo.

This demonstrates that privileged activity is being recorded by the system journal.

## Assessment

Authentication and privileged activity can be identified and reviewed.

However, dedicated Auditd functionality could not be successfully validated in the WSL2 environment.

## Control Status

**Effective with Limitations**

## Risk

If structured audit monitoring is not available, investigation and long-term evidence collection may be less consistent.

## Recommendation

Continue system log review and validate dedicated Auditd monitoring on a supported Linux environment.

## Closure Criteria

The control should be considered fully effective when:

- Authentication events are consistently captured.
- Privileged activity is logged.
- Security events can be reviewed.
- Audit monitoring is operational.
- Monitoring evidence is retained.

## GRC Conclusion

The system journal provides useful authentication and privileged activity evidence.

The Auditd limitation remains documented as an outstanding control assurance issue.
