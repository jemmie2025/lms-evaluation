# Idle recording follow-up — 2 November 2026

Three recordings per platform were attempted using 60-second Docker
stats commands. Raw files are retained for transparency.

Important host applications remained open. This does not satisfy the
requested benchmark condition of closing unrelated applications.

LearnHouse recordings contain 118, 116 and 116 complete display frames.
Mean combined container memory per run was approximately 544.7,
545.5 and 545.9 MiB.

Moodle recordings contain 26, 6 and 118 complete display frames.
Application readiness was not verified before recording. A later
HTTP check returned 500, followed by 200 after database recovery.
These Moodle recordings are excluded from the comparative baseline.

Display frames may repeat underlying statistics and are not independent
samples. Files contain no sample timestamps. Platform uptime and cache
conditions differed. These observations do not establish production
capacity or replace the earlier measurements with a controlled comparison.
