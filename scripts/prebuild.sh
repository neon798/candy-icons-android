#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

echo "=== Candy Icons Android - Prebuild ==="
echo ""

# Step 1: Generate mapping.json from Candy Icons SVGs x Lawnicons appfilter
echo "--- Step 1: Mapping Candy icons to Android components ---"
python3 "$SCRIPT_DIR/generate_mapping.py"
echo ""

# Step 2: Render SVGs to PNGs
echo "--- Step 2: Rendering SVGs to PNGs ---"
python3 "$SCRIPT_DIR/convert.py"
echo ""

# Step 3: Generate appfilter.xml
echo "--- Step 3: Generating appfilter.xml ---"
python3 "$SCRIPT_DIR/generate_appfilter.py"
echo ""

echo "=== Prebuild complete ==="
echo "Run './gradlew assembleRelease' to build the APK."
