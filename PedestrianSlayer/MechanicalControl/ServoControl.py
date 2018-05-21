from Communication import ArduinoCommunication as ac
from Communication import Mavlink as ml
#from Sensors import IMU
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
        #self.imu = IMU.IMU()
        self.oldOrient = 0
        self.oldLatError = 0
    
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

    def getCarOrient(self):
        '''
        Gets car orientation using IMU sensor
        '''
        (x,y,z) = self.imu.getOrientation()
        return z
        
    def getAngleDif(self,d_theta,d_latError,latError):
        '''
        It calculates the angle difference between center line and car orientation.
        Returns the value.
        '''
        angleDif = (math.asin((d_latError*sin(d_theta)+2*latError*sin(d_theta))/(d_latError))-d_theta)/2

        return angleDif
        
    def steerAngleControl(self,latError,k=0.02):
        '''
        Uses Stanley Method for steering angle control according to path radius.
        "latError" is deviation from center line of the path.
        "angleDif" is angle difference between center line and car orientation
        '''
        #Gain Constant
        k = 0.02
        
        #Get car speed
        speed = ServoControl.getCarSpeed(self)
        
        #Get orientation rate & update old orientation value
        newOrient = ServoControl.getCarOrient(self)
        d_theta = (newOrient-self.oldOrient)
        self.oldOrient = newOrient
        
        #Get lateral deviation from center line rate & update old deviation value
        newLatError = latError
        d_latError = newLatError-self.oldLatError
        self.oldLatError = newLatError
        
        #Get angle difference between center line and car orientation
        angleDif = ServoControl.angleDif(self,d_theta,d_latError,latError)
        
        #Calculate steering angle
        steeringAngle = angleDif + math.atan(k*latError/speed)

        return steeringAngle
