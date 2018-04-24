from Communication import ArduinoCommunication as ac
from Communication import Mavlink as ml

class MotorControl(object):
    '''
    This class includes basic motor functions like throttling, brake etc.
    The class should handle the work of sharing data with arduino using ArduinoCommunication.py
    '''
    #Initializer
    def __init__(self):
        self.componentID = "_MOTOR"
        self.messageID = None
        self.payload = None
        self.mavlink = ml.Mavlink()
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

    def stopMotor(self):
        try:
            self.messageID = "_STOP"
            payload=self.payload
            data = self.mavlink.convertToByte(self.componentID,self.messageID)
            self.payload = None
            self.serial.sendData(data)
            return data
        except:
            return -1

    def calibrateMotor(self):
        '''
        The function is forinitial calibration and setup
        '''

    def forwardMotor(self,value):
        try:
            self.messageID = "_FORWARD"
            self.payload = value 
            data = self.mavlink.convertToByte(self.componentID,self.messageID)
            self.payload = None
            self.serial.sendData(data)
            return data
        except:
            return -1

    def backwardMotor(self,value):
        try:
            self.messageID = "_BACKWARD"
            self.payload = value
            data = self.mavlink.convertToByte(self.componentID,self.messageID)
            self.payload = None
            
            self.serial.sendData(data)
            
            return data
        except:
            return -1

    #MotorInput

    #PWM Generator
