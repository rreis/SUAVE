# optimization_interface_as2.py
# 
# Created:  SUave Team, Aug 2014
# Modified: Tim MacDonald, 3/19/15


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Units

import numpy as np
import pylab as plt
from post_process import post_process

import copy, time

from SUAVE.Core import (
Data, Container, Data_Exception, Data_Warning,
)

import SUAVE.Plugins.VyPy.optimize as vypy_opt


# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():
    
    # setup the interface
    interface = setup_interface()
    
    # quick test
    inputs = Data()
    #inputs.operating_empty = 44811 # 2500 nmi without fuel cell drag
    #inputs.takeoff         = 52283
    #inputs.operating_empty = 57792 # 2500 nmi with fuel cell drag
    #inputs.takeoff         = 71424    
    #inputs.operating_empty = 54118 # 2000 nmi with fuel cell drag
    #inputs.takeoff         = 63521        
    #inputs.operating_empty = 49889.4 # 1500 nmi with fuel cell drag
    #inputs.takeoff         = 55474.7  
    inputs.operating_empty = 56956.0 # 2000 nmi with fuel cell drag and Rmax = 2.76
    inputs.takeoff         = 67612.5  
    inputs.SH_diameter     = 2.76
    
    # evalute!
    results = interface.evaluate(inputs)
    
    """
    VEHICLE EVALUATION 1
    
    INPUTS
    <data object 'SUAVE.Core.Data'>
    projected_span : 36.0
    fuselage_length : 58.0
    
    RESULTS
    <data object 'SUAVE.Core.Data'>
    fuel_burn : 15700.3830236
    weight_empty : 62746.4
    """
    
    return


# ----------------------------------------------------------------------
#   Optimization Interface Setup
# ----------------------------------------------------------------------

def setup_interface():
    
    # ------------------------------------------------------------------
    #   Instantiate Interface
    # ------------------------------------------------------------------
    
    interface = SUAVE.Optimization.Interface()
    
    # ------------------------------------------------------------------
    #   Vehicle and Analyses Information
    # ------------------------------------------------------------------
    
    from as2_fc_full_setup import full_setup
    
    configs,analyses = full_setup()
    
    interface.configs  = configs
    interface.analyses = analyses
    
    
    # ------------------------------------------------------------------
    #   Analysis Process
    # ------------------------------------------------------------------
    
    process = interface.process
    
    # the input unpacker
    process.unpack_inputs = unpack_inputs
    
    # size the base config
    process.simple_sizing = simple_sizing
    
    # finalizes the data dependencies
    process.finalize = finalize
    
    # the missions
    process.missions = missions
    
    # performance studies
    #process.field_length = field_length
    #process.noise = noise
    
    # summarize the results
    process.summary = summarize
    
    # done!
    return interface
    
    
# ----------------------------------------------------------------------
#   Unpack Inputs Step
# ----------------------------------------------------------------------
    
def unpack_inputs(interface):
    
    inputs = interface.inputs
    
    print "VEHICLE EVALUATION %i" % interface.evaluation_count
    print ""
    
    print "INPUTS"
    print inputs
    
    # unpack interface
    vehicle = interface.configs.base
    vehicle.pull_base()
    
    # apply the inputs
    vehicle.mass_properties.takeoff = inputs.takeoff
    vehicle.mass_properties.max_takeoff = inputs.takeoff
    vehicle.mass_properties.operating_empty  = inputs.operating_empty
    vehicle.fuselages.fuselage.effective_diameter = inputs.SH_diameter

    vehicle.store_diff()
     
    return None


# ----------------------------------------------------------------------
#   Apply Simple Sizing Principles
# ----------------------------------------------------------------------

def simple_sizing(interface):
    
    from full_setup import simple_sizing
    
    simple_sizing(interface.configs)
    
    return None


# ----------------------------------------------------------------------
#   Finalizing Function (make part of optimization interface)[needs to come after simple sizing doh]
# ----------------------------------------------------------------------    

def finalize(interface):
    
    interface.configs.finalize()
    interface.analyses.finalize()
    
    return None


# ----------------------------------------------------------------------
#   Process Missions
# ----------------------------------------------------------------------    

def missions(interface):
    
    missions = interface.analyses.missions
    
    results = missions.evaluate()
    
    return results
            
    
# ----------------------------------------------------------------------
#   Field Length Evaluation
# ----------------------------------------------------------------------    
    
def field_length(interface):
    
    # unpack tofl analysis
    estimate_tofl = SUAVE.Methods.Performance.estimate_take_off_field_length
    
    # unpack data
    configs  = interface.configs
    analyses = interface.analyses
    missions = interface.analyses.missions
    takeoff_airport = missions.base.airport
    
    # evaluate
    tofl = estimate_tofl( configs.takeoff,  analyses.configs.takeoff, takeoff_airport )
    tofl = tofl[0,0]
    
    # pack
    results = Data()
    results.takeoff_field_length = tofl
        
    return results


# ----------------------------------------------------------------------
#   Noise Evaluation
# ----------------------------------------------------------------------    

def noise(interface):
    
    # TODO - use the analysis
    
    # unpack noise analysis
    evaluate_noise = SUAVE.Methods.Noise.Correlations.shevell
    
    # unpack data
    vehicle = interface.configs.base
    results = interface.results
    mission_profile = results.missions.base
    
    weight_landing    = mission_profile.segments[-1].conditions.weights.total_mass[-1,0]
    number_of_engines = vehicle.propulsors['turbo_fan'].number_of_engines
    thrust_sea_level  = vehicle.propulsors['turbo_fan'].design_thrust
    thrust_landing    = mission_profile.segments[-1].conditions.frames.body.thrust_force_vector[-1,0]
    
    # evaluate
    results = evaluate_noise( weight_landing    , 
                              number_of_engines , 
                              thrust_sea_level  , 
                              thrust_landing     )
    
    return results
    
    
# ----------------------------------------------------------------------
#   Summarize the Data
# ----------------------------------------------------------------------    

def summarize(interface):
    
    vehicle = interface.configs.base
    
    results = interface.results
    mission_profile = results.missions.base
    
    
    # merge all segment conditions
    def stack_condition(a,b):
        if isinstance(a,np.ndarray):
            return np.vstack([a,b])
        else:
            return None
    
    conditions = None
    for segment in mission_profile.segments:
        if conditions is None:
            conditions = segment.conditions
            continue
        conditions = conditions.do_recursive(stack_condition,segment.conditions)
      
    # pack
    summary = SUAVE.Core.Results()
    
    # Note that the way this is being used includes reserve fuel weight
    summary.weight_empty = vehicle.mass_properties.operating_empty
    summary.weight_takeoff = vehicle.mass_properties.takeoff
    
    summary.fuel_burn = max(conditions.weights.total_mass[:,0]) - min(conditions.weights.total_mass[:,0])
    
    #results.output.max_usable_fuel = vehicle.mass_properties.max_usable_fuel
    
    #summary.noise = results.noise    
    
    summary.mission_time_min = max(conditions.frames.inertial.time[:,0] / Units.min)
    summary.max_altitude_km = max(conditions.freestream.altitude[:,0] / Units.km)
    
    summary.range_nmi = mission_profile.segments[-1].conditions.frames.inertial.position_vector[-1,0] / Units.nmi
    
    #summary.field_length = results.field_length
    
    summary.stability = Data()
    summary.stability.cm_alpha = max(conditions.stability.static.cm_alpha[:,0])
    summary.stability.cn_beta  = max(conditions.stability.static.cn_beta[:,0])
    
    #summary.conditions = conditions
    
    #TODO: revisit how this is calculated
    summary.second_segment_climb_rate = mission_profile.segments[1].climb_rate
    
    base_weight = 22500 # kg    
    reserve_fuel = 1000 # kg
    cell_weight = summary.weight_empty - base_weight - reserve_fuel
    
    max_power_req = 0 # W
    for segment in mission_profile.segments:
        velocity   = segment.conditions.freestream.velocity[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]   
        power = velocity*Thrust
        max_current_power = np.max(power)
        max_power_req = np.max(np.array([max_power_req,max_current_power]))
    
    summary.max_power_req   = max_power_req
    summary.available_power = cell_weight * 1500
    summary.excess_power    = summary.available_power - summary.max_power_req
    
    summary.weight_balance  = summary.weight_takeoff - summary.weight_empty - summary.fuel_burn
    
    cell_density = 1.9e6 # W/m^3
    cell_volume = max_power_req/cell_density
    prop_density = vehicle.propulsors.turbo_fan.propellant.density
    fuel_volume = summary.fuel_burn/prop_density
    SH_V = 3.*np.pi**2/16.*vehicle.fuselages.fuselage.effective_diameter**2/4*vehicle.fuselages.fuselage.lengths.total
    summary.excess_volume = SH_V - fuel_volume -cell_volume
    
    printme = Data()
    printme.fuel_burn = summary.fuel_burn
    printme.weight_empty = summary.weight_empty
    printme.excess_volume = summary.excess_volume
    print "RESULTS"
    print printme

    
    #post_process(vehicle,mission_profile)
    
    return summary




if __name__ == '__main__':
    main()
    
    
