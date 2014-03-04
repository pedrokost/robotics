from signature import Signature
from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer
from utilities import *
import numpy as np

orig_vector = [21, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 20, 21, 21, 23, 23, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 57, 57, 56, 55, 55, 55, 55, 55, 54, 54, 54, 54, 54, 54, 54, 54, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 54, 54, 54, 54, 54, 54, 55, 54, 55, 55, 55, 55, 56, 56, 56, 57, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 91, 91, 91, 91, 91, 92, 92, 92, 92, 92, 91, 92, 91, 92, 91, 91, 73, 72, 71, 71, 71, 71, 70, 70, 70, 70, 70, 70, 70, 70, 70, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 70, 70, 69, 69, 70, 69, 70, 70, 70, 70, 70, 70, 70, 71, 71, 71, 71, 71, 72, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 27, 25, 158, 157, 25, 26, 157, 29, 27, 157, 30, 26, 24, 27, 28, 157, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 252, 139, 139, 138, 21]


shifted_vector = np.roll(orig_vector, 56)
nBins = 50
orig = Signature(orig_vector, nBins)
shifted = Signature(shifted_vector, nBins)

container = SignatureContainer()
container.delete_loc_files()
container.save(orig)
container.save(shifted)
recognizer = SignatureRecognizer(container)

# Ehaustive returns 6, fast returns 3 which is wrong
# shift_exhaustive = recognizer.theta(orig, shifted, exhaustive=True, debug=True)
# shift_fast =  recognizer.theta(orig, shifted, exhaustive=False, debug=True)
# print "exhaustive", shift_exhaustive
# print "fast", shift_fast
# print recognizer.theta(closest, s4, exhaustive=exhaustive, debug=False)

for x in range(100):
	# recognizer.shift(orig, shifted, exhaustive=True, debug=True)
	recognizer.shift(orig, shifted, exhaustive=False, debug=True)

