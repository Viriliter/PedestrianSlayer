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
        self.isUserInterrupt = False
        self.userInput = None
        self.angle = 110
        self.cycle = 10

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


    def run(self):
        try:
            while(True):
                #Get Keyboard input from the user
                self.userInput = input()
                #Classify the input and run
                self.isisUserInterrupt = ManuelMode.inputClassifier(self,self.userInput)
                if(self.isUserInterrupt):
                    #Exit from manuel mode
                    return True
        except Exception:
            pass
    
    def inputClassifier(self,input):
        '''
        According to keyboard input, corresponding motor and servo control is implemented.
        '''
        if(input=="e"):     #Exit command
            return True
        elif(input=="w"):       #Forward command
            if(self.cycle<=100):
                self.cycle = self.cycle+10
                sleep(0.3)
            self.motorControl.forwardMotor(self.cycle)
            return False
        elif(input=="a"):       #Left command
            if(self.angle<=150):
                self.angle = self.angle+10
                sleep(0.3)
            self.servoControl.angle(self.angle)
            return False
        elif(input=="s"):       #Backward command
            if(self.cycle>=10):
                self.cycle = self.cycle-10
                sleep(0.3)
            self.motorControl(self.cycle)
            return False
        elif(input=="d"):       #Right command
            if(self.angle>=50):
                self.angle = self.angle+10
                sleep(0.3)
            self.servoControl.angle(self.angle)
            return False
        elif(input==" "):       #Stop command
            self.motorControl.stopMotor(cycle)
            sleep(0.3)
            return False

    
