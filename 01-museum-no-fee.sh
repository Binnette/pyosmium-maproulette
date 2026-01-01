#!/usr/bin/env bash
set -euo pipefail

echo "⏩ 1 - Extract all museums"
osmium tags-filter \
    in/latest.osm.pbf \
    -R -O \
    -o tmp/museum.osm \
    nw/tourism=museum

echo "⏩ 2 - Remove museums with fee tag"
osmium tags-filter \
    tmp/museum.osm \
    -O \
    -o tmp/museum-no-fee.osm \
    -i fee

echo "⏩ 3 - Export to GeoJSON ==="
osmium export \
    tmp/museum-no-fee.osm \
    -c conf/museum.conf \
    -O \
    -o out/museum-no-fee.geojson

echo "⏩ 4 - Cleaning temporary files"
rm -rf tmp/*

echo "✅ Done: museums without fee"
