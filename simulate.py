import time
import pybullet as p
physicsClient = p.connect(p.GUI)
#TO SUPPRESS SIDEBARS: p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
for i in range(1000):
    p.stepSimulation()
    time.sleep(1/60)
p.disconnect()

