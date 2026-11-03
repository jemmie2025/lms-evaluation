import datetime as dt
import json
import re
import statistics
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path.cwd()
STAMP = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = ROOT / "benchmarks" / f"idle-rerun-{STAMP}"

MOODLE = [
    "lms_moodle-db-1",
    "lms_moodle-mailpit-1",
    "lms_moodle-webserver-1",
]
LEARNHOUSE = [
    f"learnhouse-{service}-2a291fc8"
    for service in ["db", "redis", "app", "nginx", "ssr-fwd"]
]
RESTORE = MOODLE + LEARNHOUSE + [
    f"learnhouse-{service}-8c999180"
    for service in ["db", "redis", "app", "nginx", "ssr-fwd"]
] + [
    "moodle_verify_1793613396928832852-db-1",
    "moodle_verify_1793613396928832852-webserver-1",
    "moodle_restore_1793607674-db-1",
    "lms_moodle_timing_20261027113503-db-1",
    "lms_moodle_timing_20261027113503-mailpit-1",
    "lms_moodle_timing_20261027113503-webserver-1",
    "n8n-latest-postgres",
    "n8n-latest-app",
    "mattermost-intern-automation-postgres-1",
]

def run(args, check=True):
    return subprocess.run(
        args, text=True, capture_output=True, check=check
    )

def docker(*args):
    return run(["docker", *args]).stdout.strip()

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def active():
    return set(docker("ps", "--format", "{{.Names}}").splitlines())

def inspect(names):
    return json.loads(docker("inspect", *names))

def stop(names):
    running = active()
    targets = [n for n in names if n in running]
    if targets:
        docker("stop", "--timeout", "30", *targets)

def start(names):
    running = active()
    for name in names:
        if name not in running:
            docker("start", name)

def verify_only(names):
    actual = active()
    if actual != set(names):
        raise RuntimeError(
            f"Unexpected running-container set: {sorted(actual)}"
        )

def url_for(name):
    info = inspect([name])[0]
    ports = info["HostConfig"].get("PortBindings") or {}
    bindings = ports.get("80/tcp") or []
    if not bindings:
        raise RuntimeError(f"No HTTP port binding found for {name}")
    return "http://127.0.0.1:" + bindings[0]["HostPort"] + "/"

def wait_ready(url, names):
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        try:
            healthy = all(
                x["State"]["Running"]
                and x["State"].get("Health", {}).get("Status", "healthy")
                == "healthy"
                for x in inspect(names)
            )
            if healthy:
                with urllib.request.urlopen(url, timeout=10) as response:
                    if response.status == 200:
                        response.read()
                        return
        except Exception:
            pass
        time.sleep(3)
    raise RuntimeError(f"Readiness not established: {url}")

def mib(value):
    match = re.fullmatch(r"\s*([\d.]+)\s*([KMGT]?i?B)\s*", value)
    if not match:
        raise ValueError(f"Unrecognized memory value: {value}")
    factors = {
        "B": 1 / 1048576, "kB": 1000 / 1048576,
        "KB": 1000 / 1048576, "KiB": 1 / 1024,
        "MB": 1000000 / 1048576, "MiB": 1,
        "GB": 1000000000 / 1048576, "GiB": 1024,
        "TB": 1000000000000 / 1048576, "TiB": 1048576,
    }
    return float(match[1]) * factors[match[2]]

def commit(paths, message):
    relative = [str(p.relative_to(ROOT)) for p in paths]
    run(["git", "add", "--", *relative])
    run(["git", "diff", "--cached", "--check"])
    run(["git", "commit", "-m", message])
    print(message, flush=True)

answer = input(
    "\nSave your work and close WhatsApp and other unrelated desktop apps."
    "\nKeep Docker Desktop and VS Code open."
    "\nThen type READY and press Enter: "
)
if answer.strip() != "READY":
    raise SystemExit("Cancelled. No containers changed.")

if run(["git", "diff", "--cached", "--quiet"], check=False).returncode:
    raise SystemExit("Existing staged changes found. Commit them first.")

unknown = active() - set(RESTORE)
if unknown:
    raise SystemExit(
        "Unrecognized running containers; nothing stopped: "
        + ", ".join(sorted(unknown))
    )

inventory = inspect(RESTORE)
OUT.mkdir(parents=True)
(OUT / "restore-containers.txt").write_text("\n".join(RESTORE) + "\n")

metadata = {
    "created_utc": now(),
    "host_condition": (
        "Operator confirmed unrelated desktop applications closed; "
        "Docker Desktop and VS Code retained. Normal system services remain."
    ),
    "method": (
        "One platform at a time; HTTP readiness and available health checks; "
        "60-second warm-up; three 60-second windows; samples scheduled every "
        "5 seconds using docker stats --no-stream. Sample timestamps and "
        "collection durations retained. No user browsing during recordings."
    ),
    "scope": (
        "Original Moodle image versus LearnHouse 1.4.2; "
        "security candidate excluded."
    ),
    "containers": [
        {
            "name": x["Name"].lstrip("/"),
            "image_reference": x["Config"]["Image"],
            "image_id": x["Image"],
            "memory_limit": x["HostConfig"]["Memory"],
            "nano_cpus": x["HostConfig"].get("NanoCpus", 0),
            "restart_count": x.get("RestartCount", 0),
        }
        for x in inventory
    ],
}
(OUT / "method.json").write_text(json.dumps(metadata, indent=2) + "\n")
results = []
successful = False

try:
    print("Pausing other stacks for isolation...", flush=True)
    stop(RESTORE)

    for platform, names, web in [
        ("moodle", MOODLE, MOODLE[-1]),
        ("learnhouse", LEARNHOUSE, "learnhouse-nginx-2a291fc8"),
    ]:
        print(f"Starting {platform}...", flush=True)
        start(names)
        verify_only(names)
        url = url_for(web)
        wait_ready(url, names)
        ready_at = now()

        print(f"{platform}: ready; warming up for 60 seconds.", flush=True)
        time.sleep(60)
        wait_ready(url, names)
        start_restarts = {
            x["Name"]: x.get("RestartCount", 0) for x in inspect(names)
        }

        for number in range(1, 4):
            verify_only(names)
            path = OUT / f"{platform}-run-{number}.jsonl"
            totals = []
            window_start = time.monotonic()

            print(f"{platform}: recording {number}/3 for 60 seconds.", flush=True)
            with path.open("x") as output:
                for sample in range(12):
                    delay = window_start + sample * 5 - time.monotonic()
                    if delay > 0:
                        time.sleep(delay)

                    verify_only(names)
                    started = now()
                    tick = time.monotonic()
                    raw = docker(
                        "stats", "--no-stream", "--format", "{{json .}}", *names
                    )
                    stats = [json.loads(line) for line in raw.splitlines()]
                    if {x["Name"] for x in stats} != set(names):
                        raise RuntimeError("Incomplete container sample.")

                    total = sum(
                        mib(x["MemUsage"].split("/")[0]) for x in stats
                    )
                    totals.append(total)
                    record = {
                        "started_utc": started,
                        "finished_utc": now(),
                        "collection_seconds": time.monotonic() - tick,
                        "combined_memory_mib": total,
                        "stats": stats,
                    }
                    output.write(json.dumps(record) + "\n")
                    output.flush()

                remaining = window_start + 60 - time.monotonic()
                if remaining > 0:
                    time.sleep(remaining)

            verify_only(names)
            after_restarts = {
                x["Name"]: x.get("RestartCount", 0) for x in inspect(names)
            }
            if after_restarts != start_restarts:
                raise RuntimeError("A container restarted during recording.")
            wait_ready(url, names)

            results.append({
                "platform": platform,
                "run": number,
                "samples": len(totals),
                "mean_combined_mib": statistics.mean(totals),
                "min_combined_mib": min(totals),
                "max_combined_mib": max(totals),
                "ready_utc": ready_at,
            })
            (OUT / "summary.json").write_text(
                json.dumps(results, indent=2) + "\n"
            )
            commit(
                [path, OUT / "method.json", OUT / "summary.json",
                 OUT / "restore-containers.txt"],
                f"Record isolated {platform} idle measurement run {number}",
            )
        stop(names)

    successful = True

finally:
    print("Restoring previously running workloads...", flush=True)
    pending = set(RESTORE)
    for attempt in range(3):
        for name in list(pending):
            result = run(["docker", "start", name], check=False)
            if result.returncode == 0:
                pending.remove(name)
        if not pending:
            break
        time.sleep(3)

    missing = set(RESTORE) - active()
    if missing:
        print("ATTENTION: restart these containers:", sorted(missing))
    else:
        print("All listed containers are running again.")

if successful:
    print("\nMEASUREMENT SUMMARY")
    for row in results:
        print(
            f'{row["platform"]} run {row["run"]}: '
            f'{row["mean_combined_mib"]:.2f} MiB mean combined RAM'
        )
    print("\nSaved results:", OUT)
    print(
        "These are short local idle observations, not production sizing "
        "or a concurrent-load benchmark."
    )
    print("Send this summary to ChatGPT before updating the comparison.")
