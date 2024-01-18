import random

from abc import ABC, abstractmethod

from MrState import MrState
from PacketSpine import PacketSpine
from simulation import SIMULATION
import WorldEvents
import tomlikey as toml

import Utils

import re

import sys

class WorldRunner(MrState):
    def __init__(self,name,serdev,cfgFile):
        print("LDSDSL")
        super().__init__(name,cfgFile)
        print("LDSDSLODNE")

        self.simulation = SIMULATION()
        print("PCKKDPSPSON")
        self.ps = PacketSpine(self,serdev)
        print("PCKKDPSPSOFFN")

        self.pproc = WorldEvents.WorldPacketProc(self,"Wpproc")
        self.ps.registerPacketProcessor(self.pproc)

    def RunSteps(self):
        while (self.simulation.step < c.steps):
            self.simulation.Step()

    def Run(self):
        self.RunSteps()
        self.simulation.Generate_Video()


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit("Need config file argument")
    configFile = sys.argv[1]
    #with open(configFile,"rb") as f:
    #    cfg = toml.load(f)
    #print("POF",configFile,cfg)

    wr = WorldRunner("TestZONG","/dev/ttyUSB0",configFile)
    print("CNCNCNGJF",wr.config.hash)
    secsPerStep = 1.5
    se = WorldEvents.SecondsStep(wr,secsPerStep)
    wr.EQ.runIn(0, se)
    ps = WorldEvents.PacketSpineStep(wr,wr.ps,0.1)
    wr.EQ.runIn(0, ps)
    wr.mainLoop()
    
##########EVENTS############
