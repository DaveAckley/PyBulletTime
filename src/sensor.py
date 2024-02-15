import constants as c
import numpy

import pyrosim.pyrosim as pyrosim
import pybullet as p

class SENSOR:
    def __init__(self,linkName,robot):
        self.linkName = linkName
        print("YYYYSENS",linkName)
        self.robot = robot
        self.Prepare_To_Sense()

    def Prepare_To_Sense(self):
        pass # self.values = numpy.zeros(c.steps)

    def Get_Value(self,step):
        #self.value = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        self.value = pyrosim.Get_Touch_Normal_Force_For_Link(self.linkName)
        print("SENSGTVL",self.linkName,self.value)
        if self.value == None:
            self.value = 0
        self.robot.Save_Data_Item(str(self.value),"sensor",self.linkName)
        #self.values[step] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        #if step == c.steps-1:
        #   

        
    
