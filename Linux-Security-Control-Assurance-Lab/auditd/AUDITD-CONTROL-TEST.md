# Auditd Control Test

## Control Area

Security Logging and Audit Monitoring

## Control Objective

Maintain reliable audit records for security-relevant system activity to support monitoring, investigation, accountability, and control assurance.

## Test Procedure

1. Check whether Auditd is installed.
2. Check the Auditd service status.
3. Review Auditd service logs.
4. Check whether the audit subsystem can be queried.
5. Determine the control status.
6. Document remediation and closure requirements.

## Initial Finding

Auditd was initially not installed in the Linux environment.

## Remediation Performed

The following packages were installed:

- auditd
- audispd-plugins

The installation completed successfully.

## Verification Result

The Auditd service was checked after installation.

The service failed to start successfully.

The service logs reported:

`Unable to set initial audit startup state to 'enable', exiting`

The `auditctl -s` command also returned an error while processing parameters.

## Environment Limitation

The assessment was performed in Microsoft WSL2 using Ubuntu.

The Linux audit subsystem required by Auditd could not be successfully initialized in this environment.

This means Auditd installation was completed, but operational control effectiveness could not be verified.

## Control Status

**Not Verified**

## Risk Rating

**Medium**

## Risk

Without successfully validated audit monitoring, security-relevant activity may not be consistently captured and available for investigation and accountability.

## Recommended Remediation

Repeat Auditd implementation and testing on a supported Linux virtual machine or physical Linux system.

## Closure Criteria

The control can be considered effective when:

- Auditd starts successfully.
- Audit rules are loaded.
- Security events are generated.
- Events can be queried.
- Audit evidence is retained.
- Control testing confirms effective operation.

## GRC Conclusion

The remediation attempt and service failure were documented as evidence.

The control was not marked effective without sufficient evidence.

**Control Status: Not Verified**
