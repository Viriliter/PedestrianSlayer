import serial
import time
from MechanicalControl import MotorControl as mc
from MechanicalControl import ServoControl as sc

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
    """This class gets inputs from user over the serial port.
        Then it performs the task comes from the user."""
    def __init__(self,portName="/dev/ttyUSB1",baudrate=9600,bytesize=8,parity='N',stopbits=1,timeout=None,write_timeout=None):
        self.portName = portName
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.write_timeout = write_timeout
        #self.serialCom = serial.Serial(self.portName,self.baudrate,self.bytesize,self.parity,self.stopbits,timeout,write_timeout=self.write_timeout)
        self.motorControl = mc.MotorControl()
        self.servoControl = sc.ServoControl()

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
    def closePort(self):
        self.serialCom.close()
        
    def activate(self):
        #Get data over serial port
        data = UserCommunication.getData(self)
        #Sort data to its field bytes
        UserCommunication.castData(self,data)
        #Perform the command
        UserCommunication.decoder
        #Reset last values
        _STARTFIELD = None
        _PAYLOADLENGTH = None
        _PACKETSEQUENCE = None
        _SYSTEMID = None
        _COMPONENTID = None
        _MESSAGEID = None
        _PAYLOAD = None
        _CRC = None

        
    def getData(self):
        #define reader buffer
        bytes buffer[] = {0,0,0,0,0,0,0,0}
        #clear old values from serial
        self.serialCom.flushInput()
        #read the data from port up to 8 bytes
        data = self.serialCom.read(8)
        self.serialCom.inWaiting()
        return data

    def castData(self,byteData[]):
        try:
            if(byteData == None):
                pass
            _STARTFIELD = byteData[0]
            if not(_STARTFIELD == b"\xFE"):
                raise InvalidStartField("")
            _PAYLOADLENGTH = byteData[1]
            if not(_PAYLOADLENGTH == b"\x00"):
                raise InvalidPayloadLength("")
            _PACKETSEQUENCE = byteData[2]
            if not(_PACKETSEQUENCE == b"\x00"):
                raise InvalidPacketSequence("")
            _SYSTEMID = byteData[3]
            _COMPONENTID = byteData[4]
            _MESSAGEID = byteData[5]
            _PAYLOAD = byteData[6]
            _CRC = byteData[7]
            return True
        except (e):
            return False

    def decoder(self):
        if(_SYSTEMID== b"\FD"):                     
            if(_COMPONENTID==b"\xFF"):          #SYSTEM
                if(_MESSAGEID==b"\x00"):            #SHUTDOWN
                    from System import Shutdown
                    address = "SYSTEM_SHUTDOWN"
                    Shutdown.Shutdown()
                    return address
                elif(_MESSAGEID==b""):              #REBOOT
                    from System import Reboot
                    address = "SYSTEM_REBOOT"
                    Reboot.Reboot()
                    return address
            elif(_COMPONENTID==b"\xFE"):        #MOTOR
                if(_MESSAGEID==b"\xFF"):            #STOP
                    address = "MOTOR_STOP"
                    value = int(_PAYLOAD)
                    self.motorControl.stopMotor()
                    return address 
                elif(_MESSAGEID==b"\xFE"):          #FORWARD
                    address = "MOTOR_FORWARD"
                    value = int(_PAYLOAD)
                    self.motorControl.forwardMotor()
                    return address 
                elif(_MESSAGEID==b"\xFD"):          #BACKWARD
                    address = "MOTOR_BACKWARD"
                    value = int(_PAYLOAD)
                    self.motorControl.backwardMotor()
                    return address 
            elif(_COMPONENTID==b"\xFD"):        #SERVO
                if(_MESSAGEID==b"\xFF"):            #ANGLE
                    address = "SERVO_ANGLE"
                    value = int(_PAYLOAD)
                    self.servoControl.angle()
                    return address 
                elif(_MESSAGEID==b"\xFE"):          #DEFAULT
                    address = "SERVO_DEFAULT"
                    value = int(_PAYLOAD)
                    self.servoControl.default()
                    return address
            elif(_COMPONENTID=="xFC")              #SWITCH MODE
                if(_MESSAGEID==b"\xFF"):            #MANUEL
                    address = "MODE_MANUEL"
                    value = int(_PAYLOAD)
                    self.servoControl.angle()
                    return address
                elif(_MESSAGEID==b"\xFE"):          #AUTONOMOUS
                    address = "MODE_AUTO"
                    value = int(_PAYLOAD)
                    self.servoControl.angle()
                    return address
            elif(_COMPONENTID=="")              #LIGHT
                if(_MESSAGEID==b"\xFA"):            #SEQUENCE
                    address = "MODE_MANUEL"
                    value = int(_PAYLOAD)
                    self.servoControl.angle()
                    return address
                elif(_MESSAGEID==b"\xFE"):          #SE
                    address = "MODE_AUTO"
                    value = int(_PAYLOAD)
                    self.servoControl.angle()
                    return address 
        address = None
        value = 0

    
