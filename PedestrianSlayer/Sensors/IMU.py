import smbus
import math
import time

class IMU():
    def __init__(self):
    #Power management registers
        self.power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c

        self.bus = smbus.SMBus(1)
        self.address = 0x68 #MPU6050 I2C address

        #For first run, awake from sleep
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

    
    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val = IMU.read_word(self,adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self,a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x, IMU.dist(self,y,z))
        return -math.degrees(radians)

    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, IMU.dist(self,x,z))
        return math.degrees(radians)

    def readGyro(self):
        #Read from gyroscope registers
        gyro_xout = IMU.read_word_2c(self,0x43)
        gyro_yout = IMU.read_word_2c(self,0x45)
        gyro_zout = IMU.read_word_2c(self,0x47)

        print ("Gyroscope X : ", gyro_xout, " scaled: ", (gyro_xout / 131))
        print ("Gyroscope Y : ", gyro_yout, " scaled: ", (gyro_yout / 131))
        print ("Gyroscope Z: ", gyro_zout, " scaled: ", (gyro_zout / 131))

        return (gyro_xout,gyro_yout,gyro_zout)
    
    def readAccel(self): 
        #Read from accelerometer registers
        accel_xout = IMU.read_word_2c(self,0x3b)
        accel_yout = IMU.read_word_2c(self,0x3d)
        accel_zout = IMU.read_word_2c(self,0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        print ("Accelerometer X: ", accel_xout, " scaled: ", accel_xout_scaled)
        print ("Accelerometer Y: ", accel_yout, " scaled: ", accel_yout_scaled)
        print ("Accelerometer Z: ", accel_zout, " scaled: ", accel_zout_scaled)

        return (accel_xout,accel_yout,accel_zout)
    
    def readOrient(self):
        #Read from accelerometer registers
        accel_xout = IMU.read_word_2c(self,0x3b)
        accel_yout = IMU.read_word_2c(self,0x3d)
        accel_zout = IMU.read_word_2c(self,0x3f)
        
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        orient_x = IMU.get_x_rotation(self,accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        orient_y = IMU.get_y_rotation(self,accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        
        print ("X orientation: " , orient_x)
        print ("Y orientation: " , orient_y)

        return (orient_x,orient_y)

if __name__=="__main__":
    imu= IMU()
    while(1):
        x,y = imu.readOrient()
        print(x)
        print(y)
        print("----")
        time.sleep(2)
