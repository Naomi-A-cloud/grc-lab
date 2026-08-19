"""
CTL-001, Layer 3 — check the real account, and save proof that we checked.

WHAT THIS DOES
    Looks at every bucket that actually exists in the AWS account and checks
    whether it is public. Then it writes an "evidence pack" -- a saved record
    of what was checked, when, and what was found.

WHY IT IS DIFFERENT FROM LAYER 2
    Layer 2 (check_public_buckets.py) reads a Terraform plan. It only ever
    sees things built through the pipeline.

    This one looks at what is REALLY in the account, including buckets someone
    created by hand in the AWS console. Those never touch the pipeline, so
    Layer 2 is blind to them.

WHY WE SAVE AN EVIDENCE PACK
    Running a check proves nothing later. In three months an auditor will ask
    "how do you know this control was working in August?" and you need a
    record, not a memory.

HOW TO RUN IT
    python collect_evidence.py
"""

import hashlib
import json
from datetime import datetime, timezone


SNAPSHOT_FILE = "account-snapshot.json"

BLOCK_PUBLIC_ACCESS_SETTINGS = [
    "block_public_acls",
    "block_public_policy",
    "ignore_public_acls",
    "restrict_public_buckets",
]

PUBLIC_ACLS = ["public-read", "public-read-write", "authenticated-read"]


def check_one_bucket(bucket):
    """Look at a single bucket and return a list of what is wrong with it."""
    problems = []

    # Are all four safety switches on?
    settings = bucket.get("public_access_block", {})

    for setting_name in BLOCK_PUBLIC_ACCESS_SETTINGS:
        if settings.get(setting_name, False) is not True:
            problems.append(f"Block Public Access setting '{setting_name}' is off")

    # Is the ACL open to people outside Meridian?
    if bucket.get("acl") in PUBLIC_ACLS:
        problems.append(f"Bucket ACL is '{bucket['acl']}'")

    # Does the bucket policy let anyone in?
    if bucket.get("policy_allows_anyone"):
        problems.append("Bucket policy allows access to any principal (\"*\")")

    return problems


def fingerprint(data):
    """
    Make a short fingerprint of some data.

    If even one character of the data changes, this fingerprint changes
    completely. That is how you can tell later whether an evidence file has
    been edited since it was written.
    """
    as_text = json.dumps(data, sort_keys=True)
    return hashlib.sha256(as_text.encode()).hexdigest()


def collect():
    with open(SNAPSHOT_FILE) as file:
        snapshot = json.load(file)

    buckets = snapshot["buckets"]
    results = []

    for bucket in buckets:
        problems = check_one_bucket(bucket)

        results.append({
            "bucket": bucket["name"],
            "created_by": bucket.get("created_by", "unknown"),
            "data_classification": bucket.get("data_classification", "unknown"),
            "result": "pass" if not problems else "fail",
            "problems": problems,
        })

    failed = [r for r in results if r["result"] == "fail"]

    evidence_pack = {
        "control": "CTL-001",
        "control_statement": "No S3 bucket may be publicly accessible",
        "layer": "3 - detective check of the live account",

        # WHO, WHAT, WHEN. An auditor asks all three about any evidence.
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "aws_account": snapshot["collected_from_account"],
        "collected_by": "automated check (collect_evidence.py)",
        "source": "saved snapshot -- NOT a live AWS account, so this is a "
                  "demonstration and not real audit evidence",

        # POPULATION. The first thing an auditor asks about any finding is
        # "out of how many?" A list of failures with no total means nothing.
        "buckets_checked": len(buckets),
        "buckets_passed": len(buckets) - len(failed),
        "buckets_failed": len(failed),

        "results": results,
    }

    evidence_pack["fingerprint_sha256"] = fingerprint(results)

    return evidence_pack


def write_readable_report(pack):
    """Write a version a human (or an auditor) can actually read."""
    lines = []

    lines.append("# Evidence — CTL-001 (no public storage)")
    lines.append("")
    lines.append(f"- **Control:** {pack['control']} — {pack['control_statement']}")
    lines.append(f"- **Checked at:** {pack['checked_at_utc']}")
    lines.append(f"- **AWS account:** {pack['aws_account']}")
    lines.append(f"- **Buckets checked:** {pack['buckets_checked']}")
    lines.append(f"- **Passed:** {pack['buckets_passed']}  ·  **Failed:** {pack['buckets_failed']}")
    lines.append(f"- **Fingerprint:** `{pack['fingerprint_sha256']}`")
    lines.append("")
    lines.append(f"> Source: {pack['source']}")
    lines.append("")

    lines.append("## What was found")
    lines.append("")
    lines.append("| Bucket | Built by | Data | Result |")
    lines.append("|---|---|---|---|")

    for r in pack["results"]:
        mark = "PASS" if r["result"] == "pass" else "**FAIL**"
        lines.append(
            f"| `{r['bucket']}` | {r['created_by']} | {r['data_classification']} | {mark} |"
        )

    lines.append("")

    failures = [r for r in pack["results"] if r["result"] == "fail"]

    if failures:
        lines.append("## Problems needing a decision")
        lines.append("")

        for r in failures:
            lines.append(f"### {r['bucket']}")
            lines.append("")
            for problem in r["problems"]:
                lines.append(f"- {problem}")
            lines.append("")
            lines.append(f"*Built by: {r['created_by']}. "
                         f"Holds `{r['data_classification']}` data.*")
            lines.append("")
            lines.append("**Decision needed from the control owner:** fix it, "
                         "or write down why the risk is being accepted and until when.")
            lines.append("")

    with open("evidence-report.md", "w") as file:
        file.write("\n".join(lines))


def main():
    pack = collect()

    with open("evidence-pack.json", "w") as file:
        json.dump(pack, file, indent=2)

    write_readable_report(pack)

    print()
    print("CTL-001 Layer 3 — checking the live account")
    print("-" * 70)
    print(f"Buckets checked : {pack['buckets_checked']}")
    print(f"Passed          : {pack['buckets_passed']}")
    print(f"Failed          : {pack['buckets_failed']}")
    print()

    for r in pack["results"]:
        if r["result"] == "fail":
            print(f"FAIL  {r['bucket']}   (built by: {r['created_by']})")
            for problem in r["problems"]:
                print(f"        - {problem}")
            print()

    print(f"Fingerprint: {pack['fingerprint_sha256'][:32]}...")
    print()
    print("Saved: evidence-pack.json and evidence-report.md")
    print()


if __name__ == "__main__":
    main()
