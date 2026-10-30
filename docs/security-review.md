# Moodle Initial Security Assessment

Assessment date: 30 October 2026.

## Scope

The local PoC uses Moodle 4.5.15+ and PHP 8.3.36 on Linux.
Trivy 0.76.1 scanned the exported webserver image and identified
Debian 12.15. The report covers detected image packages, not a
complete audit of Moodle, plugins, configuration or the Windows host.

## Scan Results

| Severity | Reported findings |
|---|---:|
| Critical | 13 |
| High | 361 |
| Medium | 1,807 |
| Low | 1,315 |
| Unknown | 17 |
| Total | 3,513 |

These are package-level findings, not necessarily unique CVEs or
confirmed exploitable vulnerabilities in this deployment.

## Critical Findings and Fix Information

| Package | Findings | Status in report |
|---|---:|---|
| libbrotli1 | 1 | Fixed version: 1.0.9-2+deb12u1; installed: 1.0.9-2+b6 |
| libsqlite3-0 | 1 | Affected; no fixed version listed |
| libunbound8 | 5 | Affected; no fixed version listed |
| linux-libc-dev | 2 | Affected; no fixed version listed |
| libxml2 | 1 | Fix deferred |
| openssh-client | 1 | Fix deferred |
| zlib1g and zlib1g-dev | 2 | Will not fix; applicability requires review |

A fixed status means a corrected package is available, not installed.
Missing fix versions and deferred fixes require vendor-advisory review.

## Conclusion and Follow-up

The current development image is not approved for production.
Validate critical and high findings against vendor advisories,
assess runtime exposure, then test an updated production image.
Preserve the existing PoC and backups during remediation.

No fixes were applied and no post-remediation scan was performed.
This scan does not certify Moodle or PHP as secure, establish the
cause of laptop slowness, or demonstrate that an attack occurred.
The specific PHP attack referenced by the requester remains unidentified.

Evidence: [Trivy report](../benchmarks/security/moodle-image-trivy.txt).
