# maproulette-challenges-workflows
MapRoulette challenges with Osmium updated monthly with GitHub workflows.

## Description

This repository contains scripts that are runned monthly by GitHub workflows.
These script download the latest OSM data of Europe in "osm.pbf" format.
Then it performs filtering operations to create geojson files.
These files contains tasks that should be fixed in MapRoulette.

## Challenge list

1. [Is this museum free of charge? - Europe](https://maproulette.org/browse/challenges/53974)
2. [Museum without website - Europe](https://maproulette.org/browse/challenges/53990)
3. [Fix discouraged oneway values - Europe](https://maproulette.org/browse/challenges/53991)
4. [Places of worship without religion - Europe](https://maproulette.org/browse/challenges/53992)

## Run in local

### Prerequisites 

1. Use Debian/Ubuntu or WSL
2. Install python: `sudo apt install python3 python3-venv python-is-python3`
3. Install osmium and aria2: `sudo apt install osmium-tool aria2`
4. Create python venv: `pip install -r requirements.txt`
5. Activate python venv: `source venv/bin/activate`
6. Install python libs: `pip install -r requirements.txt`
