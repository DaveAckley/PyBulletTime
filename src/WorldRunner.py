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

        self.IndexTerminals()
        self.simulation = SIMULATION(self)

        self.EstablishDirs()

        print("PCKKDPSPSON")
        self.ps = PacketSpine(self,serdev)
        print("PCKKDPSPSOFFN")

        self.pproc = WorldEvents.WorldPacketProc(self,"Wpproc")
        self.ps.registerPacketProcessor(self.pproc)

    def GetPayloadForTile(self,tilenum):
        terms = self.getRequiredSection('term')
        payload = bytearray()
        termindices = terms['_tiles_'].get(tilenum)
        tnames = terms['_indices_']
        if not termindices:
            return payload
        for index in termindices:
            tname = tnames[index]
            term = terms[tname]
            # so how now?
            payload+=tname.encode()
        
        return payload
    
    def IndexTerminals(self):
        indices = []
        tiles = {}       # tile# -> [indices]
        terms = self.getInitializedSection('term',{})
        for tname in sorted(terms.keys()):
            if tname.startswith("_"):
                raise Exception("Illegal term key: "+tname)
            term = terms[tname]
            index = len(indices)
            term['_index_'] = index
            opttile = term.get('tile')
            if not opttile == None:
                if opttile not in tiles:
                    tiles[opttile] = []
                tiles[opttile].append(index)
                indices.append(tname)
        terms['_indices_'] = indices
        terms['_tiles_'] = tiles
        print("INDSL",self.getRequiredSection('term'))

    def GetTermValue(self,termtag):
        terms = self.getRequiredSection('term')
        term = terms[termtag]
        return term.get('value',0)

    def SetTermValue(self,termtag,byteval):
        assert(byteval >= 0 and byteval <= 255)
        ival = int(byteval)
        terms = self.getRequiredSection('term')
        term = terms[termtag]
        term[termtag] = ival
        return ival

    def EstablishDirs(self):
        terms = self.getRequiredSection('term')
        for k,v in terms.items():
            if k.startswith("_"):
                continue
            #print("SLDKEIZXXDIR",k,v)
            if v['type'] != 'sensor':
                continue
            self.simulation.EnsureSimSubdir("imgs/"+k)

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

    wr = WorldRunner("TestZONG","/dev/ttyUSB1",configFile)
    print("CNCNCNGJF",wr.config.hash)
    secsPerStep = 1
    se = WorldEvents.SecondsStep(wr,secsPerStep)
    wr.EQ.runIn(0, se)
    ps = WorldEvents.PacketSpineStep(wr,wr.ps,0.1)
    wr.EQ.runIn(0, ps)
    wr.mainLoop()
    
##########EVENTS############
