import json

class Configuration():
    # class to organize Netlogo simulation parameters
    def __init__(self):
    # costants
        self.constants={
            'strategy?' : 3,
            'drone.radius': 0.2,
            'drone.speedMax': 8.5,
            'drone.cruisingSpeed': 2,
            'drone.acceleration': 2,
            'drone.deceleration': -2,
            'drone.velocityAngularMax': 2.6,
            'drone.accelerationAng': 7,
            'drone.decelerationAng': -7,
            'drone.endurance': 24,
            'sensing.radius': 2.5,
            'sensing.angle': 360,
            'rectangleBase': 5,     #sensingBase
            'rectangleHeight': 4,     #sensingHeight
            'drone.reachable.radius': 4,
            'drone.reachable.angle': 360,
            'drone.collision.vision': 6,
            'drone.sight.angleMax': 60,
            'drone.collision.gapAngle': 20
        }
    #configuration parameters
        self.parameters={
            'strategy?' : 3,
            'drone.radius': 0.2,
            'drone.speedMax': 8.5,
            'drone.cruisingSpeed': 2,
            'drone.acceleration': 2,
            'drone.deceleration': -2,
            'drone.velocityAngularMax': 2.6,
            'drone.accelerationAng': 7,
            'drone.decelerationAng': -7,
            'drone.endurance': 24,
            'sensing.radius': 2.5,
            'sensing.angle': 360,
            'rectangleBase': 5,     #sensingBase
            'rectangleHeight': 4,     #sensingHeight
            'drone.reachable.radius': 4,
            'drone.reachable.angle': 360,
            'drone.collision.vision': 6,
            'drone.sight.angleMax': 60,
            'drone.collision.gapAngle': 20,
            'mark.radiusTop': 8,
            'mark.radiusDown': 18,
            'track.evapRate': 0.16,
            'olfactoryHabituation': 22,
            'drone.flocking.angle': 42,
            'drone.flocking.wiggleVar': 14,
            'drone.flocking.radiusSeparate': 15,
            'drone.flocking.maxSeparateTurn': 33,
            'drone.flocking.radiusAlign': 19,
            'drone.flocking.maxAlignTurn': 33,
            'drone.flocking.radiusCohere': 21,
            'drone.flocking.maxCohereTurn': 24
        }
    
    #boundaries of parameters
        self.paramBoundaries={
            
            'mark.radiusTop': (1,13),
            'mark.radiusDown': (13,19),
            'track.evapRate': (0.01,0.2),
            'olfactoryHabituation': (1,100),
            'drone.flocking.angle': (15,45),
            'drone.flocking.wiggleVar': (5,15),
            'drone.flocking.radiusSeparate': (6,16),
            'drone.flocking.maxSeparateTurn': (30,45),
            'drone.flocking.radiusAlign': (16,22),
            'drone.flocking.maxAlignTurn': (30,45),
            'drone.flocking.radiusCohere': (18,26),
            'drone.flocking.maxCohereTurn': (15,30)
        }
    # print parameters and boundaries     
    def showParameters(self):
        for key,value in self.parameters.items():
            if key in self.paramBoundaries:
                bounds=self.paramBoundaries[key]
                print( key,' =',value,' | bounds= ',bounds)
            else:
                print( key,' =',value,' | bounds= const value')

    # create list for differential_evolution algorythm
    def createBoundsList(self):
        bounds=[]
        for key,value in self.paramBoundaries.items():
            bounds.append(value)
        return bounds

    # name passed as 'name'
    def addParameter(self,name,value,min_bounder,max_bounder):
        self.parameters[name]=value
        self.paramBoundaries[name]=(min_bounder,max_bounder)
    
    #remove parameter
    def removeParameter(self,name):
        del self.parameters[name]
        del self.paramBoundaries[name]
        print('removed ' + ' ' 
            + name 
            + ' : ' + str(self.parameters[name]) 
            + ', bounds = ' + str(self.paramBoundaries[name])
         )
    
    # set parameters value from a specified array
    # the order of values in the array must
    # be the same of Configuration.parameters
    def refreshConfiguration(self,x):
        count=0
        for key,value in self.paramBoundaries.items():
            self.parameters[key]=x[count]
            count+=1
        for key,value in self.constants.items():
            self.parameters[key]=self.constants[key]
        print('saved new configuration!')
    
    # save parameters to JSON file
    def save_toFile(self):
        filename='optimized_parameters.json'
        with open(filename,'w') as f_obj:
            json.dump(self.parameters,f_obj)
            print('saved optimized parameters to file!')

    # load parameters from JSON file
    def loadParameters_fromFile(self):
        filename='optimized_parameters.json'
        try:
            with open(filename) as f_obj:
                self.parameters=json.load(f_obj)
        except FileNotFoundError:
            print('file not found!')
        else:
            print('loaded parameters from file!')
        
    
