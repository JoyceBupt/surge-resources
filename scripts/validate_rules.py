#!/usr/bin/env python3
"""Validate public rule syntax and optional published contents."""
import argparse
import ipaddress
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remote", action="store_true")
    args = parser.parse_args()
    total = 0
    for path in sorted((ROOT / "rules").glob("*.list")):
        seen = set()
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split(",")
            valid = False
            if len(parts) == 2 and parts[0] in {"DOMAIN", "DOMAIN-SUFFIX"}:
                valid = bool(re.fullmatch(r"[a-z0-9.-]+", parts[1])) and "." in parts[1]
            elif len(parts) == 3 and parts[0] in {"IP-CIDR", "IP-CIDR6"} and parts[2] == "no-resolve":
                network = ipaddress.ip_network(parts[1], strict=True)
                valid = network.is_global and network.version == (6 if parts[0] == "IP-CIDR6" else 4)
            if not valid or line in seen:
                raise ValueError(f"Invalid, duplicate or unsupported public rule: {path.name}:{number}")
            seen.add(line)
        if not seen:
            raise ValueError(f"Empty ruleset: {path.name}")
        if args.remote:
            with urllib.request.urlopen(BASE + path.relative_to(ROOT).as_posix(), timeout=30) as response:
                if response.read() != path.read_bytes():
                    raise ValueError(f"Published rules differ: {path.name}")
        print(f"OK {path.name}: {len(seen)} rules")
        total += len(seen)
    if not total:
        raise ValueError("No rules found")
    print("PASS: public rule syntax (not a comprehensive secret scanner)")


if __name__ == "__main__":
    main()
