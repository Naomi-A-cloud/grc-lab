# SIEM Monitoring Use Cases

## Purpose

Document security events that could be monitored by a SIEM platform.

## Use Case 1

### Multiple Failed Login Attempts

Detect repeated failed authentication attempts.

### Risk

Potential unauthorized access attempt.

### Data Source

Linux authentication logs.

### Severity

Medium.

---

## Use Case 2

### Privilege Escalation

Detect unexpected use of elevated privileges.

### Risk

Unauthorized administrative activity.

### Data Source

Audit logs and system logs.

### Severity

High.

---

## Use Case 3

### New User Creation

Detect creation of new user accounts.

### Risk

Unauthorized account creation.

### Data Source

Audit logs.

### Severity

Medium.

## Investigation

Security analysts should review the event, user, timestamp, source, related activity, and determine whether escalation is required.