#!/bin/bash
# Script to package Microsoft Teams app manifest for upload

set -e


MANIFEST_FILE="manifest.json"
ZIP_NAME="teams-app-package.zip"

# Check if manifest file exists
if [ ! -f "$MANIFEST_FILE" ]; then
  echo "Manifest file not found: $MANIFEST_FILE"
  exit 1
fi

# Check for icons
for icon in outline.png color.png; do
  if [ ! -f "$icon" ]; then
    echo "Warning: $icon not found. Teams app may require icons."
  fi
done

# Create zip package
zip -j "$ZIP_NAME" "$MANIFEST_FILE" "outline.png" "color.png"

echo "Teams app package created: $ZIP_NAME"
