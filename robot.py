import numpy

import pybullet as p

import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self,simulation):
        self.simulation = simulation

    def Prepare_To_Simulate(self,urdf,scale=1):
        self.robotId = p.loadURDF(urdf,[0,0,1.0],globalScaling=scale)
        #self.robotId = p.loadURDF("sphere2red.urdf")
        #self.robotId = p.loadURDF("quadruped/spirit40newer.urdf")
        #self.robotId = p.loadURDF("bicycle/bike.urdf",[0,0,5],globalScaling=2)
        #self.robotId = p.loadURDF("quadruped/minitaur.urdf",[0,0,5],globalScaling=16)
        #self.robotId = p.loadURDF("racecar.urdf",[0,0,1.0],globalScaling=6)

        #self.robotId = p.loadURDF("differential/diff_ring.urdf")
        return self.robotId

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName,self)

    def Save_Data_Item(self,s,type):
        self.simulation.Save_Data(s,type)

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

            
