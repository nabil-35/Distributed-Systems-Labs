# Student:  mohamed nabil se3

import matplotlib.pyplot as plt
import numpy as np
import statistics

def read_latencies(filename='latency_results.txt'):
    latencies = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('Request'):
                value = line.strip().split(': ')[1].replace(' ms', '')
                latencies.append(float(value))
    return latencies

latencies = read_latencies()
sorted_lat = sorted(latencies)
cdf = np.arange(1, len(sorted_lat) + 1) / len(sorted_lat) * 100

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Lab 1 – TCP Latency Analysis', fontsize=14, fontweight='bold')

# --- Histogram ---
axes[0].hist(latencies, bins=20, color='steelblue', edgecolor='black', alpha=0.75)
axes[0].axvline(statistics.mean(latencies), color='red', linestyle='--',
                linewidth=2, label=f'Mean: {statistics.mean(latencies):.4f} ms')
axes[0].axvline(statistics.median(latencies), color='green', linestyle='--',
                linewidth=2, label=f'Median: {statistics.median(latencies):.4f} ms')
axes[0].set_xlabel('Latency (ms)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Latency Distribution Histogram')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# --- CDF ---
axes[1].plot(sorted_lat, cdf, color='steelblue', linewidth=2)
p95_val = sorted_lat[int(len(sorted_lat) * 0.95)]
p99_val = sorted_lat[int(len(sorted_lat) * 0.99)]
axes[1].axvline(p95_val, color='orange', linestyle='--',
                linewidth=2, label=f'P95: {p95_val:.4f} ms')
axes[1].axvline(p99_val, color='red', linestyle='--',
                linewidth=2, label=f'P99: {p99_val:.4f} ms')
axes[1].set_xlabel('Latency (ms)')
axes[1].set_ylabel('Cumulative %')
axes[1].set_title('Cumulative Distribution Function (CDF)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('latency_histogram.png', dpi=150, bbox_inches='tight')
plt.show()
print("Histogram saved as latency_histogram.png")