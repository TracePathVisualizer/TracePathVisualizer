# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

from urllib.parse import urlparse

# ==================================================
# URL Target Normalization
# ==================================================

def normalize_target(target: str) -> str:
    target = target.strip()

    if "://" not in target:
        target = "//" + target

    parsed = urlparse(target)

    return parsed.hostname or target.strip()