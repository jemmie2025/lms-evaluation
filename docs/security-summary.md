# Moodle Security Decision Summary

Date: 2 November 2026
Decision: Keep the current development image out of production.
Pilot provisioning remains subject to plan approval and security review.

## Triage Outcome

The scan reported 374 critical/high package-level findings.
These are package-CVE pairs, not 374 confirmed exploitable vulnerabilities.

| Disposition | Findings | Required action |
|---|---:|---|
| PHP CLI dependency linkage identified | 19 | Prioritize exposure assessment and remediation |
| Runtime reachability unresolved | 164 | Investigate before accepting or deferring |
| Scoped deferrals documented | 191 | Review the stated conditions and obtain acceptance |

183 findings remain open. The 191 scoped deferrals comprise 189
linux-libc-dev header findings and two zlib findings with a documented
Debian package-specific exception.

CLI linkage does not prove that Moodle's web process invokes the
vulnerable code. No blanket claim that the remaining findings are
unreachable is supported by the evidence.

## Prioritized Actions

1. Test an updated replacement image in isolation, preserving the PoC
   and backups. The report lists fixed targets for five findings:
   libbrotli1 1.0.9-2+deb12u1;
   libexpat1 2.5.0-1+deb12u5;
   libssl3 and openssl 3.0.22-1~deb12u2.
   Confirm target availability and compatibility before rebuilding.
2. Investigate actual web-process linkage, enabled features and
   Moodle/plugin/scheduled-task invocation for the 183 open findings.
3. For applicable findings without fixes, propose restricted inputs,
   reduced privileges, restricted network access or removal of unused
   components. Verify each control against its specific exposure.
4. Assign an owner and review date to every accepted deferral.
   Header-package deferrals do not assess the host kernel.
5. Rescan the replacement image and retest login, course access,
   completion and restore before requesting pilot security approval.

## Evidence and Limits

See [security review](security-review.md) and the
[complete triage ledger](../benchmarks/security/moodle-critical-high-triage.md)
for package-level evidence, reasons and proposed controls.

No remediation or post-remediation scan has been performed.
Controls are proposals, not verified protections.
The current evidence does not establish production readiness.
