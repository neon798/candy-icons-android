#!/usr/bin/env python3
"""Render Candy Icons SVGs to pixel-perfect PNGs for Android icon pack."""

import os
import sys
import subprocess
from pathlib import Path

CANDY_SVG_DIR = "candy-icons/apps/scalable"
OUTPUT_DIR = "app/src/main/res/drawable-nodpi"
MATCHED_SVGS = "matched_svgs.txt"
PNG_SIZE = 192


def sanitize(name):
    """Replace invalid resource name chars with underscores, lowercase,
    and prepend underscore if it starts with a non-letter."""
    result = ""
    for c in name.lower():
        result += c if c.isalnum() or c == "_" else "_"
    if result and not result[0].isalpha():
        result = "_" + result
    return result


def render_svg(svg_path, png_path, size):
    """Render SVG to PNG using cairosvg at the given size."""
    try:
        import cairosvg
    except ImportError:
        print("cairosvg not found. Run: pip install cairosvg")
        sys.exit(1)

    try:
        # First try cairosvg's svg2png with scale
        with open(svg_path, "rb") as f:
            svg_data = f.read()
        # Calculate scale factor (cairosvg default DPI is 96, so at 96 DPI the
        # output size is determined by the SVG's viewport. We just set output_width)
        cairosvg.svg2png(bytestring=svg_data,
                         write_to=str(png_path),
                         output_width=size,
                         output_height=size,
                         background_color="transparent")
        return True
    except Exception as e:
        print(f"    cairosvg failed: {e}", file=sys.stderr)
        return False


def main():
    root_dir = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    svg_dir = Path(CANDY_SVG_DIR)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read matched SVGs
    if not Path(MATCHED_SVGS).exists():
        print(f"Error: {MATCHED_SVGS} not found. Run generate_mapping.py first.")
        sys.exit(1)

    with open(MATCHED_SVGS) as f:
        svg_files = [line.strip() for line in f if line.strip()]

    print(f"Rendering {len(svg_files)} Candy Icons SVGs to {PNG_SIZE}x{PNG_SIZE} PNGs...")

    success = 0
    failed = 0
    for svg_file in sorted(svg_files):
        svg_path = svg_dir / svg_file
        if not svg_path.exists():
            # Try alternative names: some SVGs might be in other directories
            alt_path = Path("candy-icons") / svg_file
            if alt_path.exists():
                svg_path = alt_path
            else:
                print(f"  SKIP: {svg_file} not found")
                failed += 1
                continue

        stem = svg_file[:-4]
        png_name = sanitize(stem) + ".png"
        png_path = output_dir / png_name

        if png_path.exists():
            print(f"  EXISTS: {png_name}")
            success += 1
            continue

        print(f"  RENDERING: {png_name}")
        if render_svg(svg_path, png_path, PNG_SIZE):
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} rendered, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
