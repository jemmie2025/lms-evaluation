#!/usr/bin/env bash
set -euo pipefail
unset COMPOSE_PROJECT_NAME COMPOSE_FILE

cd "$HOME/.learnhouse/lms-timing-20261028113739"
mkdir -p "$HOME/lms-evaluation/benchmarks"
exec > >(tee "$HOME/lms-evaluation/benchmarks/learnhouse-deployment-timing.txt") 2>&1

echo "LearnHouse 1.4.2 deployment-readiness measurement"
echo "Excludes configuration generation and manual login."
date -Is
SECONDS=0

docker compose up -d --wait --wait-timeout 600

deadline=$((SECONDS + 300))
while true; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
        http://localhost:8081/login) || code=000

    if [[ "$code" == 200 ]]; then
        break
    fi

    if (( SECONDS >= deadline )); then
        echo "FAILED: login page did not return HTTP 200."
        exit 1
    fi
    sleep 2
done

echo "Deployment duration: $SECONDS seconds"
date -Is
echo "Result: services ready; login page returned HTTP 200."