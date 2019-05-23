from configuration import Configuration
import pyNetLogo
import pygmo

def eseguiSimulazione(x):
        # path for Netlogo bridge
        netlogo_path='../netlogo-5.3.1-64'
        model_path='../sciadro-3.1/SCD src.nlogo'

        #open dialog with netlogo
        netlogo=pyNetLogo.NetLogoLink(gui='false',
                                    netlogo_home=netlogo_path,
                                    netlogo_version='5')
        netlogo.load_model(model_path)
        #set scenario
        netlogo.command('set selectScenario "dump" ')
        
        #setup
        netlogo.command('setup read-from-string substring date-and-time 9 12')

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
                tick_number=4000
                break
            netlogo.repeat_command('go',1)
            target_found=netlogo.report('percentageTgtsFound')
            tick_number=netlogo.report('ticks')
        
        # debug
        #print(optimized_params)
        print('ticks: ' +str(tick_number) )
        netlogo.kill_workspace()
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

# pygmo class used to define the behaviour of 
# differential_evolution algorithm
class pygmo_de:
    def fitness(self,x):
        tick=eseguiSimulazione(x)
        return [tick]
    def get_bounds(self):
        inf=[]
        sup=[]
        for x in bounds:
            inf.append(x[0])
            sup.append(x[1])
        tup=(inf,sup)
        return tup
'''
def evolve_func(algo, pop):
    new_pop=algo.evolve(pop)
    return algo, new_pop

class my_island():

    def __init__(self):
        pygmo.mp_island.init_pool()
    
    def run_evolve(self,algo,pop):
        with pygmo.mp_island._pool_lock:
            res=pygmo.mp_island._pool.apply_async(evolve_func, (algo, pop))
            return res.get()
'''

if __name__ == '__main__':

    parameters_config=Configuration()

    #create array of only parameters boundaries
    bounds=parameters_config.createBoundsList()

    #modifyModel('../sciadro-3.1')

    print('starting optimization...\n')

    #define problem
    prob=pygmo.problem(pygmo_de())
    #define algoritm to use
    algo=pygmo.algorithm(pygmo.de(gen=1,ftol=0.1,xtol=0.1))
    # logging every one generation
    algo.set_verbosity(1)
    #print(algo)
    # population size
    pop=pygmo.population(prob,size=6,seed=32)
    #is1=pygmo.island(algo=algo, pop=pop, udi=my_island())
    #print(is1)
    #is1.evolve()
    archi=pygmo.archipelago(n=2,algo=algo,pop=pop,udi=pygmo.mp_island())
    #start optimization
    #pop=algo.evolve(pop)
    archi.evolve()
    print(archi)
    archi.wait()
    res = [isl.get_population().champion_x for isl in archi]
    print(res)

