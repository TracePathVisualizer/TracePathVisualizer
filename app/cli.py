# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

from core.diagnostic import run_diagnostic_steps
from core.targets import normalize_target


# ==================================================
# General CLI Formatting
# ==================================================

def print_section(title: str, width: int = 90) -> None:
    print()
    print(title)
    print("-" * width)


def print_header() -> None:
    print()
    print("=" * 50)
    print("TracePathVisualizer (TPV)")
    print("=" * 50)


def format_probe(value: str | None) -> str:
    return "*" if value is None else value


# ==================================================
# DNS Output
# ==================================================

def print_dns(dns) -> None:
    print(f"{'Resolved:':<15} {dns.resolved}")

    if dns.ip_addresses:
        print(f"{'IP Addresses:':<15} {', '.join(dns.ip_addresses)}")

    if dns.error:
        print(f"{'DNS Error:':<15} {dns.error}")


# ==================================================
# Ping Output
# ==================================================

def print_ping(ping) -> None:
    print(f"{'Reachable:':<18} {ping.reachable}")
    print(f"{'Packets:':<18} {ping.packets_received}/{ping.packets_sent}")
    print(f"{'Packet Loss:':<18} {ping.packet_loss:.0f}%")

    if ping.avg_latency is not None:
        print(f"{'Average Latency:':<18} {ping.avg_latency:.0f} ms")


# ==================================================
# Traceroute Output
# ==================================================

def print_traceroute_header() -> None:
    print(
        f"{'Hop':<5}"
        f"{'Probe 1':<12}"
        f"{'Probe 2':<12}"
        f"{'Probe 3':<15}"
        f"{'IP':<20}"
        f"{'Assessment':<30}"
        f"{'Routing Type'}"
    )
    print("-" * 125)


def print_traceroute_hop(hop) -> None:
    routing_type = "AnyCast" if hop.anycast else "Standard"

    print(
        f"{hop.hop:<5}"
        f"{format_probe(hop.probe1):<12}"
        f"{format_probe(hop.probe2):<12}"
        f"{format_probe(hop.probe3):<15}"
        f"{(hop.ip or ''):<20}"
        f"{(hop.assessment or ''):<30}"
        f"{routing_type}",
        flush=True
    )

# ==================================================
# Network Path Output
# ==================================================

def print_route_map(result) -> None:
    print(
        f"{'Hop':<3} | "
        f"{'Network Owner':<40} | "
        f"{'IP':<18} | "
        f"{'City':<18} | "
        f"{'Country':<7} | "
        f"{'Avg':<8} | "
        f"{'Assessment'}"
    )

    print("-" * 125)

    for hop in result.trace.hops:
        avg_latency = (
            f"{hop.average_latency:.0f} ms"
            if hop.average_latency is not None
            else "N/A"
        )

        if not hop.ip:
            owner = hop.asn or f"[{hop.assessment}]"
            if owner.startswith("AS") and " " in owner:
                owner = owner.split(" ", 1)[1]
            ip = "Unknown"
            city = hop.city or ""
            country = hop.country or ""

        elif hop.hop == 1:
            owner = "Local Network"
            ip = result.local.public_ip or hop.ip
            city = result.local.city or ""
            country = result.local.country or ""
        
        else:
            owner = ""

            if hop.asn:
                owner = hop.asn
                if owner.startswith("AS") and " " in owner:
                    owner = owner.split(" ", 1)[1]

            ip = hop.ip
            city = hop.city or ""
            country = hop.country or ""

        print(
            f"{hop.hop:<3} | "
            f"{owner:<40} | "
            f"{ip:<18} | "
            f"{city:<18} | "
            f"{country:<7} | "
            f"{avg_latency:<8} | "
            f"{(hop.assessment or '')}"
        )
    print("-" * 125)

# ==================================================
# CLI Runner
# ==================================================

def run_cli() -> None:
    print_header()

    raw_target = input("\nEnter target host, IP, or URL: ").strip()
    target = normalize_target(raw_target)

    if not raw_target:
        print()
        print("No target entered. Exiting.")
        return

    print()
    print(f"Target: {raw_target}")

    if target != raw_target:
        print(f"Using host: {target}")

    final_result = None

    for stage in run_diagnostic_steps(target):
        if stage.name in ("local_started", "local_complete"):
            continue

        elif stage.name == "dns_started":
            print_section("DNS")
            print(stage.message, flush=True)

        elif stage.name == "dns_complete":
            print_dns(stage.data)

        elif stage.name == "ping_started":
            print_section("Ping")
            print(stage.message, flush=True)

        elif stage.name == "ping_complete":
            print_ping(stage.data)

        elif stage.name == "traceroute_started":
            print_section("Traceroute")
            print(stage.message, flush=True)
            print_traceroute_header()

        elif stage.name == "traceroute_hop":
            print_traceroute_hop(stage.data)

        elif stage.name == "traceroute_complete":
            pass

        elif stage.name == "enrichment_started":
            pass

        elif stage.name == "enrichment_complete":
            pass

        elif stage.name == "complete":
            final_result = stage.data
            print_section("Network Path")
            print()
            print_route_map(final_result)

    if final_result is None:
        print()
        print("Diagnostic did not complete.")
    try:
        input("\nPress Enter to exit...")
    except EOFError:
        pass