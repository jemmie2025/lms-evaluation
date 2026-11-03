# Moodle Security Update Results

Date: 3 November 2026

## Decision
Keep the updated image as a test candidate. It has not replaced
the running Moodle application and is not approved for production.

## Verified Results
Comparable scans used Trivy 0.76.1, the same vulnerability database
and the same operating-system package scan settings.

| Severity | Original image | Updated candidate | Net reduction |
|---|---:|---:|---:|
| Critical | 12 | 11 | 1 |
| High | 336 | 332 | 4 |
| Critical and high combined | 348 | 343 | 5 |

Four packages were updated: libbrotli1, libexpat1, libssl3 and openssl.
PHP startup and module listing passed.

## Meaning for Sponsors
The updates reduced reported critical/high findings by five.
The remaining 343 findings require further assessment; they are
not 343 confirmed exploitable vulnerabilities.

The candidate scan lists no fixed versions for those remaining
findings. This does not establish that remediation is impossible.

The earlier total of 374 came from a previous scan. Its difference
from the fresh baseline of 348 is not credited to these updates.

## Outstanding Work
- Test Moodle login, course access and completion with the candidate.
- Review remaining findings and document justified deferrals,
  required controls and unresolved exposure.
- Obtain security review and pilot-plan approval before provisioning.

Development-package removal was simulated but has not been applied
as part of this work. No additional reduction is claimed.
