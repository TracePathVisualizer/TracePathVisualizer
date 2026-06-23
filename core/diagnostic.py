# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

from collections.abc import Generator
from dataclasses import dataclass

from core.models import DiagnosticResult, DnsResult, LocalEndpoint, PingResult, TraceResult
from core.ping import run_ping
from core.dns import resolve_dns
from core.traceroute import run_traceroute_live
from core.enrichment import enrich_hops, get_local_endpoint


# ==================================================
# Diagnostic Stage Event
# ==================================================

@dataclass
class DiagnosticStage:
    name: str
    message: str = ""
    data: object | None = None


# ==================================================
# Sequential Diagnostic Runner
# ==================================================

def run_diagnostic_steps(target: str) -> Generator[DiagnosticStage, None, DiagnosticResult]:
    local_endpoint: LocalEndpoint | None = None
    dns_result: DnsResult | None = None
    ping_result: PingResult | None = None
    trace_result: TraceResult | None = None

    # --------------------------------------------------
    # Local Endpoint
    # --------------------------------------------------

    local_endpoint = get_local_endpoint()

    # --------------------------------------------------
    # DNS
    # --------------------------------------------------

    yield DiagnosticStage(name="dns_started")
    dns_result = resolve_dns(target)
    yield DiagnosticStage(name="dns_complete", data=dns_result)

    # --------------------------------------------------
    # Ping
    # --------------------------------------------------

    yield DiagnosticStage(name="ping_started")
    ping_result = run_ping(target)
    yield DiagnosticStage(name="ping_complete", data=ping_result)

    # --------------------------------------------------
    # Traceroute
    # --------------------------------------------------

    yield DiagnosticStage(name="traceroute_started")

    trace_runner = run_traceroute_live(target)

    try:
        while True:
            hop = next(trace_runner)
            yield DiagnosticStage(name="traceroute_hop", data=hop)

    except StopIteration as finished:
        trace_result = finished.value

    yield DiagnosticStage(name="traceroute_complete", data=trace_result)

    # --------------------------------------------------
    # Enrichment
    # --------------------------------------------------

    yield DiagnosticStage(name="enrichment_started")

    if trace_result is None:
        raise RuntimeError("Traceroute failed before producing a result.")

    trace_result.hops = enrich_hops(trace_result.hops)

    yield DiagnosticStage(name="enrichment_complete", data=trace_result)

    # --------------------------------------------------
    # Final Result
    # --------------------------------------------------

    result = DiagnosticResult(
        target=target,
        local=local_endpoint,
        ping=ping_result,
        dns=dns_result,
        trace=trace_result
    )

    yield DiagnosticStage(name="complete", data=result)

    return result


# ==================================================
# Standard Diagnostic Runner
# ==================================================

def run_diagnostic(target: str) -> DiagnosticResult:
    result: DiagnosticResult | None = None

    for stage in run_diagnostic_steps(target):
        if stage.name == "complete":
            result = stage.data

    if result is None:
        raise RuntimeError("Diagnostic failed before completion.")

    return result