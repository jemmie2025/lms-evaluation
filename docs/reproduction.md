# Local Deployment Guide

Reproduction instructions for the Moodle and LearnHouse evaluation. Run setup commands only in a fresh environment.

## Prerequisites

Linux or WSL2 with Docker, Docker Compose and Git. LearnHouse also requires Node.js and npm. Keep ports 8000 and 8080 available.

## Moodle

### Download and configure

```bash
mkdir -p ~/lms-evaluation/vendor
cd ~/lms-evaluation

git clone https://github.com/moodlehq/moodle-docker.git vendor/moodle-docker
git clone --depth 1 --branch MOODLE_405_STABLE \
  https://github.com/moodle/moodle.git vendor/moodle

source scripts/moodle-env.sh
cd vendor/moodle-docker
cp config.docker-template.php "$MOODLE_DOCKER_WWWROOT/config.php"

bin/moodle-docker-compose up -d db webserver
bin/moodle-docker-wait-for-db
```

The repository's `scripts/moodle-env.sh` configures PostgreSQL, PHP 8.3, port 8000 and Compose project `lms_moodle`.

### Initialize once

```bash
read -rsp "Moodle admin password: " MOODLE_POC_PASSWORD
printf '\n'

bin/moodle-docker-compose exec webserver \
  php admin/cli/install_database.php \
  --agree-license \
  --fullname="LMS Evaluation" \
  --shortname="LMS-PoC" \
  --adminuser=admin \
  --adminemail=admin@example.com \
  --adminpass="$MOODLE_POC_PASSWORD"

unset MOODLE_POC_PASSWORD
```

Open http://localhost:8000 and sign in as `admin`.

This official Docker stack is intended for development and testing.

## LearnHouse Community

```bash
unset COMPOSE_PROJECT_NAME
mkdir -p ~/lms-evaluation/vendor/learnhouse
cd ~/lms-evaluation/vendor/learnhouse
npx learnhouse@1.5.1 setup
```

Configure the wizard:

| Setting | Value |
|---|---|
| Edition / channel | Community / Stable |
| Installation | lms-poc |
| Host / port | localhost / 8080 |
| Database / cache | Local Docker PostgreSQL / Redis |
| Organization / slug | LMS Evaluation / default |
| Administrator | Your email and a unique password |
| HTTPS / optional integrations | Disabled for local evaluation |
| Start services | Yes |

Open http://localhost:8080.

The evaluated application image was `ghcr.io/learnhouse/app:1.4.2`. Generated Compose configuration is stored in `~/.learnhouse/lms-poc`.

## Functional Validation

For each platform:

1. Create **DevOps Fundamentals** with an **Introduction to DevOps** lesson.
2. Make the course accessible; in LearnHouse, publish both course and activity.
3. Create a separate learner account and grant course access.
4. Verify learner login and lesson access in a private browser session.
5. Restart the deployment and confirm that saved content remains accessible.

LearnHouse learner completion and its persistence after restart were also verified. Moodle completion was not tested.

## Backup and Recovery

| Platform | Required backup | Recovery approach |
|---|---|---|
| Moodle | Database, data directory, configuration and matching code/plugins | Restore into a compatible isolated deployment; verify login and course access |
| LearnHouse | CLI database/configuration backup plus a separate backup of uploaded files | Restore database and content into a compatible isolated deployment; verify login, content and completion |

Backup restoration was not tested. Restart persistence is not a recovery test. Store backups privately.

## Reproducibility Limits

Upstream branches and stable image selections can change. The commands reproduce the deployment workflow; exact Git commits and image digests were not captured.

## References

- [Moodle Docker](https://github.com/moodlehq/moodle-docker)
- [Moodle backup guidance](https://docs.moodle.org/en/Site_backup)
- [LearnHouse installation](https://docs.learnhouse.app/self-hosting/installation/quick-install)
- [LearnHouse backups](https://docs.learnhouse.app/self-hosting/maintenance/backups)
