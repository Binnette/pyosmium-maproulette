#!/usr/bin/env bash
set -euo pipefail

echo "⏩ 1 - Extract all places of worship"
osmium tags-filter \
    in/latest.osm.pbf \
    -R -O \
    -o tmp/place_of_worship.osm \
    amenity=place_of_worship

echo "⏩ 2 - Remove those that *have* a religion tag"
osmium tags-filter \
    tmp/place_of_worship.osm \
    -O \
    -o tmp/place_of_worship-no-religion.osm \
    -i religion

echo "⏩ 3 - Export to GeoJSON"
osmium export \
    tmp/place_of_worship-no-religion.osm \
    -c conf/place-of-worship.conf \
    -O \
    -o out/place_of_worship-no-religion.geojson

echo "⏩ 4 - Cleaning temporary files"
rm -rf tmp/*

echo "✅ Done: place_of_worship without religion"
