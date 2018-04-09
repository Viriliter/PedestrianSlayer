class Mavlink(object):
    """
    This class takes systemID, componentID, messageID, payload as input
    and converts to binary.
   """
    def __init__(self,systemID,componentID,messageID,payload):
        self.startField = b"\FE"
        self.payloadLength = b"\00"
        self.packetSequence = b"\00"
        self.CRC = b"\FF"
        Mavlink.CombineFields(self,systemID,componentID,messageID,payload)

    def CombineFields(self,systemID,componentID,messageID,payload):
        return ((self.startField)
                +(self.payloadLength)
                +(self.packetSequence)
                +(systemID)
                +(componentID)
                +(messageID)
                +(payload)
                +(self.CRC))

class ProtocolLibrary(object):
    '''
    This class takes required inputs for establishing mavlink protocol.
    And then it converts them into data for ready-to-transmission
    '''
    def __init__(self):
        #Define fields
        self.PAYLOAD = None
        # systemID
        self._COM_ARDUINO = b"\FE"
        self._COM_RASPBERRY = b"\FF"
        self._COM_USER = None
        # componentID
        self._COM_USER_SYSTEM = b"\4F"
        self._COM_RASPBERRY_MOT = b"\4D"
        self._COM_RASPBERRY_SERV = b"\53"
        self._COM_RASPBERRY_LIGHT = b"\4C"
        # messageID
        self._COM_RASPBERRY_MOT_STOP = b"\53"
        self._COM_RASPBERRY_MOT_FORWARD = b"\46"
        self._COM_RASPBERRY_MOT_BACKWARD = b"\42"
        self._COM_RASPBERRY_SERV_ANGLE = b"\41"
        self._COM_RASPBERRY_SERV_DEFAULT = b"\44"

        self._COM_RASPBERRY_LIGHT_SEQ = b"\53"
        self._COM_USER_SYSTEM_REBOOST = b"\00"
        

    def convertToByte(self,componentID,messageID,payload = 0):
        '''
        It converts fields into HEX form
        '''
        systemID = self._COM_RASPBERRY
        if(componentID=="_MOT"):
            componentID = self._COM_RASPBERRY_MOT
            if(messageID=="_STOP"):
                messageID = self._COM_RASPBERRY_MOT_STOP
            elif(messageID=="_FORWARD"):
                messageID = self._COM_RASPBERRY_MOT_FORWARD
            elif(messageID=="_BACKWARD"):
                messageID = self._COM_RASPBERRY_MOT_BACKWARD
        elif(componentID=="_SERVO"):
            componentID = self._COM_RASPBERRY_SERV
            if(messageID=="_ANGLE"):
                messageID = self._COM_RASPBERRY_SERV_ANGLE
            elif(messageID=="_DEFAULT"):
                messageID = self._COM_RASPBERRY_SERV_DEFAULT
        elif(componentID=="_LIGHT"):
            componentID = self._COM_RASPBERRY_LIGHT
            messageID = self._COM_RASPBERRY_LIGHT_SEQ

        return Mavlink(systemID,componentID,messageID,str(payload).encode('ascii'))