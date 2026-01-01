#!/usr/bin/env bash
set -euo pipefail

echo "⏩ 1 - Extract all shops with missing category (shop=yes)"
osmium tags-filter \
    in/latest.osm.pbf \
    -t -O \
    -o tmp/shop-no-category.osm \
    n/shop=yes

echo "⏩ 2 - Export to GeoJSON"
osmium export \
    tmp/shop-no-category.osm \
    -c conf/shop.conf \
    -O \
    -o out/shop-no-category.geojson

echo "⏩ 3 - Cleaning temporary files"
rm -rf tmp/*

echo "✅ Done: shops with missing category (shop=yes)"
