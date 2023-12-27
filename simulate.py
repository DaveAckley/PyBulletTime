import random
import time
import pybullet as p
import pybullet_data
import numpy
from math import pi, sin

import pyrosim.pyrosim as pyrosim

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

#TO SUPPRESS SIDEBARS: p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
steps = 10000
backLegSensorValues = numpy.zeros(steps)
frontLegSensorValues = numpy.zeros(steps)

backLegPeriod = .01
backLegPeriodOffset = -4
backLegAmplitude = -pi/2
backLegAmplitudeOffset = +pi/4

frontLegPeriod = .01
frontLegPeriodOffset = 1
frontLegAmplitude = .8*pi/2
frontLegAmplitudeOffset = -pi/4

for i in range(steps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    defaultForce = 50
    backTarget = backLegAmplitude*sin(i*backLegPeriod+backLegPeriodOffset)+backLegAmplitudeOffset
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = backTarget,
        maxForce = defaultForce)
    frontTarget = frontLegAmplitude*sin(i*frontLegPeriod+frontLegPeriodOffset)+frontLegAmplitudeOffset
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontTarget,
        maxForce = defaultForce)
    time.sleep(1/240)
p.disconnect()
numpy.save("data/backleg.npy",backLegSensorValues)
numpy.save("data/frontleg.npy",frontLegSensorValues)
exit()

