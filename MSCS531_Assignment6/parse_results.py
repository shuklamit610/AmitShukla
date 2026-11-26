import csv
import os
import re

OUT_BASE = "/home/amitshukla/gem5/assignment6_tlp/sweep_out"
THREAD_COUNTS = [1, 2, 4, 8]
LATENCY_PAIRS = [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]

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

rows = []
baselines_sim = {}

for threads in THREAD_COUNTS:
    for op_lat, issue_lat in LATENCY_PAIRS:
        out_dir = os.path.join(OUT_BASE, f"t{threads}_op{op_lat}_iss{issue_lat}")
        metrics = parse_stats(out_dir, threads, issue_lat)
        row = {
            "threads": threads,
            "opLat": op_lat,
            "issueLat": issue_lat,
            **metrics,
        }
        rows.append(row)
        if threads == 1:
            baselines_sim[(op_lat, issue_lat)] = metrics["sim_seconds"]

for row in rows:
    key = (row["opLat"], row["issueLat"])
    row["speedup_vs_same_fu"] = baselines_sim[key] / row["sim_seconds"]
    row["speedup_vs_default_1t"] = baselines_sim[(6, 1)] / row["sim_seconds"]

csv_path = "/home/amitshukla/gem5/assignment6_tlp/results.csv"
fieldnames = [
    "threads", "opLat", "issueLat", "sim_seconds", "avg_cycles",
    "speedup_vs_same_fu", "speedup_vs_default_1t", "avg_ipc",
    "worker_ipc_avg", "avg_cpi", "fu_util_pct"
]
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"{'Threads':>7} | {'opLat':>5} | {'issLat':>6} | {'SimSec':>9} | {'AvgCycles':>10} | {'Spd(FU)':>7} | {'Spd(Def)':>8} | {'AvgIPC':>6} | {'WrkIPC':>6} | {'AvgCPI':>6} | {'FU_Util%':>8}")
print("-" * 105)
for r in rows:
    print(f"{r['threads']:>7} | {r['opLat']:>5} | {r['issueLat']:>6} | {r['sim_seconds']:>9.6f} | {r['avg_cycles']:>10.0f} | {r['speedup_vs_same_fu']:>7.2f} | {r['speedup_vs_default_1t']:>8.2f} | {r['avg_ipc']:>6.3f} | {r['worker_ipc_avg']:>6.3f} | {r['avg_cpi']:>6.3f} | {r['fu_util_pct']:>7.2f}%")
