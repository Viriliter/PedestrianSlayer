from Communication import ArduinoCommunication as ac
from Communication import Mavlink as ml

class LightControl(object):
    """description of class"""
    def __init__(self):
        self.componentID="_LIGHT"
        self.messageID = None
        self.payload = None
        self.mavlink = ml.Mavlink()
        self.serial = ac.ArduinoCommunication()

    def stopLight(self):
        try:
            self.messageID = "_STOP"
            self.payload = value
            data = self.mavlink.convertToByte(self,self.componentID,self.messageID,self.payload)
            self.payload = None
            self.serial.sendData(data)
            return True
        except:
            return False

    def rearLeft(self):
        try:
            self.messageID = "_LEFT"
            self.payload = value
            data = self.mavlink.convertToByte(self,self.componentID,self.messageID,self.payload)
            self.payload = None
            self.serial.sendData(data)
            return True
        except:
            return False

    def rearRight(self):
        try:
            self.messageID = "_RIGHT"
            self.payload = value
            data = self.mavlink.convertToByte(self,self.componentID,self.messageID,self.payload)
            self.payload = None
            self.serial.sendData(data)
            return True
        except:
            return False

    def reverseLight(self):
        try:
            self.messageID = "_REVERSE"
            self.payload = value
            data = self.mavlink.convertToByte(self,self.componentID,self.messageID,self.payload)
            self.payload = None
            self.serial.sendData(data)
            return True
        except:
            return False


