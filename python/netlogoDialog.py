import pyNetLogo

class NetlogoDialog():
    # comunication with Netlogo
    def __init__(self,netlogoVersion,netlogoPath,ModelPath):
        #comunicate with Netlogo
        self.netlogo=pyNetLogo.NetLogoLink(gui='true',
                        netlogo_home=netlogoPath,
                        netlogo_version=netlogoVersion)
        
        # load model
        self.netlogo.load_model(ModelPath)
    def passConfigurationParams(self,configuration_params):
        self.params=configuration_params
    def eseguiSimulazione(self,parameters):
        #set parameters
        count=0
        # used for visual debug
        optimized_params={}
        for key,value in self.params.items():
            cmd="set " + key + " " + str(parameters[count])
            self.netlogo.command(cmd)
            print(cmd)
            #used for debug
            optimized_params[key]=parameters[count]
            count=count+1
        
        #set scenario
        self.netlogo.command('set selectScenario "dump" ')
        
        #setup
        self.netlogo.command('setup read-from-string substring date-and-time 9 12')
        
        #initial target found
        target_found=self.netlogo.report('percentageTgtsFound')

        while (target_found<=95):
            self.netlogo.repeat_command('go',1)
            target_found=self.netlogo.report('percentageTgtsFound')
            tick_number=self.netlogo.report('ticks')
        
        print(optimized_params)
        print('\ntarget found: ' + str(target_found)
            + '\nticks: ' +str(tick_number) )
        self.netlogo.kill_workspace()
        return tick_number
