import constants as c
import numpy

import pyrosim.pyrosim as pyrosim

class SENSOR:
    def __init__(self,linkName,robot):
        self.linkName = linkName
        self.robot = robot
        self.Prepare_To_Sense()

    def Prepare_To_Sense(self):
        pass # self.values = numpy.zeros(c.steps)

    def Get_Value(self,step):
        self.value = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        self.robot.Save_Data_Item(str(self.value),"sensor")
        #self.values[step] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        #if step == c.steps-1:
        #   print("AZLK",self.values[step])

        
    
