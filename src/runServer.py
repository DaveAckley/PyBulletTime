import pybullet_data
import pybullet as p
import time

p.connect(p.GUI_SERVER)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

while (1):
  #this is a no-op command, to allow GUI updates on Mac OSX (main thread)
  p.setPhysicsEngineParameter()
  time.sleep(0.1)
  
