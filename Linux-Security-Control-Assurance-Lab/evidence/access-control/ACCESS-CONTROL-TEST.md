# Access Control Test

## Control Area

Access Control and Privileged Access

## Control Objective

Ensure that Linux users and privileged accounts have appropriate access to the system.

## Test Activities

The assessment reviewed:

- Local user accounts
- User identity information
- Group membership
- Sudo access
- Privileged groups

## Evidence Reviewed

The Linux environment confirmed that the assessment user has membership in the `sudo` and `adm` groups.

The sudo configuration demonstrates that the user has administrative privileges.

## Assessment

Privileged access exists and can be identified through Linux group membership.

The assessment demonstrates the ability to review privileged access, but a complete organizational access approval and periodic review process cannot be established from the local WSL environment alone.

## Control Status

**Partially Effective**

## Risk

Unreviewed or excessive privileged access could increase the risk of unauthorized administrative activity.

## Recommendation

Establish periodic privileged access reviews and document:

- User
- Privileged group
- Business justification
- Approver
- Review date
- Review result

## Closure Criteria

The control can be considered effective when privileged access is reviewed periodically and approval evidence is retained.

## GRC Conclusion

The technical configuration was reviewed and the limitation was documented.

Further governance evidence is required to demonstrate a complete access review process.
