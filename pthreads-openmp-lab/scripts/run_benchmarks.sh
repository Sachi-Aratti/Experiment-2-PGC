#!/usr/bin/env bash
# Re-run the performance experiment on your own machine.
# Usage: make all && ./scripts/run_benchmarks.sh
set -e
cd "$(dirname "$0")/.."

THREADS="1 2 4 6 16"
RUNS=5

echo "== Sequential baseline ($RUNS runs) =="
for _ in $(seq $RUNS); do ./bin/sequential | grep "Execution time"; done

for prog in pthread_perf omp_perf; do
  echo
  echo "== $prog =="
  for t in $THREADS; do
    printf "%2d threads: " "$t"
    echo "$t" | ./bin/$prog | grep "Execution time"
  done
done
