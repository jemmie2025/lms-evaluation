# Moodle Security Assessment and Triage

Original scan: 30 October 2026. Triage review: 2 November 2026.

## Decision

The development image remains unsuitable for production approval. The review accounts for all 13 critical and 361 high package-CVE findings. It identifies concrete patch targets and narrow evidence-supported deferrals; it does not claim that all exploit paths have been tested or that remediation is complete.

## Scope and evidence

The PoC uses Moodle 4.5.15+ and PHP 8.3.36. Trivy 0.76.1 scanned the exported webserver image and identified Debian 12.15. The runtime evidence was collected from the isolated second recovery stack using the same original webserver image. All 374 critical/high installed-package versions match the scan after normalizing Debian architecture suffixes.

- [Original image scan](../benchmarks/security/moodle-image-trivy.txt).
- [Runtime evidence](../benchmarks/security/moodle-runtime-evidence.txt): PHP CLI modules, Apache configuration module listing, PHP CLI shared-library dependencies and installed packages.
- [Complete critical/high ledger](../benchmarks/security/moodle-critical-high-triage.md): every package-CVE pair, scan line, status, version, disposition and next action.

The evidence does not include an image-digest capture, a live Apache process memory map, tracing of Moodle/plugin/job subprocesses or adversarial exploit tests. Matching package versions strengthens the comparison but does not independently prove image identity. PHP CLI evidence must not be presented as a complete web-SAPI reachability test.

## Scan totals

| Severity | Reported findings |
|---|---:|
| Critical | 13 |
| High | 361 |
| Medium | 1,807 |
| Low | 1,315 |
| Unknown | 17 |
| Total | 3,513 |

These are package-level findings, not unique CVEs or confirmed exploitable paths. The detailed ledger covers critical and high findings only; other severities remain in the original scan.

## Disposition of all critical/high findings

| Disposition | Critical | High | Total | Meaning |
|---|---:|---:|---:|---|
| A1: linked runtime component | 3 | 16 | 19 | Resolved by PHP CLI dynamic linkage; prioritize mitigation and call-path review. Exploitability not established. |
| A2: actionable investigation | 6 | 158 | 164 | Installed; insufficient evidence to prove unused or unreachable. Keep open for removal, patching or further tracing. |
| D1: scoped runtime deferral | 2 | 187 | 189 | linux-libc-dev userspace headers are not executable kernel code in the image. Host kernel assessment remains separate. |
| D2: vendor-supported exception | 2 | 0 | 2 | Specific Debian zlib/MiniZip source-package mapping; affected code is not built into these binaries. |
| Total | 13 | 361 | 374 | No finding omitted from the ledger. |

A1 and A2 are open work, not accepted residual risks. These counts do not reduce the scanner's raw totals. There is no blanket "development package" or "not used by Moodle" dismissal.

## Patch targets available in this scan

Five critical/high package-CVE pairs have fixed versions in the report. Debian's tracker corroborates these targets as of the review date. These are package targets for a rebuilt isolated candidate, not changes applied to the current PoC.

| Package | Installed | Debian bookworm target, or a newer compatible security version | Findings addressed |
|---|---|---|---|
| libbrotli1 | 1.0.9-2+b6 | 1.0.9-2+deb12u1 | CVE-2026-111497 (critical) |
| libexpat1 | 2.5.0-1+deb12u4 | 2.5.0-1+deb12u5 | CVE-2025-59375 and CVE-2026-77214 (high) |
| libssl3 | 3.0.22-1~deb12u1 | 3.0.22-1~deb12u2 | CVE-2026-84782 (high) |
| openssl | 3.0.22-1~deb12u1 | 3.0.22-1~deb12u2 | CVE-2026-84782 (high) |

Brotli decoder libraries appear in PHP CLI linkage through the dependency tree. Treat this as actionable even without Apache mod_brotli: compressed outbound responses can be a distinct input path, whose use must be assessed. OpenSSL's cited CVE concerns DTLS; library linkage alone does not establish that this deployment invokes DTLS. Expat is installed but not shown in the captured PHP CLI linkage: patch availability still warrants an update rather than an unsupported exception.

## Critical findings without a listed bookworm fix

| Package / CVEs | Evidence and disposition | Proposed controls until removal or validated remediation |
|---|---|---|
| libsqlite3-0: CVE-2025-7458 | A1. SQLite library linked by PHP CLI; sqlite3 and pdo_sqlite enabled. PostgreSQL as Moodle's database does not prove SQLite unreachable. Debian describes a crafted-SQL prerequisite. | Prevent untrusted SQL execution; audit plugins/tools using SQLite; disable unnecessary extensions in a candidate image, and determine whether the linked library can actually be removed. Disablement alone does not remove linkage. |
| libxml2: CVE-2026-6653 | A1. Linked library, with DOM, XML, SOAP and related PHP modules enabled. The scan says fix_deferred, not fixed. | Restrict untrusted XML import/integration features pending review; enforce bounded input size and processing resources, and assess external entity/network handling in actual parser call sites. Size limits alone do not eliminate a parser memory-safety defect. |
| libunbound8: CVE-2026-33278, CVE-2026-42960, CVE-2026-50252, CVE-2026-81642, CVE-2026-82717 | A2. Installed; absent from captured PHP CLI dependency list. That does not exclude extension/tool/job consumers or prove no resolver use. | Identify consumers and configuration, remove unused resolver tooling/library in the final image, or restrict DNS to trusted resolvers with enforced egress policy. Require specific call-path evidence before approving deferral. |
| openssh-client: CVE-2026-60002 | A2. Installed client; no captured evidence excludes invocation by jobs or tools. A missing SSH server is irrelevant to this client-side issue. | Remove SSH tooling if not required; prohibit application-triggered SSH and enforce egress restrictions until verified. Confirm actual necessity before accepting any exception. |

"No listed fix" refers to the supplied scan and checked bookworm advisory status, not a claim that no upstream or other-distribution fix exists. Do not install packages from Debian unstable into the current image as a shortcut. Test a coherent supported base-image upgrade or remove unnecessary functionality.

## Evidence-supported deferrals

### D1: linux-libc-dev — 2 critical and 187 high

The installed package is linux-libc-dev 6.1.190-1. Debian describes this package as Linux userspace development headers. Headers do not execute a kernel inside the Moodle image; the image package version cannot establish the vulnerability status of Docker Desktop's Linux VM/WSL kernel.

Defer these package mappings from the Moodle application-runtime patch gate, while retaining every CVE in the ledger. Exclude build headers from the final runtime image where possible. Separately inventory and update Docker Desktop/WSL and assess the actual running kernel. This scoped decision is not a finding that the host is safe, nor a complete CVE-by-CVE kernel advisory validation. Reassess if the runtime compiles or consumes these headers.

### D2: zlib1g and zlib1g-dev — CVE-2023-45853

Both packages are installed at 1:1.2.13.dfsg-1. Debian's CVE notes state that the affected contrib/minizip code is not built for this bookworm source version, so the affected source code is not provided by these binary packages. This supports deferring these two package findings despite zlib being linked by PHP.

This exception is limited to this CVE and these Debian binaries. It does not cover separately bundled MiniZip, custom builds, Python packages or other zlib CVEs. Recheck if package provenance or version changes.

## Remaining high findings and runtime limits

All 361 high package-CVE pairs appear in the ledger. Beyond the header deferral, 16 high findings affect libraries resolved by PHP CLI: libsqlite3-0, libxml2, libssl3, libcurl4, libldap-2.5-0 and libtinfo6. libtinfo linkage can be specific to CLI/readline, so its web-SAPI applicability is not assumed. The remaining 158 high findings stay open as A2.

The four Apache packages account for 28 high findings representing seven repeated CVEs. Their scan descriptions identify mod_heartmonitor, mod_charset_lite, mod_rewrite, mod_vhost_alias, mod_xml2enc, mod_proxy_uwsgi and mod_auth_digest. None appears in the captured module listing. However, apache2ctl emitted APACHE_DOCUMENT_ROOT warnings, so this configuration invocation is not treated as definitive evidence of the live server's exact configuration. These findings remain A2 until the running server's modules/configuration and relevant advisory prerequisites are verified. Do not count all Apache findings as reachable just because Apache runs, or as unreachable just because this listing omits a module.

Other A2 packages include command-line clients, document/image processors, MariaDB client components, system utilities and supporting libraries. Installed package names, a PostgreSQL deployment and a single dependency listing cannot exclude plugins, cron tasks or subprocess invocation. Investigate/remove unused components and restrict high-risk document conversion and outbound-network features until checked; the ledger preserves each affected pair and vendor tracker link.

## Remediation and release checks

1. Preserve the current PoC, original scan and private backups. Build a separate candidate from a maintained, compatible production-oriented base; pin its digest and record the installed package inventory.
2. Include the Brotli, Expat and OpenSSL fixes above or newer compatible Debian security versions. Minimize build tooling and unused database/SSH/document-processing components; do not run a blind package purge against the working PoC.
3. For each remaining no-fix A1/A2 finding, document its consumer, vulnerable input/call-path prerequisites, mitigation owner and review deadline. A vendor status of affected, fix_deferred or will_not_fix is not itself a risk acceptance.
4. Validate controls on the candidate: localhost-only access for local tests; authenticated pilot access, least privilege, resource limits and enforced egress policy for any later approved pilot. Proposed controls are not asserted to be deployed or tested.
5. Test administrator login, course/lesson delivery, learner activity/course completion, scheduled tasks and backup/restore on the candidate. Test independent learner authentication separately from administrator impersonation.
6. Rescan the exact candidate digest, compare every critical/high pair with this ledger, and retain fixed/removed/no-fix evidence. Obtain explicit review of remaining A1/A2 risks before any pilot provisioning.

No package fixes, candidate-image rebuild, exploit test or post-remediation scan has been performed as part of this triage. These remain completion criteria for remediation. Email delivery, production readiness and the Windows/WSL host are not certified. The evidence does not establish that an attack occurred or identify the requester's specific PHP attack.

## Primary references

Reviewed 2 November 2026. The ledger supplies a Debian tracker link for each finding; that link is a follow-up reference, not a claim that every linked advisory has been individually read.

- [Debian linux-libc-dev package description](https://packages.debian.org/bookworm/linux-libc-dev).
- [Debian zlib/MiniZip CVE-2023-45853 notes](https://security-tracker.debian.org/tracker/CVE-2023-45853).
- [Brotli CVE-2026-111497 and bookworm fix](https://security-tracker.debian.org/tracker/CVE-2026-111497).
- [Expat CVE-2025-59375](https://security-tracker.debian.org/tracker/CVE-2025-59375) and [CVE-2026-77214](https://security-tracker.debian.org/tracker/CVE-2026-77214).
- [OpenSSL CVE-2026-84782](https://security-tracker.debian.org/tracker/CVE-2026-84782).
- [SQLite CVE-2025-7458](https://security-tracker.debian.org/tracker/CVE-2025-7458), [libxml2 CVE-2026-6653](https://security-tracker.debian.org/tracker/CVE-2026-6653), and [OpenSSH client CVE-2026-60002](https://security-tracker.debian.org/tracker/CVE-2026-60002).
- Unbound: [CVE-2026-33278](https://security-tracker.debian.org/tracker/CVE-2026-33278), [CVE-2026-42960](https://security-tracker.debian.org/tracker/CVE-2026-42960), [CVE-2026-50252](https://security-tracker.debian.org/tracker/CVE-2026-50252), [CVE-2026-81642](https://security-tracker.debian.org/tracker/CVE-2026-81642), [CVE-2026-82717](https://security-tracker.debian.org/tracker/CVE-2026-82717).
