from ImageProcessing import LaneDetector as ld

class AutonomousMode(object):
    '''
    ***Algorithm Summary***
    Stop motor
    Set to default servo angle
    Initiate the mode:
        Activate image processing:
            Activate LaneDetector.py
            Activate RoadSignDetector.py
        Take input from image processing classes
        Put inputs into machine learning algorithm
        Use PID.py in MechanicalControl for motor input
        According to PID.py outputs
            Use MotorControl.py in MechanicalControl
            Use ServoControl.py in MechanicalControl

            Use ArduinoCommunication to send data
    '''

    #Initializer
    def __init__(self):
        '''
        After each driving mode switch, the motor will be stoped and servo is setted to default
        For this, MotorControl class will be used.
        '''
        AutonomousMode.run(self)

    def run(self):
        '''
        Initialize LaneDetector.py and RoadSignDetector.py
        Multi threading is neccasary for both lane and road sign detection
        '''
        lanedetector = ld.LaneDetector()
        lanedetector.run()

        #Take input from LaneDetector class
        #Take input from sensors
        #Combine these inputs and send them to NeuralNetwork class.
        #NeuralNetwork class will give 2 outputs: Motor PWM and Servo PWM
        #Use MotorControl.py and ServoControl.py controlling

    #Mutators

    #Accessors

    #Methods



