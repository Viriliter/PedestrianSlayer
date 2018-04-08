class Mavlink(object):
    """
    This class takes systemID, componentID, messageID, payload as input
    and converts to single string.
   """
    def __init__(self,systemID,componentID,messageID,payload):
        self.startField = 0xFE
        self.payloadLength = 0x00
        self.packetSequence = 0x00
        self.CRC = 0xFF
        Mavlink.HEXtoString(self,systemID,componentID,messageID,payload)

    def HEXtoString(self,systemID,componentID,messageID,payload):
        return (str(self.startField)
                +str(self.payloadLength)
                +str(self.packetSequence)
                +str(systemID)
                +str(componentID)
                +str(messageID)
                +str(payload)
                +str(self.CRC))