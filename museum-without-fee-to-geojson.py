"""
This script store museum without fee in a osm file.

1. Run the script
2. Open the osm file with JOSM
3. Update data
4. Ctrl+F with filter tourism=museum -fee
5. Create a new layer
6. Merge selection to new layer(Ctrl+Shift+M)
7. save the new layer as geojson

Stats for planet-220818.osm.pbf
-Ways found: 36224
-Program ended in 01:18:40.64

"""
import os
import osmium
import sys
import getopt
import time


class MuseumWithoutFee(osmium.SimpleHandler):

    def __init__(self, writer):
        super(MuseumWithoutFee, self).__init__()
        self.writer = writer  # osmium writer
        self.nbWay = 0  # counter ways
        self.nbNode = 0  # counter nodes

    def isConcerned(self, obj):
        return obj.tags.get('tourism') == 'museum' and 'fee' not in obj.tags

    # osmium way handler
    def node(self, n):

        if not self.isConcerned(n):
            return

        # all filter passed, adding the parking_space to osm file
        self.nbNode += 1  # increment counter
        self.writer.add_node(n)
        sys.stdout.write("\rNodes found: %i - Ways found: %i" %
                         (self.nbNode, self.nbWay))
        sys.stdout.flush()

    # osmium way handler
    def way(self, w):

        if not self.isConcerned(w):
            return

        # all filter passed, adding the parking_space to osm file
        self.nbWay += 1  # increment counter
        self.writer.add_way(w)
        sys.stdout.write("\rNodes found: %i - Ways found: %i" %
                         (self.nbNode, self.nbWay))
        sys.stdout.flush()


def print_help():
    print("Usage: python %s -i <osmfile> -o <output.geojson>" % sys.argv[0])
    print("")
    print("Read the <osmfile> in input. Write a geojson file of found objects.")
    print("Use this geojson to create a MapRoulette challenge.")
    print("")
    print("  -i <input osm file> such as planet.osm.pbf. All file supported by osmium should work")
    print("  -o <output filename.geojson>. A file containing found objects")
    print("", flush=True)
    exit()


def main(input, output):
    try:
        start = time.time()
        if os.path.exists(output):
            print("Delete file %s" % output)
            os.remove(output)
        print("Initialize writer", flush=True)
        writer = osmium.SimpleWriter(output)
        print("Initialize handler", flush=True)
        handler = MuseumWithoutFee(writer)
        print("Start handler...", flush=True)
        handler.apply_file(input, locations=False)
        writer.close()
        del handler
        del writer
        print()
        end = time.time()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("Program ended in {:0>2}:{:0>2}:{:05.2f}".format(
            int(hours), int(minutes), seconds), flush=True)
    except Exception as e:
        print("%s" % e)


if __name__ == '__main__':
    nbArgs = len(sys.argv)
    if nbArgs != 3 and nbArgs != 5:
        print_help()

    # default arguments values
    input = ""
    output = "out/museum.osm"

    # parse arguments
    opts, args = getopt.getopt(sys.argv[1:], "i:o", ["input =", "output ="])
    for k, v in opts:
        if k == "-i":
            input = v
        if k == "-o":
            output = v

    print("Args: input=%s ; output=%s" % (input, output), flush=True)

    if input == "":
        print_help()

    if output == "":
        print_help()

    main(input, output)
    exit()
