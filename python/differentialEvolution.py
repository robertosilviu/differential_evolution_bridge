from configuration import Configuration
from netlogoDialog import NetlogoDialog
from scipy.optimize import differential_evolution
import pyNetLogo

netlogo_path='../netlogo-5.3.1-64'
model_path='../sciadro-3.1/SCD src.nlogo'

# parameter configuration initialize
parameters_config=Configuration()

#open dialog with netlogo
netlogo=pyNetLogo.NetLogoLink(gui='false',
                            netlogo_home=netlogo_path,
                            netlogo_version='5')
netlogo.load_model(model_path)
#create array of only parameters boundaries
parameters_config.createBoundsList()

#pass configuration parameters to netlogo class for dialog
#netlogo.passConfigurationParams(parameters_config.paramBoundaries)

def eseguiSimulazione(x):
        #set scenario
        netlogo.command('set selectScenario "dump" ')
        
        #setup
        netlogo.command('setup read-from-string substring date-and-time 9 12')

        #set parameters
        count=0
        # used for visual debug
        optimized_params={}
        for key,value in parameters_config.parameters.items():
            cmd="set " + key + " " + str(x[count])
            netlogo.command(cmd)
            #used for debug
            optimized_params[key]=x[count]
            count += 1

        
        #initial target found
        target_found=netlogo.report('percentageTgtsFound')

        #continue simulation until stop condition 
        while (target_found<=95):
            netlogo.repeat_command('go',1)
            target_found=netlogo.report('percentageTgtsFound')
            tick_number=netlogo.report('ticks')
        
        # debug
        print(optimized_params)
        print('\ntarget found: ' + str(target_found)
            + '\nticks: ' +str(tick_number) )
        #netlogo.kill_workspace()
        return tick_number

# differential evolution algorithm
# get array of bounds
bounds=parameters_config.bounds
print('starting optimization')
result=differential_evolution(eseguiSimulazione,
                            bounds,
                            disp=True,
                            init='latinhypercube',
                            tol=0.01,
                            polish=True,
                            workers=1)
result.x
