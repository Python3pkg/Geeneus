#!/bin/bash
 ./build_deployment.sh

cd ../deployment/
python setup.py sdist
cd dist/
unpack Geeneus-0.1.5.tar.gz
cd Geeneus-0.1.5/
sudo python setup.py install
