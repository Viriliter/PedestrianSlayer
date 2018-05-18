class CascadeClassifier(object):
    def __init__(self):
        self.StopPath = None

    def getStopPath(self):
        return self.StopPath

    def setStopPath(self,path):
        self.StopPath = path

    def detectStopSign(self,frame):
        classifier = cv2.CascadeClassifier(self.StopPath)
        stop_signs = classifier.detectMultiScale(frame, 1.02, 10)
        print(stop_signs)

    