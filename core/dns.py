# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

import socket

from core.models import DnsResult


def resolve_dns(target: str) -> DnsResult:
    try:
        results = socket.getaddrinfo(target, None)

        ip_addresses = sorted({
            item[4][0]
            for item in results
        })

        return DnsResult(
            target=target,
            resolved=True,
            ip_addresses=ip_addresses
        )

    except socket.gaierror as error:
        return DnsResult(
            target=target,
            resolved=False,
            ip_addresses=[],
            error=str(error)
        )