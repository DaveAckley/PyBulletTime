# import random
# import time
# import pybullet as p
# import pybullet_data
# import numpy
# from math import pi, sin

# import constants as c
# import pyrosim.pyrosim as pyrosim



# numpy.save("data/backleg.npy",backLegSensorValues)
# numpy.save("data/frontleg.npy",frontLegSensorValues)
# exit()

from simulation import SIMULATION
simulation = SIMULATION()
simulation.Run()
