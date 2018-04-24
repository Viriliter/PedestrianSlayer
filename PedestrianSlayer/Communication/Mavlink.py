class Mavlink(object):
    '''
    This class takes required inputs for establishing mavlink protocol.
    And then it converts them into data for ready-to-transmission
    '''
    def __init__(self):
        #Define fields
        self.startField = b"\xFE"
        self.payloadLength = b"\x00"
        self.packetSequence = b"\x00"
        self.CRC = b"\xFF"
        self.PAYLOAD = None
        # systemID
        self._COM_ARDUINO = b"\xFE"
        self._COM_RASPBERRY = b"\xFF"
        self._COM_USER = None
        # componentID
        self._COM_USER_SYSTEM = b"\xFF"
        self._COM_RASPBERRY_MOT = b"\xFE"
        self._COM_RASPBERRY_SERV = b"\xFD"
        self._COM_RASPBERRY_LIGHT = b"\x4C"
        # messageID
        self._COM_RASPBERRY_MOT_STOP = b"\xFF"
        self._COM_RASPBERRY_MOT_FORWARD = b"\xFE"
        self._COM_RASPBERRY_MOT_BACKWARD = b"\xFD"
        self._COM_RASPBERRY_SERV_ANGLE = b"\xFC"
        self._COM_RASPBERRY_SERV_DEFAULT = b"\xFB"

        self._COM_RASPBERRY_LIGHT_SEQ = b"\xFA"
        self._COM_USER_SYSTEM_REBOOST = b"\xEF"

    def CombineFields(self,systemID,componentID,messageID,payload):
        byteArray = [self.startField,self.payloadLength,self.packetSequence,systemID,componentID,messageID,payload,self.CRC]
        raw = b"".join([self.startField,self.payloadLength,self.packetSequence,systemID])
        raw2 = b"".join([componentID,messageID,payload,self.CRC])
        combinedField = b"".join([raw,raw2])      
        return(combinedField)

    def convertToByte(self,componentID,messageID,payload = b"\x00"):
        '''
        It converts fields into HEX form
        '''
        try:
            systemID = self._COM_RASPBERRY
            if(componentID=="_MOTOR"):
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
            
            return Mavlink.CombineFields(self,systemID,componentID,messageID,payload)
        except Exception:
            pass
