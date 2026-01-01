"""
Return a list of ways with discouraged oneway values
Encouraged values are yes, no, -1, reversible & alternating
Execution take 4m50 on france.osm.pbf (4.5GB)
"""
import osmium as o
import sys


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
        print("  [oneway]")
        print("  [oneway!=yes]")
        print("  [oneway!=no]")
        print("  [oneway!=-1]")
        print("  [oneway!=reversible]")
        print("  [oneway!=alternating];")
        print("// End of Overpass query")
        print("out meta geom;", flush=True)

    def print_way(self, id, val):
        try:
            print("  way(%s); // oneway=%s" % (id, val), flush=True)
        except:
            print("  way(%s);" % id, flush=True)

    def way(self, w):
        if 'oneway' in w.tags:
            val = w.tags.get('oneway')
            ok = ["yes", "no", "-1", "reversible", "alternating"]
            if val not in ok:
                self.print_way(w.id, val)


def main(osmfile):
    handler = DiscouragedOnewayValuesHandler()
    handler.apply_file(osmfile)
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile> > oneway-val.opq" % sys.argv[0])
        sys.exit(-1)

    exit(main(sys.argv[1]))
