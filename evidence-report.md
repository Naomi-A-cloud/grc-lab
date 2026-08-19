# Evidence — CTL-001 (no public storage)

- **Control:** CTL-001 — No S3 bucket may be publicly accessible
- **Checked at:** 2026-08-19T14:26:47.586600+00:00
- **AWS account:** 111122223333
- **Buckets checked:** 3
- **Passed:** 3  ·  **Failed:** 0
- **Fingerprint:** `47d53d434b8b08e4e150679f37d07da998e3e1a4573f97531d7d23585f771dce`

> Source: saved snapshot -- NOT a live AWS account, so this is a demonstration and not real audit evidence

## What was found

| Bucket | Built by | Data | Result |
|---|---|---|---|
| `meridian-clinical-data` | terraform | restricted | PASS |
| `meridian-reports` | terraform | restricted | PASS |
| `meridian-temp-incident-20260814` | console | restricted | PASS |
