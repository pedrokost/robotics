from signature import Signature
from signature_recognizer import SignatureRecognizer

s1 = Signature([1,3,6,7,4,2,3,4,6,1,2,4,5,6,7,7], 10)
s2 = Signature([3,4,6,1,2,4,5,6,7,7,1,3,6,7,4,2], 10)

recognizer = SignatureRecognizer()
print recognizer.distance(s1, s2)
print recognizer.shift(s1, s2)