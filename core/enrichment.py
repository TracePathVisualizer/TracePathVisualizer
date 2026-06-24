# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

import ipaddress
import json
import urllib.request

from core.models import Hop, LocalEndpoint


# ==================================================
# IP Utilities
# ==================================================

def is_public_ip(ip: str) -> bool:
    try:
        address = ipaddress.ip_address(ip)
        return address.is_global
    except ValueError:
        return False


def parse_location(loc: str | None) -> tuple[float | None, float | None]:
    if not loc:
        return None, None

    try:
        latitude, longitude = loc.split(",", 1)
        return float(latitude), float(longitude)
    except ValueError:
        return None, None


# ==================================================
# IPInfo Lookups
# ==================================================

def get_ipinfo(ip: str | None = None) -> dict:
    url = "https://ipinfo.io/json" if ip is None else f"https://ipinfo.io/{ip}/json"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return {}


def get_local_endpoint() -> LocalEndpoint:
    data = get_ipinfo()

    latitude, longitude = parse_location(data.get("loc"))

    return LocalEndpoint(
        public_ip=data.get("ip"),
        isp=data.get("org"),
        city=data.get("city"),
        country=data.get("country"),
        latitude=latitude,
        longitude=longitude
    )


# ==================================================
# Provider Inference
# ==================================================

def infer_owner_from_hostname(hostname: str | None) -> str | None:
    if not hostname:
        return None

    name = hostname.lower()

    if "vocus" in name:
        return "Vocus"

    if "google" in name:
        return "Google"

    if "microsoft" in name or "msn.net" in name:
        return "Microsoft"

    if "ovh" in name:
        return "OVH"
    
    if ".ix.asn.au" in name:
        return "IX Australia"

    return None


# ==================================================
# Hop Assessment
# ==================================================

def assess_hop(hop: Hop, hops: list[Hop]) -> str | None:
    probes = [hop.probe1, hop.probe2, hop.probe3]

    responses = sum(1 for probe in probes if probe is not None)

    if responses == 3:
        return "Responsive"

    if responses == 2:
        return "Partially Responsive"

    if responses == 1:
        return "Minimally Responsive"

    later_success = any(
        later_hop.ip
        for later_hop in hops
        if later_hop.hop > hop.hop
    )

    if later_success:
        return "Silent Node"

    return "Route Failure"


# ==================================================
# Silent Node Probability Engine
# ==================================================

def infer_silent_nodes(hops: list[Hop]) -> None:
    for index, hop in enumerate(hops):

        if hop.ip:
            continue

        previous_hop = None
        next_hop = None

        for i in range(index - 1, -1, -1):
            if hops[i].ip:
                previous_hop = hops[i]
                break

        for i in range(index + 1, len(hops)):
            if hops[i].ip:
                next_hop = hops[i]
                break

        if not previous_hop or not next_hop:
            continue

        if (
            previous_hop.asn == next_hop.asn
            and previous_hop.city == next_hop.city
            and previous_hop.country == next_hop.country
        ):
            hop.asn = next_hop.asn
            hop.city = next_hop.city
            hop.country = next_hop.country

        elif previous_hop.country == next_hop.country:
            hop.asn = "Domestic Handoff"
            hop.city = next_hop.city
            hop.country = next_hop.country

        else:
            hop.asn = "International Handoff"
            hop.city = next_hop.city
            hop.country = next_hop.country


# ==================================================
# Anycast Location Inference
# ==================================================

# NOTE:
# This is a basic first-pass anycast inference engine.
# It is intended only to detect obvious cases where an
# anycast endpoint's reported geolocation is inconsistent
# with the observed latency profile.
#
# Current logic uses a simple latency tolerance threshold
# and should be considered indicative only.
#
# Future versions should incorporate regional latency
# models, country proximity, submarine cable routes,
# and additional path-analysis heuristics.

def infer_anycast_locations(hops: list[Hop]) -> None:
    latency_tolerance_ms = 10

    for index, hop in enumerate(hops):
        if not hop.anycast:
            continue

        if hop.average_latency is None:
            continue

        previous_hop = None

        for i in range(index - 1, -1, -1):
            if (
                hops[i].ip
                and hops[i].average_latency is not None
                and hops[i].city
                and hops[i].country
            ):
                previous_hop = hops[i]
                break

        if not previous_hop:
            continue

        latency_jump = hop.average_latency - previous_hop.average_latency

        if latency_jump <= latency_tolerance_ms:
            hop.city = previous_hop.city
            hop.country = previous_hop.country


# ==================================================
# Hop Enrichment
# ==================================================

def enrich_live_hop(hop: Hop, previous_hops: list[Hop]) -> Hop:
    """
    Enrich a single hop as it is discovered.

    Used by live traceroute output and future GUI map updates.
    Path-wide inference is handled separately after each hop is added
    to the current hop list.
    """
    hop.assessment = assess_hop(hop, previous_hops + [hop])

    if not hop.ip:
        return hop

    if not is_public_ip(hop.ip):
        return hop

    data = get_ipinfo(hop.ip)

    latitude, longitude = parse_location(data.get("loc"))
    owner = data.get("org") or infer_owner_from_hostname(hop.hostname)

    hop.asn = owner
    hop.isp = owner
    hop.country = data.get("country")
    hop.city = data.get("city")
    hop.latitude = latitude
    hop.longitude = longitude
    hop.anycast = bool(data.get("anycast"))

    return hop


def enrich_hops(hops: list[Hop]) -> list[Hop]:
    """
    Final path cleanup.

    By this point, live hops should already have IPinfo enrichment.
    This function only applies route-wide inference that benefits from
    seeing the full known path.
    """
    for hop in hops:
        hop.assessment = assess_hop(hop, hops)

    infer_anycast_locations(hops)
    infer_silent_nodes(hops)

    return hops