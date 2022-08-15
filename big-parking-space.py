"""
Return a list of parking space that are too big
They should be converted as parking lot
"""
import osmium as o
import sys
import shapely.wkb as wkblib

wkbfab = o.geom.WKBFactory()


class DiscouragedOnewayValuesHandler(o.SimpleHandler):
    def __init__(self):
        super(DiscouragedOnewayValuesHandler, self).__init__()
        self.print_overpass_header()

    def __del__(self):
        self.print_overpass_footer()

    def print_overpass_header(self):
        print("[out:json];")
        print("// Start of Overpass query")
        print("(", flush=True)

    def print_overpass_footer(self):
        print(");")
        print("")
        print("// Just reapply filter to ignore updated objects")
        print("way._")
        print("  [amenity=parking_space]")
        print("  [!capacity]")
        print("  (if: length() > 100);")
        print("// End of Overpass query")
        print("out body geom;", flush=True)

    def print_area(self, id, val):
        print("  way(%s); // length=%s" % (id, val), flush=True)

    def area(self, a):
        if a.tags.get('amenity') == 'parking_space':
            if 'capacity' not in a.tags:
                wkb = wkbfab.create_multipolygon(a)
                poly = wkblib.loads(wkb, hex=True)
                len = poly.length * 100000
                if poly.length > 100:
                    self.print_area(a.orig_id(), len)


def main(osmfile):
    handler = DiscouragedOnewayValuesHandler()
    handler.apply_file(osmfile)
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile> > parking-too-big.txt" % sys.argv[0])
        sys.exit(-1)

    exit(main(sys.argv[1]))
