# Copyright 2012 by Alex Holehouse - see LICENSE for more info
# Contact at alex.holehouse@wustl.edu

""" This is test folder for running unit tests.
"""
import sys
import os
# Add the parent directory (which holds the geeneus package)
sys.path.insert(0,os.path.abspath(__file__+"/../../../"))

from . import Proteome_tests
from . import Genome_tests
from . import GeneObject_tests
from . import GeneParser_tests
from . import ProteinObject_tests
from . import ProteinParser_tests
from . import Networking_tests
from . import UniprotAPI_tests
from . import Isoform_algorithm_tests
