# LMS Technical Comparison

Moodle and LearnHouse Community were tested locally. Open edX and Canvas were evaluated through official documentation. Deployment complexity ratings are qualitative assessments.

## Deployment and Hardware

Published requirements are planning baselines, not measured container usage or guarantees of production capacity.

| Platform | Deployment and complexity | Published hardware baseline | Database and cache |
|---|---|---|---|
| Moodle | Moderate: official Docker development stack; production needs separate operational configuration | Minimum: 512 MB RAM, 1 GHz CPU. Recommended: 1 GB+ RAM, dual-core 2 GHz CPU; larger production sites need more | PostgreSQL, MySQL or MariaDB; optional Redis |
| LearnHouse | Low for local evaluation: guided CLI configures Docker services | Minimum: 2 GB RAM, 1 core. Recommended: 4 GB RAM, 2+ cores | PostgreSQL and Redis |
| Open edX / Tutor | Moderate–high: Docker Compose deployment with multiple services | Minimum: 4 GB RAM, 2 CPUs. Recommended: 8 GB RAM, 4 CPUs | MySQL, MongoDB and Redis; exact services depend on release |
| Canvas LMS | High: production guide requires application, database, web server and background-job configuration | At least 8 GB RAM recommended for an all-in-one server; CPU minimum not specified in the cited guide | PostgreSQL and Redis |

The Moodle Docker stack used here is intended for development and testing. It is not a production deployment template.

## Standards and Integration

| Platform | SCORM | xAPI / cmi5 | APIs and extensibility |
|---|---|---|---|
| Moodle | Native SCORM 1.2; SCORM 2004 requires an external solution | xAPI through third-party plugins; cmi5 not verified | Established web services, including REST; extensive plugin and theme ecosystem |
| LearnHouse Community | Documented SCORM 1.2/2004 support requires Enterprise | Not verified | FastAPI-based REST API with OpenAPI documentation; source-level customization |
| Open edX | SCORM 1.2/2004 through the SCORM XBlock | Configurable xAPI event export; cmi5 not verified | Documented REST APIs, XBlocks and platform extensions |
| Canvas LMS | SCORM integration exists, but availability must be confirmed separately for open-source self-hosting | Self-hosted xAPI/cmi5 support not verified | Extensive documented REST API and external-tool integrations |

xAPI event export does not establish support for launching xAPI or cmi5 course packages. Standards and API integrations were researched, not tested in this PoC.

## Authentication

| Platform | Documented integration options |
|---|---|
| Moodle | LDAP, OAuth 2, Shibboleth and additional authentication plugins |
| LearnHouse | Enterprise SSO documentation covers custom OIDC and WorkOS integrations; these were not enabled in the Community PoC |
| Open edX | Third-party OAuth2 and SAML identity providers |
| Canvas LMS | SAML, OpenID Connect, LDAP and other authentication providers |

Only local account login was validated during testing.

## Measured Local Results

| Metric | Moodle | LearnHouse |
|---|---:|---:|
| Total idle container RAM | ~259 MiB | ~604 MiB |
| Application container peak RAM | 184.80 MiB | 528.40 MiB |
| Application container peak CPU | 0.75% | 23.50% |
| Database container peak RAM | 66.50 MiB | 80.36 MiB |
| Database container peak CPU | 0.88% | 19.04% |

Active measurements came from 60-second recordings during manual learner activity. Peak values are per container and may occur at different times. They must not be added together as a simultaneous system peak.

These single-user observations do not establish production capacity or comparative throughput. Other applications were running on the host, and learner actions were not automated.

Full measurements are available in [benchmarks](../benchmarks/).

## Evaluation Limits

- End-to-end setup duration was not reliably measured; only setup start timestamps were retained.
- Open edX and Canvas were not deployed or benchmarked locally.
- Backup restoration, concurrent-user load, SSO and standards packages were not tested.
- Container restart persistence was verified; this is not a backup-recovery test.

## Official References

- [Moodle requirements](https://docs.moodle.org/en/Installing_Moodle)
- [Moodle Docker development stack](https://github.com/moodlehq/moodle-docker)
- [Moodle standards support](https://docs.moodle.org/en/SCORM_FAQ)
- [Moodle authentication](https://docs.moodle.org/en/Authentication)
- [Moodle REST clients](https://docs.moodle.org/dev/Creating_a_web_service_client)
- [LearnHouse requirements](https://docs.learnhouse.app/self-hosting/installation/requirements)
- [LearnHouse API](https://docs.learnhouse.app/developers/api)
- [LearnHouse SCORM](https://docs.learnhouse.app/enterprise/scorm)
- [LearnHouse WorkOS SSO](https://docs.learnhouse.app/enterprise/sso/workos)
- [Tutor requirements](https://docs.tutor.edly.io/gettingstarted/requirements.html)
- [Open edX databases](https://docs.openedx.org/en/latest/site_ops/concepts/databases.html)
- [Open edX SCORM](https://docs.openedx.org/en/latest/educators/references/course_development/exercise_tools/SCORM_overview.html)
- [Open edX xAPI](https://docs.openedx.org/en/latest/developers/references/internal_data_formats/xapi_events.html)
- [Open edX REST APIs](https://docs.openedx.org/projects/edx-platform/en/latest/concepts/rest_apis.html)
- [Open edX authentication](https://docs.openedx.org/en/latest/site_ops/install_configure_run_guide/configuration/tpa/tpa_integrate_open/index.html)
- [Canvas production installation](https://github.com/instructure/canvas-lms/wiki/Production-Start)
- [Canvas APIs](https://developerdocs.instructure.com/services/canvas)
- [Canvas authentication](https://developerdocs.instructure.com/services/canvas/resources/authentication_providers)
