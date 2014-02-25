from signature import Signature
from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer

container = SignatureContainer()
container.delete_loc_files()

s0 = Signature([1,3,6,7,4,2,3,4,6,1,2,4,5,6,7,7], 10)
s1 = Signature([3,4,6,1,2,4,5,6,7,7,0,3,6,7,4,2], 10)
s2 = Signature([5,6,7,7,3,3,4,3,3,2,6,3,4,5,6,5], 10)
s3 = Signature([5,6,7,8,9,7,8,9,8,7,8,5,4,3,2,3], 10)

container.save(s0)
container.save(s1)
container.save(s2)
container.save(s3)

s4 = Signature([8,5,4,3,2,3,5,6,7,8,9,7,8,9,8,7], 10)  # permuted s3

recognizer = SignatureRecognizer(container)

# print recognizer.sigs()

i, d, closest = recognizer.closest(s4)
print i, d, closest
print recognizer.shift(closest, s4, exhaustive=False)