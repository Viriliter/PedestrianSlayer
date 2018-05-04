from Communication import ArduinoCommunication as ac
from Communication import Mavlink as ml
from Sensors import SpeedSensor
import math

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
        self.speedSensor = SpeedSensor.SpeedSensor()

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
        The function is for initial calibration and setup of the motor
        '''

    def forwardMotor(self,value):
        '''
        Sends duty cycle of the motor in forward direction to Arduino
        '''
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
        '''
        Sends duty cycle of the motor in reverse direction to Arduino
        '''
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
    
    def getIdealSpeed(self,radius):
        #Friction coefficient(between 0.1-0.16)
        nu = 0.13
        #Gravitiy constant
        g = 9.81

        #Curvature information
        k=1/radius
        
        #Calculate ideal speed
        v_ideal = math.sqrt((e+nu)*g/k)
        return idealSpeed

    def speedNegotiation(self,radius,v_target,v_current):
        #Deceleration  value
        a_neg = 2   #Maximum deceleration (m/s^2)
        a_max = 2   #Maximum acceleration (m/s^2)
        
        #Calculate trigger distance
        d_trig =(v_target*v_target-v_current*v_current)/(2*a)
        
        #Get ideal speed
        v_ideal = MotorControl.getIdealSpeed(self,radius)
        
        #Get current speed
        v_current = self.speedSensor.getCurrentSpeed()

        if(v_current>v_ideal):
            if(v_ideal==v_c):
                if((d_current>=d_c-d_trig) and
                (d_current<=d_c+l_c)):
                    #Apply a_neg until v_current=v_ideal
                    min_value = 0 #Duty cycle of motor(0-100) for max acceleration

            else:
                if((d_current>=d_l-d_trig) and
                (d_current<=d_l)):
                    #Apply a_neg until v_current = v_ideal
                    min_value = 0 #Duty cycle of motor(0-100) for max acceleration

        else:
            #Apply a_max until reaching v_ideal
            max_value = 100 #Duty cycle of motor(0-100) for max acceleration
            MotorControl.forwardMotor(self,value)
            