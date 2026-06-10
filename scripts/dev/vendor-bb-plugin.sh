#!/usr/bin/env bash
# DEPRECATED (06/09/2026): historical vendoring script — DO NOT RE-RUN.
# The repo's templates-us/ files were translated to English, renamed to English
# slugs, and reorganized into the 5 hardware-division department folders
# (+ _shared/). Re-running this script would restore Vietnamese-named files in
# the old 12-department layout from the upstream zip and destroy that work.
echo "DEPRECATED: this script would undo the US localization + division restructure. Aborting."
exit 1
set -euo pipefail

if [[ "${BASH_VERSINFO[0]}" -lt 4 ]]; then
  echo "❌ Requires bash >= 4 (on macOS: brew install bash)"
  exit 1
fi

PLUGIN_PATH="${1:-references/business-builder.plugin}"
TARGET="templates-us"

if [ ! -f "$PLUGIN_PATH" ]; then
  echo "❌ Not found: $PLUGIN_PATH"
  exit 1
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
unzip -q "$PLUGIN_PATH" -d "$TMP"

mkdir -p "$TARGET"

# Map bb-* skills → templates-us dept codes
declare -A MAP=(
  [bb-orchestrator]="_orchestrator"
  [bb-governance]="01-governance"
  [bb-strategy]="02-strategy"
  [bb-finance]="03-finance"
  [bb-people]="04-people"
  [bb-operations]="05-operations"
  [bb-sales]="06-sales"
  [bb-marketing]="07-marketing"
  [bb-customer]="08-customer"
  [bb-product-tech]="09-product-tech"
  [bb-training]="10-training"
  [bb-reporting]="11-reporting"
  [bb-growth]="12-growth"
)

for src in "${!MAP[@]}"; do
  dst="${MAP[$src]}"
  mkdir -p "$TARGET/$dst"
  if [ -d "$TMP/skills/$src/references" ]; then
    cp -r "$TMP/skills/$src/references/"* "$TARGET/$dst/"
    echo "✓ $src → $dst ($(find "$TARGET/$dst" -maxdepth 1 -name '*.md' | wc -l) files)"
  fi
done

echo "✅ Vendored to $TARGET/"
