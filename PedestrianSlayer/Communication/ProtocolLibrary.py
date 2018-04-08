import Mavlink as ml

class ProtocolLibrary(object):
    '''
    This class takes required inputs for establishing mavlink protocol.
    And then it converts them into data for ready-to-transmission
    '''
    def __init__(self):
        self.PAYLOAD = None
        self._COM_ARDUINO = 0xFE
        self._COM_RASPBERRY = 0xFF
        self._COM_RASPBERRY_MOT = 0x4D4F54
        self._COM_RASPBERRY_MOT_STOP = 0x535450
        self._COM_RASPBERRY_MOT_FORWARD = 0x465744
        self._COM_RASPBERRY_MOT_BACKWARD = 0x425744
        self._COM_RASPBERRY_SERV = 0x534552
        self._COM_RASPBERRY_SERV_ANGLE = 0x425744
        self._COM_RASPBERRY_LIGHT = 0x4C4854
        self._COM_RASPBERRY_LIGHT_SEQ = 0x534551
        

    def convertToHEX(self,componentID,messageID,payload):
        systemID = self._COM_RASPBERRY
        if(componentID==_MOT):
            componentID= self._COM_RASPBERRY_MOT
            if(messageID==_STOP):
                messageID = self._COM_RASPBERRY_MOT_STOP
            elif(messageID==_FORWARD):
                messageID = self._COM_RASPBERRY_MOT_FORWARD
            elif(messageID==_BACKWARD):
                messageID = self._COM_RASPBERRY_MOT_BACKWARD
        elif(componentID==_SERVO):
            componentID = self._COM_RASPBERRY_SERV
            messageID= self._COM_RASPBERRY_SERV_ANGLE
        elif(componentID==_LIGHT):
            componentID = self._COM_RASPBERRY_LIGHT
            messageID = self._COM_RASPBERRY_LIGHT_SEQ
        return ml.HEXtoString(systemID,componentID,messageID,hex(payload))

    def convertToData(self,systemID,componentID,messageID,payload):
        ProtocolLibrary.convertToHEX(self,systemID,componentID,messageID,payload)
        return ml.Mavlink(systemID,componentID,messageID,payload)

