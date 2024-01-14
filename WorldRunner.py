import random

from abc import ABC, abstractmethod

from MrState import MrState
from PacketSpine import PacketSpine
from simulation import SIMULATION
import WorldEvents

import Utils

import re

class WorldRunner(MrState):
    def __init__(self,name,serdev):
        print("LDSDSL")
        super().__init__(name)
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
    wr = WorldRunner("TestZONG","/dev/ttyUSB0")
    secsPerStep = 5
    se = WorldEvents.SecondsStep(wr,secsPerStep)
    wr.EQ.runIn(0, se)
    ps = WorldEvents.PacketSpineStep(wr,wr.ps,0.1)
    wr.EQ.runIn(0, ps)
    wr.mainLoop()
    
##########EVENTS############
