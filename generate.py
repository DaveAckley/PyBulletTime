#generate.py from Josh's course

import pyrosim.pyrosim as pyrosim

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    length = 1
    width = 1
    height = 1
    x = 0
    y = 5
    z = height/2

    pyrosim.Send_Cube(name="Box10", pos=[x,y,z] , size=[length,width,height])
    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    length = 1
    width = 1
    height = 1
    x = 0
    y = 0
    z = height/2

    pyrosim.Send_Cube(name="Torso", pos=[x,y,z+1] , size=[length,width,height])

    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" ,
                        type = "revolute", position = [.5,0,1]) 
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5] , size=[length,width,height])

    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" ,
                        type = "revolute", position = [-.5,0,1]) 
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5,0,-.5] , size=[length,width,height])
    
    pyrosim.End()
    


Create_World()
Create_Robot()
