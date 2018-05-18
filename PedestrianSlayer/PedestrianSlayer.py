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
        PedestrianSlayer.run(self)
    
    def setModeSelection(self,mode):
        self.modeSelection = mode
    
    def captureModeSelection(self):
        '''
        This function will capture user driving mode preferences.
        Depending on choice, it will set modeSelection either True  or False.
        This method will use UserCommunication class which interprets the input from users
        '''

    def run(self):
        while(True):
            if(self.modeSelection ):
                manuelMode = mm.ManuelMode()
                while (True):
                    isExit = manuelMode.run()
                    if(isExit):
                        PedestrianSlayer.setModeSelection(self,False)
                        break
            elif not(self.modeSelection):
                autoMode = am.AutonomousMode()
                while (True):
                    isExit = autoMode.run()
                    if(isExit):
                        PedestrianSlayer.setModeSelection(self,True)
                        break


