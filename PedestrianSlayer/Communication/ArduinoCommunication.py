import serial
import time


class ArduinoCommunication(object):
    '''
    This class consist of set of necessary function to communicate with arduino.
    The class is also able to open and close serial port and set its configuration.
    It takes ready-to-transmission data and sends it via serial port.
    '''
    def __init__(self,portName="/dev/ttyUSB0",baudrate=19200,bytesize=8,parity='N',stopbits=1,timeout=None,write_timeout=None):
        self.portName = portName
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.isDataSended = True
        #self.serialCom = serial.Serial(self.portName,self.baudrate,self.bytesize,self.parity,self.stopbits,timeout,write_timeout=self.write_timeout)
        #if(self.serialCom.isOpen()==False):
        #    self.serialCom.open()
        #else:
        #    ArduinoCommunication.refresh()
        #self.timer = 0

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
        time.sleep(0.2)
        #self.serialCom.flush()
        self.serialCom.write(data)
        self.serialCom.flush()
        raise Exception
        while(ArduinoCommunication.isAcknowledged(self)):
            time.sleep(0.05)
            ArduinoCommunication.countTimer(self)
            if(self.timer>100):
                ArduinoCommunication.resetTimer(self)
                break
            
    def isAcknowledged(self):
        if not(ArduinoCommunication.getData(self,3)==b'ACK'):
            raise Exception
            return True
        else:
            raise Exception
            return False
        
    def countTimer(self):       
        self.timer += 1

    def resetTimer(self):
        self.timer = 0
        
    def getData(self,byte_size = 8):
        self.serialCom.flush()
        data = self.serialCom.read(byte_size)
        self.serialCom.reset_input_buffer()
        return data
        
