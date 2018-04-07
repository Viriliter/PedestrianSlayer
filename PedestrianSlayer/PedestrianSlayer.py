from Main import AutonomousMode as am
from Main import ManuelMode as mm

'''
***Algorithm Summary***
Set default driving mode as ManualMode.py
Use UserCommunication.py for initial driving choice(manual/autonomous modes)
    Infinite loop:
        If manual is activated
            Activate ManuelMode.py

        If autonomous is activated
            ActivateAutonomousMode.py
        Wait the interrput input
'''
class PedestrianSlayer(object):
    def __init__(self):
        self.modeSelection = False       #True:Manuel False:Autonomous driving modes
        self.isSelectionChanged= True
        PedestrianSlayer.run(self)

    def setIsSelectionChanged(self,isSelectionChanged):
        self.isSelectionChanged = isSelectionChanged
    
    def changeSelection(self):
        setIsSelectionChanged(self,True)
    
    def captureModeSelection(self):
        '''
        This function will capture user driving mode preferences.
        Depending on choice, it will set modeSelection either True  or False.
        This method will use ArduinoCommunication class which interprets the input from users
        '''

    def run(self):
        while(True):
            if(self.isSelectionChanged):
                if(self.modeSelection ):
                    manuelmode = mm.ManuelMode()
                    manuelmode.run()
                    setIsSelectionChanged(self,False)
                elif not(self.modeSelection):

                    automode = am.AutonomousMode()
                    automode.run()
                    setIsSelectionChanged(self,False)
            '''
            There will be if statement to capture user change.
            And then value of isSlectionChanged is setted to true.
            CaptureModeSelection function will be used at there.
            '''


