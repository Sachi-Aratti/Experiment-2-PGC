#!/usr/bin/env python3
"""Compute speedup/efficiency from the measured times and draw the 3 graphs."""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RES = os.path.join(ROOT, "results")

with open(os.path.join(RES, "sequential_runs.csv")) as f:
    runs = [float(r["time_s"]) for r in csv.DictReader(f)]
seq = sum(runs) / len(runs)

threads, pth, omp = [], [], []
with open(os.path.join(RES, "performance.csv")) as f:
    for r in csv.DictReader(f):
        threads.append(int(r["threads"]))
        pth.append(float(r["pthreads_time_s"]))
        omp.append(float(r["openmp_time_s"]))

sp_p = [seq / t for t in pth]
sp_o = [seq / t for t in omp]
ef_p = [s / n * 100 for s, n in zip(sp_p, threads)]
ef_o = [s / n * 100 for s, n in zip(sp_o, threads)]

with open(os.path.join(RES, "speedup_efficiency.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["threads", "pthreads_speedup", "openmp_speedup",
                "pthreads_efficiency_pct", "openmp_efficiency_pct"])
    for row in zip(threads, sp_p, sp_o, ef_p, ef_o):
        w.writerow([row[0]] + [f"{x:.3f}" for x in row[1:]])

print(f"Sequential baseline (mean of {len(runs)} runs): {seq:.6f} s")
print(f"{'thr':>4} {'Pth s':>9} {'OMP s':>9} {'Pth S':>7} {'OMP S':>7} {'Pth E%':>7} {'OMP E%':>7}")
for i, n in enumerate(threads):
    print(f"{n:>4} {pth[i]:>9.6f} {omp[i]:>9.6f} {sp_p[i]:>7.3f} {sp_o[i]:>7.3f} {ef_p[i]:>7.2f} {ef_o[i]:>7.2f}")

def style(ax, title, ylabel):
    ax.set_title(title)
    ax.set_xlabel("Number of threads")
    ax.set_ylabel(ylabel)
    ax.set_xticks(threads)
    ax.grid(True, alpha=0.3)
    ax.legend()

# Figure 1: execution time
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(threads, pth, "o-", label="Pthreads")
ax.plot(threads, omp, "s-", label="OpenMP")
ax.axhline(seq, color="gray", ls="--", label=f"Sequential ({seq:.3f} s)")
style(ax, "Figure 1 - Execution Time vs Number of Threads", "Execution time (s)")
fig.tight_layout(); fig.savefig(os.path.join(RES, "fig1_execution_time.png"), dpi=150); plt.close(fig)

# Figure 2: speedup
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(threads, sp_p, "o-", label="Pthreads")
ax.plot(threads, sp_o, "s-", label="OpenMP")
ax.plot(threads, threads, "k:", label="Ideal (linear)")
style(ax, "Figure 2 - Speedup vs Number of Threads", "Speedup (T_seq / T_par)")
fig.tight_layout(); fig.savefig(os.path.join(RES, "fig2_speedup.png"), dpi=150); plt.close(fig)

# Figure 3: efficiency
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(threads, ef_p, "o-", label="Pthreads")
ax.plot(threads, ef_o, "s-", label="OpenMP")
ax.axhline(100, color="k", ls=":", label="Ideal (100%)")
style(ax, "Figure 3 - Efficiency vs Number of Threads", "Efficiency (%)")
fig.tight_layout(); fig.savefig(os.path.join(RES, "fig3_efficiency.png"), dpi=150); plt.close(fig)
