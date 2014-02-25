from histogram import Histogram
from histogram_recognizer import HistogramRecognizer

h1 = Histogram([1,3,6,7,4,2,3,4,6,1,2,4,5,6,7,7], 10)
h2 = Histogram([3,4,6,1,2,4,5,6,7,7,1,3,6,7,4,2], 10)

recognizer = HistogramRecognizer()
# print recognizer.distance(h1.hist, h2.hist)
print recognizer.shift(h1.values, h2.values)