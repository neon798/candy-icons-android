#!/usr/bin/env python3
"""Generate app/assets/appfilter.xml from mapping.json."""

import json
import os
import sys
from pathlib import Path

MAPPING_JSON = "mapping.json"
APPFILTER_OUT = "app/src/main/assets/appfilter.xml"


def sanitize(name):
    """Replace invalid resource name chars with underscores and lowercase."""
    result = ""
    for c in name.lower():
        result += c if c.isalnum() or c == "_" else "_"
    return result


def generate():
    root_dir = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    if not Path(MAPPING_JSON).exists():
        print(f"Error: {MAPPING_JSON} not found.", file=sys.stderr)
        sys.exit(1)

    with open(MAPPING_JSON) as f:
        entries = json.load(f)

    print(f"Generating appfilter.xml from {len(entries)} mapping entries...")

    # Group by drawable name for sorted output
    # Format: <item component="ComponentInfo{package/activity}" drawable="svgname" />
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<resources>')
    lines.append('')

    # Sort by drawable name (SVG name) for consistency
    sorted_entries = sorted(entries, key=lambda e: (e["svg"].lower(), e["component"]))
    for entry in sorted_entries:
        component = entry["component"]
        # Remove ComponentInfo{...} wrapper if present
        if component.startswith("ComponentInfo{"):
            component = component[14:-1]
        # Use the SVG name as drawable name so it matches the PNG filename
        drawable = sanitize(entry["svg"])
        name = entry.get("name", drawable)
        lines.append(
            f'  <item component="ComponentInfo{{{component}}}" drawable="{drawable}" name="{name}" />'
        )

    lines.append('')
    lines.append('</resources>')

    out_path = Path(APPFILTER_OUT)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Written {APPFILTER_OUT} with {len(sorted_entries)} entries")


if __name__ == "__main__":
    generate()
