# Battery_Ducted_Serial_Parallel_Hybrid.py
#
# Created:  Feb 2017, M. Vegh
# Modified: 

'''
Uses a battery to run a motor connected to a ducted fan; there is a generator that charges the battery
'''
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE

# package imports
import numpy as np
import copy
from SUAVE.Core import Data
from SUAVE.Methods.Power.Battery.Variable_Mass import find_mass_gain_rate
from SUAVE.Components.Propulsors.Propulsor import Propulsor

# ----------------------------------------------------------------------
#  Network
# ----------------------------------------------------------------------
class Propulsor_Battery_Series_Hybrid(Propulsor):
    #uses whatever propulsor you want, included ducted fans in a series hybrid configurations
    #uses simple component efficiencies
    def __defaults__(self):
        self.propulsor            = None
        self.battery              = None # battery
        self.combustion_engine    = None
        #just use efficiency
        self.motor_efficiency       = .95
        self.generator_efficiency   = .95
        self.electronics_efficiency = .9  #speed controller, avionics
        self.tag                    = 'Network'
    
    # manage process with a driver function
    def evaluate_thrust(self,state):
        
        # unpack
        engine      = self.combustion_engine
        propulsor   = self.propulsor
        battery     = self.battery
        conditions  = state.conditions
        numerics    = state.numerics
        # Set battery energy
        battery.current_energy = conditions.propulsion.battery_energy 
        results     = propulsor.evaluate_thrust(state)
     
        # Run the internal combustion engine
        
        conditions.propulsion.combustion_engine_throttle = np.fmin(conditions.propulsion.throttle, np.ones_like(conditions.propulsion.throttle)) #limit throttle going to engine to 1
        engine.power(conditions)
        # Run the internal combustion engine
        engine.power(conditions)
        
        #calculate power going into the battery
       
        results.power = np.transpose(np.array([results.power]))
      
        
        Pe = results.power - engine.outputs.power*self.generator_efficiency
        
        pbat=-Pe/(self.motor_efficiency*self.electronics_efficiency)
     
        battery_logic            = Data()
        battery_logic.power_in   = pbat
        battery_logic.current    = 90.  #use 90 amps as a default for now; will change this for higher fidelity methods
        
        battery.inputs           = battery_logic
        tol                      = 1e-6
        battery.energy_calc(numerics)
    
        #allow for mass gaining batteries
       
        try:
            mdot_bat = find_mass_gain_rate(battery,-(pbat-battery.resistive_losses))
        except AttributeError:
            mdot_bat = np.zeros_like(results.thrust_force_vector[:,0]) 
        #align
        mdot_bat = np.transpose(np.array([mdot_bat]))
        mdot=mdot_bat+engine.outputs.fuel_flow_rate
        mdot=np.reshape(mdot, np.shape(conditions.freestream.velocity))
        #Pack the conditions for outputs
        battery_draw                         = battery.inputs.power_in
        battery_energy                       = battery.current_energy
                                               
        conditions.propulsion.vehicle_power  = results.power
        conditions.propulsion.battery_draw   = battery_draw
        conditions.propulsion.engine_power   = engine.outputs.power
        conditions.propulsion.battery_energy = battery_energy
        #propulsor itself may have a mass flow rate
        results.vehicle_mass_rate += mdot
        
        return results
            
    __call__ = evaluate_thrust