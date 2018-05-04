from Communication import ArduinoCommunication as ac
from Communication import Mavlink as ml
import math

class ServoControl(object):
    '''
        This class includes basic motor functions like ervo calibration, turning servo in defined angle etc.
    '''
    #Initializer
    def __init__(self):
        self.componentID = "_SERVO"
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

    def angle(self,value):
        '''
        Servo rotates in specific angle
        '''
        try:
            self.messageID = "_ANGLE"
            self.payload = value
            data = self.mavlink.convertToByte(self,self.componentID,self.messageID,self.payload)
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
            data = self.mavlink.convertToByte(self,self.componentID,self.messageID,self.payload)
            self.payload = None
            self.serial.sendData(data)
            return True
        except:
            return False
    
    def smoothPath(self):
        '''

        '''
    
    def getCarSpeed(self):
        '''
        Gets motor speed from speed sensor(s). Converts to car speed.
        '''

    def steerAngleControl(void,speed,k,angleDif,latError):
        '''
        Uses Stanley Method for steering angle control according to path radius.
        "latError" is deviation from center line of the path.
        "angleDif" is angle difference between center line and car orientation
        '''
        #Gain Constant
        k = 0.02
        #Get car speed
        ServoControl.getCarSpeed(self)
        steeringAngle = angleDif + math.atan(k*latError/speed)
        return steeringAngle