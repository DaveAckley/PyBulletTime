#!/usr/bin/python3
import random

from abc import ABC, abstractmethod

from MrState import MrState
from PacketSpine import PacketSpine
from simulation import SIMULATION
import WorldEvents
import tomlikey as toml

import Spine

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

        self.cproc = WorldEvents.ConfigPacketProc(self,"Cpproc")
        self.ps.registerPacketProcessor(self.cproc)

    def AcceptPayloadFromTile(self,payload,tilenum):
        if len(payload) < 1:
            print("SHORTPAYIGNRD?",payload)
            return
        if payload[0] != ord(b'O'):
            print("NOTOPPLOD?",payload)
            return
        print("AACCCLFT",payload)

        terms = self.getRequiredSection('term')
        termindicesintile = terms['_tiles_'].get(tilenum)
        tnames = terms['_indices_']
        print("APFFTRM",termindicesintile)
        for i in range(1,len(payload),2):
            idx = payload[i]
            val = payload[i+1]
            if idx in termindicesintile:
                tname = tnames[idx]
                term = terms.get(tname)
                if term != None and term['type'] == 'motor':
                    term['value'] = val
                    #print("MOTOID",tname,val)
            else:
                print("NBABADINDEX",idx,termindicesintile)

    def GetTermForJointIfAny(self,jointname):
        terms = self.getRequiredSection('term')
        joints = terms['_joints_']
        index = joints.get(jointname)
        if index == None:
            return None
        name = terms['_indices_'][index]
        term = terms[name]
        return term

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
            value = term.get('value',0)
            #print("GPFT",term,index,tname,value)
            payload.append(index)
            payload.append(value)
        
        return payload
    
    def IndexTerminals(self):
        terms = self.getInitializedSection('term',{})
        Spine.IndexTerminals(terms)

    def GetTermValue(self,termtag):
        terms = self.getRequiredSection('term')
        term = terms[termtag]
        return term.get('value',0)

    def SetTermValue(self,termtag,byteval):
        assert(byteval >= 0 and byteval <= 255)
        ival = int(byteval)
        terms = self.getRequiredSection('term')
        term = terms[termtag]
        term['value'] = ival
        print("WRSTV",termtag,ival,term)
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
    secsPerStep = 2
    se = WorldEvents.SecondsStep(wr,secsPerStep)
    wr.EQ.runIn(0, se)
    ms = WorldEvents.MinutesStep(wr)
    wr.EQ.runIn(10, ms)
    ps = WorldEvents.PacketSpineStep(wr,wr.ps,0.1)
    wr.EQ.runIn(0, ps)
    wr.mainLoop()
    
##########EVENTS############
