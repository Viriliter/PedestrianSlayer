import smbus
import math
import time

class IMU():
    '''
    This class consist relevant function for acquiring data comes from inertial measurement unit.
    For this project, the IMU sensor is MPU6050.
    '''
    #Initializer
    def __init__(self):
        # Power management registers
        self.power_mgmt_1 = 0x6b

        self.power_mgmt_2 = 0x6c

        self.gyro_scale = 131.0

        self.accel_scale = 16384.0

        self.address = 0x68  # This is the address value read via the i2cdetect command

    def getAccel(self):
        pass
    
    def getGlobalAccel(self):
        pass

    def getOrientation(self):
        pass

    def read_all():
        raw_gyro_data = bus.read_i2c_block_data(self.address, 0x43, 6)

        raw_accel_data = bus.read_i2c_block_data(self.address, 0x3b, 6)

        gyro_scaled_x = twos_compliment((raw_gyro_data[0] << 8) + raw_gyro_data[1]) / self.gyro_scale

        gyro_scaled_y = twos_compliment((raw_gyro_data[2] << 8) + raw_gyro_data[3]) / self.gyro_scale

        gyro_scaled_z = twos_compliment((raw_gyro_data[4] << 8) + raw_gyro_data[5]) / self.gyro_scale

        accel_scaled_x = twos_compliment((raw_accel_data[0] << 8) + raw_accel_data[1]) / self.accel_scale

        accel_scaled_y = twos_compliment((raw_accel_data[2] << 8) + raw_accel_data[3]) / self.accel_scale

        accel_scaled_z = twos_compliment((raw_accel_data[4] << 8) + raw_accel_data[5]) / self.accel_scale

        return (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z)

    def twos_compliment(val):
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)
'''
bus = smbus.SMBus(0)  # or bus = smbus.SMBus(1) for Revision 2 boards

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(self.address, self.power_mgmt_1, 0)

now = time.time()

K = 0.98

K1 = 1 - K

time_diff = 0.01

(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

gyro_offset_x = gyro_scaled_x

gyro_offset_y = gyro_scaled_y

gyro_total_x = (last_x) - gyro_offset_x

gyro_total_y = (last_y) - gyro_offset_y

print "{0:.4f} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}".format( time.time() - now, (last_x), gyro_total_x, (last_x), (last_y), gyro_total_y, (last_y))

for i in range(0, int(3.0 / time_diff)):
    time.sleep(time_diff - 0.005)

    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

    gyro_scaled_x -= gyro_offset_x

    gyro_scaled_y -= gyro_offset_y

    gyro_x_delta = (gyro_scaled_x * time_diff)

    gyro_y_delta = (gyro_scaled_y * time_diff)

    gyro_total_x += gyro_x_delta

    gyro_total_y += gyro_y_delta

    rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)

    print ("{0:.4f} {1:.2f} {2:.2f} {3:.2f} {4:.2f} {5:.2f} {6:.2f}".format( time.time() - now, (rotation_x), (gyro_total_x), (last_x), (rotation_y), (gyro_total_y), (last_y)))
