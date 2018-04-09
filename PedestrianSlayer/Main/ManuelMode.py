from MechanicalControl import MotorControl as mc
from MechanicalControl import ServoControl as sc

class ManuelMode(object):
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

    #Mutators

    #Accessors

    #Methods


