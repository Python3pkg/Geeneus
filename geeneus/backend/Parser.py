# Base class which deals with caching and storing of data objects, as well as coordinating network access (private)
#
# Copyright 2012 by Alex Holehouse - see LICENSE for more info
# Contact at alex.holehouse@wustl.edu

from Bio import Entrez
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

import Networking

class GeneralRequestParser:
    
    def __init__(self, email, cache, retry=0, loud=True):
        try:
            Entrez.email = email
            self.Networking = Networking.Networking(30)
            self.loud = loud
            self.retry = retry
            self.cache = cache
            self.error_status = False
        except: 
            print "Error building generic parser object"
            self.error_status = True
    

            ###
    def error(self):
        return self.error_status

    # Preconditions
    # ID must be a valid ID, so probably want to run through a preprocessing function before you
    # call this
    # 
    def _get_object(self, ID, datastore, fetchFunction, newObjectConstructor):
        if ID not in datastore or not self.cache:  
           
            if ID  == -1:

                self.printWarning("\nWarning - The ID {ID} is an invalid accession number, and the database will not be queried".format(ID=ID))
                # by returning the object associated with [] we don't pollute the datastore with invalid and pointless
                # searches, we avoid queriying NCBI without a hope in hell of a hit, and we take advantage of the built in
                # bad XML behaviour without raising an error, because, technically, no error has happened, we just know
                # that the ID in question won't return valid XML. It's not an error - it's just stupid.
                
                return newObjectConstructor([])
                       
            xml = -1
            retry = self._build_retry_function(fetchFunction);
                     
            while (xml == -1):
                xml = retry(ID);
                        
            # if we still can't get through after retrying a number of times
            if (xml == -2):
                print "Unable to find accession value at NCBI end"
                datastore[ID] = newObjectConstructor(-1)
               
            else:
                datastore[ID] = newObjectConstructor(xml)
                
        return datastore[ID]

    
#--------------------------------------------------------
# PRIVATE FUNCTION
#-------------------------------------------------------
# This function provides an interface with the Networking
# functionality to return a list of XML elements, each of
# which corresponds to the ID in the listofIDs
#
#
    def _get_batch_XML(self, listOfIDs, function_to_apply):
        
        # base case 1 (base case 2 if len == 1)
        if len(listOfIDs) == 0:
            return []

        xml = -1
        retry = self._build_retry_function(function_to_apply);

        while (xml == -1):
            xml = retry(listOfIDs)

        # If we fail implement recursive batch fetch, such that we split the list in half
        # and batch fetch each half. Do this after troubleshooting!
        if xml == -2 or not len(xml) == len(listOfIDs):
            if len(listOfIDs) == 1:
                return [-1]
            
            # split list in half and recursivly batch both halves
            # this serves two purposes - it lets us retry a number of times proportional
            # to the length of the list, and it provides a binary search mechanism to 
            # root out a potential rotten apple which may be causing the list to error

            xml = self._get_batch_XML(listOfIDs[:int(len(listOfIDs)/2)])
            xml_2 = self._get_batch_XML(listOfIDs[int(len(listOfIDs)/2):])

            xml.extend(xml_2)
            
        return xml


#--------------------------------------------------------
# PRIVATE FUNCTION
#--------------------------------------------------------          
# Builds a closure based retry function, which when called
# the first self.retry times will atempt to get the parsed
# xml for the ID in question. However, on the
# self.retry+1 time it will simply return -2 
#
    def _build_retry_function(self, function_to_apply):

        retryCounter = [0]
        numberOfRetries = self.retry

        def retry(ID):

            if retryCounter[0] < numberOfRetries+1:
                
                retryCounter[0] = retryCounter[0]+1
                
                ## if we're not on our first try
                if not retryCounter[0]-1 == 0:
                    print("Retry number " + str(retryCounter[0]) + " of " + str(numberOfRetries+1))
                
                ## return value may be a real handle or -1
                handle = function_to_apply(ID)
                
                ## if we failed return -1
                if handle == -1:
                    return -1
                
                try:
                    XML = Entrez.read(handle)

                # what are these errors?
                # httplib.IncompleteRead - we accidentally closed the session early, either because of a timeout on the client end (i.e. here) or because 
                #                          of some kind of server error
                # 
                # Bio.Entrez.Parser.CorruptedXMLError - Something is wrong with the XML 
                # Bio.Entrez.Parser.NotXMLError - the XML is not XML (unlikely, but worth keeping!)
                # Bio.Entrez.Parser.ValidationError - unable to validate the XML (this can be ignored, but best not to!)
                except (httplib.IncompleteRead, Bio.Entrez.Parser.CorruptedXMLError, Bio.Entrez.Parser.NotXMLError, Bio.Entrez.Parser.ValidationError), err:  
                    return -1

                return XML

            else:
                return -2;

        return retry