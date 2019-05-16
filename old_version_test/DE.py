import numpy as np 
import pyNetLogo
import pandas as pd 
from scipy.optimize import differential_evolution

#parameters boundaries
bounds=[(0,99),(0,99)]

#parameters list

# 0=droneRadius
# 1=speedMax
# 2=cruisingSpeed
# 3=acceleration
# 4=deceleration
# 5=angularVelMax
# 6=angularAcc
# 7=angularDec
# 8=endurance
# 9=sensingRadius
# 10=sensingAngle
# 11=sensingHeight
# 12=reachableRadius
# 13=reachableAngle
# 14=collisionVision
# 15=sightAngleMax
# 16=gapAngle
# 17=radiusTop
# 18=radiusDown
# 19=evapRate
# 20=olfaction
# 21=flockAngle
# 22=wiggleVar
# 23=radiusSeparate
# 24=maxSeparateTurn
# 25=radiusAlign
# 26=maxAlignTurn
# 27=radiusCohere
# 28=maxCohereTurn

parameters={
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
#function called during optimization
def esegui_simulazione(): #add x when running evolution
    # must adapt netlogo_home to the right path
    netlogo=pyNetLogo.NetLogoLink(gui='true',
                        netlogo_home='/home/roberto/netlogo-5.3.1-64',
                        netlogo_version='5')
    # must adapt load_model to the right experiment path                    
    netlogo.load_model('/home/roberto/drones-swarm-master/sciadro-3.1/SCD src.nlogo')

    #set parameters
    for key,value in parameters.items():
        cmd="set " + key + " " + str(value)
        netlogo.command(cmd)
    
    #set scenario
    netlogo.command('set selectScenario "dump" ')
    #setup
    netlogo.command('setup read-from-string substring date-and-time 9 12')
    #initial target found
    target_found=netlogo.report('percentageTgtsFound')

    while (target_found<=95):
        netlogo.repeat_command('go',1)
        target_found=netlogo.report('percentageTgtsFound')
        tick_number=netlogo.report('ticks')
    
    print('\ntarget found: ' + str(target_found)
        + '\nticks: ' +str(tick_number) )
    #netlogo.kill_workspace()
    return tick_number

esegui_simulazione()

# differential evolution algorithm 
'''
result=differential_evolution(esegui_simulazione,
                            bounds,
                            popsize=1,
                            mutation=(0.5,1),
                            recombination=0.8,
                            disp=True,
                            workers=3,
                            maxiter=10)
result.x, result.fun
'''
