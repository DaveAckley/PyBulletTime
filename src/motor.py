import numpy
import random
import constants as c
from math import pi, sin, sqrt
import pyrosim.pyrosim as pyrosim

import pybullet as p

class MOTOR:
    def __init__(self, jointName, robot):
        self.robot = robot
        self.jointName = jointName
        #self.values = numpy.zeros(c.steps)
        self.Prepare_To_Act();
        self.currentVelocity = 0
        self.velocityAlpha = .75
    
    def Prepare_To_Act(self):
        ###DEBUG
        bodyID =  self.robot.robotId
        for jointIndex in range( 0 , p.getNumJoints(bodyID) ):
            jointInfo = p.getJointInfo( bodyID , jointIndex )
            print("GETJOINTIFNO",jointInfo)
            dyn = p.getDynamicsInfo( bodyID , jointIndex )
            print("GETDYNIFNO",dyn)
         ###DEBUG
        #exit(3)

        self.amplitude = c.backLegAmplitude
        self.amplitudeOffset = c.backLegAmplitudeOffset
        self.frequency = c.backLegFrequency
        self.frequencyOffset = c.backLegFrequencyOffset
        # XXX Torso_FrontLeg":
        print("YYYYPREACTMOT",self.jointName)
        #if self.jointName == "left_rear_wheel_joint" or self.jointName == "right_rear_wheel_joint" or self.jointName == "left_front_wheel_joint" or self.jointName == "right_front_wheel_joint":
        if self.jointName == "base_lwheel" or self.jointName == "base_rwheel":
            print("MTOASXCON",self.jointName)
            self.frequency = .01
            self.frequencyOffset = pi/4
            self.amplitude = -10
            if self.jointName == "base_lwheel":
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
        mrs = sim.worldrunner
        
        ctrl = False
        jterm = mrs.GetTermForJointIfAny(self.jointName)
        #print("MOTSVL",self.jointName, jterm)
        self.target = 0
        val = None
        modval = None
        if jterm:
            val = jterm.get('value')
            if val != None:
                modval = (val-0)/4 # back to linear now that friction is happier?
                #modval = sqrt(val)*4  # fog it go non-linear (but monotonic)
                # Let's not be like deterministic here
                self.target = max(0,modval+random.uniform(-.1, .1))  
                #print("MOTGV",self.jointName,val,modval,self.target)
                ctrl = True
            else:
                print("MOTGVNO VAL?",self.jointName)

        # if self.jointName == "base_lwheel":
        #     self.target = (sim.lastRightYellow-2)/1.5
        #     ctrl = True
        # elif self.jointName == "base_rwheel":
        #     self.target = (sim.lastLeftYellow-2)/1.5
        #     ctrl = True
        # else:
        #     self.target = self.amplitude*sin(step*self.frequency+
        #                                      self.frequencyOffset)+self.amplitudeOffset

        self.currentVelocity = (self.velocityAlpha*self.currentVelocity +
                                (1-self.velocityAlpha)*self.target)
        if ctrl:
            print("MOTSEV",self.jointName,val,modval,self.target,self.currentVelocity)

        self.robot.Save_Data_Item(str(self.currentVelocity),"motor",self.jointName)

        #self.values[step] = target
        pyrosim.Set_Motor_For_Joint_Velocity(
            bodyIndex = self.robot.robotId,
            jointName = self.jointName,
            controlMode = p.VELOCITY_CONTROL,
            targetVelocity = self.currentVelocity,
            maxForce = c.defaultForce)

