import time
import pybullet as p
import pybullet_data
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

#TO SUPPRESS SIDEBARS: p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
p.loadSDF("box.sdf")
for i in range(1000):
    p.stepSimulation()
    time.sleep(1/60)
p.disconnect()

