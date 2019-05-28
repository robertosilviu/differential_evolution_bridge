from configuration import Configuration
import pyNetLogo
import pygmo
import gc

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

# pygmo class used to define the behaviour of 
# differential_evolution algorithm
class pygmo_de:
    def __init__(self):
        self.parameters_config=Configuration()
        #create array of only parameters boundaries
        self.bounds=self.parameters_config.createBoundsList()

    def fitness(self,x):
        tick=self.eseguiSimulazione(x)
        return [tick]
    def get_bounds(self):
        inf=[]
        sup=[]
        for x in self.bounds:
            inf.append(x[0])
            sup.append(x[1])
        tup=(inf,sup)
        return tup

    def eseguiSimulazione(self,x):

        # path for Netlogo bridge
        netlogo_path='../netlogo-5.3.1-64'
        model_path='../sciadro-3.1/SCD src.nlogo'
        
        # open dialog with netlogo
        netlogo=pyNetLogo.NetLogoLink(gui='false',
                                    netlogo_home=netlogo_path,
                                    netlogo_version='5')
        # load Netlogo model
        netlogo.load_model(model_path)
        
        # set scenario
        netlogo.command('set selectScenario "dump" ')
        
        # setup
        netlogo.command('setup read-from-string substring date-and-time 9 12')

        #set parameters
        count=0
        # used for visual debug
        #optimized_params={}
        for key,value in self.parameters_config.paramBoundaries.items():
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
                tick_number=4000
                break
            netlogo.repeat_command('go',1)
            target_found=netlogo.report('percentageTgtsFound')
            tick_number=netlogo.report('ticks')
        
        # debug
        #print(optimized_params)
        print('ticks: ' +str(tick_number) )
        
        # close netlogo connection
        netlogo.kill_workspace()
        gc.collect()
        return tick_number

if __name__ == '__main__':

    

    #modifyModel('../sciadro-3.1')

    print('starting optimization...\n')
    
    # define problem
    prob=pygmo.problem(pygmo_de())
    
    # define algoritm to use
    algo=pygmo.algorithm(pygmo.de(gen=2,ftol=0.1,xtol=0.1))
    
    # logging every one generation
    algo.set_verbosity(1)
    print(algo)
    
    # population size
    pop=pygmo.population(prob,size=12,seed=32)

    # archipelago for parallel optimization
    # n= number of CPU to use
    archi=pygmo.archipelago(n=2,algo=algo,pop=pop,udi=pygmo.mp_island())
    
    #start optimization
    archi.evolve()
    print(archi)
    
    # wait until all islands finish evolution
    archi.wait()
    
    print('optimized parameters of all islands\n')
    res = [isl.get_population().champion_x for isl in archi]
    print(res)

    print('best simulation result found on each island')
    res = [isl.get_population().champion_f for isl in archi]
    print(res)

