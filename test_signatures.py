from signature import Signature
from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer

container = SignatureContainer()

s1 = Signature([1,3,6,7,4,2,3,4,6,1,2,4,5,6,7,7], 10)
s2 = Signature([3,4,6,1,2,4,5,6,7,7,1,3,6,7,4,2], 10)

container.save(s1, 0)
container.save(s2, 5)

s1 = container.read(0)
s2 = container.read(5)

print s1, s2

recognizer = SignatureRecognizer(container)
print recognizer.distance(s1, s2)
print recognizer.shift(s1, s2)


