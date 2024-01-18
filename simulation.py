import time

import subprocess

import numpy
from math import pi, sin

import pybullet as p
import pybullet_data

import pkgutil

import pyrosim.pyrosim as pyrosim

from PIL import Image

import constants as c
from world import WORLD
from robot import ROBOT

from datetime import datetime
from pathlib import Path

class SIMULATION:
    def __init__(self):
        self.step = 0

        self.Set_Up_Simulation_Directory()
        self.Set_Up_Spine_Communications()
        self.world = WORLD(self)
        self.robot = ROBOT(self)
        #self.physicsClient = p.connect(p.GUI)
        self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
        #TO SUPPRESS SIDEBARS:p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW,0)
        p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW,0)
        p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW,0)

        egl = pkgutil.get_loader('eglRenderer')
        if (egl):
            pluginId = p.loadPlugin(egl.get_filename(), "_eglRendererPlugin")
            print("egl loader")
        else:
            pluginId = p.loadPlugin("eglRendererPlugin")
            print("no egl loader")
        print("pluginId=",pluginId)

        #TO DEBUG LOG TO mp4: p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4,"sim.mp4")
        #p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4,"sim.mp4")

        p.setRealTimeSimulation(False)
        
        p.setGravity(0,0,-9.8)
        self.planeId = p.loadURDF("plane.urdf")
        #self.robotId = self.robot.Prepare_To_Simulate("car/racecar.urdf",10)
        self.robotId = self.robot.Prepare_To_Simulate("genRobot.urdf",3)
        p.loadSDF("world.sdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()
        print("SIMULATIO _INTIF_")

    def __del__(self):
        p.disconnect()

    def Set_Up_Simulation_Directory(self):
        now = datetime.now()
        self.simTag = "{:%Y%m%d-%H%M%S}".format(now)
        print("SIMULATION TAG",self.simTag)

        self.simPath = c.simulationBaseDir + "/" + self.simTag
        Path(self.simPath).mkdir(parents=True,exist_ok=False)

        self.imgPath = c.simulationBaseDir + "/" + self.simTag + "/" + "imgs"
        Path(self.imgPath).mkdir(parents=True,exist_ok=False)

        self.savedSimData = ""
        self.savedSensorData = ""
        self.savedMotorData = ""

    def Set_Up_Spine_Communications(self):
        self.spinePath = c.spineCommunicationsDir
        Path(self.spinePath).mkdir(parents=True,exist_ok=True)
        self.savedSimData = ""
        self.savedSensorData = ""
        self.savedMotorData = ""

    def Save_Data(self,data,type):
        if type == "sim":
            self.savedSimData += " " + data
        elif type == "sensor":
            self.savedSensorData += " " + data
        elif type == "motor":
            self.savedMotorData += " " + data
        else:
            raise Exception("Unknown Save_Data type "+type)

    def Flush_Data(self):
        fullRow = self.savedSimData + self.savedSensorData + self.savedMotorData + "\n"
        with open(self.simPath + "/" + "data.dat","a") as f:
            f.write(fullRow)
        noMotorRow = self.savedSimData + self.savedSensorData + "\n"
        with open(self.spinePath + "/" + "sensors.dat","w") as f:
            f.write(noMotorRow)
        self.savedSimData = ""
        self.savedSensorData = ""
        self.savedMotorData = ""

    def Generate_Video(self):
        cmd = 'ffmpeg -f image2 -r 60 -i step%08d.png -vcodec libx264 -vf pad=1920:1080:(ow-iw)/2:(oh-ih)/2:0x0f0f0f -r 60 -pix_fmt yuv420p'
        cmd += " ../../merges/" + self.simTag + ".mp4"
        args = cmd.split()
        imgDir = self.simPath + "/" + "imgs"
        print("CWD:",imgDir,args)
        subprocess.run(args,cwd=imgDir)

    def Step(self):
        w=1920
        h=1080
        
        camTargetPos = [0, 0, 0]
        cameraUp = [0, 0, 1]
        cameraPos = [-3, 3, 3]
        camDistance = 4

        pitch = -40.0
        yaw = 50 #?

        roll = 0
        upAxisIndex = 2
        pixelWidth = w
        pixelHeight = h
        nearPlane = 0.01
        farPlane = 100

        fov = 100

        self.step += 1
        i = self.step
        self.Save_Data(str(i),"sim")
        p.stepSimulation()

        viewMatrix = p.computeViewMatrixFromYawPitchRoll(camTargetPos, camDistance, yaw, pitch,
                                                         roll, upAxisIndex)
        aspect = pixelWidth / pixelHeight
        projectionMatrix = p.computeProjectionMatrixFOV(fov, aspect, nearPlane, farPlane)
        img = p.getCameraImage(1*pixelWidth,
                               1*pixelHeight,
                               viewMatrix,
                               projectionMatrix,
                               shadow=1,
                               lightDirection=[0, 0, 1],
                               renderer=p.ER_BULLET_HARDWARE_OPENGL)
        #img = p.getCameraImage(w,h, renderer=p.ER_BULLET_HARDWARE_OPENGL)
        rgbim = Image.fromarray(img[2])
        rgbim.save(self.imgPath+"/step{:08}.png".format(i)) #FIX FOR LEX
        self.robot.Sense(i)
        self.robot.Act(i)
        self.Flush_Data()
        #time.sleep(c.wallSecsPerStep)


    def Run(self):

        for i in range(c.steps):
            self.Step()
