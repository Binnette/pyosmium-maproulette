#!/usr/bin/env bash
set -euo pipefail

echo "=== Update apt ==="
sudo apt-get update -y

echo "=== Install osmium & aria2 ==="
sudo apt-get install -y osmium-tool aria2

echo "=== Install Python requirements ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Create directories ==="
mkdir -p in
mkdir -p tmp
mkdir -p out

echo "=== Download France OSM extract with aria2 ==="
aria2c \
  --max-connection-per-server=16 \
  --split=16 \
  --continue=true \
  --dir="in" \
  --out="latest.osm.pbf" \
  "https://download.geofabrik.de/europe-latest.osm.pbf"

echo "=== Done ==="
