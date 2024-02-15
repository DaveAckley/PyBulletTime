import time
import datetime
import random

import subprocess

import numpy
from math import pi, sin, cos

import pybullet as p
import pybullet_data

import pkgutil

import pyrosim.pyrosim as pyrosim

from PIL import Image, ImageDraw, ImageFont

import constants as c
from world import WORLD
from robot import ROBOT

from datetime import datetime
from pathlib import Path

class SIMULATION:
    def __init__(self,wr):
        self.worldrunner = wr

        self.selfie = False   # set up to take a Beevee selfie
        self.step = 0

        self.Set_Up_Simulation_Directory()
        self.Set_Up_Spine_Communications()
        self.world = WORLD(self)
        self.robot = ROBOT(self)

        #self.physicsClient = p.connect(p.GUI)
        #self.physicsClient = p.connect(p.DIRECT)
        conid = p.connect(p.SHARED_MEMORY)  # ?? manyspheres does this
        print(conid)
        assert(conid >= 0)
            
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # stuff cargo-culted from manyspheres.py
        p.setInternalSimFlags(0)    
        p.resetSimulation()
        p.setPhysicsEngineParameter(numSolverIterations=10) 
        p.setPhysicsEngineParameter(contactBreakingThreshold=0.001) 
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 0)

        #self.lastLeftYellow = 0
        #self.lastRightYellow = 0

        self.imgFont = ImageFont.truetype('fonts/Inconsolata-Regular.ttf',32)

        #TO SUPPRESS SIDEBARS:p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,1,rgbBackground=[0,0,0])   # let's have blackness beyond the world
        p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW,1)
        p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW,1)
        p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW,1)

        egl = pkgutil.get_loader('eglRenderer')
        if False: # XXX WAS: (egl):
            pluginId = p.loadPlugin(egl.get_filename(), "_eglRendererPlugin")
            print("egl loader")
        else:
            pluginId = p.loadPlugin("eglRendererPlugin")
            print("no egl loader")
        print("pluginId=",pluginId)

        #TO DEBUG LOG TO mp4: p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4,"sim.mp4")
        #p.startStateLogging(p.STATE_LOGGING_VIDEO_MP4,"sim.mp4")

        p.setRealTimeSimulation(False)
        
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)
        p.setGravity(0,0,-9.8)
        self.planeId = p.loadURDF("plane11.urdf", useMaximalCoordinates=True)     # use.. from manyspheres.py
        #self.robotId = self.robot.Prepare_To_Simulate("car/racecar.urdf",10)
        self.robotId = self.robot.Prepare_To_Simulate("genRobot.urdf",3,self.selfie)
        print("CARID",self.robotId)

        sphereScale = 1
        for c in range(0 if self.selfie else 5):
            dist = random.uniform(.5,6)
            angle = random.uniform(0,1.5*pi)
            x = cos(angle)*dist
            y = sin(angle)*dist
            urdfob = p.loadURDF("sphere2yellow.urdf",[0,0,1],globalScaling=sphereScale, useMaximalCoordinates=True)
            sphereMarkId = p.loadTexture("sphere10-texture11.png")
            #(rid, linkIndex, vgt, dims, mesh, lvfpos, lvforn, rgb) = p.getVisualShapeData(sphereMarkId)
            list = p.getVisualShapeData(urdfob)
            assert(len(list)==1)
            (rid, linkIndex, vgt, dims, mesh, lvfpos, lvforn, rgb) = list[0]
            print("ZONG ",rid, linkIndex, vgt, dims, mesh, lvfpos, lvforn, rgb)
            p.resetVisualShapeData(urdfob,-1,0,sphereMarkId)
            print("BOOND", p.getVisualShapeData(urdfob))
            #exit(9)

            #sdfob = p.loadSDF("world.sdf")
            rot = random.uniform(0,pi)
            quant = p.getQuaternionFromEuler([0,0,rot])

            #p.resetBasePositionAndOrientation(sdfob[0], [x,y,random.uniform(1.3,1.7)], quant)
            #p.resetBasePositionAndOrientation(sdfob[0], [x,y,random.randint(0,1)/2+.5], quant)
            p.resetBasePositionAndOrientation(urdfob, [x,y,random.randint(0,1)/2+2], quant)
            # p.changeDynamics(urdfob,-1,
            #                  lateralFriction=.1,
            #                  spinningFriction=.1,
            #                  rollingFriction=.1,
            #                  restitution=.9)

        #sdfob2 = p.loadSDF("world2.sdf")
        #p.resetBasePositionAndOrientation(sdfob2[0], [-1.8,3,1], [0,0,0,1])

        print("NUMJOINTORG",p.getNumJoints(self.robotId)) # useMaximalCoordinates=True breaks this??
        pyrosim.Prepare_To_Simulate(self.robotId)
        print("SIMINNT10")
        self.robot.Prepare_To_Sense()
        print("SIMINNT11")
        self.robot.Prepare_To_Act()
        print("SIMULATIO _INTIF_")

    def __del__(self):
        p.disconnect()

    def EnsureSimSubdir(self,subdir,makeit=True):
        assert(self.simPath)
        path = self.simPath + "/" + subdir
        Path(path).mkdir(parents=True,exist_ok= not makeit)
        #print("ESSDI",path)
        return path

    def Set_Up_Simulation_Directory(self):
        now = datetime.now()
        self.simTag = "{:%Y%m%d-%H%M%S}".format(now)
        print("SIMULATION TAG",self.simTag)

        self.simPath = c.simulationBaseDir + "/" + self.simTag
        Path(self.simPath).mkdir(parents=True,exist_ok=False)

        self.imgPath = self.EnsureSimSubdir("imgs")
        self.EnsureSimSubdir("imgs/view")

        self.savedSimData = ""
        self.savedSensorData = ""
        self.savedMotorData = ""

        self.simNames = []
        self.sensorNames = []
        self.motorNames = []

        self.namesFlushed = False

    def Set_Up_Spine_Communications(self):
        self.spinePath = c.spineCommunicationsDir
        Path(self.spinePath).mkdir(parents=True,exist_ok=True)
        self.savedSimData = ""
        self.savedSensorData = ""
        self.savedMotorData = ""

    def Save_Packet_Data(self,bytesout,pktsin,bytesin):
        self.Save_Data(str(bytesout),"sim","bytesout")
        self.Save_Data(str(pktsin),"sim","pktsin")
        self.Save_Data(str(bytesin),"sim","bytesin")

    def Save_Data(self,data,type,name):
        if type == "sim":
            self.savedSimData += " " + data
            if name not in self.simNames:
                self.simNames.append(name)
        elif type == "sensor":
            self.savedSensorData += " " + data
            if name not in self.sensorNames:
                self.sensorNames.append(name)
        elif type == "motor":
            self.savedMotorData += " " + data
            if name not in self.motorNames:
                self.motorNames.append(name)
        else:
            raise Exception("Unknown Save_Data type "+type+" "+name)

    def Flush_Data(self):
        fullRow = self.savedSimData + self.savedSensorData + self.savedMotorData + "\n"
        with open(self.simPath + "/" + "data.dat","a") as f:
            if not self.namesFlushed:
                titles = "# "+ str(self.simNames) + " " + str(self.sensorNames) + " " + str(self.motorNames) + "\n"
                f.write(titles)
                self.namesFlushed = True
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

    def radToDDeg(self,rads):
        degrad = 57.29577951
        deg = rads*degrad
        if deg<0:
            deg += 360
        assert(deg >= 0 and deg <= 360)
        dbldeg = int(deg/2)
        return dbldeg  # 0..180

    def ComputeCarView(self,sensortag,angle,count=255):
        wr = self.worldrunner

        distance = 100000
        img_w, img_h = 128, 128
        numb = p.getNumBodies()
        #print("COMCARV",numb)
        agent_pos, agent_orn =\
            p.getBasePositionAndOrientation(self.robotId)
        euler = p.getEulerFromQuaternion(agent_orn)
        (bodyroll,bodypitch,bodyyaw) = euler

        if angle == 'omni':
            (ddegroll,ddegpitch,ddegyaw) = (
                self.radToDDeg(bodyroll),self.radToDDeg(bodypitch),self.radToDDeg(bodyyaw))
            print("BODROLPIT--->  ",ddegroll,ddegpitch)
            wr.SetTermValue('BVPITCH',ddegpitch)
            wr.SetTermValue('BVROLL',ddegroll)

        #print("CMBO10",agent_pos,agent_orn,euler,bodyyaw)
        xA, yA, zA = agent_pos
        zA = zA + 0.35 # make the camera a little higher than the robot

        if angle == 'omni':
            distfoc = 1
            xB = xA + .0
            yB = yA + .0
            zB = zA + distfoc
            fov = 179
            view_matrix = p.computeViewMatrixFromYawPitchRoll(
                cameraTargetPosition=[xB, yB, zB],
                distance=distfoc,
                yaw=90, pitch=90, roll=0,
                upAxisIndex=2
            )

        else:
            camerayaw = bodyyaw+angle
            #print("CMBO11",camerayaw)

            # compute focusing point of the camera
            xB = xA + cos(camerayaw) * distance
            yB = yA + sin(camerayaw) * distance
            zB = zA # + 0.4 # and look a bit upwards?
            fov = 60

            view_matrix = p.computeViewMatrix(
                cameraEyePosition=[xA, yA, zA],
                cameraTargetPosition=[xB, yB, zB],
                cameraUpVector=[0, 0, 1.0]
            )

        projection_matrix = p.computeProjectionMatrixFOV(
            fov=fov, aspect=1.0, nearVal=0.01, farVal=100.0)

        imgs = p.getCameraImage(img_w, img_h,
                                view_matrix,
                                projection_matrix, shadow=False,
                                renderer=p.ER_TINY_RENDERER)
#                                renderer=p.ER_BULLET_HARDWARE_OPENGL)
        rgbim = Image.fromarray(imgs[2])
        yellowpix = 0
        ylw = (200,200,0)
        #ylwthreshold = 2000
        ylwthreshold = 25000
        avgdist = 0
        samples = 0
        for i in range(count):
            x = random.randrange(img_w)
            y = random.randrange(img_h)
            pix = rgbim.getpixel((x,y))
            (dx,dy,dz) = (pix[0]-ylw[0],pix[1]-ylw[1],pix[2]-ylw[2])
            sqdist = dx*dx+dy*dy+dz*dz
            # if random.uniform(0,sqdist) < ylwthreshold:
            #     yellowpix += 1
            if sqdist < ylwthreshold and yellowpix < 255:
                yellowpix += 1
            samples += 1
            avgdist += sqdist
        avgdist /= samples
        print("YLWMINPIX  ",sensortag,yellowpix)
        draw = ImageDraw.Draw(rgbim)
        draw.text((0,0),str(yellowpix),(55,55,255),font=self.imgFont)
        #rgbim.save(self.imgPath+"/"+sensortag+"{:08}.png".format(self.step)) #FIX FOR LEX
        self.SaveImageInSubdir(rgbim,sensortag)

        wr.SetTermValue(sensortag,yellowpix)
        #if name == "viewl":
        #    self.lastLeftYellow = yellowpix
        #elif name == "viewr":
        #    self.lastRightYellow = yellowpix
    

    def Step(self):
        w=1920
        h=1080
        
        agent_pos, agent_orn =\
            p.getBasePositionAndOrientation(self.robotId)
        cameraOffset = [-1,-1,.75]

        camTargetPos = agent_pos
        cameraUp = [0, 0, 1]
        cameraPos = tuple(i + j for i,j in zip(agent_pos, cameraOffset))
        camDistance = 4

        pitch = -60.0
        yaw = 0 #?

        roll = 0
        upAxisIndex = 2
        pixelWidth = w
        pixelHeight = h
        nearPlane = 0.01
        farPlane = 100

        fov = 100

        self.stepnow = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        self.step += 1
        i = self.step
        self.Save_Data(str(i),"sim","step#")
        p.stepSimulation()

        self.ComputeCarView("SLFL",+.5)   # see .toml for SFLL/SFRL
        self.ComputeCarView("SRFL",-.5)
        #self.ComputeCarView("SUPL",'omni',255*2) # double samples ugh hack
        self.ComputeCarView("SUPL",'omni',255) # double samples ugh hack
        #self.ComputeCarView("SUPL",'omni',2) # debug: 2 samples, ~ignore up

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
        self.SaveImageInSubdir(rgbim,'view')
        self.robot.Sense(i)
        self.robot.Act(i)

        wr = self.worldrunner
        (bytesout, pktsin, bytesin) = wr.ps.getBufferSizes()
        self.Save_Packet_Data(bytesout,pktsin,bytesin)
        
        self.Flush_Data()
        #time.sleep(c.wallSecsPerStep)

    def SaveImageInSubdir(self,img,subdir):
        img.save(self.imgPath+"/{}/{}.png".format(subdir,self.stepnow))

    def Run(self):

        for i in range(c.steps):
            self.Step()
