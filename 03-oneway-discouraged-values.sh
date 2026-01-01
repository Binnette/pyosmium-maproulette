#!/usr/bin/env bash
set -euo pipefail

echo "⏩ 1 - Filtering all oneway-tagged elements"
osmium tags-filter in/latest.osm.pbf \
    -t -O \
    -o tmp/oneway.osm \
    w/oneway

echo "⏩ 2 - Extracting discouraged oneway values"
osmium tags-filter tmp/oneway.osm \
    -t -O \
    -o tmp/oneway-discouraged-values.osm \
    -i oneway=yes oneway=no oneway=-1 oneway=reversible oneway=alternating

echo "⏩ 3 - Exporting to GeoJSON"
osmium export \
    tmp/oneway-discouraged-values.osm \
    -c conf/oneway.conf \
    -O \
    -o out/oneway-discouraged-values.geojson

echo "⏩ 4 - Cleaning temporary files"
rm -rf tmp/*

echo "✅ Done: oneways discouraged values"
