from abc import ABC, abstractmethod

import re

import Utils
from Event import Event
from PacketProcessor import PacketProcessor

import constants as c

WPP_START = 0
WPP_RUNNING = 1

class WorldPacketProc(PacketProcessor):
    def __init__(self,mrs,name):
        super().__init__(mrs,name)
        self.state = WPP_START
        self.ps = mrs.ps
        
    def matches(self,packet):
        ret = re.match(b'(.)W(.)(.)([SM].*)',packet,re.DOTALL) # DOTALL mode for 8BC? None if no match
        if ret == None:
            print("WPPZNOmat",packet)
        return ret

    def handle(self,packet,match):
        hops=Utils.signedByteToIntAt(packet,0)
        dest=Utils.signedByteToInt(match.group(2)[0])
        impliedLoopLen=dest-hops
        self.ps.updateLoopLengthIfNeeded(impliedLoopLen)
        nonce=match.group(3)[0]
        pay=match.group(4)
        #print("  PAY0",pay[0],ord(b'S'),b'S')
        if pay[0] == ord(b'S'):
            self.ps.flagSPacketSeen()
        elif pay[0] == ord(b'M'):
            self.ps.flagMPacketSeen()

        print("WPPZhdl",packet,
              "hops=",hops,
              "dest=",dest,
              "nonce=",nonce,
              "pay=",pay)


class PacketSpineStep(Event):
    def __init__(self,mrs,ps,secs):
        super().__init__(mrs,"PacketSpineStep")
        assert(secs>0.0)
        self.ps = ps
        self.secs = secs
        self.calls = 0

    def run(self,eq,now,dead):
        self.calls += 1
        if self.calls % 100 == 0:
            print("PSSCALLS",self.calls)
        while self.ps.update() > 0:
            pass
        then = now+self.secs
        eq.runAt(then,self)

class SecondsStep(Event):
    def __init__(self,mrs,secs):
        super().__init__(mrs,"SecondsStep")
        assert(secs>=1.0)
        self.secs = int(secs)

    def run(self,eq,now,dead):
        #### timestep management
        delta = now - dead
        print(f'WorldEvents: {dead} executed at {now} delay {delta}')
        if delta >= self.secs:
            evts = int(delta/self.secs)
            print(f'WARNING: {evts} event(s) missed')
        then = int(now/self.secs)*self.secs+self.secs
        eq.runAt(then,self)

        #### update world
        self.mrs.simulation.Step()

        #### begin sensorimotor update
        self.mrs.ps.initSM()
        
        #### kill sim if at EoU
        if c.steps > 0 and self.mrs.simulation.step > c.steps:
            self.mrs.simulation.Generate_Video()
            exit()
