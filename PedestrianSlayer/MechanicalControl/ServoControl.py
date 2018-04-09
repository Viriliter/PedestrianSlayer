from Communication import ArduinoCommunication as ac
from Communication import Mavlink as ml

class ServoControl(object):
    '''
        This class includes basic motor functions like ervo calibration, turning servo in defined angle etc.
    '''
    #Initializer
    def __init__(self):
        self.componentID = "_SERVO"
        self.messageID = None
        self.payload = None
        self.protocolLib = ml.ProtocolLibrary()
        self.serial = ac.ArduinoCommunication()
    
    #Mutators
    def setPayload(self,payload):
        self.payload = payload
    
    #Accessors
    #region
    def getComponentID(self):
        return self.componentID

    def getMessageID(self):
        return self.messageID

    def getPayload(self):
        return self.payload
    
    #endregion

    #Methods

    def angle(self,value):
        '''
        Servo rotates in specific angle
        '''
        try:
            self.messageID = "_ANGLE"
            self.payload = value
            data = self.protocolLib.convertToByte(self,self.componentID,self.messageID,self.payload)
            self.payload = None
            self.serial.sendData(data)
            return True
        except:
            return False


    def defaultPosition(self):
        '''
        Servo rotates to default position
        '''
        try:
            self.messageID = "_DEFAULT"
            self.payload = 0
            data = self.protocolLib.convertToByte(self,self.componentID,self.messageID,self.payload)
            self.payload = None
            self.serial.sendData(data)
            return True
        except:
            return False

