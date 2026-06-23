# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

from dataclasses import dataclass

@dataclass
class LocalEndpoint:
    public_ip: str | None
    isp: str | None
    city: str | None
    country: str | None
    latitude: float | None = None
    longitude: float | None = None

@dataclass
class PingResult:
    target: str
    reachable: bool
    packets_sent: int
    packets_received: int
    packet_loss: float
    min_latency: float | None
    avg_latency: float | None
    max_latency: float | None
    raw_output: str

@dataclass
class DnsResult:
    target: str
    resolved: bool
    ip_addresses: list[str]
    error: str | None = None

@dataclass
class Hop:
    hop: int
    probe1: str | None
    probe2: str | None
    probe3: str | None
    ip: str | None
    hostname: str | None
    assessment: str | None = None
    asn: str | None = None
    isp: str | None = None
    country: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    anycast: bool = False
    
    @property
    def average_latency(self) -> float | None:
        values = []

        for probe in (self.probe1, self.probe2, self.probe3):
            if probe is None:
                continue

            if "ms" not in probe:
                continue

            try:
                values.append(float(probe.replace("ms", "").replace("<", "").strip()))
            except ValueError:
                pass

        if not values:
            return None

        return round(sum(values) / len(values), 1)

@dataclass
class TraceResult:
    target: str
    destination_ip: str | None
    hops: list[Hop]
    raw_output: str
    error: str | None = None 

@dataclass
class DiagnosticResult:
    local: LocalEndpoint
    target: str
    ping: PingResult
    dns: DnsResult
    trace: TraceResult

