# Isolated idle measurements — 3 November 2026

Unrelated desktop applications were closed; Docker Desktop and VS Code
remained open. Other container stacks were paused. Each platform was
measured separately after HTTP and available container-health checks.

Each platform received a 60-second warm-up followed by three 60-second
recordings. Each recording collected 12 timestamped Docker stats snapshots
at scheduled five-second intervals. Combined memory sums the measured
containers within each snapshot.

| Platform | Run 1 mean | Run 2 mean | Run 3 mean | Overall mean |
|---|---:|---:|---:|---:|
| Moodle | 89.95 MiB | 96.67 MiB | 98.15 MiB | 94.92 MiB |
| LearnHouse | 507.51 MiB | 526.60 MiB | 528.56 MiB | 520.89 MiB |

Moodle used the original evaluation stack: webserver, PostgreSQL and
Mailpit. The security candidate image was not the idle measurement target.
LearnHouse used application, PostgreSQL, Redis, nginx and SSR forwarding.

The script recorded each measurement run in a separate commit and reported
that all listed workloads were running again after restoration.

## Evidence and limitations

Raw snapshots, summary.json and method.json are retained in this directory.
The collection script is scripts/controlled-idle-rerun.py at repository root.

Memory increased across successive runs. The warm-up does not establish
equivalent cache maturity, and the platforms have different stack
compositions. Docker stats snapshots are observations, not independent
experimental trials. Desktop application closure was operator-reported.

These short local idle observations replace the earlier preliminary idle
figures. They do not replace the active-use measurements or establish
production sizing, concurrent-user capacity or comparative throughput.
