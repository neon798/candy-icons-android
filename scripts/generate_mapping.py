#!/usr/bin/env python3
"""Cross-reference Candy Icons SVG names against Lawnicons' appfilter.xml
to produce mapping.json — our source of truth for which Android components
map to which Candy icon."""

import json
import os
import re
import xml.etree.ElementTree as ET

CANDY_SVG_DIR = "candy-icons/apps/scalable"
LAWNICONS_APPFILTER = "lawnicons_appfilter.xml"
MAPPING_OUT = "mapping.json"


def parse_lawnicons_appfilter(path):
    """Parse Lawnicons appfilter.xml, return dict: drawable_name -> [components]"""
    tree = ET.parse(path)
    root = tree.getroot()
    mapping = {}
    for item in root.findall("item"):
        component = item.get("component", "")
        drawable = item.get("drawable", "")
        name = item.get("name", drawable)
        if not drawable:
            continue
        if drawable not in mapping:
            mapping[drawable] = []
        mapping[drawable].append({
            "component": component,
            "name": name,
        })
    return mapping


def get_candy_svg_names(svg_dir):
    """Return set of SVG base names (without .svg) from Candy Icons apps/scalable."""
    names = set()
    for f in os.listdir(svg_dir):
        if f.endswith(".svg"):
            names.add(f[:-4])
    return names


def normalize_name(name):
    """Normalize name for fuzzy matching: lowercase, strip common prefixes/suffixes."""
    n = name.lower()
    # Remove leading numbers/hashes like "5961_"
    n = re.sub(r'^[0-9a-f]{3,6}_', '', n)
    # Remove trailing version/build qualifiers
    n = re.sub(r'[-_](?:bin|icon|gtk3|linux|desktop|nativefier|original|mozilla-build|48x48|512x512)(?:-\d+(?:\.\d+)*)?$', '', n)
    # Remove version numbers like -2.10, -3.5, -4.0
    n = re.sub(r'[-_]\d+(?:\.\d+)*$', '', n)
    # Remove -Default suffix from Chrome extension icons
    n = re.sub(r'[-_][Dd]efault$', '', n)
    # Remove "org." prefix for matched org.* names
    # (we'll handle this separately)
    return n


def generate_mapping():
    print("Parsing Lawnicons appfilter.xml...")
    lawnicons = parse_lawnicons_appfilter(LAWNICONS_APPFILTER)
    print(f"  Found {len(lawnicons)} unique drawable names in Lawnicons")

    print("Reading Candy Icons SVG names...")
    candy_names = get_candy_svg_names(CANDY_SVG_DIR)
    print(f"  Found {len(candy_names)} SVGs in Candy Icons")

    # Build lookup by normalized name
    lawnicons_by_normalized = {}
    for drawable, entries in lawnicons.items():
        norm = normalize_name(drawable)
        if norm not in lawnicons_by_normalized:
            lawnicons_by_normalized[norm] = []
        lawnicons_by_normalized[norm].append((drawable, entries))

    matches = []
    candy_matched = set()

    # Phase 1: exact match on normalized name
    for candy_name in sorted(candy_names):
        norm_candy = normalize_name(candy_name)
        
        # Also try without "org." prefix for names that start with "org."
        alt_names = [norm_candy]
        if candy_name.startswith("org."):
            # Try org.Package.Name -> packagename
            parts = candy_name.split(".")
            if len(parts) >= 3:
                # Try the last two parts as a name
                for i in range(1, len(parts)):
                    alt_names.append(parts[i].lower())
                # Also try the full name without "org."
                alt_names.append(normalize_name(".".join(parts[1:])))

        for alt in alt_names:
            if alt in lawnicons_by_normalized:
                for (orig_drawable, entries) in lawnicons_by_normalized[alt]:
                    for entry in entries:
                        match = {
                            "svg": candy_name,
                            "component": entry["component"],
                            "name": entry["name"],
                            "drawable": entry.get("drawable", orig_drawable),
                        }
                        matches.append(match)
                        candy_matched.add(candy_name)
                break  # Only match once per candy icon

    print(f"  Matched {len(matches)} component entries using {len(candy_matched)} Candy SVGs")

    # Phase 2: Try more aggressive matching for unmatched
    unmatched = candy_names - candy_matched
    print(f"  Unmatched: {len(unmatched)} Candy SVGs remain")

    # For unmatched, try matching by ignoring underscores/hyphens
    for candy_name in sorted(unmatched):
        norm_candy = normalize_name(candy_name)
        # Try removing all non-alphanumeric chars
        condensed = re.sub(r'[^a-z0-9]', '', norm_candy)
        
        for lawn_drawable, entries in lawnicons.items():
            lawn_norm = normalize_name(lawn_drawable)
            lawn_condensed = re.sub(r'[^a-z0-9]', '', lawn_norm)
            
            if condensed == lawn_condensed and len(condensed) > 3:
                for entry in entries:
                    matches.append({
                        "svg": candy_name,
                        "component": entry["component"],
                        "name": entry["name"],
                        "drawable": entry.get("drawable", lawn_drawable),
                    })
                candy_matched.add(candy_name)
                break

    print(f"  After fuzzy match: {len(matches)} total entries, {len(candy_matched)} Candy SVGs matched")

    # Deduplicate: keep first occurrence of each component only
    # (multiple SVGs may match the same component; first match wins)
    seen = set()
    deduped = []
    for m in matches:
        key = m["component"]
        if key not in seen:
            seen.add(key)
            deduped.append(m)

    print(f"  After dedup: {len(deduped)} entries")

    # Write mapping.json
    with open(MAPPING_OUT, "w") as f:
        json.dump(deduped, f, indent=2)

    print(f"\nWritten {MAPPING_OUT} with {len(deduped)} entries")

    # Summary
    print(f"\n--- Summary ---")
    print(f"Total Candy SVGs:          {len(candy_names)}")
    print(f"Matched (have mapping):    {len(candy_matched)}")
    print(f"Unmatched (no mapping):    {len(unmatched & candy_matched)}")
    print(f"Total mapping entries:     {len(deduped)}")

    # Save list of matched SVGs for the convert script
    matched_svgs = sorted(candy_matched)
    with open("matched_svgs.txt", "w") as f:
        for s in matched_svgs:
            f.write(s + ".svg\n")
    print(f"Written matched_svgs.txt with {len(matched_svgs)} SVG filenames")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    generate_mapping()
