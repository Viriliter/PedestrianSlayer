from ImageProcessing import LaneDetector as ld
from ImageProcessing import ObjectDetector as od
from ImageProcessing import CascadeClassifier as cc
from MechanicalControl import MotorControl as mc
from MechanicalControl import ServoControl as sc
#from MechanicalControl import NeuralNetwork as nn
#from Sensors import SensorThread as st
import time

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
        self.motorControl = mc.MotorControl()
        self.servoControl = sc.ServoControl()
        #self.objectDetector = od.ObjectDetector()
        #self.cascadeClassifier = cc.CascadeClassifier()
        #self.sensorThread = st.SensorThread()
        #self.neuralNetwork = nn.NeuralNetwork()
        self.count = 0
        self.user_input = None
        # Create new threads
        AutonomousMode.run(self)
        
    def getInput(self):
        self.user_input = input()


    def run(self):
        '''
        Initialize LaneDetector.py and RoadSignDetector.py
        Multi threading is neccasary for both lane and road sign detection
        '''
        radiusLeft = 0
        radiusRight = 0
        deviation = 0
        lanedetector = ld.LaneDetector()
        while(True):
            millis1 = int(round(time.time() * 1000))
            #radiusLeft,radiusRight,deviation = lanedetector.getLaneParameters()
            millis2 = int(round(time.time() * 1000))
            self.motorControl.forwardMotor(0)
            self.servoMotor.angle(0)
            #print (millis2-millis1)
            if not(radiusLeft==0 and radiusRight==0 and deviation==0):
                #print(str(radiusLeft)+" ; "+str(radiusRight)+" ; "+str(deviation))
                #lanedetector.showFrame("AnnotedFrame")
                #lanedetector.waitKey()
                #middle_radius = (radiusLeft+radiusRight)/2
                #Get undistorted frame. Run objectDetector
                #frame = self.objectDetector.getUndistortedFrame()
                #magnitude = self.objectDetector.run(frame)


                magnitude=-1
                #Use motor and servo control algorithm to find steering angle and motor thrust.
                #Use 4 parameters:p1, p2, p3, and magnitude. Magnitude value overrules steering angle.
                #if(magnitude==-1):
                #   latError = deviation
                # Get ideal angular speed by using radius of curvature of the road
                #   angular_speed = self.motorControl.getIdelAngularVelocity(radius)
                #   self.motorControl.forwardMotor(angular_speed)
                # Get ideal steering angle of the tires using perceptron learning algorithm
                #   angle = self.neuralNetwork.getSteeringAngle(middle_radius,deviation,angular_speed,orient)
                #   self.servoControl.angle(angle)
                #else:
                    #Overrule magnitude value.
                #    latError = deviation - magnitude
                #    self.motorControl.speedNegotiation(radius,v_target,v_current)
                #    self.servoControl.steerAngleControl(speed,k,angleDif,latError)
                
                if(self.user_input=="e"):
                    break
            else:
                count = AutonomousMode.errorCounter(self)
                if(self.count>=10):
                    #This is the case when the car gets out of the lane.
                    value = 50
                    #motorControl.backwardMotor(value)
                    AutonomousMode.resetCounter(self)
                if(self.user_input=="e"):
                    break
        return True
        #Use MotorControl.py and ServoControl.py controlling
            
    #Mutators

    #Accessors

    #Methods

    def errorCounter(self):
        self.count += 1
        return self.count

    def resetCounter(self):
        self.count = 0
