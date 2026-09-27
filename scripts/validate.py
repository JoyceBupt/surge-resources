#!/usr/bin/env python3
"""Validate icons and Meta rules, with optional published-byte checks."""
import argparse
import hashlib
import json
import struct
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remote", action="store_true", help="Verify published files")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "manifest.json").read_text())
    subscription = json.loads((ROOT / "surge-icons.json").read_text())
    require(manifest["schema_version"] == 1, "Unsupported manifest version")
    expected, seen = [], set()
    for item in manifest["icons"]:
        key = item["id"]
        require(key not in seen, f"Duplicate icon: {key}")
        seen.add(key)
        require(item["path"] == f"icons/{key}.png", f"Unexpected path: {key}")
        require(item["url"] == BASE + item["path"], f"Unexpected URL: {key}")
        data = (ROOT / item["path"]).read_bytes()
        require(data[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG: {key}")
        require(struct.unpack(">II", data[16:24]) == (item["width"], item["height"]),
                f"Dimensions differ: {key}")
        require(hashlib.sha256(data).hexdigest() == item["sha256"], f"Hash differs: {key}")
        source = (ROOT / item["source_file"]).resolve()
        require(source.is_relative_to(ROOT / "sources"), f"Invalid source path: {key}")
        require(hashlib.sha256(source.read_bytes()).hexdigest() == item["source_sha256"],
                f"Source hash differs: {key}")
        expected.append({"name": item["name"], "url": item["url"]})
        if args.remote:
            with urllib.request.urlopen(item["url"], timeout=30) as response:
                require(response.headers.get_content_type() == "image/png", f"Wrong MIME: {key}")
                require(response.read() == data, f"Remote bytes differ: {key}")
        print(f"OK {key}: {item['width']}x{item['height']}")
    require(subscription["icons"] == expected, "Subscription differs from manifest")
    require({p.name for p in (ROOT / "icons").iterdir()} == {f"{k}.png" for k in seen},
            "Unlisted files in icons directory")
    meta = (ROOT / "rules/meta.list").read_bytes()
    rules = [line for line in meta.decode("utf-8").splitlines()
             if line and not line.startswith("#")]
    require(len(rules) >= 500, "Meta ruleset is unexpectedly small")
    require(len(rules) == len(set(rules)), "Duplicate Meta rules")
    require(all(line.startswith(("DOMAIN,", "DOMAIN-SUFFIX,")) and line.count(",") == 1
                for line in rules), "Unsupported Meta rule")
    for domain in ("facebook.com", "instagram.com", "whatsapp.com", "threads.com",
                   "meta.ai", "oculus.com", "muse.ai", "instagr.am", "metacareers.com"):
        require(f"DOMAIN-SUFFIX,{domain}" in rules, f"Missing Meta domain: {domain}")
    print(f"OK meta: {len(rules)} domain rules")
    if args.remote:
        with urllib.request.urlopen(BASE + "surge-icons.json", timeout=30) as response:
            require(json.load(response) == subscription, "Remote subscription differs")
        with urllib.request.urlopen(BASE + "rules/meta.list", timeout=30) as response:
            require(response.read() == meta, "Remote Meta rules differ")
    print("PASS: icons, sources, metadata, subscription and Meta rules" +
          (" (including remote)" if args.remote else ""))


if __name__ == "__main__":
    main()
