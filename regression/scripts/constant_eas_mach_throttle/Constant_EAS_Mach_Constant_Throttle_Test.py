# Constant_EAS_Mach_Constant_Throttle_Test.py
#
# Created:  Aug 2016, T. MacDonald
# Modified: 


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Units
from SUAVE.Core import Data
import time

import numpy as np
import pylab as plt
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing

import copy, time
# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():

    configs, analyses, vehicle = full_setup()

    simple_sizing(configs)

    configs.finalize()
    analyses.finalize()  

    # mission analysis
    mission = analyses.missions.base
    results = mission.evaluate()

    ending_mass_expected = 74296.0549274
    ending_mass = results.segments.descent_mach_low.conditions.weights.total_mass[-1,0]

    error_percent = (ending_mass-ending_mass_expected)/ending_mass_expected
    
    #assert(np.abs(error_percent)<0.001) 

    return results


# ----------------------------------------------------------------------
#   Analysis Setup
# ----------------------------------------------------------------------

def full_setup():

    # vehicle data
    vehicle  = vehicle_setup()
    configs  = configs_setup(vehicle)

    # vehicle analyses
    configs_analyses = analyses_setup(configs)

    # mission analyses
    mission  = mission_setup(configs_analyses)
    missions_analyses = missions_setup(mission)

    analyses = SUAVE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses

    return configs, analyses, vehicle

# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):

    analyses = SUAVE.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis

    return analyses

def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = SUAVE.Analyses.Vehicle()

    # ------------------------------------------------------------------
    #  Basic Geometry Relations
    sizing = SUAVE.Analyses.Sizing.Sizing()
    sizing.features.vehicle = vehicle
    analyses.append(sizing)

    # ------------------------------------------------------------------
    #  Weights
    weights = SUAVE.Analyses.Weights.Weights()
    weights.vehicle = vehicle
    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.geometry = vehicle

    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Stability Analysis
    stability = SUAVE.Analyses.Stability.Fidelity_Zero()
    stability.geometry = vehicle
    analyses.append(stability)

    # ------------------------------------------------------------------
    #  Energy
    energy= SUAVE.Analyses.Energy.Energy()
    energy.network = vehicle.propulsors 
    analyses.append(energy)

    # ------------------------------------------------------------------
    #  Planet Analysis
    planet = SUAVE.Analyses.Planets.Planet()
    analyses.append(planet)

    # ------------------------------------------------------------------
    #  Atmosphere Analysis
    atmosphere = SUAVE.Analyses.Atmospheric.US_Standard_1976()
    atmosphere.features.planet = planet.features
    analyses.append(atmosphere)   

    # done!
    return analyses    

# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------

def vehicle_setup():

    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    

    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'Boeing_737800'    


    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    

    # mass properties
    vehicle.mass_properties.max_takeoff               = 79015.8   # kg
    vehicle.mass_properties.takeoff                   = 77435.484
    vehicle.mass_properties.max_zero_fuel             = 0.9 * vehicle.mass_properties.max_takeoff
    vehicle.mass_properties.cargo                     = 10000.  * Units.kilogram   

    # envelope properties
    vehicle.envelope.ultimate_load = 2.5
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area         = 124.862       
    vehicle.passengers             = 170
    vehicle.systems.control        = "fully powered" 
    vehicle.systems.accessories    = "medium range"


    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------        

    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'main_wing'

    wing.aspect_ratio            = 10.18
    wing.sweeps.quarter_chord    = 25 * Units.deg
    wing.thickness_to_chord      = 0.1
    wing.taper                   = 0.16
    wing.span_efficiency         = 0.9

    wing.spans.projected         = 35.66    

    wing.chords.root             = 6.81
    wing.chords.tip              = 1.09
    wing.chords.mean_aerodynamic = 4.235

    wing.areas.reference         = 124.862 

    wing.twists.root             = 4.0 * Units.degrees
    wing.twists.tip              = -4.0 * Units.degrees

    wing.origin                  = [20,0,0]
    wing.aerodynamic_center      = [3,0,0] 

    wing.vertical                = False
    wing.symmetric               = True
    wing.high_lift               = True

    wing.dynamic_pressure_ratio  = 1.0

    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------        
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------        

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'horizontal_stabilizer'

    wing.aspect_ratio            = 6.16
    wing.sweeps.quarter_chord    = 30 * Units.deg
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.4
    wing.span_efficiency         = 0.9

    wing.spans.projected         = 14.146

    wing.chords.root             = 3.28
    wing.chords.tip              = 1.31    
    wing.chords.mean_aerodynamic = 8.0

    wing.areas.reference         = 32.488

    wing.twists.root             = 3.0 * Units.degrees
    wing.twists.tip              = 3.0 * Units.degrees  

    wing.origin                  = [50,0,0]
    wing.aerodynamic_center      = [2,0,0]

    wing.vertical                = False 
    wing.symmetric               = True

    wing.dynamic_pressure_ratio  = 0.9  

    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'vertical_stabilizer'    

    wing.aspect_ratio            = 1.91
    wing.sweeps.quarter_chord    = 25 * Units.deg
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.25
    wing.span_efficiency         = 0.9

    wing.spans.projected         = 7.877

    wing.chords.root             = 6.60
    wing.chords.tip              = 1.65
    wing.chords.mean_aerodynamic = 8.0

    wing.areas.reference         = 32.488

    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees  

    wing.origin                  = [50,0,0]
    wing.aerodynamic_center      = [2,0,0]    

    wing.vertical                = True 
    wing.symmetric               = False
    wing.t_tail                  = False

    wing.dynamic_pressure_ratio  = 1.0

    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------

    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'fuselage'

    fuselage.seats_abreast         = 6
    fuselage.seat_pitch            = 1

    fuselage.fineness.nose         = 1.6
    fuselage.fineness.tail         = 2.

    fuselage.lengths.nose          = 6.4
    fuselage.lengths.tail          = 8.0
    fuselage.lengths.cabin         = 28.85
    fuselage.lengths.total         = 38.02
    fuselage.lengths.fore_space    = 6.
    fuselage.lengths.aft_space     = 5.    

    fuselage.width                 = 3.74

    fuselage.heights.maximum       = 3.74
    fuselage.heights.at_quarter_length          = 3.74
    fuselage.heights.at_three_quarters_length   = 3.74
    fuselage.heights.at_wing_root_quarter_chord = 3.74

    fuselage.areas.side_projected  = 142.1948
    fuselage.areas.wetted          = 446.718
    fuselage.areas.front_projected = 12.57

    fuselage.effective_diameter    = 3.74 #4.0

    fuselage.differential_pressure = 5.0e4 * Units.pascal # Maximum differential pressure

    # add to vehicle
    vehicle.append_component(fuselage)


    # ------------------------------------------------------------------
    #   Turbofan Network
    # ------------------------------------------------------------------    

    #instantiate the gas turbine network
    turbofan = SUAVE.Components.Energy.Networks.Turbofan()
    turbofan.tag = 'turbo_fan'

    # setup
    turbofan.number_of_engines = 2.0
    turbofan.bypass_ratio      = 5.4
    turbofan.engine_length     = 2.71
    turbofan.nacelle_diameter  = 2.05

    # working fluid
    turbofan.working_fluid = SUAVE.Attributes.Gases.Air()


    # ------------------------------------------------------------------
    #   Component 1 - Ram

    # to convert freestream static to stagnation quantities

    # instantiate
    ram = SUAVE.Components.Energy.Converters.Ram()
    ram.tag = 'ram'

    # add to the network
    turbofan.append(ram)


    # ------------------------------------------------------------------
    #  Component 2 - Inlet Nozzle

    # instantiate
    inlet_nozzle = SUAVE.Components.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag = 'inlet_nozzle'

    # setup
    inlet_nozzle.polytropic_efficiency = 0.98
    inlet_nozzle.pressure_ratio        = 0.98

    # add to network
    turbofan.append(inlet_nozzle)


    # ------------------------------------------------------------------
    #  Component 3 - Low Pressure Compressor

    # instantiate 
    compressor = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag = 'low_pressure_compressor'

    # setup
    compressor.polytropic_efficiency = 0.91
    compressor.pressure_ratio        = 1.14    

    # add to network
    turbofan.append(compressor)


    # ------------------------------------------------------------------
    #  Component 4 - High Pressure Compressor

    # instantiate
    compressor = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag = 'high_pressure_compressor'

    # setup
    compressor.polytropic_efficiency = 0.91
    compressor.pressure_ratio        = 13.415    

    # add to network
    turbofan.append(compressor)


    # ------------------------------------------------------------------
    #  Component 5 - Low Pressure Turbine

    # instantiate
    turbine = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag='low_pressure_turbine'

    # setup
    turbine.mechanical_efficiency = 0.99
    turbine.polytropic_efficiency = 0.93     

    # add to network
    turbofan.append(turbine)


    # ------------------------------------------------------------------
    #  Component 6 - High Pressure Turbine

    # instantiate
    turbine = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag='high_pressure_turbine'

    # setup
    turbine.mechanical_efficiency = 0.99
    turbine.polytropic_efficiency = 0.93     

    # add to network
    turbofan.append(turbine)


    # ------------------------------------------------------------------
    #  Component 7 - Combustor

    # instantiate    
    combustor = SUAVE.Components.Energy.Converters.Combustor()   
    combustor.tag = 'combustor'

    # setup
    combustor.efficiency                = 0.99 
    combustor.alphac                    = 1.0     
    combustor.turbine_inlet_temperature = 1450
    combustor.pressure_ratio            = 0.95
    combustor.fuel_data                 = SUAVE.Attributes.Propellants.Jet_A()    

    # add to network
    turbofan.append(combustor)


    # ------------------------------------------------------------------
    #  Component 8 - Core Nozzle

    # instantiate
    nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    nozzle.tag = 'core_nozzle'

    # setup
    nozzle.polytropic_efficiency = 0.95
    nozzle.pressure_ratio        = 0.99    

    # add to network
    turbofan.append(nozzle)


    # ------------------------------------------------------------------
    #  Component 9 - Fan Nozzle

    # instantiate
    nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    nozzle.tag = 'fan_nozzle'

    # setup
    nozzle.polytropic_efficiency = 0.95
    nozzle.pressure_ratio        = 0.99    

    # add to network
    turbofan.append(nozzle)


    # ------------------------------------------------------------------
    #  Component 10 - Fan

    # instantiate
    fan = SUAVE.Components.Energy.Converters.Fan()   
    fan.tag = 'fan'

    # setup
    fan.polytropic_efficiency = 0.93
    fan.pressure_ratio        = 1.7    

    # add to network
    turbofan.append(fan)


    # ------------------------------------------------------------------
    #Component 10 : thrust (to compute the thrust)
    thrust = SUAVE.Components.Energy.Processes.Thrust()       
    thrust.tag ='compute_thrust'

    #total design thrust (includes all the engines)
    thrust.total_design             = 2*24000. * Units.N #Newtons

    #design sizing conditions
    altitude      = 35000.0*Units.ft
    mach_number   = 0.78 
    isa_deviation = 0.

    # add to network
    turbofan.thrust = thrust

    #size the turbofan
    turbofan_sizing(turbofan,mach_number,altitude)   

    # add  gas turbine network gt_engine to the vehicle 
    vehicle.append_component(turbofan)      


    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------

    return vehicle


# ----------------------------------------------------------------------
#   Define the Configurations
# ---------------------------------------------------------------------

def configs_setup(vehicle):

    # ------------------------------------------------------------------
    #   Initialize Configurations
    # ------------------------------------------------------------------

    configs = SUAVE.Components.Configs.Config.Container()

    base_config = SUAVE.Components.Configs.Config(vehicle)
    base_config.tag = 'base'
    configs.append(base_config)

    # ------------------------------------------------------------------
    #   Cruise Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'cruise'

    configs.append(config)


    # done!
    return configs

# ----------------------------------------------------------------------
#   Sizing for the Vehicle Configs
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results,line_style='bo-'):

    axis_font = {'fontname':'Arial', 'size':'14'}    

    # ------------------------------------------------------------------
    #   Altitude, sfc, vehicle weight
    # ------------------------------------------------------------------ 
    
    fig = plt.figure("Throttle and Speed",figsize=(8,10))
    for segment in results.segments.values():
        
        base_density = 1.225        
        
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        velocity = segment.conditions.freestream.velocity[:,0]
        density  = segment.conditions.freestream.density[:,0]
        eas      = velocity * np.sqrt(density/base_density)
        eta      = segment.conditions.propulsion.throttle[:,0]
        
        axes = fig.add_subplot(3,1,1)
        axes.plot( time , eta , 'bo-' )
        axes.set_ylabel('Throttle')
        axes.grid(True)
    
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , velocity , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Speed (m/s)')
        axes.grid(True)
    
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , eas , 'bo-' )
        axes.set_ylabel('EAS (m/s)')
        axes.grid(True) 
    
    mgr = plt.get_current_fig_manager()
    mgr.window.setGeometry(50,100,600,900)  
    
    fig = plt.figure("Altitude, Weight, Mach",figsize=(8,10))
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        mass   = segment.conditions.weights.total_mass[:,0] / Units.lb
        altitude = segment.conditions.freestream.altitude[:,0] / Units.ft
        mach = segment.conditions.freestream.mach_number[:,0]

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , altitude , line_style )
        axes.set_ylabel('Altitude (ft)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , mass , 'ro-' )
        axes.set_ylabel('Weight (lb)',axis_font)
        axes.grid(True)   
        
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , mach , line_style )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Mach Number',axis_font)
        axes.grid(True)        
        
    mgr = plt.get_current_fig_manager()
    mgr.window.setGeometry(675,100,600,900)   
    
    fig = plt.figure("solver params",figsize=(8,10))
    for segment in results.segments.values():       
        
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        body_angle = segment.conditions.frames.body.inertial_rotations[:,1]
        vx = segment.conditions.frames.inertial.velocity_vector[:,0]
        vz = segment.conditions.frames.inertial.velocity_vector[:,2]
        gamma = np.tan(-vz/vx)   
        theta = body_angle
        alpha = theta-gamma   
        
        eta      = segment.conditions.propulsion.throttle[:,0]
    
        axes = fig.add_subplot(3,1,1)
        axes.plot( time , eta , 'bo-' )
        axes.set_ylabel('Throttle')
        axes.grid(True)         
        
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , body_angle / Units.deg, 'bo-' )
        axes.set_ylabel('Body Angle (deg)')
        axes.grid(True)
    
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , alpha / Units.deg, 'bo-' )
        axes.set_ylabel('Wing Angle (deg)')
        axes.grid(True) 
              
    
    mgr = plt.get_current_fig_manager()
    mgr.window.setGeometry(1300,100,600,900)     
    
    print 'Ending Mass: ' + str(mass[-1] * Units.lb) + ' kg'
     
    plt.show()

def simple_sizing(configs):

    base = configs.base
    base.pull_base()

    # zero fuel weight
    base.mass_properties.max_zero_fuel = 0.9 * base.mass_properties.max_takeoff 

    # wing areas
    for wing in base.wings:
        wing.areas.wetted   = 2.0 * wing.areas.reference
        wing.areas.exposed  = 0.8 * wing.areas.wetted
        wing.areas.affected = 0.6 * wing.areas.wetted

    # fuselage seats
    base.fuselages['fuselage'].number_coach_seats = base.passengers

    # diff the new data
    base.store_diff()

    return

# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------

def mission_setup(analyses):

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'

    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()

    mission.airport = airport    

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments

    # base segment
    base_segment = Segments.Segment()
    
    # ------------------------------------------------------------------
    #   EAS Climb
    # ------------------------------------------------------------------

        
    segment = Segments.Climb.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "climb_EAS"

    segment.analyses.extend( analyses.cruise )

    segment.altitude_start       = 10000.0    * Units.ft
    segment.altitude_end         = 30000.0    * Units.ft
    segment.equivalent_air_speed = 290. * Units.kts
    segment.throttle             = 1.0
    
    # add to misison
    mission.append_segment(segment)     
    
    
    # ------------------------------------------------------------------    
    #   EAS Descent
    # ------------------------------------------------------------------       
    
    segment = Segments.Descent.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "descent_EAS"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end         = 10000.0 * Units.ft
    segment.equivalent_air_speed = 290. * Units.kts
    segment.throttle             = .15
    
    # add to mission
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------
    #   Mach Climb - below tropopause
    # ------------------------------------------------------------------

        
    segment = Segments.Climb.Constant_Throttle_Constant_Mach(base_segment)
    segment.tag = "climb_Mach_low"

    segment.analyses.extend( analyses.cruise )

    segment.altitude_start = 10000.0    * Units.ft
    segment.altitude_end   = 11000.
    segment.mach_number    = 0.75
    segment.throttle       = 1.0
    
    # add to misison
    mission.append_segment(segment) 
    
    # ------------------------------------------------------------------
    #   Mach Climb - above tropopause
    # ------------------------------------------------------------------

        
    segment = Segments.Climb.Constant_Throttle_Constant_Mach(base_segment)
    segment.tag = "climb_Mach_high"

    segment.analyses.extend( analyses.cruise )

    segment.altitude_start = 11000.
    segment.altitude_end   = 12000.
    segment.mach_number    = 0.75
    segment.throttle       = 1.2
    
    # add to misison
    mission.append_segment(segment)     
    
    
    # ------------------------------------------------------------------    
    #   Mach Descent - above tropopause
    # ------------------------------------------------------------------       
    
    segment = Segments.Descent.Constant_Throttle_Constant_Mach(base_segment)
    segment.tag = "descent_Mach_high"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end = 11000.
    segment.mach_number  = 0.75
    segment.throttle     = .08
    
    # add to mission
    mission.append_segment(segment)        
    
    # ------------------------------------------------------------------    
    #   Mach Descent - below tropopause
    # ------------------------------------------------------------------       
    
    segment = Segments.Descent.Constant_Throttle_Constant_Mach(base_segment)
    segment.tag = "descent_Mach_low"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end = 10000.0 * Units.ft
    segment.mach_number  = 0.75
    segment.throttle     = .08
    
    # add to mission
    mission.append_segment(segment)    


    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------

    return mission

def missions_setup(base_mission):

    # the mission container
    missions = SUAVE.Analyses.Mission.Mission.Container()

    # ------------------------------------------------------------------
    #   Base Mission
    # ------------------------------------------------------------------

    missions.base = base_mission

    return missions  


if __name__ == '__main__':
    
    results = main()
    
    plot_mission(results)