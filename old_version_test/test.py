import numpy as np 
import pyNetLogo
import pandas as pd 
from scipy.optimize import differential_evolution

#parameters boundaries
bounds=[(0,1),(50,99)]

#parameters list
param=[1,1]

#function called during optimization
def esegui_simulazione(par):
    # must adapt netlogo_home to the right path
    netlogo=pyNetLogo.NetLogoLink(gui='false',
                        netlogo_home='/home/roberto/netlogo-5.3.1-64',
                        netlogo_version='5')
    # must adapt load_model to the right experiment path                    
    netlogo.load_model('/home/roberto/netlogo-5.3.1-64/app/models/Sample Models/Biology/Ants.nlogo')
    
    #param0=diffusion-rate
    #param1=evaporation-rate

    #set param0
    param0="set diffusion-rate " + str(par[0])
    netlogo.command(param0)
    #set param1
    param1="set evaporation-rate "+ str(par[1])
    netlogo.command(param1)
    #setup
    netlogo.command('setup')
    #initial food value
    food_pile1=netlogo.report('sum [food] of patches with [pcolor = cyan]')
    food_pile2=netlogo.report('sum [food] of patches with [pcolor = sky]')
    food_pile3=netlogo.report('sum [food] of patches with [pcolor = blue]')
    
    while (food_pile1+food_pile2+food_pile3) != 0:
        netlogo.repeat_command('go',1)
        food_pile1=netlogo.report('sum [food] of patches with [pcolor = cyan]')
        food_pile2=netlogo.report('sum [food] of patches with [pcolor = sky]')
        food_pile3=netlogo.report('sum [food] of patches with [pcolor = blue]')
        tick_number=netlogo.report('ticks')
    
    print('\nevaporation-rate:' + str(par[1])
        + '\ndiffusion-rate: ' + str(par[0]) 
        + '\nticks: ' +str(tick_number) )
    netlogo.kill_workspace()
    return tick_number

# differential evolution algorithm 
result=differential_evolution(esegui_simulazione,
                            bounds,
                            popsize=1,
                            mutation=(0.5,1),
                            recombination=0.8,
                            disp=True,
                            workers=3,
                            maxiter=10)
result.x, result.fun