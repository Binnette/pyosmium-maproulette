"""
Return a list of parking space that are too big
They should be converted as parking lot

Stats for planet-220808.osm.pbf
-Total of ways: 682118
-Program ended in 00:47:25.52
"""
from io import TextIOWrapper
import osmium
import sys
import getopt
import time
import shapely.wkb as wkblib

wkbfab = osmium.geom.WKBFactory()

class DiscouragedOnewayValuesHandler(osmium.SimpleHandler):
    # output file
    out: TextIOWrapper
    # total ways for stats
    nbWay: int = 0
    # write in file or print in console
    withFile = True

    def __init__(self, withFile, outFileName):
        super(DiscouragedOnewayValuesHandler, self).__init__()
        self.withFile = withFile
        if self.withFile:
            self.out = open(outFileName, "w")

        self.printHeader()

    def __del__(self):
        self.printFooter()
        if self.withFile:
            self.out.close()

    def write(self, txt):
        if self.withFile:
            self.out.write("%s\n" % txt)
            self.out.flush()
        else:
            print(txt)

    # create and init output file
    def printHeader(self):
        self.write("[out:json];")
        self.write("// Start of Overpass query")
        self.write("(")

    # close output file
    def printFooter(self):
        self.write(");")
        self.write("")
        self.write("// Just reapply filter to ignore updated objects")
        self.write("way._")
        self.write("  [amenity=parking_space]")
        self.write("  [!capacity]")
        self.write("  (if: length() > 100);")
        self.write("// End of Overpass query")
        self.write("// Total of ways: %i" % self.nbWay)
        self.write("out meta geom;")
        if self.withFile:
            print("")
            print("Total of ways: %i" % self.nbWay, flush=True)

    def write_area(self, id, val):
        try:
            if val > 0:
                self.write("  way(%s); // len=%s" % (id, val))
            else:
                self.write("  way(%s);" % id)
            if self.withFile:
                sys.stdout.write("\rWays found: %i" % self.nbWay)
                sys.stdout.flush()
        except:
            self.write("  way(%s);" % id)
            if self.withFile:
                print("Warning: can not print length of way %s" % id)
                print("Ways found: %i" % self.nbWay, flush=True)

    def getlen(self, w):
        length = 0
        try:
            wkb = wkbfab.create_linestring(w, use_nodes=osmium.geom.use_nodes.UNIQUE)
            line = wkblib.loads(wkb, hex=True)
            length = line.length
        except Exception:
            length = -1

        if length != -1:
            return length

        try:
            length = osmium.geom.haversine_distance(w.nodes)
        except osmium.InvalidLocationError:
            length = -2

        return length
        

    # osmium way handler
    def way(self, w):
        osmium.make_simple_handler
        if w.tags.get('amenity') == 'parking_space':
            if 'capacity' not in w.tags:
                self.nbWay += 1 # increment counter
                self.write_area(w.id, -1)

    # osmium area handler
    def old_area(self, a):
        osmium.make_simple_handler
        if a.tags.get('amenity') == 'parking_space':
            if 'capacity' not in a.tags:
                try:
                    wkb = wkbfab.create_multipolygon(a)
                    poly = wkblib.loads(wkb, hex=True)              
                    len = poly.length * 100000               
                except:
                    len = -1
                if poly.length > 100:
                    self.nbWay += 1 # increment counter
                    self.write_area(a.orig_id(), len)

def main(input, withFile, output):
    osmium.make_simple_handler()
    handler = DiscouragedOnewayValuesHandler(withFile, output)
    handler.apply_file(input, locations=False)
    return 0

def print_help():
    print("Usage: python %s -i <osmfile> -o <output filename.opq>" % sys.argv[0])
    print("")
    print("Read the <osmfile> in input. Find the parking space that are too big.")
    print("Write an Overpass query in the <output filename.opq> that get osm elements (opq stands for Overpass Query")
    print("Use this query to create a MapRoulette challenge or in JOSM to create a QuickFix challenge with mr-cli util")
    print("")
    print("  -i <input osm file> such as planet.osm.pbf. All file supported by osmium should work")
    print("  -o <output filename.opq>. A file to write the Overpass query inside")
    print("", flush=True)

if __name__ == '__main__':
    nbArgs = len(sys.argv)
    if nbArgs != 3 and nbArgs != 5:
        print_help()
        sys.exit(-1)

    # default arguments values
    input = ""
    output = "big-parking-space.opq"

    # parse arguments
    opts, args = getopt.getopt(sys.argv[1:], "i:o", ["input =", "output ="])
    for k, v in opts:
        if k == "-i": input = v
        if k == "-o": output = v
   
    print("Args: input=%s ; output=%s" % (input,output), flush=True)

    if input == "":
        print_help()
        sys.exit(-1)

    if output == "":
        print_help()
        sys.exit(-1)

    print("Start reading osmfile...", flush=True)
    withFile = True
    start = time.time()
    ret = main(input, withFile, output)
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Program ended in {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds), flush=True)
    sys.exit(ret)
