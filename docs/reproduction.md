## Backup and Recovery

Backups were created successfully on **27 October 2026** and stored privately in `~/lms-backups/`, outside Git. LearnHouse returned to a healthy state afterward. Restoration has not been tested.

| Platform | Saved components |
|---|---|
| Moodle | Database dump, `moodledata`, source and deployment configuration |
| LearnHouse | Database dump, uploaded content and installation configuration |

### Backup Procedure

1. Stop application writes while keeping PostgreSQL available.
2. Export the database in custom format:

```bash
docker exec SOURCE_DB sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "${POSTGRES_DB:-$POSTGRES_USER}" -Fc' \
  > "$BACKUP_DIR/database.dump"
```

3. Copy the application data and archive its configuration:

| Platform | Data directory inside application container |
|---|---|
| Moodle | `/var/www/moodledata` |
| LearnHouse | `/app/api/content` |

```bash
docker cp SOURCE_APP:/path/to/data "$BACKUP_DIR/"
```

4. Confirm backup files exist and are non-empty, then return services to their previous running state.

Replace container names, paths and `BACKUP_DIR` with the appropriate deployment values.

### Recovery Procedure

1. Prepare a separate deployment with matching software versions, fresh storage and different host ports.
2. Restore configuration, updating paths and connections for the recovery environment.
3. Keep the application stopped and start an empty target database.
4. Import the database:

```bash
docker exec -i TARGET_DB sh -c \
  'pg_restore --exit-on-error --no-owner --no-acl \
  -U "$POSTGRES_USER" -d "${POSTGRES_DB:-$POSTGRES_USER}"' \
  < "$BACKUP_DIR/database.dump"
```

5. Copy the saved data into the target application's data directory and set the required file ownership.
6. Start the application and verify administrator login, learner access, course content and saved completion where applicable.

Use only isolated recovery containers and volumes. Local backup creation does not establish recoverability or provide off-device disaster recovery.