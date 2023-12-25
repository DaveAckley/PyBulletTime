#generate.py from Josh's course

import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")


length = 1
width = 1
height = 1

x = 0
y = 0
z = height/2

#pyrosim.Send_Cube(name="Box10", pos=[x,y,z] , size=[length,width,height])
#pyrosim.Send_Cube(name="Box11", pos=[x,y,z] , size=[length,width,height])
for x in range(4):
    for y in range(4):
        sz = [length,width,height]
        for h in range(10):
            pyrosim.Send_Cube(name="Box11", pos=[x,y,1.5*h] , size=sz)
            sz = [.9*sz[0],.9*sz[1],.9*sz[2]]
pyrosim.End()

