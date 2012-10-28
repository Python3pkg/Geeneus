#!/bin/bash
cd ../ # move back into base directory

## Make sure we really want to rebuild the deployment directoyr
echo "Delete existing deployment\n(note yes will delete EVERYTHING, not just\nGenome.py"
rm -ri deployment/geeneus/Genome.py
sudo rm -rf deployment/

# build folders
mkdir deployment/
mkdir deployment/geeneus
mkdir deployment/geeneus/backend/
mkdir deployment/geeneus/test/

# /Geeneus files
cp geeneus/Genome.py deployment/geeneus/
cp geeneus/Proteome.py deployment/geeneus/
cp geeneus/__init__.py deployment/geeneus/
cp geeneus/backend/*.py deployment/geeneus/backend/
cp geeneus/test/*.py deployment/geeneus/test/

# induvidual files
cp LICENSE.txt deployment/
cp MANIFEST.in deployment/
cp README.rest deployment/README.txt
cp setup.py deployment/

echo "Deployment directory structure rebuilt from current version"
