"""
Return a list of parking space that are too big
They should be converted as parking lot

Stats for planet-220818.osm.pbf
-Ways found: 36224
-Program ended in 01:18:40.64

Stats for planet-221010.osm.pbf
-Ways found: 33121
-Program ended in 01:11:30.79

Once python script id completed:
1. Open the OSM file in JOSM
2. In "File" menu, click "Update the data" to download all nodes and refresh data
3. Create a new layer
4. Select all data with Ctrl+A
5. Do "Merge selection" in the new layer (Ctrl+Maj+M). It allows us to ignore ways/nodes deleted on server
6. Ctrl+F in mode "select" with filter:
        type:way amenity=parking_space -aeroway -bicycle -bus -capacity -disabled -emergency -footway -hgv -hov
7. Ctrl+F in mode "remove" with filter (it will select all parking_space with area > 500m²):
        areasize:-500
8. Edit those object replace amenity value from parking_space to parking
9. Save in a new osm file
10. Use the following command (mr-cli):
        mr coop tag --out parking_space.geojson big-parking-space.osm
"""
import os
import osmium
import sys
import getopt
import time


class BigParkingSpaceHandler(osmium.SimpleHandler):

    def __init__(self, writer):
        super(BigParkingSpaceHandler, self).__init__()
        self.writer = writer  # osmium writer
        self.nbWay = 0  # counter ways
        self.firstWayRead = False

    # osmium way handler
    def way(self, w):
        if self.firstWayRead == False:
            print("First way read!")
            self.firstWayRead = True

        # search only for parking_space
        if w.tags.get('amenity') != 'parking_space':
            return

        # ignore parking_space with less than 5 nodes
        if w.nodes.__len__() <= 5:
            return

        # ignore aeroway
        if 'aeroway' in w.tags:
            return

        # ignore bicycle
        if 'bicycle' in w.tags:
            return

        # ignore bus
        if 'bus' in w.tags:
            return

        # ignore parking_space with capacity
        if 'capacity' in w.tags:
            return

        # ignore capacity:disabled
        if 'capacity:disabled' in w.tags:
            return

        # ignore parking_space with tag 'disabled'
        if 'disabled' in w.tags:
            return

        # ignore parking_space with tag 'disabled'
        if 'emergency' in w.tags:
            return

        # ignore disabled patking_space
        if w.tags.get('parking_space') == 'disabled':
            return

        if 'wheelchair' in w.tags:
            return

        # all filter passed, adding the parking_space to osm file
        self.nbWay += 1  # increment counter
        self.writer.add_way(w)
        sys.stdout.write("\rWays found: %i" % self.nbWay)
        sys.stdout.flush()


def print_help():
    print("Usage: python %s -i <osmfile> -o <output.osm>" % sys.argv[0])
    print("")
    print("Read the <osmfile> in input. Find the parking space that are too big.")
    print("Write an Overpass query in the <output.osm> that get osm elements (opq stands for Overpass Query")
    print("Use this query to create a MapRoulette challenge or in JOSM to create a QuickFix challenge with mr-cli util")
    print("")
    print("  -i <input osm file> such as planet.osm.pbf. All file supported by osmium should work")
    print("  -o <output filename.opq>. A file to write the Overpass query inside")
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
        handler = BigParkingSpaceHandler(writer)
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
    output = "big-parking-space.osm"

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
