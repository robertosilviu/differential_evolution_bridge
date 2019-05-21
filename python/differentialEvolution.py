from configuration import Configuration
from scipy.optimize import differential_evolution
import pyNetLogo

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
        print('\n')
        print(optimized_params)
        print('\ntarget found: ' + str(target_found)
            + '\nticks: ' +str(tick_number) + '\n' )
        #netlogo.kill_workspace()
        return tick_number

# verify if Netlogo model uses parameters
# from configuration.txt or the ones specified in python
def modifyModel(model_home_home_path):
    print('verifying Netlogo model configuration...')
    filename=model_home_home_path+'/include/setup_procedures.nls'
    with open(filename) as f_obj:
        content=f_obj.read()
    f_obj.close()

    if ';import_configuration' not in content:
        content=content.replace('import_configuration',';import_configuration')
        with open(filename,'w') as f_obj:
            f_obj.write(content)
            f_obj.close()
        print(' -> reading of model parameters from configuration.txt disabled')
    else:
        print(' -> model ready to use')
    content=None

# differential evolution algorithm
def scipy_DE(bounds_list):
    result=differential_evolution(eseguiSimulazione,
                                bounds_list,
                                disp=True,
                                init='latinhypercube',
                                tol=0.01,
                                polish=True,
                                workers=2)
    return result.x                     
if __name__ == '__main__':
    # path for Netlogo bridge
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
    bounds=parameters_config.createBoundsList()

    modifyModel('../sciadro-3.1')

    print('starting optimization...\n')

    scipy_DE(bounds)
