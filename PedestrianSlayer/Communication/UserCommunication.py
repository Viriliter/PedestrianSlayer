import serial
import time

#Declare global variables
global _STARTFIELD
global _PAYLOADLENGTH
global _PACKETSEQUENCE
global _SYSTEMID
global _COMPONENTID
global _MESSAGEID
global _PAYLOAD
global _CRC

#Error Classifiers
class InvalidStartField(Exception):
    pass

class InvalidPayloadLength(Exception):
    pass

class InvalidPacketSequence(Exception):
    pass

class UserCommunication(object):
    """description of class"""
    def __init__(self,portName="/dev/ttyUSB1",baudrate=9600,bytesize=8,parity='N',stopbits=1,timeout=None,write_timeout=None):
        self.portName = portName
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        #self.serialCom = serial.Serial(self.portName,self.baudrate,self.bytesize,self.parity,self.stopbits,timeout,write_timeout=self.write_timeout)
    
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
    def read(self):
        return 

    def getData(self):
        return self.serialCom.read(8)

    def castData(self):
        try:
            byteData = UserCommunication.getData(self)
            stringData = byteData.decode("utf-8") 
            if(byteData == None):
                pass
            _STARTFIELD = byteData[:7]
            if(_STARTFIELD == b"FE"):
                raise InvalidStartField("")
            _PAYLOADLENGTH = byteData[8:15]
            if(_STARTFIELD == b"FE"):
                raise InvalidPayloadLength("")
            _PACKETSEQUENCE = byteData[16:23]
            if(_STARTFIELD == b"FE"):
                raise InvalidPacketSequence("")
            _SYSTEMID = byteData[24:31]
            _COMPONENTID = byteData[32:39]
            _MESSAGEID = byteData[40:47]
            _PAYLOAD = stringData[48:55]
            _CRC = byteData[56:63]
            return True
        except (e):
            if (e == InvalidStartField):
                UserCommunication.castData(self)
            else:
                return False

    def decoder(self):
        if(_SYSTEMID== b"55"):
            if(_COMPONENTID==b"4F"):            #SYSTEM
                if(_MESSAGEID==b"00"):              #REBOOT
                    from System import Shutdown
                    Shutdown.Shutdown()
                elif(_MESSAGEID==b""):              #SHUTDOWN
                    from System import Reboot
                    Reboot.Reboot()

            elif(_COMPONENTID==b"4D"):          #MOTOR
                if(_MESSAGEID==b"53"):              #STOP
                    #
                    pass
                elif(_MESSAGEID==b"46"):            #FORWARD
                    #
                    pass
                elif(_MESSAGEID==b"42"):            #BACKWARD
                    #
                    pass
            elif(_COMPONENTID==b"53"):          #SERVO
                if(_MESSAGEID==b"41"):              #ANGLE
                    pass


    