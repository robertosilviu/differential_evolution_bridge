from configuration import Configuration
import pyNetLogo
import pygmo

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
        #netlogo.kill_workspace()
        del netlogo
        return tick_number

def evolve_func(algo, pop):
    new_pop=algo.evolve(pop)
    return algo, new_pop

class my_island():

    def __init__(self):
        pygmo.mp_island.init_pool(n=1)

        # path for Netlogo bridge
        self.netlogo_path='../netlogo-5.3.1-64'
        self.model_path='../sciadro-3.1/SCD src.nlogo'

        #open dialog with netlogo
        self.netlogo=pyNetLogo.NetLogoLink(gui='false',
                                    netlogo_home=self.netlogo_path,
                                    netlogo_version='5')
        self.netlogo.load_model(self.model_path)
        #set scenario
        self.netlogo.command('set selectScenario "dump" ')

    def run_evolve(self,algo,pop):
        with pygmo.mp_island._pool_lock:
            res=pygmo.mp_island._pool.apply_async(evolve_func, (algo, pop))
            return res.get()



if __name__ == '__main__':

    

    #modifyModel('../sciadro-3.1')

    print('starting optimization...\n')
    # numero generazioni totali
    generazioni=200
    
    #define problem
    prob=pygmo.problem(pygmo_de())
    
    #define algoritm to use
    algo=pygmo.algorithm(pygmo.de(gen=1,ftol=0.1,xtol=0.1))
    # logging every one generation
    algo.set_verbosity(1)
    #print(algo)
    
    # population size
    pop=pygmo.population(prob,size=6,seed=32)
    #pop=algo.evolve(pop)

    #is1=pygmo.island(algo=algo, pop=pop, udi=my_island())
    #print(is1)
    #is1.evolve()
    
    #multiCore optimization
    archi=pygmo.archipelago(n=2,algo=algo,pop=pop,udi=pygmo.mp_island()) 
    print(archi)
    
    #start optimization

    #conta numero di round dell'evoluzione
    count=0
    best_dx=None
    best_fx=None
    best_pop=None

    while count<10:
        # evoluzione
        archi.evolve()
        archi.wait()
        
        for isl in archi:
            tmp_algo=isl.get_algorithm()
            uda=tmp_algo.extract(pygmo.de)
            log=uda.get_log()
            if(best_dx == None):
                best_dx=log[-1][3]
                best_fx=log[-1][4]
                best_pop=isl.get_population()

            if(log[-1][3] < best_dx) and (log[-1][4] < best_fx):
                best_dx=log[-1][3]
                best_fx=log[-1][4]
                best_pop=isl.get_population()
            print(log)
            print(best_dx)
            print(best_fx)
        
        # refresh population of every island with best one
        for isl in archi:
            isl.set_population(best_pop)

        # incremento round
        count+=1

