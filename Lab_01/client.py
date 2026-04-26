# Student: mohamed nabil se3

import socket
import time
import statistics
import sys

def measure_latency(host='127.0.0.1', port=5000, num_requests=100):
    latencies = []
    message = b'PING'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"[CLIENT] Connected to {host}:{port}")
        print(f"[CLIENT] Sending {num_requests} requests...\n")

        for i in range(num_requests):
            start = time.perf_counter()
            s.sendall(message)
            _ = s.recv(1024)
            end = time.perf_counter()

            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)

            if (i + 1) % 20 == 0:
                print(f"  Completed {i+1}/{num_requests} | "
                      f"Last: {latency_ms:.4f} ms")

    return latencies

def print_stats(latencies):
    sorted_lat = sorted(latencies)
    p50 = sorted_lat[int(len(sorted_lat) * 0.50)]
    p95 = sorted_lat[int(len(sorted_lat) * 0.95)]
    p99 = sorted_lat[int(len(sorted_lat) * 0.99)]

    print("\n" + "=" * 55)
    print("        LATENCY STATISTICS REPORT")
    print("=" * 55)
    print(f"  Total Requests : {len(latencies)}")
    print(f"  Min Latency    : {min(latencies):.4f} ms")
    print(f"  Max Latency    : {max(latencies):.4f} ms")
    print(f"  Mean Latency   : {statistics.mean(latencies):.4f} ms")
    print(f"  Median (P50)   : {p50:.4f} ms")
    print(f"  Std Deviation  : {statistics.stdev(latencies):.4f} ms")
    print(f"  P95            : {p95:.4f} ms")
    print(f"  P99            : {p99:.4f} ms")
    print("=" * 55)

def print_ascii_histogram(latencies, bins=10):
    min_lat = min(latencies)
    max_lat = max(latencies)
    bin_size = (max_lat - min_lat) / bins if max_lat != min_lat else 1

    hist = [0] * bins
    for lat in latencies:
        idx = min(int((lat - min_lat) / bin_size), bins - 1)
        hist[idx] += 1

    max_count = max(hist)

    print("\n  ASCII Latency Histogram:")
    print("  " + "-" * 60)
    for i, count in enumerate(hist):
        lower = min_lat + i * bin_size
        upper = lower + bin_size
        bar_len = int(count / max_count * 40) if max_count > 0 else 0
        bar = '█' * bar_len
        print(f"  {lower:7.4f}-{upper:7.4f} ms | {bar:<40} ({count})")
    print("  " + "-" * 60)

def save_results(latencies):
    with open('latency_results.txt', 'w') as f:
        f.write("Latency Measurement Results\n")
        f.write("="*40 + "\n")
        f.write(f"Total Requests: {len(latencies)}\n")
        f.write(f"Min: {min(latencies):.4f} ms\n")
        f.write(f"Max: {max(latencies):.4f} ms\n")
        f.write(f"Mean: {statistics.mean(latencies):.4f} ms\n\n")
        f.write("Individual Measurements:\n")
        for i, lat in enumerate(latencies):
            f.write(f"Request {i+1:03d}: {lat:.4f} ms\n")
    print("\n[CLIENT] Results saved to latency_results.txt")

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    num_requests = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    latencies = measure_latency(host, port, num_requests)
    print_stats(latencies)
    print_ascii_histogram(latencies)
    save_results(latencies)