# Moodle Backup Restore Drill

Date: 2 November 2026

## Scope and results

Restored Moodle 4.5.15+ using the original webserver and PostgreSQL
container image IDs, with separate Compose projects, database volumes,
content directories and localhost ports.

| Check | Result |
|---|---|
| Original database backup restored | Passed |
| Original course and lesson content | Verified in browser |
| Original users and enrolments | Test Learner and Admin User present |
| Original completion records | Zero activity and course records |
| New activity completion test | Test Learner achieved Done: View |
| New course completion test | learner01 completed DEVOPS101 |
| Completion preserved through another restore | Timestamp 1793611726 matched exactly |
| Second restored site | Opened on localhost:8020 |

The original backup was moodle-20261027-121004. Its moodledata contained
1,119 files. Because it contained no completion records, a separate
completion test and backup were required.

## Restore procedure

1. Preserve the source stack and backup. Create a fresh private working
   directory outside Git.
2. Extract vendor/moodle from code-and-deployment.tar.gz and copy the
   saved moodledata directory into the working directory.
3. Prepare a Compose file using the recorded original image IDs.
   Give it a new project name and fresh database volume. Bind only the
   copied code and content. Use an unused localhost port.
4. Configure the application for database host db, database/user moodle,
   table prefix m_, and dataroot /var/www/moodledata. Match its database
   password to the recovery database and set its recovery web port.
5. Validate the Compose file, start only db, and wait for pg_isready.
6. Restore the custom-format dump into the empty database:

```bash
docker compose -f "$RESTORE_DIR/compose.yml" exec -T db \
  pg_restore --exit-on-error --single-transaction --no-owner --no-acl \
  -U moodle -d moodle < "$BACKUP_DIR/database.dump"
```

7. Set ownership of the copied moodledata to www-data:www-data using
   a one-off recovery webserver container.
8. Disable outgoing email in the recovery environment before functional
   testing. The drill initially reported an email-processor error;
   noemailever=1 was subsequently set and the visible warning cleared.
   Email delivery was not repaired or validated.
9. Start the recovery webserver. Verify administrator access, course
   content, users, enrolments and completion records.

RESTORE_DIR and BACKUP_DIR must point to the chosen private recovery
directory and backup set. Never target the source database or storage.

## Completion recovery test

In the first recovery stack, enabled lesson completion on viewing and
made that lesson the course-completion criterion. Used Log in as Test
Learner to view the lesson, then ran the completion scheduled task.

Confirmed learner01 had timecompleted=1793611726. Stopped that recovery
webserver, exported its database with pg_dump -Fc, copied moodledata,
and archived code and configuration.

Restored this new backup into a second fresh project. Before starting
its webserver, queried the database and confirmed the identical learner,
course and completion timestamp.

Evidence: [Restored completion query](../benchmarks/restore/moodle-completion-restored.txt).

## Limits

This was a local restore drill, not an off-host disaster recovery test.
Learner testing used administrator impersonation; independent learner
password authentication was not established by that test.
Uploaded-file integrity was not exhaustively checked. Email delivery,
production readiness, recovery-time and recovery-point objectives
remain unverified. Private backups and credentials stay outside Git.
