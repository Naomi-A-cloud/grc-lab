"""
CTL-001, Layer 2 — refuse a public bucket before it is built.

WHAT THIS DOES
    Reads a Terraform plan (Terraform's own description of what it is about to
    change, saved as JSON) and looks for anything that would make an S3 bucket
    public. If it finds something, it reports it and exits with an error, which
    stops the deployment.

WHY IT EXISTS
    Control CTL-001 says no bucket may be publicly readable. This is the part
    that stops a public bucket ever being created.

HOW TO RUN IT
    python check_public_buckets.py plans/bad-plan.json
    python check_public_buckets.py plans/good-plan.json
"""

import json
import sys


# ---------------------------------------------------------------------------
# The rules. Kept at the top so a reader can see what we check without
# reading any code.
# ---------------------------------------------------------------------------

# S3 ACLs that let people outside the account read or write.
# "authenticated-read" is included because it means ANY logged-in AWS user
# anywhere in the world -- not just ours. That surprises most people.
PUBLIC_ACLS = [
    "public-read",
    "public-read-write",
    "authenticated-read",
]

# The four Block Public Access switches. All four must be on.
BLOCK_PUBLIC_ACCESS_SETTINGS = [
    "block_public_acls",
    "block_public_policy",
    "ignore_public_acls",
    "restrict_public_buckets",
]


def load_plan(path):
    """Open the Terraform plan file and turn it into Python data."""
    with open(path) as file:
        return json.load(file)


def resources_being_created_or_changed(plan):
    """
    Pull out the resources this plan will create or update.

    We deliberately ignore resources being DELETED. A bucket that is being
    destroyed cannot leak anything, and flagging it would produce a failure
    the engineer cannot act on. Controls that cry wolf get switched off.
    """
    wanted = []

    for change in plan.get("resource_changes", []):
        actions = change.get("change", {}).get("actions", [])

        if "create" in actions or "update" in actions:
            wanted.append(change)

    return wanted


# ---------------------------------------------------------------------------
# One function per way a bucket can become public.
# Each returns a list of problems it found.
# ---------------------------------------------------------------------------


def check_acls(resources):
    """Way 1: a bucket ACL that grants access to people outside Meridian."""
    problems = []

    for resource in resources:
        if resource["type"] != "aws_s3_bucket_acl":
            continue

        acl = resource["change"]["after"].get("acl")

        if acl in PUBLIC_ACLS:
            problems.append({
                "resource": resource["address"],
                "problem": f"Bucket ACL is set to '{acl}', which allows access from outside Meridian",
                "fix": "Set acl = \"private\" and grant access with an IAM policy instead",
            })

    return problems


def check_block_public_access(resources):
    """Way 2: one of the four account safety switches is turned off."""
    problems = []

    for resource in resources:
        if resource["type"] != "aws_s3_bucket_public_access_block":
            continue

        settings = resource["change"]["after"]

        for setting_name in BLOCK_PUBLIC_ACCESS_SETTINGS:
            # We use .get() with a default of False on purpose. If the setting
            # is missing entirely, that is NOT safe -- it must count as off.
            # Assuming a missing setting is fine is a real and common bug.
            value = settings.get(setting_name, False)

            if value is not True:
                problems.append({
                    "resource": resource["address"],
                    "problem": f"Block Public Access setting '{setting_name}' is not switched on",
                    "fix": f"Set {setting_name} = true",
                })

    return problems


def check_bucket_policies(resources):
    """Way 3: a bucket policy that says 'anyone is allowed'."""
    problems = []

    for resource in resources:
        if resource["type"] != "aws_s3_bucket_policy":
            continue

        # The policy is stored as text, so we have to read it as JSON first.
        policy_text = resource["change"]["after"].get("policy", "{}")
        policy = json.loads(policy_text)

        for statement in policy.get("Statement", []):
            if statement.get("Effect") != "Allow":
                continue  # A "Deny" statement is a guardrail, not a problem.

            if is_anyone(statement.get("Principal")):
                problems.append({
                    "resource": resource["address"],
                    "problem": "Bucket policy allows access to any principal (\"*\") -- meaning the whole internet",
                    "fix": "Name the specific AWS roles or accounts that need access",
                })

    return problems


def is_anyone(principal):
    """
    Work out whether a policy's Principal means 'literally anyone'.

    AWS lets this be written several ways, which is exactly the sort of detail
    that makes a hand-written check unreliable and an automated one valuable.
    """
    if principal == "*":
        return True

    if isinstance(principal, dict):
        aws = principal.get("AWS")

        if aws == "*":
            return True

        if isinstance(aws, list) and "*" in aws:
            return True

    return False


# ---------------------------------------------------------------------------
# Putting it together
# ---------------------------------------------------------------------------


def check_plan(path):
    """Run every check against one plan file and return what we found."""
    plan = load_plan(path)
    resources = resources_being_created_or_changed(plan)

    problems = []
    problems += check_acls(resources)
    problems += check_block_public_access(resources)
    problems += check_bucket_policies(resources)

    return problems


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_public_buckets.py <plan.json>")
        return 1

    path = sys.argv[1]
    problems = check_plan(path)

    print()
    print(f"CTL-001 Layer 2 — checking {path}")
    print("-" * 70)

    if not problems:
        print("PASS — nothing in this plan would make a bucket public.")
        print()
        return 0

    for problem in problems:
        print(f"BLOCKED  {problem['resource']}")
        print(f"         {problem['problem']}")
        print(f"         Fix: {problem['fix']}")
        print()

    print(f"{len(problems)} problem(s) found. This deployment is blocked.")
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
