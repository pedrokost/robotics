from signature_recognizer import SignatureRecognizer
from signature_container import SignatureContainer
# from place_recognizer import PlaceRecognizer


container = SignatureContainer()
print container.read(7).sig
print container.read(2).sig
print container.read(1).sig
print container.read(4).sig
print container.read(5).sig
