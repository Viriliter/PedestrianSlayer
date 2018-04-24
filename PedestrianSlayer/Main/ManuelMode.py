from MechanicalControl import MotorControl as mc
from MechanicalControl import ServoControl as sc
#import UserCommunication as uc
from time import sleep
from Communication import ArduinoCommunication

class ManuelMode():
    '''
    ***Algorithm Summary***
    Use UserCommunication.py for input
    According to input use MotorCOntrol.py and ServoControl.py
    Send these outputs to arduino using ArduinoCommunication.py
    '''
    #Initializer
    def __init__(self):
        '''
        After each driving mode switch, the motor will be stoped and servo is setted to default
        For this, MotorControl class will be used.
        '''
        self.motorControl = mc.MotorControl()
        self.servoControl = sc.ServoControl()
        #self.userCom = uc.UserCommunication()
        isUserInterrupt = False
        
    #Mutators

    #Accessors

    #Methods
    '''def interpreter(self,address,value):
        if(address=="MOTOR_STOP"):
            result = self.motorControl.stopMotor()
            #print(result)
        elif(address=="MOTOR_FORWARD"):
            result = self.motorControl.forwardMotor(value)
            #print(result)
        elif(address=="MOTOR_BACKWARD"):
            result = self.motorControl.backwardMotor(value)
            #print(result)
        elif(address=="SERVO_ANGLE"):
            result = self.servoControl.angle(value)
            #print(result)
    '''
    def stopMotor(self):
        self.motorControl.stopMotor()
        

    def forwardMotor(self, value = 0):
        self.motorControl.forwardMotor(value)


    def backwardMotor(self, value = 0):
        self.motorControl.backwardMotor(value)


    def testCommunication(self):
        try:
            while(1):
                ManuelMode.stopMotor(self)
                
                ManuelMode.forwardMotor(self)
                
                ManuelMode.stopMotor(self)
                
                ManuelMode.backwardMotor(self)
        except KeyboardInterrupt:
            raise
 
    '''
    def activate(self):
        while not(isUserInterrupt):
            address,value = self.userCom.read()
            if(address==None):
                isUserInterrupt=False
            else:
                isUserInterrupt=True
                ManuelMode.interpreter(address,value)
    '''
    
