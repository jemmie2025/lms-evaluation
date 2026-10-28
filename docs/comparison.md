# LMS Technical Comparison

Moodle and LearnHouse Community were tested locally. Open edX and Canvas were assessed through official documentation. Deployment complexity ratings are qualitative.

## Deployment and Hardware

Published requirements are planning baselines, not measured container usage or guarantees of production capacity.

| Platform | Deployment complexity | Published hardware baseline | Database and cache |
|---|---|---|---|
| Moodle | Moderate: official Docker development stack; production requires additional configuration | Minimum: 512 MB RAM, 1 GHz CPU. Recommended: 1 GB+ RAM, dual-core 2 GHz CPU; larger sites require more | PostgreSQL, MySQL or MariaDB; optional Redis |
| LearnHouse | Low for local evaluation: guided CLI configures Docker services | Minimum: 2 GB RAM, 1 core. Recommended: 4 GB RAM, 2+ cores | PostgreSQL and Redis |
| Open edX / Tutor | Moderate–high: Docker Compose deployment with multiple services | Minimum: 4 GB RAM, 2 CPUs. Recommended: 8 GB RAM, 4 CPUs | MySQL, MongoDB and Redis; services depend on release |
| Canvas LMS | High: application, database, web server and background jobs require configuration | At least 8 GB RAM recommended for an all-in-one server; CPU minimum not specified in the cited guide | PostgreSQL and Redis |

The Moodle Docker stack used in this evaluation is intended for development and testing, not production.

## Standards Support

| Platform | SCORM | xAPI | cmi5 |
|---|---|---|---|
| Moodle | Native SCORM 1.2; SCORM 2004 requires an external solution | Available through third-party integrations | Advertised through the third-party SCORM Cloud plugin, which requires an external service |
| LearnHouse Community | Documented SCORM 1.2/2004 support requires Enterprise | Not confirmed in the official documentation reviewed | Not confirmed in the official documentation reviewed |
| Open edX | SCORM 1.2/2004 through the SCORM XBlock | Selected events can be exported through event-routing-backends and an LRS integration | Package launch support not verified |
| Canvas LMS | SCORM integration exists; availability for open-source self-hosting requires confirmation | Limited callbacks from LTI tools record activity time and page views | Package launch support not verified |

Event reporting does not establish xAPI package playback or cmi5 compliance. Unverified capabilities should not be interpreted as confirmed support or confirmed absence. Standards integrations were researched, not tested locally.

## APIs and Customization

| Platform | API access and extensibility |
|---|---|
| Moodle | Established web services, including REST; extensive plugin and theme ecosystem |
| LearnHouse | FastAPI-based REST API with OpenAPI documentation; source-level customization |
| Open edX | Documented REST APIs, XBlocks and platform extensions |
| Canvas LMS | Extensive documented REST API and external-tool integrations |

API availability was researched; integration behavior and performance were not benchmarked.

## Authentication

| Platform | Documented integration options |
|---|---|
| Moodle | LDAP, OAuth 2, Shibboleth and additional authentication plugins |
| LearnHouse | Enterprise SSO documentation covers custom OIDC and WorkOS integrations |
| Open edX | Third-party OAuth 2 and SAML identity providers |
| Canvas LMS | SAML, OpenID Connect, LDAP and other authentication providers |

Only local account login was validated. Enterprise SSO was not enabled in the LearnHouse Community PoC.

## Measured Local Results

Tests ran on Windows 11 with WSL2 Ubuntu 22.04.5, an Intel Core i7-1355U, 12 logical CPUs and approximately 7.6 GiB of Docker memory.

| Metric | Moodle | LearnHouse 1.4.2 |
|---|---:|---:|
| Total idle container RAM | ~259 MiB | ~604 MiB |
| Application container peak RAM | 184.80 MiB | 528.40 MiB |
| Application container peak CPU | 0.75% | 23.50% |
| Database container peak RAM | 66.50 MiB | 80.36 MiB |
| Database container peak CPU | 0.88% | 19.04% |

Active measurements came from 60-second recordings during manual learner activity. Per-container peaks may occur at different times and must not be added together as a simultaneous system peak.

These single-user observations do not establish production capacity or comparative throughput. Other applications were running on the host, and learner actions were not automated.

See [benchmark records](../benchmarks/) for raw measurements and summaries.

## Deployment Timing

Separate test installations were used for readiness measurements.

| Platform | Measured duration | Scope |
|---|---:|---|
| Moodle | 290 seconds (4 min 50 sec) | Fresh-database deployment using existing source and configuration; database installation completed and login page responded |
| LearnHouse 1.4.2 | 40 seconds | Deployment using generated configuration; services ready and login page returned HTTP 200 |

Administrator login was verified separately for both installations after timing. These single-run measurements exclude configuration preparation and manual browser validation. Image downloads were not measured separately.

The results describe the tested workflows, not full first-time installation times or controlled cold-install comparisons.

## Data Ownership and Backup

Both local PoCs provided direct access to their databases, application files and deployment configuration.

| Platform | Backup created |
|---|---|
| Moodle | PostgreSQL custom-format dump, moodledata, source code and deployment configuration |
| LearnHouse | PostgreSQL custom-format dump, uploaded content and installation configuration |

Backups were created while application writes were stopped and saved outside the Git repository. Restoration was not tested.

Open edX and Canvas backup procedures were not exercised locally. Operational instructions for the tested platforms are in the [deployment guide](reproduction.md).

## Evaluation Limits

- Full first-time setup duration was not measured; scoped readiness timings were recorded for both tested platforms.
- Open edX and Canvas were researched but not deployed locally.
- Backup restoration, concurrent-user load, SSO, API integrations and standards packages were not tested.
- Restart persistence and backup creation do not establish backup recoverability.
- Local measurements are not production sizing recommendations.
- The local PoCs are not production-ready deployments.

## Official References

### Moodle

- [Hardware and installation requirements](https://docs.moodle.org/en/Installing_Moodle)
- [Docker development stack](https://github.com/moodlehq/moodle-docker)
- [SCORM support](https://docs.moodle.org/en/SCORM_FAQ)
- [SCORM Cloud plugin](https://moodle.org/plugins/mod_scormcloud)
- [Authentication](https://docs.moodle.org/en/Authentication)
- [Web service clients](https://docs.moodle.org/dev/Creating_a_web_service_client)
- [Site backup guidance](https://docs.moodle.org/en/Site_backup)

### LearnHouse

- [Hardware requirements](https://docs.learnhouse.app/self-hosting/installation/requirements)
- [Installation](https://docs.learnhouse.app/self-hosting/installation/quick-install)
- [API documentation](https://docs.learnhouse.app/developers/api)
- [Enterprise SCORM](https://docs.learnhouse.app/enterprise/scorm)
- [Enterprise WorkOS SSO](https://docs.learnhouse.app/enterprise/sso/workos)
- [Backup guidance](https://docs.learnhouse.app/self-hosting/maintenance/backups)

### Open edX / Tutor

- [Tutor requirements](https://docs.tutor.edly.io/gettingstarted/requirements.html)
- [Databases](https://docs.openedx.org/en/latest/site_ops/concepts/databases.html)
- [SCORM](https://docs.openedx.org/en/latest/educators/references/course_development/exercise_tools/SCORM_overview.html)
- [xAPI events](https://docs.openedx.org/en/latest/developers/references/internal_data_formats/xapi_events.html)
- [REST APIs](https://docs.openedx.org/projects/edx-platform/en/latest/concepts/rest_apis.html)
- [Authentication](https://docs.openedx.org/en/latest/site_ops/install_configure_run_guide/configuration/tpa/tpa_integrate_open/index.html)

### Canvas LMS

- [Production installation](https://github.com/instructure/canvas-lms/wiki/Production-Start)
- [APIs](https://developerdocs.instructure.com/services/canvas)
- [Authentication providers](https://developerdocs.instructure.com/services/canvas/resources/authentication_providers)
- [xAPI callbacks](https://developerdocs.instructure.com/services/canvas/external-tools/file.xapi)