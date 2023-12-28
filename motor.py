import numpy
import constants as c
from math import pi, sin
import pyrosim.pyrosim as pyrosim

import pybullet as p

class MOTOR:
    def __init__(self, jointName, robot):
        self.robot = robot
        self.jointName = jointName
        self.values = numpy.zeros(c.steps)
        self.Prepare_To_Act();
    
    def Prepare_To_Act(self):
        self.amplitude = c.backLegAmplitude
        self.amplitudeOffset = c.backLegAmplitudeOffset
        self.frequency = c.backLegFrequency
        if self.jointName == "Torso_FrontLeg":
            self.frequency = self.frequency*2
        self.frequencyOffset = c.backLegFrequencyOffset

    def Set_Value(self,step):
        target = self.amplitude*sin(step*self.frequency+
                                    self.frequencyOffset)+self.amplitudeOffset
        self.values[step] = target
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = self.robot.robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = target,
            maxForce = c.defaultForce)

