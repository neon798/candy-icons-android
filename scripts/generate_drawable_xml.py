#!/usr/bin/env python3
"""Generate res/xml/drawable.xml for manual icon picking."""

import os
import sys
from pathlib import Path

MATCHED_SVGS = "matched_svgs.txt"
DRAWABLE_XML = "app/src/main/res/xml/drawable.xml"


_RESERVED = frozenset({
    "abstract", "assert", "boolean", "break", "byte", "case", "catch",
    "char", "class", "const", "continue", "default", "do", "double",
    "else", "enum", "extends", "final", "finally", "float", "for",
    "goto", "if", "implements", "import", "instanceof", "int",
    "interface", "long", "native", "new", "null", "package",
    "private", "protected", "public", "return", "short", "static",
    "strictfp", "super", "switch", "synchronized", "this", "throw",
    "throws", "transient", "true", "false", "try", "void", "volatile",
    "while",
})


def sanitize(name):
    """Replace invalid resource name chars with underscores, lowercase,
    and prepend underscore if it starts with a non-letter or is a
    reserved keyword."""
    result = ""
    for c in name.lower():
        result += c if c.isalnum() or c == "_" else "_"
    if result and not result[0].isalpha():
        result = "_" + result
    if result in _RESERVED:
        result = "_" + result
    return result


def generate():
    root_dir = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    if not Path(MATCHED_SVGS).exists():
        print(f"Error: {MATCHED_SVGS} not found. Run generate_mapping.py first.",
              file=sys.stderr)
        sys.exit(1)

    with open(MATCHED_SVGS) as f:
        svg_files = [line.strip() for line in f if line.strip()]

    names = sorted({sanitize(svg.replace(".svg", "")) for svg in svg_files})
    print(f"Generating drawable.xml with {len(names)} icons...")

    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>", ""]
    for n in names:
        lines.append(f'    <item drawable="{n}" />')
    lines.append("")
    lines.append("</resources>")

    out_path = Path(DRAWABLE_XML)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Written {DRAWABLE_XML}")


if __name__ == "__main__":
    generate()
