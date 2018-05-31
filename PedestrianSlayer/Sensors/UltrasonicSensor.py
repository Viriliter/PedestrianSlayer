
#Not activate until the system is integrated to RasPi
#import RPi.GPIO as GPIO

class SonicSensor():
    '''
    This class consist relevant function for acquiring distance between any obstacle and the car.
    '''
    #Initializer
    def __init__(self):
        #--------------------------------------------------------------------------------------------------
        #Set ultrasonic sensor configuraiton.These will be unactive until the system is integrated to RasPi
        #--------------------------------------------------------------------------------------------------
        #Set GPIO Mode
        #GPIO.setmode(GPIO.BCM)
        #Set GPIO Pins
        #self.GPIO_TRIGGER = 18
        #self.GPIO_ECHO = 24
        i=0

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