from configuration import Configuration
from scipy.optimize import differential_evolution
import pyNetLogo
import multiprocessing
import sys

netlogo=None
# path for Netlogo bridge
netlogo_path='../netlogo-5.3.1-64'
model_path='../sciadro-3.1/SCD src.nlogo'
def init_worker():
    global netlogo,netlogo_path,model_path

    #open dialog with netlogo
    netlogo=pyNetLogo.NetLogoLink(gui='false',
                                netlogo_home=netlogo_path,
                                netlogo_version='5')
    netlogo.load_model(model_path)
    #set scenario
    netlogo.command('set selectScenario "dump" ')

def eseguiSimulazione(x):
        #setup
        global netlogo,parameters_config,netlogo_path,model_path
        if netlogo is None:
            #open dialog with netlogo
            netlogo=pyNetLogo.NetLogoLink(gui='false',
                                netlogo_home=netlogo_path,
                                netlogo_version='5')
            netlogo.load_model(model_path)
            #set scenario
            netlogo.command('set selectScenario "dump" ')
        
        cmd="setup read-from-string substring date-and-time 9 12"
        netlogo.command(cmd)

        #set parameters
        count=0
        # used for visual debug
        #optimized_params={}
        for key,value in parameters_config.paramBoundaries.items():
            cmd="set " + key + " " + str(x[count])
            netlogo.command(cmd)
            #used for debug
            #optimized_params[key]=x[count]

            count += 1

        
        #initial target found
        target_found=netlogo.report('percentageTgtsFound')
        tick_number=0
        #continue simulation until stop condition 
        while (target_found<=95):
            if(tick_number > 1000):
                tick_number=1000
                break
            netlogo.repeat_command("go",1)
            target_found=netlogo.report('percentageTgtsFound')
            tick_number=netlogo.report('ticks')
        
        # debug
        #print(optimized_params)
        print('ticks: ' +str(tick_number) )
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

     
if __name__ == '__main__':
    
    # parameter configuration initialize
    parameters_config=Configuration()
    #create array of only parameters boundaries
    bounds=parameters_config.createBoundsList()
    #modifyModel('../sciadro-3.1')

    pool=multiprocessing.Pool(processes=1,initializer=init_worker,initargs=())
    print('starting optimization...\n')
    try:    
        result=differential_evolution(eseguiSimulazione,
                                bounds,
                                disp=True,
                                init='latinhypercube',
                                polish=False,
                                atol=0,
                                tol=0.1,
                                maxiter=200,
                                popsize=4,
                                updating='deferred',
                                workers=pool.map)    
    except KeyboardInterrupt:
        print('closing pool...')
        pool.close()
        pool.join()
        sys.exit()

    print('Valori parametri ottimi:\n')
    print(result.x)
    # refresh configuration class with optimized parameters
    parameters_config.refreshConfiguration(result.x)
    # save new configuration to file as JSON
    parameters_config.save_toFile()
    #close open pool
    pool.close()
    pool.join()
    
    
