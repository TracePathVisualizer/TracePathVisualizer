# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

import re
import subprocess
from collections.abc import Generator

from core.models import Hop, TraceResult


# ==================================================
# Probe Parsing
# ==================================================

def parse_probe_tokens(tokens: list[str], index: int) -> tuple[str | None, int]:
    if index >= len(tokens):
        return None, index

    token = tokens[index]

    if token == "*":
        return None, index + 1

    if token.startswith("<"):
        return f"{token} ms", index + 2

    if index + 1 < len(tokens) and tokens[index + 1] == "ms":
        return f"{token} ms", index + 2

    return token, index + 1


# ==================================================
# Traceroute Line Parsing
# ==================================================

def assess_probe_response(probe1: str | None, probe2: str | None, probe3: str | None) -> str:
    responses = sum(
        1
        for probe in (probe1, probe2, probe3)
        if probe is not None
    )

    if responses == 3:
        return "Responsive"

    if responses == 2:
        return "Partially Responsive"

    if responses == 1:
        return "Limited Response"

    return "No Response"


def parse_traceroute_hop(line: str) -> Hop | None:
    line = line.strip()

    if not line:
        return None

    if not re.match(r"^\d+\s+", line):
        return None

    tokens = line.split()

    hop_number = int(tokens[0])
    index = 1

    probe1, index = parse_probe_tokens(tokens, index)
    probe2, index = parse_probe_tokens(tokens, index)
    probe3, index = parse_probe_tokens(tokens, index)

    host_part = " ".join(tokens[index:])

    ip = None
    hostname = None
    assessment = assess_probe_response(probe1, probe2, probe3)

    if "Request timed out" in host_part:
        assessment = "No Response"
    else:
        ip_match = re.search(r"\[(.*?)\]", host_part)

        if ip_match:
            ip = ip_match.group(1)
            hostname = host_part.replace(f"[{ip}]", "").strip()
        else:
            ip = host_part if host_part else None

    return Hop(
        hop=hop_number,
        probe1=probe1,
        probe2=probe2,
        probe3=probe3,
        ip=ip,
        hostname=hostname,
        assessment=assessment
    )


# ==================================================
# Live Traceroute Runner
# ==================================================

def run_traceroute_live(target: str) -> Generator[Hop, None, TraceResult]:
    command = ["tracert", target]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    raw_lines: list[str] = []
    hops: list[Hop] = []
    destination_ip: str | None = None

    if process.stdout is not None:
        for line in process.stdout:
            raw_lines.append(line)

            if destination_ip is None:
                destination_match = re.search(r"\[(.*?)\]", line)
                if destination_match:
                    destination_ip = destination_match.group(1)

            hop = parse_traceroute_hop(line)

            if hop is None:
                continue

            hops.append(hop)
            yield hop

    stderr = ""

    if process.stderr is not None:
        stderr = process.stderr.read()

    return_code = process.wait()

    raw_output = "".join(raw_lines)

    return TraceResult(
        target=target,
        destination_ip=destination_ip,
        hops=hops,
        raw_output=raw_output,
        error=None if return_code == 0 else stderr
    )


# ==================================================
# Standard Traceroute Runner
# ==================================================

def run_traceroute(target: str) -> TraceResult:
    live_runner = run_traceroute_live(target)

    try:
        while True:
            next(live_runner)
    except StopIteration as finished:
        return finished.value