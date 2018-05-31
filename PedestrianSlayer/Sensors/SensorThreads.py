from Sensors import IMU
from Sensors import UltrasonicSensor as us
from Communication import ArduinoCommunication as ac
import threading
import time

#Declare Gloabal Variables
_distance = 0
_imu_gyro_x = 0
_imu_gyro_y = 0
_imu_gyro_z = 0
_speed = 0

class SensorThread():
    def __init__(self):
        self.imu = IMU.IMU()
        self.distanceSensor = us.UltrasonicSensor()
        self.serial = ac.ArduinoCommunication()
        self.distance = 0
        self.imu_gyro_x = 0
        self.imu_gyro_y = 0
        self.imu_gyro_z = 0
        self.speed = 0
        self.threads = []
        super().__init__()

    def get_distance(self):
        return self.distance

    def get_speed(self):
        return self.speed 

    def get_gyro_X(self):
        return self.imu_gyro_x

    def get_gyro_Y(self):
        return self.imu_gyro_y
    
    def get_gyro_Z(self):
        return self.imu_gyro_z

    def set_speed(self,speed):
        self.speed = speed

    def set_gyro_X(self,imu_gyro_x):
        self.imu_gyro_x = imu_gyro_x

    def set_gyro_Y(self,imu_gyro_y):
        self.imu_gyro_y = imu_gyro_y
    
    def set_gyro_Z(self,imu_gyro_z):
        self.imu_gyro_z = imu_gyro_z

    def run_threads(self):
        threads = []
        thread_imu = threading.Thread(target=SensorThread.pool_imu, args=(self,))
        thread_speed = threading.Thread(target=SensorThread.pool_speed, args=(self,))
        thread_distane = threading.Thread(target=SensorThread.pool_distance, args=(self,))
        
        self.threads.append(thread_imu)
        self.threads.append(thread_speed)
        self.threads.append(thread_distane)

        thread_imu.start()
        thread_speed.start()
        thread_distane.start()
    
    def pool_imu(self):
        '''
        Pools imu datas from MPU6050 using GPIO pins
        '''
        while(True):
            self.imu_gyro_x, self.imu_gyro_y, self.imu_gyro_z = self.imu.getGyro()
            #print("Reading IMU")
            #print(_imu_gyro_z)
            time.sleep(0.2)
        
    def pool_speed(self):
        '''
        Pools speed from encoder using serial communication via arduino
        '''
        while(True):
            self.speed = self.serial.getData('_SENSORS','_SPEED')
            self.speed += 20
            #print("Reading Speed")
            #print(_speed)
            time.sleep(0.2)
        
    def pool_distance(self):
        '''
        Pools distance data from ultrasonic sensor using GPIO pins
        '''
        while(True):
            self.distance = self.distanceSensor.getDistance()
            self.distance += 10
            #print("Reading Distance")
            #print(_distance)
            time.sleep(0.2)


    
        
        
