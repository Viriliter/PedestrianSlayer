import serial
import time
import Mavlink as ml
class ArduinoCommunication(object):
    '''
    This class consist of set of necessary function to communicate with arduino.
    The class is also able to open and close serial port and set its configuration.
    It takes ready-to-transmission data and sends it via serial port.
    '''
    def __init__(self,portName="/dev/ttyUSB0",baudrate=9600,bytesize=EIGHTBITS,parity=PARITY_NONE,stopbits=STOPBITS_ONE,timeout=None,write_timeout=None):
        self.portName = portName
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.serialCom = serial.Serial(self.portName,self.baudrate,self.bytesize,self.parity,self.stopbits,timeout,write_timeout=self.write_timeout)

    #Mutators
    #region
    def refresh(self):
        self.serialCom.close()
        self.serialCom = serial.Serial(self.portName,self.baudrate,self.bytesize,self.parity,self.stopbits,timeout,write_timeout=self.write_timeout)
    
    def setPortName(self,portName):
        self.portName = portName

    def setBaudrate(self,baudrate):
        self.baudrate = baudrate

    def setByteSize(self,bytesize):
        self.bytesize = bytesize

    def setParity(self,parity):
        self.parity = parity

    def setStopBits(self,stopbits):
        self.stopbits = stopbits

    def setTimeout(self,timeout):
        self.timeout = timeout

    def setWTimeout(self,write_timeout):
        self.write_timeout = write_timeout
    
    #endregion

    #Accessors
    #region

    def setPortName(self,portName):
        return self.portName

    def setBaudrate(self,baudrate):
        return self.baudrate

    def setByteSize(self,bytesize):
        return self.bytesize

    def setParity(self,parity):
        return self.parity

    def setStopBits(self,stopbits):
        return self.stopbits

    def setTimeout(self,timeout):
        return self.timeout

    def setWTimeout(self,write_timeout):
        return self.write_timeout

    #endregion
    #Methods

    def sendData(self,data):
        self.serialCom.write(data)
