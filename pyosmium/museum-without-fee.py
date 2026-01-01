#!/usr/bin/env python3
"""
Extract museums without fee from an input file (PBF, etc).

Workflow suggestion:
1. Run this script
2. Open the output OSM file in JOSM
3. Update data
4. Ctrl+F with filter: tourism=museum -fee
5. Create a new layer
6. Merge selection into new layer (Ctrl+Shift+M)
7. Save the new layer as GeoJSON
"""

import argparse
import logging
import os
import time
import osmium


# ---------------------------------------------------------------------------
# Handler
# ---------------------------------------------------------------------------

class MuseumWithoutFee(osmium.SimpleHandler):
    """Extract nodes and ways tagged tourism=museum without a fee tag."""

    def __init__(self, writer, show_progress=True):
        super().__init__()
        self.writer = writer
        self.show_progress = show_progress
        self.nb_nodes = 0
        self.nb_ways = 0

    @staticmethod
    def is_concerned(obj):
        return obj.tags.get("tourism") == "museum" and "fee" not in obj.tags

    def _progress(self):
        if self.show_progress:
            print(f"\rNodes: {self.nb_nodes:,}  Ways: {self.nb_ways:,}", end="", flush=True)

    def node(self, n):
        if self.is_concerned(n):
            self.nb_nodes += 1
            self.writer.add_node(n)
            self._progress()

    def way(self, w):
        if self.is_concerned(w):
            self.nb_ways += 1
            self.writer.add_way(w)
            self._progress()


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def extract_museums(input_file, output_file, show_progress=True):
    start = time.time()

    if os.path.exists(output_file):
        logging.info(f"Deleting existing file: {output_file}")
        os.remove(output_file)

    logging.info("Initializing writer")
    writer = osmium.SimpleWriter(output_file)

    logging.info("Initializing handler")
    handler = MuseumWithoutFee(writer, show_progress=show_progress)

    logging.info("Processing input file...")
    handler.apply_file(input_file, locations=False)

    writer.close()

    duration = time.time() - start
    h, rem = divmod(duration, 3600)
    m, s = divmod(rem, 60)

    print()  # newline after progress
    logging.info(f"Nodes found: {handler.nb_nodes:,}")
    logging.info(f"Ways found:  {handler.nb_ways:,}")
    logging.info(f"Program ended in {int(h):02d}:{int(m):02d}:{s:05.2f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract museums without fee from an OSM file."
    )
    parser.add_argument("-i", "--input", required=True, help="Input OSM/PBF file")
    parser.add_argument("-o", "--output", default="museum-no-fee.osm",
                        help="Output OSM file")
    parser.add_argument("--no-progress", action="store_true",
                        help="Disable progress display")
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    args = parse_args()

    logging.info(f"Input:  {args.input}")
    logging.info(f"Output: {args.output}")

    extract_museums(args.input, args.output, show_progress=not args.no_progress)


if __name__ == "__main__":
    main()
