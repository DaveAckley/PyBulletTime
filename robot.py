import numpy

import pybullet as p

import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        self.motors = {}

    def Prepare_To_Simulate(self,urdf):
        self.robotId = p.loadURDF(urdf)
        return self.robotId

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self,step):
        for name,sense in self.sensors.items():
            sense.Get_Value(step)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName,self)

    def Act(self,step):
        for motorName,motor in self.motors.items():
            motor.Set_Value(step)

            
