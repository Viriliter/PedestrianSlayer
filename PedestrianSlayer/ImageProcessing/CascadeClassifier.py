import cv2

class CascadeClassifier(object):
    def __init__(self):
        self.StopPath = '/HaarCascade/StopSign_HAAR.xml'

    def getStopPath(self):
        return self.StopPath

    def setStopPath(self,path):
        self.StopPath = path

    def detectStopSign(self,frame):
        classifier = cv2.CascadeClassifier(self.StopPath)
        stop_signs = classifier.detectMultiScale(
                    frame,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(100,100)
                    )
        print(stop_signs)

    
