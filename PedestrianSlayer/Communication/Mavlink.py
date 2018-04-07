class Mavlink(object):
    """
    This class takes systemID, componentID, messageID, payload as input
    and converts to single string.
   """
    def __init__(self,systemID,componentID,messageID,payload):
        self.startField = 0xFE
        self.payloadLength = 0x00
        self.packetSequence = 0x00
        self.systemID = systemID
        self.componentID = componentID
        self.messageID = messageID
        self.payload = payload
        self.CRC = 0xFF
        Mavlink.HEXtoString(self)

    def HEXtoString(self):
        return (str(self.startField)
                +str(self.payloadLength)
                +str(self.packetSequence)
                +str(self.systemID)
                +str(self.componentID)
                +str(self.messageID)
                +str(self.payload)
                +str(self.CRC))