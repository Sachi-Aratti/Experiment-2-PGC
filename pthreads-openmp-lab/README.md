# Multithreaded Programming with Pthreads and OpenMP

Lab on thread creation, management, work distribution, race conditions, synchronization, coordination, and performance scaling using **Pthreads** and **OpenMP** in C.

**Environment:** Windows + WSL Ubuntu, GCC 15.2.0, Pthreads, OpenMP.

## Repository layout

```
src/
  pthreads/      thread1, thread2, thread_sum, race, mutex
  openmp/        omp_hello, omp_for, omp_race, omp_critical, omp_barrier
  performance/   sequential, pthread_perf, omp_perf
scripts/
  run_benchmarks.sh   re-run the timing experiment
  plot_results.py     compute speedup/efficiency and draw the graphs
results/
  performance.csv, sequential_runs.csv, speedup_efficiency.csv
  fig1_execution_time.png, fig2_speedup.png, fig3_efficiency.png
docs/screenshots/    terminal output from the actual runs
Makefile
```

## Build and run

```bash
make all                 # builds everything into ./bin
./bin/thread1
./bin/race               # race condition (wrong count)
./bin/mutex              # fixed with mutex
./bin/omp_race           # race condition (wrong count)
./bin/omp_critical       # fixed with critical
echo 4 | ./bin/pthread_perf
echo 4 | ./bin/omp_perf
make bench               # full timing experiment
make plots               # regenerate graphs (needs python3 + matplotlib)
make clean
```

Pthreads programs compile with `-pthread`, OpenMP programs with `-fopenmp`.

## Part A - Pthreads

| Program | Concept | Observed result |
|---|---|---|
| `thread1.c` | `pthread_create` / `pthread_join` | `Hello from the thread!` then `Main thread finished.` |
| `thread2.c` | Multiple threads | 4 hello lines, order scheduled by the OS, then `All threads have finished.` |
| `thread_sum.c` | Work distribution | partial sums 30, 70, 110, 150 → total **360** |
| `race.c` | Race condition | expected 400000, actual **124775** |
| `mutex.c` | Mutex fix | expected 400000, actual **400000** |

## Part B - OpenMP

| Program | Concept | Observed result |
|---|---|---|
| `omp_hello.c` | `#pragma omp parallel` | 16 threads (0-15) printed in non-deterministic order |
| `omp_for.c` | `parallel for` + `reduction` | indices 0-7 spread across threads, total **360** |
| `omp_race.c` | Race condition | expected 400000, actual **180342** |
| `omp_critical.c` | `critical` fix | expected 400000, actual **400000** |
| `omp_barrier.c` | `barrier` | all 4 "reached" lines appear before any "passed" line |

## Part C - Performance analysis

Workload: `sum += i * 0.000001` for `i` in `[0, 1e9)`, compiled without optimization flags.
All runs produced `Result = 499999999500.00`.

**Sequential baseline** (5 runs): 1.785932, 1.779894, 1.778588, 1.775721, 1.787648 s → **mean 1.781557 s**

### Execution time (s)

| Threads | Pthreads | OpenMP |
|---:|---:|---:|
| 1 | 1.782130 | 1.777617 |
| 2 | 0.890190 | 0.889226 |
| 4 | 0.468415 | 0.491119 |
| 6 | 0.360562 | 0.363452 |
| 16 | 0.195346 | 0.204598 |

### Speedup = T_sequential / T_parallel

| Threads | Pthreads | OpenMP |
|---:|---:|---:|
| 1 | 1.000x | 1.002x |
| 2 | 2.001x | 2.003x |
| 4 | 3.803x | 3.628x |
| 6 | 4.941x | 4.902x |
| 16 | 9.120x | 8.708x |

### Efficiency = Speedup / Threads

| Threads | Pthreads | OpenMP |
|---:|---:|---:|
| 1 | 99.97% | 100.22% |
| 2 | 100.07% | 100.17% |
| 4 | 95.08% | 90.69% |
| 6 | 82.35% | 81.70% |
| 16 | 57.00% | 54.42% |

![Execution time](results/fig1_execution_time.png)
![Speedup](results/fig2_speedup.png)
![Efficiency](results/fig3_efficiency.png)

### Observations

- Execution time drops steadily as threads increase for both Pthreads and OpenMP; at 16 threads it is roughly 9x faster than sequential.
- Scaling is near-ideal up to 2 threads, then efficiency falls (about 91-95% at 4 threads, about 82% at 6, 54-57% at 16).
- Pthreads and OpenMP perform almost identically; differences are small and within what run-to-run variation can produce (each thread count was measured once).
- 16 threads gives about 9x, not 16x. Real parallel programs pay for thread management, scheduling, memory access, OS activity, and non-parallel work (the sequential baseline itself varies by about 0.01 s across runs).
- Race conditions occurred in both models when `counter++` was unprotected; a mutex (Pthreads) and `critical` (OpenMP) both restored the correct result.

## Pthreads vs OpenMP

| Concept | Pthreads | OpenMP |
|---|---|---|
| Create threads | `pthread_create()` | `#pragma omp parallel` |
| Wait for threads | `pthread_join()` | implicit at end of region |
| Work distribution | programmer divides the work | `parallel for` |
| Protect shared data | mutex | `critical` |
| Coordination | join / synchronization | `barrier` |
| Combine partial results | programmer-managed | `reduction` |

## Screenshots (actual terminal output)

**Setup, `thread1`, `thread2`**
![Setup, thread1, thread2](docs/screenshots/01_setup_thread1_thread2.png)

**`thread_sum`, `race`, `mutex`**
![thread_sum, race, mutex](docs/screenshots/02_thread_sum_race_mutex.png)

**`omp_hello`**
![omp_hello](docs/screenshots/03_omp_hello.png)

**`omp_for`, `omp_race`, `omp_critical`**
![omp_for, omp_race, omp_critical](docs/screenshots/04_omp_for_race_critical.png)

**`omp_barrier`**
![omp_barrier](docs/screenshots/05_omp_barrier.png)

**Sequential baseline (5 runs)**
![sequential](docs/screenshots/06_sequential.png)

**`pthread_perf` (1, 2, 4, 6, 16 threads)**
![pthread_perf](docs/screenshots/07_pthread_perf.png)

**`omp_perf` (1, 2, 4, 6, 16 threads)**
![omp_perf](docs/screenshots/08_omp_perf.png)
