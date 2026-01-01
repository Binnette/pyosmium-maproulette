#!/usr/bin/env bash
set -euo pipefail

echo "⏩ 1 - Extract all museums"
osmium tags-filter \
    in/latest.osm.pbf \
    -R -O \
    -o tmp/museum.osm \
    nw/tourism=museum

echo "⏩ 2 - Remove museums with website tag"
osmium tags-filter \
    tmp/museum.osm \
    -O \
    -o tmp/museum-no-website.osm \
    -i website contact:website

echo "⏩ 3 - Export to GeoJSON"
osmium export \
    tmp/museum-no-website.osm \
    -c conf/museum.conf \
    -O \
    -o out/museum-no-website.geojson

echo "⏩ 4 - Cleaning temporary files"
rm -rf tmp/*

echo "✅ Done: museums without website"
