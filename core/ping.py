# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

import subprocess
import re

from core.models import PingResult


def run_ping(target: str, count: int = 4) -> PingResult:
    cmd = ["ping", "-n", str(count), target]

    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    raw = completed.stdout

    received_match = re.search(r"Received = (\d+)", raw)
    lost_match = re.search(r"Lost = (\d+)", raw)
    avg_match = re.search(r"Average = (\d+)ms", raw)
    min_match = re.search(r"Minimum = (\d+)ms", raw)
    max_match = re.search(r"Maximum = (\d+)ms", raw)

    received = int(received_match.group(1)) if received_match else 0
    lost = int(lost_match.group(1)) if lost_match else count

    return PingResult(
        target=target,
        reachable=completed.returncode == 0,
        packets_sent=count,
        packets_received=received,
        packet_loss=(lost / count) * 100,
        min_latency=float(min_match.group(1)) if min_match else None,
        avg_latency=float(avg_match.group(1)) if avg_match else None,
        max_latency=float(max_match.group(1)) if max_match else None,
        raw_output=raw
    )