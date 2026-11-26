import csv
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

GEM5_BIN = "/home/amitshukla/gem5/build/X86/gem5.opt"
SE_SCRIPT = "/home/amitshukla/gem5/assignment6_tlp/se_tlp.py"
DAXPY_BIN = "/home/amitshukla/gem5/assignment6_tlp/daxpy_static"
OUT_BASE = "/home/amitshukla/gem5/assignment6_tlp/sweep_out"

VECTOR_SIZE = 100000
THREAD_COUNTS = [1, 2, 4, 8]
LATENCY_PAIRS = [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]

os.makedirs(OUT_BASE, exist_ok=True)

def run_sim(params):
    threads, op_lat, issue_lat = params
    tag = f"t{threads}_op{op_lat}_iss{issue_lat}"
    out_dir = os.path.join(OUT_BASE, tag)

    cmd = [
        GEM5_BIN, "-d", out_dir, SE_SCRIPT,
        "--cpu-type=X86MinorCPU",
        f"--num-cpus={threads}",
        "--caches", "--l2cache",
        f"--cmd={DAXPY_BIN}",
        f"--options={VECTOR_SIZE} {threads}",
    ]
    for c in range(threads):
        cmd.extend(["-P", f"system.cpu[{c}].executeFuncUnits.funcUnits[4].opLat={op_lat}"])
        cmd.extend(["-P", f"system.cpu[{c}].executeFuncUnits.funcUnits[4].issueLat={issue_lat}"])

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    kernel_sec = None
    for line in res.stdout.splitlines():
        m = re.search(r"elapsed_seconds=([0-9.]+)", line)
        if m:
            kernel_sec = float(m.group(1))
    return (threads, op_lat, issue_lat, out_dir, kernel_sec, res.returncode)

def parse_stats(out_dir, threads, issue_lat):
    stats_path = os.path.join(out_dir, "stats.txt")
    data = {}
    with open(stats_path) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2 and not parts[0].startswith("-"):
                try:
                    data[parts[0]] = float(parts[1])
                except ValueError:
                    pass

    sim_sec = data.get("simSeconds", 0.0)
    ipcs, cpis, utils, cycles_list = [], [], [], []
    fp_classes = [
        "SimdFloatMult", "SimdFloatAdd", "SimdFloatCvt",
        "SimdAlu", "SimdMisc", "FloatAdd", "FloatMult"
    ]

    for c in range(threads):
        prefix = f"system.cpu{c}" if threads > 1 else "system.cpu"
        cyc = data.get(f"{prefix}.numCycles", 1.0)
        ipc = data.get(f"{prefix}.ipc", 0.0)
        cpi = data.get(f"{prefix}.cpi", 0.0)
        fp_insts = sum(data.get(f"{prefix}.issuedInstType_0::{cls}", 0.0) for cls in fp_classes)
        util = (fp_insts * issue_lat / cyc) * 100.0 if cyc > 0 else 0.0

        cycles_list.append(cyc)
        ipcs.append(ipc)
        cpis.append(cpi)
        utils.append(util)

    return {
        "sim_seconds": sim_sec,
        "avg_cycles": sum(cycles_list) / len(cycles_list),
        "avg_ipc": sum(ipcs) / len(ipcs),
        "worker_ipc_avg": sum(ipcs[1:]) / len(ipcs[1:]) if threads > 1 else ipcs[0],
        "avg_cpi": sum(cpis) / len(cpis),
        "fu_util_pct": sum(utils) / len(utils),
    }

tasks = [(t, op, iss) for t in THREAD_COUNTS for (op, iss) in LATENCY_PAIRS]
print(f"Running {len(tasks)} simulations...")

with ThreadPoolExecutor(max_workers=4) as pool:
    raw_results = list(pool.map(run_sim, tasks))

rows = []
baselines_sim = {}
baselines_kernel = {}

for threads, op_lat, issue_lat, out_dir, kernel_sec, rc in raw_results:
    if rc != 0:
        print(f"FAILED: t={threads} op={op_lat} iss={issue_lat}")
        continue
    metrics = parse_stats(out_dir, threads, issue_lat)
    row = {
        "threads": threads,
        "opLat": op_lat,
        "issueLat": issue_lat,
        "kernel_sec": kernel_sec,
        **metrics,
    }
    rows.append(row)
    if threads == 1:
        baselines_sim[(op_lat, issue_lat)] = metrics["sim_seconds"]
        baselines_kernel[(op_lat, issue_lat)] = kernel_sec

for row in rows:
    key = (row["opLat"], row["issueLat"])
    row["total_speedup"] = baselines_sim[key] / row["sim_seconds"]
    row["kernel_speedup"] = baselines_kernel[key] / row["kernel_sec"]

csv_path = "/home/amitshukla/gem5/assignment6_tlp/results.csv"
fieldnames = [
    "threads", "opLat", "issueLat", "sim_seconds", "kernel_sec",
    "total_speedup", "kernel_speedup", "avg_ipc", "worker_ipc_avg",
    "avg_cpi", "fu_util_pct"
]
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\nDone! Summary Table:")
print(f"{'Threads':>7} | {'opLat':>5} | {'issLat':>6} | {'SimSec':>9} | {'KernSec':>9} | {'TotSpd':>6} | {'KernSpd':>7} | {'AvgIPC':>6} | {'WrkIPC':>6} | {'FU_Util%':>8}")
print("-" * 88)
for r in rows:
    print(f"{r['threads']:>7} | {r['opLat']:>5} | {r['issueLat']:>6} | {r['sim_seconds']:>9.6f} | {r['kernel_sec']:>9.6f} | {r['total_speedup']:>6.2f} | {r['kernel_speedup']:>7.2f} | {r['avg_ipc']:>6.3f} | {r['worker_ipc_avg']:>6.3f} | {r['fu_util_pct']:>7.2f}%")
