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
        ret = re.match(b'(.)W(.)(.)([IO].*)',packet,re.DOTALL) # DOTALL mode for 8BC? None if no match
        #if ret == None:
        #    print("WPPZNOmat",packet)
        return ret

    def handle(self,packet,match):
        hops=Utils.signedByteToIntAt(packet,0)
        dest=Utils.signedByteToInt(match.group(2)[0])
        impliedLoopLen=dest-hops
        self.ps.updateLoopLengthIfNeeded(impliedLoopLen)
        nonce=match.group(3)[0]
        pay=match.group(4)
        if nonce != self.ps.nonce:
            print("UNNONC MISS DISCARD", packet, nonce, self.ps.nonce)
            return
        
        #print("  PAY0",pay[0],ord(b'S'),b'S')
        if pay[0] == ord(b'I'):
            self.ps.flagIPacketSeen()
        elif pay[0] == ord(b'O'):
            self.ps.flagOPacketSeen()
            self.mrs.AcceptPayloadFromTile(pay,dest)

        print("WPPZhdl",packet,
              "hops=",hops,
              "dest=",dest,
              "nonce=",nonce,
              "pay=",pay)

class ConfigPacketProc(PacketProcessor):
    def __init__(self,mrs,name):
        super().__init__(mrs,name)
        self.ps = mrs.ps
        
    def matches(self,packet):
        # 0   12          34..
        # \x7eC[BCHOPS:1b]f[FULL CONFIG FILE]
        # \x7eC[BCHOPS:1b]s[NEEDFULL:1b][CONFIG FILE CHECKSUM]

        ret = re.match(b'\x7eC(.)([fs])(.)(.*)',packet,re.DOTALL)
        #if ret == None:
        #    print("CPPZNOmat",packet)
        return ret

    def handle(self,packet,match):
        print("WENDCPPDL",match,match.group(0),match.group(1),match.group(2))
        bchops=Utils.signedByteToIntAt(match.group(1),0)
        fs=match.group(2)[0]
        needfull=Utils.signedByteToIntAt(match.group(3),0)
        pay=match.group(4)
        if fs == ord(b's'):     # if checksum return, check if anybody wants full
            if needfull > 0:
                self.shipFullConfig()
        else:
            print("CPPhdl",bchops,fs,needfull)

    def shipFullConfig(self):
        wr = self.mrs
        conf = wr.config
        if conf.rawfile == None:
            print("SHPFLCF: No config")
            return            
        print("IUIUSHIPFULLCF",len(conf.rawfile))
        payload = (b'C'          # Config packet
                   + b'\x00'     # broadcast hops == 0
                   + b'f'        # config 'f'ull subpacket
                   + conf.rawfile) # and the config file itself
        wr.ps.sendBroadcastPacket(payload)


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

class MinutesStep(Event): 
    def __init__(self,mrs):
        super().__init__(mrs,"MinutesStep")
        self.secs = 60
        self.secsoffset = 3 # Run at 3 seconds past the minute

    def run(self,eq,now,dead):
        #### timestep management
        delta = now - dead
        if delta >= self.secs:
            evts = int(delta/self.secs)
            print(f'WARNING: {evts} event(s) missed')
        then = int((now+self.secs)/self.secs)*self.secs+self.secsoffset
        print("MSNSXT",now,then)
        eq.runAt(then,self)
        
        #### issue config check
        self.shipConfigCheck()


    def shipConfigCheck(self):
        wr = self.mrs
        conf = wr.config
        if conf.rawfile == None or conf.rawfileCS == None:
            print("MinutesStep: No config")
            return            
        print("KDKDshipConfigCheck",len(conf.rawfile),conf.rawfileCS)
        payload = (b'C'          # Config packet
                   + b'\x00'     # broadcast hops == 0
                   + b's'        # check's'um subpacket
                   + b'\x00'     # need full count == 0
                   + conf.rawfileCS) # and the checksum itself
        wr.ps.sendBroadcastPacket(payload)
        
