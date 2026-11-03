# Moodle Pilot Plan

Prepared by: Jemimah Godswill
Status: Proposal awaiting Friendy's approval.
No pilot provisioning will begin before agreement.

## Scope

Propose 10 internal learners, one course and a two-week pilot.
Friendy will confirm the cohort, dates and operational owner.
Client-facing access is outside this initial pilot.

## Hosting

Propose a dedicated managed Linux VM in an approved company account.
Provider, region, budget and domain require Friendy's agreement.
An initial 2 vCPU and 4 GiB RAM allocation is proposed for validation,
not established sizing.

Use HTTPS, persistent storage, restricted administration and private
database access. Select a supported Moodle release and compatible plugins.
Review the deployment image, address applicable security findings,
document accepted exceptions and rescan before learner onboarding.

## SSO

Propose Keycloak SAML through a compatible Moodle authentication plugin.
Confirm the identity provider and responsible identity administrator.
Test independent login, logout, account matching, learner permissions
and access revocation. Protect a local recovery administrator account.
SSO has not yet been implemented or tested.

## Backups

Propose nightly consistent backups of the database, moodledata,
configuration and application/plugin version records.
Store encrypted copies in a separate company-controlled object-storage
bucket off the VM. Confirm the provider, bucket, access and key ownership.

Proposed retention: seven daily and four weekly backups.
Proposed RPO: 24 hours. Proposed RTO: four hours.
These targets require approval and measurement.
Before launch, restore an off-host backup in isolation and verify users,
course content and completion records.

## Monitoring

Propose Prometheus with a compatible exporter for container CPU/RAM,
restarts and host disk usage. Use Loki for application/container logs.
Confirm whether existing company monitoring can be reused.

Monitor HTTPS availability, Moodle scheduled tasks and backup success.
Agree alert thresholds, recipients and escalation arrangements.
Test alert delivery and restrict access to logs before launch.

## Change Control

Record image digests, Moodle/plugin versions, configuration, resource
limits, dataset and test scripts before testing.
Keep these unchanged between comparable runs.
Record each change and establish a new baseline after changes.
Commit each completed deployment, measurement run and documentation unit.

## Proposed Success Criteria

- All 10 learners authenticate independently and access the course.
- At least 9 learners complete the course within two weeks.
- Completion records survive restart and isolated backup restoration.
- Recovery meets the approved RPO and RTO.
- A representative 10-user concurrent test achieves p95 page-response
  time below three seconds and HTTP errors below 1%.
- Monitoring and backup alerts reach the assigned operator.
- No unresolved security issue exceeds the approved risk tolerance.

Agree test pages, duration and measurement method before execution.
Passing the pilot supports a separate production-readiness review;
production promotion requires explicit approval.

## Pause and Revert

Pause access for unauthorized access, missing completion records,
failed recovery or an unacceptable security issue.
Notify the owner, preserve evidence and take a consistent backup.
Restore a verified backup into an isolated replacement, validate its
records and obtain approval before reopening access.
Do not downgrade code against an incompatible upgraded database.

## Approval and Walkthrough

Friendy must agree scope, hosting/budget, SSO, backup destination,
operational owners, monitoring and success/revert criteria.
After agreement, arrange a walkthrough before implementation.

## Current Limitations

The idle comparison with unrelated host applications closed remains
outstanding. The latest Moodle idle recordings were excluded.
Existing measurements do not establish pilot or production capacity.
