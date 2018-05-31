import numpy as np

class NeuralNetwork():
    '''
    This neural network is designed for Pedestrian Car Project.
    It constructs an input layer that gets 4 road and car parameters.
    Using neural network algorithm, it gives optimum steering angle of the car.
    To use this class:
        -Firstly, using trainingIn() and trainingOut() functions, set the input
         and output training values.
        -Then, run train() function to estimate each synaptic weight.
        -Finally, using getSteeringAngle() function get optimum steering
         angle for car based on training input and outputs.
    It is possible to adjust the normalized input values using threshold functions.
    '''
    def __init__(self):
        self.training_inputs = np.array([0,0,0,0])
        self.training_inputs = np.array([0]).T
        setRadiusThreshold(self,0.100)
        setDeviationThreshold(self,0.100)
        setSpeedThreshold(self,0.100)
        setOrientThreshold(self,0.100)
        self.synaptic_weights = None
        
    def setRadiusThreshold(self,radiusB,radiusU):  
        self.radiusThreshB = radiusB
        self.radiusThreshU = radiusU

    def setDeviationThreshold(self,deviationB,deviationU):
        self.deviatThreshB = deviationB
        self.deviatThreshU = deviationU

    def setSpeedThreshold(self,speedB,speedU):
        self.speedThreshB = speedB
        self.speedThreshU = speedU

    def setOrientThreshold(self,orientB,orientU):  
        self.orientThreshB = orientB
        self.orientThreshU = orientU

        
    def normalizeParameter(self,radius,deviation,speed,orient):
        '''
        Normalize input parameters
        '''
        if(radiusThreshB<radius<self.radiusThreshU):
            nor_rad = radius*0.01
        else:
            nor_rad = 1
            
        if(self.deviatThreshB<deviation<self.deviatThreshU):
            nor_dev = deviation*0.01
        else:
            nor_dev = 1
            
        if(self.speedThreshB<speed<self.speedThreshU):
            nor_speed = speed*0.01
        else:
            nor_speed = 1
            
        if(self.orientThreshB<orient<self.orientThreshU):
            nor_orient = orient*0.01
        else:
            nor_orient = 1
        return np.array([nor_rad,nor_dev,nor_speed,nor_orient])

    def normalizeOutput(self,output):
        '''
        Normalize output parameter
        '''
        nor_output = output/90
        return nor_output

    def revertOutput(self,normal_out):
        '''
        Convert the normalized output to angle
        '''
        return normal_out*90
    
    def trainingIn(self,radius,deviation,speed,orient):
        '''
        Joints new training input to existing one
        '''
        self.training_inputs = np.array([self.training_inputs,normalizeParameter(radius,deviation,speed,orient)])

    def trainingOut(self,angle):
        '''
        Joints new training output to existing one
        '''
        self.training_outputs = np.array(self.training_outputs,[normalizeOutput(self,angle)]).T
        
    def train(self):
        '''
        Calculates synaptic weights of each neuron
        '''
        np.random.seed(1)
        self.synaptic_weights = 2*random.random((3,1))-1
        for iteration in range(10000):
            output = 1/(1+exp(-np.dot(self.training_inputs,self.synaptic_weights)))
            self.synaptic_weights += np.dot(self.training_inputs.T,(self.training_outputs-output)*output*(1-output))

    def getSteeringAngle(self,radius,deviation,speed,orient):
        '''
        Uses sigmoid function to compute desired steering angle
        Returns the angle
        '''
        nor_param = normalizeParameter(self,radius,deviation,speed,orient)
        normal_out=(1/(1+np.exp(-np.dot(nor_param,self.synaptic_weights))))
        return revertOutput(normal_out)
