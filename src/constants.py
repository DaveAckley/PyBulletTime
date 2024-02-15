from math import pi, sin

simulationBaseDir = "/data/ackley/PART4/code/D/PyBulletTime/data"
spineCommunicationsDir = "/data/ackley/PART4/code/D/PyBulletTime/spine"

steps = 0

#wallSecsPerStep = 1/60

backLegFrequency = .01
backLegFrequencyOffset = -4
backLegAmplitude = -pi/2
backLegAmplitudeOffset = +pi/4

backLegFrequency = .0
backLegFrequencyOffset = -4
backLegAmplitude = 0
backLegAmplitudeOffset = 0

frontLegFrequency = .01
frontLegFrequencyOffset = 1
frontLegAmplitude = .8*pi/2
frontLegAmplitudeOffset = -pi/4

defaultForce = 80   # Really max force?
