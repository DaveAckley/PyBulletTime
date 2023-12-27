import time
import pybullet as p
import pybullet_data
import numpy

import pyrosim.pyrosim as pyrosim

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

#TO SUPPRESS SIDEBARS: p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
steps = 500
backLegSensorValues = numpy.zeros(steps)
frontLegSensorValues = numpy.zeros(steps)
for i in range(steps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    time.sleep(1/60)
p.disconnect()
numpy.save("data/backleg.npy",backLegSensorValues)
numpy.save("data/frontleg.npy",frontLegSensorValues)
exit()

