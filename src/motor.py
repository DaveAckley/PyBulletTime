import numpy
import random
import constants as c
from math import pi, sin
import pyrosim.pyrosim as pyrosim

import pybullet as p

class MOTOR:
    def __init__(self, jointName, robot):
        self.robot = robot
        self.jointName = jointName
        #self.values = numpy.zeros(c.steps)
        self.Prepare_To_Act();
    
    def Prepare_To_Act(self):
        self.amplitude = c.backLegAmplitude
        self.amplitudeOffset = c.backLegAmplitudeOffset
        self.frequency = c.backLegFrequency
        self.frequencyOffset = c.backLegFrequencyOffset
        # XXX Torso_FrontLeg":
        print("YYYYPREACTMOT",self.jointName)
        #if self.jointName == "left_rear_wheel_joint" or self.jointName == "right_rear_wheel_joint" or self.jointName == "left_front_wheel_joint" or self.jointName == "right_front_wheel_joint":
        if self.jointName == "base_to_lwheel" or self.jointName == "base_to_rwheel":
            print("MTOASXCON",self.jointName)
            self.frequency = .01
            self.frequencyOffset = pi/4
            self.amplitude = -10
            if self.jointName == "base_to_lwheel":
                self.amplitude = -12
                self.frequency = .011
                self.frequencyOffset += .2
            self.amplitudeOffset = -4
        elif self.jointName == "right_steering_hinge_joint" or self.jointName == "left_steering_hinge_joint":
            print("STEER",self.jointName)
            self.frequency = .01
            self.frequencyOffset = pi/4
            self.amplitude = 1
	    #if self.jointName == "right_steering_hinge_joint":
            #  self.amplitude = -4
            self.amplitudeOffset = 0

    def Set_Value(self,step):
        robot = self.robot
        sim = robot.simulation
        
        ctrl = False
        if self.jointName == "base_to_lwheel":
            self.target = (sim.lastRightYellow-2)/1.5
            ctrl = True
        elif self.jointName == "base_to_rwheel":
            self.target = (sim.lastLeftYellow-2)/1.5
            ctrl = True
        else:
            self.target = self.amplitude*sin(step*self.frequency+
                                             self.frequencyOffset)+self.amplitudeOffset
        self.target += random.uniform(-.5, .5)  # Let's not be like deterministic here

        if ctrl:
            print("MOTSEV",self.jointName,self.target)

        self.robot.Save_Data_Item(str(self.target),"motor")
        #self.values[step] = target
        pyrosim.Set_Motor_For_Joint_Velocity(
            bodyIndex = self.robot.robotId,
            jointName = self.jointName,
            controlMode = p.VELOCITY_CONTROL,
            targetVelocity = self.target,
            maxForce = c.defaultForce)

