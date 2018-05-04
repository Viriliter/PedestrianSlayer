import numpy as np
import cv2
import time
import math
#Not activate until the system is integrated to RasPi
#import RPi.GPIO as GPIO

class ObjectDetector():
    '''
    This class finds the road lines using warpPerspective and Canny method, and then
    polyfit them in order to find their curvature parameters.
    '''
    #Initializer
    def __init__(self):
        self.frame = None
        self.width = None               #Set to default value
        self.height = None              #Set to default value
        self.frameSize = (self.width,self.height)
        self.XmperPix = 3.7/700         # meters per pixel in x dimension
        self.YmperPix = 30/720          # meters per pixel in y dimension
        self.minimumDistance = math.inf
        #--------------------------------------------------------------------------------------------------
        #Set ultrasonic sensor configuraiton.These will be unactive until the system is integrated to RasPi
        #--------------------------------------------------------------------------------------------------
        #Set GPIO Mode
        #GPIO.setmode(GPIO.BCM)
        #Set GPIO Pins
        #self.GPIO_TRIGGER = 18
        #self.GPIO_ECHO = 24

    #Mutators

    #region
    def setFrame(self, frame):
        self.frame = frame

    def setResolutionValue(self,resolutionValue):
        self.getResolutionValue = resolutionValue

    def setSrc(self, src):
        self.src = src

    def setDst(self, dst):
        self.dst = dst

    def setLeftFit(self,LeftFit):
        self.LeftFit = LeftFit

    def setLeftCurveRad(self,LeftCurveRad):
        self.LeftCurveRad = LeftCurveRad

    def setRightFit(self,RightFit):
        self.RightFit = RightFit

    def setRightCurveRad(self,RightCurveRad):
        self.RightCurveRad = RightCurveRad

    def setXmperPix(self,XmperPix):
        self.XmperPix = XmperPix

    def setYmperPix(self,YmperPix):
        self.YmperPix = YmperPix
    
    #endregion

    #Accessors 
    #region 
    def getFrame(self):
        return self.frame

    def getResolutionValue(self):
        return self.resolutionValue

    def getFrameSize(self):
        return self.frameSize

    def getSrc(self):
        return self.src

    def getDst(self):
        return self.dst
        
    def getUndistorted(self):
        return self.undistorted
    
    def getBinaryWarped(self):
        return self.binary_warped

    def getVideoCapture(self):
        return self.videoCapture

    def getLeftFit(self):
        return self.LeftFit

    def getRightFit(self):
        return self.RightFit

    def getLeftCurveRad(self):
        return self.LeftCurveRad

    def getRightCurveRad(self):
        return self.RightCurveRad

    def getXmperPix(self):
        return self.XmperPix

    def getYmperPix(self):
        return self.YmperPix

    def getCountedError(self):
        return self.errorCnt

    #endregion
    
    #Methods
    #region 
    def measureDistance(self):
        #==========================================================================================================
        #Measures distance from ultrasoin sensor using ultrasonic sensor class. Return the distance as double value
        #==========================================================================================================
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
 
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
 
        StartTime = time.time()
        StopTime = time.time()
 
        #Save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            startTime = time.time()
 
        #Save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            stopTime = time.time()
 
        #Time difference between start and arrival
        timeElapsed = stopTime - startTime
        #Multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
        measuredDistance = (timeElapsed * 34300) / 2
 
        return measuredDistance

    def detectObject(self,frame):
        #==========================================================================================================
        #If distance is at specific distance, gets video frame, searches, and points the object out on the frame.
        #Return as frame with highlighted object.
        #==========================================================================================================

        #Point out the object
        #Return manipulatedFrame
        return manipulatedFrame
        
    def getObjectPosition(self,manipulatedFrame):
        #==========================================================================================================
        #Decides whether the object is left or right side of the frame. Return as magnitude value how far the object from the frame.
        #==========================================================================================================
        width = frame.shape[1]      #Width
        height = frame.shape[0]     #Height
        #Find center point of the object(pointX,pointY)
        
        out_img = (np.dstack((manipulatedFrame, manipulatedFrame, manipulatedFrame)) * 255).astype(np.uint8)
        histogram = np.sum(manipulatedFrame[int(manipulatedFrame.shape[0]/2):,:], axis=0)

        return (pointX-width/2)/width    #if positive, it is right; if not left
    
    def run(self,frame):
        #==========================================================================================================
        #Runs object detection function
        #==========================================================================================================
        
        #Measure the distance
        #if condition satisfies run detectObject() and return magnitude; if not return as -1
        measuredDistance = ObjectDetector.measureDistance(self)
        if(measuredDistance<=self.minimumDistance):
            manipulatedFrame = ObjectDetector.detectObject(self,frame)
            magnitude = ObjectDetector.getObjectPosition(self,manipulatedFrame)
            return magnitude
        else:
            return -1
    #endregion