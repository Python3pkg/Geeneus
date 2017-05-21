import unittest
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from Bio import Entrez

from geeneus.backend import Networking

class TestNetworkingFunctions(unittest.TestCase):

    # Build manager object for all tests here
    def setUp(self):
        pass

    def test_internet_is_working_up(self):
        try:
            self.assertEquals(200, urllib.request.urlopen("http://www.google.com").getcode())
        except IOError:
            self.fail("Unable to connect to internet")

    def test_NCBI_is_up(self):
        try:
            self.assertEquals(200, urllib.request.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/").getcode())
        except IOError:
            self.fail("Unable to connect to the eutils base connection")

    def test_ENTREZ_efetch(self):
        Entrez.email = "alex.holehouse@gmail.com"  
        try:
            handle = Entrez.efetch(db="protein", id="NP_005566",  retmode="xml")
        except urllib.error.HTTPError:
            self.fail("ENTREZ efetch to the protein database doesn't seem to be work")
            return

