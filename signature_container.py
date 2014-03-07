from signature import Signature
import os, glob, re
from constants import NUMBER_OF_SIGNATURE_BINS

# --------------------- File management class ---------------
class SignatureContainer():
    """
    A container that handles storing/reading signatures
    """
    def __init__(self, size = 100):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = self.createFilenames(size);

    def createFilenames(self, size):
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number.
        filenames = []
        for i in range(size):
            filenames.append('loc_{0:02d}.dat'.format(i))
        return filenames

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;
 
    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        # print "STATUS:  All signature files removed."
        for n in range(self.size):
            self.remove_loc_file(self.filenames[n])
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])

    def remove_loc_file(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)
            return True
        return False
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index=-1):
    	if index < 0:
    		index = self.get_free_index()

        if index > self.size - 1:
            print "FAIL:  You exceeded the maximum size of the signature container"
            return False

        filename = self.filenames[index]
        self.remove_loc_file(filename)
            
        f = open(filename, 'w')
        # f.write(str(len(signature.sig)) + "\n")  # nBins

        f.write(str(signature.name) + "\n")  # name
        for i in range(len(signature.values)):
            s = str(signature.values[i]) + "\n"
            f.write(s)

        f.close();

    def readAll(self):
    	"""
		Returns a list of all existing stored signatures.
		Assumes indexes are written consecutively.
    	"""

        filenames = glob.glob('loc_*.dat')
        indices = [int(re.search("loc_(\d+).dat", f).group(1)) for f in filenames]
        print "Existing Signatures for places", indices
    	sigs = []
    	for x in indices:
    		sigs.append( self.read(x) )
    	return sigs


    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
    	if index > self.size - 1:
            print "FAIL:  You exceeded the maximum size of the signature container"
            return None

        s = None
        filename = self.filenames[index]

        if os.path.isfile(filename):
            f = open(filename, 'r')
            name = str(f.readline()).rstrip()
            data = f.readlines()
            values = [int(v) for v in data]
            s = Signature(values, NUMBER_OF_SIGNATURE_BINS, name)
            f.close();
        else:
            print "WARNING: Signature does not exist."
        
        return s
        