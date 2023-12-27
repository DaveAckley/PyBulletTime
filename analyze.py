import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load("data/backleg.npy")
frontLegSensorValues = numpy.load("data/frontleg.npy")
matplotlib.pyplot.plot(backLegSensorValues,label="Back",linewidth=5)
matplotlib.pyplot.plot(frontLegSensorValues,label="Front",linewidth=2)
matplotlib.pyplot.legend()
matplotlib.pyplot.show()

