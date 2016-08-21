# run_aircraft_function.py
# December 2, 2014
# Trent Lukaczyk


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Units
from SUAVE.Core import Data

import numpy as np
import pylab as plt
import scipy.optimize
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing

import copy, time


# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main(base_filename):
    
 
    
    #filename = "B737_bada_climb9.csv"
    #filename = "B737_bada_descent3.csv"
    #filename = "B737_bada_cruise1.csv"
    #filename = "B737_bada_climb4.csv"
        
    #Mass
    MTOW = 79015.8
    #MLW
    MZFW = 0.9*MTOW

    reference_mass = MZFW + 0.8 * (MTOW-MZFW)
    minimum_mass = MZFW + 0.2*(MTOW-MZFW)
    maximum_mass = MTOW
    
    TOW = MTOW * 0.85 # ANP fit pg. 7
    delta_isa = 0.0 # K
    
    vehicle_inputs = Data()
    mission_inputs = Data()
    
    vehicle_inputs.tow = TOW
    mission_inputs.delta_isa = delta_isa

    configs, analyses,vehicle = full_setup(mission_inputs,vehicle_inputs)
        
    static_thrust = np.array([float(vehicle.ANP.thrustStatic)])   
    
    simple_sizing(configs)
        
    configs.finalize()
    analyses.finalize()
    
    count = 1
        
    # mission analysis
    print 'Takeoff Config - Accel'
    mission = analyses.missions.takeoff_accel
    results = mission.evaluate()
    takeoff_accel_mat = write_mission_data(results,vehicle,None,count)
    
    print 'Climb Config - Accel'
    mission = analyses.missions.climb_accel
    results = mission.evaluate()
    climb_accel_mat = write_mission_data(results,vehicle,None,count)  
    
    print 'Takeoff Config/Power - Climb'
    mission = analyses.missions.takeoff_climb
    results = mission.evaluate()
    takeoff_climb_mat = write_mission_data(results,vehicle,None,count)  
    
    print 'Climb Config/Power - Climb'
    mission = analyses.missions.climb_climb
    results = mission.evaluate()
    climb_climb_mat = write_mission_data(results,vehicle,None,count)   
    
    print 'Terminal Area Descent without Flaps'
    mission = analyses.missions.term_descent
    results = mission.evaluate()
    term_descent_mat = write_mission_data(results,vehicle,None,count) 
    
    print 'Terminal Area Descent with Flaps'
    mission = analyses.missions.flap_descent
    results = mission.evaluate()
    flap_descent_mat = write_mission_data(results,vehicle,None,count)    
    
    np.save('anp_' + base_filename + '_takeoff_accel.npy',takeoff_accel_mat)
    np.save('anp_' + base_filename + '_takeoff_climb.npy',takeoff_climb_mat)
    np.save('anp_' + base_filename + '_climb_accel.npy',climb_accel_mat)
    np.save('anp_' + base_filename + '_climb_climb.npy',climb_climb_mat)
    np.save('anp_' + base_filename + '_term_descent.npy',term_descent_mat)
    np.save('anp_' + base_filename + '_static_thrust.npy',static_thrust)
    np.save('anp_' + base_filename + '_flap_descent.npy',flap_descent_mat)
    
                    
    return (takeoff_accel_mat,takeoff_climb_mat,climb_accel_mat,climb_climb_mat)




# ----------------------------------------------------------------------
#   Vehicle Setup
# ----------------------------------------------------------------------

def full_setup(mission_inputs,vehicle_inputs):

    # vehicle data
    vehicle  = vehicle_setup(vehicle_inputs)
    configs  = configs_setup(vehicle)
    
    # vehicle analyses
    configs_analyses = analyses_setup(configs)
    
    # mission analyses
    missions_analyses = missions_setup(configs_analyses,mission_inputs)

    analyses = SUAVE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = missions_analyses
    
    return configs, analyses,vehicle


# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------

def vehicle_setup(inputs):
    
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
    vehicle.mass_properties.takeoff                   = inputs.tow
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
    wing.sweep                   = 25 * Units.deg
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
    wing.sweep                   = 30 * Units.deg
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
    wing.sweep                   = 25 * Units.deg
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
    #   ANP Data
    # ------------------------------------------------------------------    
    
    vehicle.ANP = Data()
    an = vehicle.ANP
    
    an.anpAirplaneId = '737800T2' # overridden in main xml generation function
    
    # anpAirplane
    an.description = 'BOEING 737-800T/CFM56-7B26'
    an.sizeCode = 'L'
    an.owner = 'C'
    an.engineTypeCode = 'J'
    an.numberEngines = '2'
    an.maxGrossWeightTakeoff = '174200'
    an.maxGrossWeightLand = '146300'
    an.maxDsStop = '5435'
    an.depThrustCoeffType = 'J'
    an.thrustStatic = '26300'
    an.thrustRestore = 'N'
    an.noiseId = 'CF567B'
    an.noiseCategory = '3'
    an.minBurn = '0.092513944'
    
    #anpProfileSet
    an.profile = []
    
    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------

    return vehicle

# ----------------------------------------------------------------------
#   Define the Configurations
# ----------------------------------------------------------------------

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
    
    
    # ------------------------------------------------------------------
    #   Takeoff Configuration
    # ------------------------------------------------------------------
    
    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'takeoff'
    
    config.wings['main_wing'].flaps.angle = 20. * Units.deg
    config.wings['main_wing'].slats.angle = 25. * Units.deg
    
    config.V2_VS_ratio = 1.21
    config.maximum_lift_coefficient = 2.
    
    configs.append(config)
    
    
    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------

    config = SUAVE.Components.Configs.Config(base_config)
    config.tag = 'landing'
    
    config.wings['main_wing'].flaps_angle = 30. * Units.deg
    config.wings['main_wing'].slats_angle = 25. * Units.deg

    config.Vref_VS_ratio = 1.23
    config.maximum_lift_coefficient = 2.
    
    configs.append(config)
    
    
    # done!
    return configs


# ----------------------------------------------------------------------
#   Sizing for the Vehicle Configs
# ----------------------------------------------------------------------

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
    
    # ------------------------------------------------------------------
    #   Landing Configuration
    # ------------------------------------------------------------------
    landing = configs.landing
    
    # make sure base data is current
    landing.pull_base()
    
    # landing weight
    landing.mass_properties.landing = 0.85 * base.mass_properties.takeoff
    
    # diff the new data
    landing.store_diff()
    
    # done!
    return


# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):
    
    analyses = SUAVE.Analyses.Analysis.Container()
    
    # build a base analysis for each config
    for tag,config in configs.items():
        analysis = base_analysis(config)
        analyses[tag] = analysis
        
    # adjust analyses for configs
    
    # takeoff_analysis
    analyses.takeoff.aerodynamics.settings.drag_coefficient_increment = 0.020
    
    # landing analysis
    aerodynamics = analyses.landing.aerodynamics
    # do something here eventually
    
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
    
    ## modify inviscid wings - linear lift model
    #inviscid_wings = SUAVE.Analyses.Aerodynamics.Linear_Lift()
    #inviscid_wings.settings.slope_correction_coefficient = 1.04
    #inviscid_wings.settings.zero_lift_coefficient = 2.*np.pi* 3.1 * Units.deg    
    #aerodynamics.process.compute.lift.inviscid_wings = inviscid_wings        
    
    ## modify inviscid wings - avl model
    #inviscid_wings = SUAVE.Analyses.Aerodynamics.Surrogates.AVL()
    #inviscid_wings.geometry = vehicle
    #aerodynamics.process.compute.lift.inviscid_wings = inviscid_wings
    
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
    energy.network = vehicle.propulsors #what is called throughout the mission (at every time step))
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

#: def analyses_setup()


# ----------------------------------------------------------------------
#   Define the Mission
# ----------------------------------------------------------------------
    



# ----------------------------------------------------------------------
#   Various Missions
# ----------------------------------------------------------------------
    
def missions_setup(analyses,inputs):

    # the mission container
    missions = SUAVE.Analyses.Mission.Mission.Container()
    
    # ------------------------------------------------------------------
    #   Max Takeoff Accelerating Level Flight
    # ------------------------------------------------------------------
    
    mission_1 = SUAVE.Analyses.Mission.Sequential_Segments()
    mission_1.tag = 'max_takeoff_accel'
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission_1.airport = airport
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment()    
    
    segment_size = 16
    
    segment = Segments.Cruise.Constant_Throttle_Constant_Altitude()
    segment.tag = "accel_1"
    segment.state.numerics.number_control_points = segment_size
    
    segment.analyses.extend( analyses.takeoff )
    
    segment.altitude        = 1500 * Units.ft
    segment.air_speed_start = 170 * Units.kts
    segment.air_speed_end   = 250 * Units.kts
    segment.throttle        = 1.0
    segment.temperature_deviation = 0.0
    
    segment.settings.root_finder = scipy.optimize.root
    
    
    # add to misison
    mission_1.append_segment(segment)    
    
    # ------------------------------------------------------------------
    #   Max Climb Accelerating Level Flight
    # ------------------------------------------------------------------
    
    mission_2 = SUAVE.Analyses.Mission.Sequential_Segments()
    mission_2.tag = 'max_climb_accel'
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission_2.airport = airport
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment()    
    
    
    segment = Segments.Cruise.Constant_Throttle_Constant_Altitude()
    segment.tag = "accel_1"
    segment.state.numerics.number_control_points = segment_size
    
    segment.analyses.extend( analyses.takeoff )
    
    segment.altitude        = 1500 * Units.ft
    segment.air_speed_start = 170 * Units.kts # 3.0   * Units.km
    segment.air_speed_end   = 250 * Units.kts
    segment.throttle        = 0.8
    segment.temperature_deviation = 0.0
    
    segment.settings.root_finder = scipy.optimize.root
    
    # add to misison
    mission_2.append_segment(segment)  
    
    # ------------------------------------------------------------------
    #   Max Takeoff Climbing
    # ------------------------------------------------------------------
    
    mission_3 = SUAVE.Analyses.Mission.Sequential_Segments()
    mission_3.tag = 'max_takeoff_climbing'
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission_3.airport = airport
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment()    
    
    
    segment = Segments.Climb.Constant_Throttle_Constant_EAS()
    segment.tag = "climb_1"
    segment.state.numerics.number_control_points = segment_size
    
    segment.analyses.extend( analyses.takeoff )
    
    segment.altitude_start        = 0.0 * Units.ft
    segment.altitude_end          = 16000.0 * Units.ft
    segment.equivalent_air_speed  = 170.0 * Units.kts
    segment.throttle              = 1.0
    segment.temperature_deviation = 0.0
    
    
    # add to misison
    mission_3.append_segment(segment)  
    
    # ------------------------------------------------------------------
    #   Max Climb Climbing
    # ------------------------------------------------------------------
    
    mission_4 = SUAVE.Analyses.Mission.Sequential_Segments()
    mission_4.tag = 'max_climb_climbing'
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission_4.airport = airport
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment()    
    
    
    segment = Segments.Climb.Constant_Throttle_Constant_EAS()
    segment.tag = "climb_1"
    segment.state.numerics.number_control_points = segment_size
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_start        = 0.0 * Units.ft 
    segment.altitude_end          = 15900.0 * Units.ft # set to 
    segment.equivalent_air_speed  = 250.0 * Units.kts
    segment.throttle              = 0.8
    segment.temperature_deviation = 0.0
    
    segment.settings.root_finder = scipy.optimize.fsolve
    
    
    # add to misison
    mission_4.append_segment(segment)      
    
    # ------------------------------------------------------------------
    #   Terminal Area Descent
    # ------------------------------------------------------------------
    
    mission_6 = SUAVE.Analyses.Mission.Sequential_Segments()
    mission_6.tag = 'terminal_area_descent'
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission_6.airport = airport
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment()    
    
    
    segment = Segments.Climb.Constant_Throttle_Constant_EAS()
    segment.tag = "climb_1"
    segment.state.numerics.number_control_points = segment_size
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end          = 0.0 * Units.ft
    segment.altitude_start        = 10000.0 * Units.ft
    segment.equivalent_air_speed  = 250.0 * Units.kts
    segment.throttle              = 0.15
    segment.temperature_deviation = 0.0
    
    
    # add to misison
    mission_6.append_segment(segment) 
    
    # ------------------------------------------------------------------
    #   Terminal Area Descent wiith Flaps
    # ------------------------------------------------------------------
    
    mission_7 = SUAVE.Analyses.Mission.Sequential_Segments()
    mission_7.tag = 'terminal_area_descent'
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission_7.airport = airport
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment()    
    
    
    segment = Segments.Climb.Constant_Throttle_Constant_EAS()
    segment.tag = "climb_1"
    segment.state.numerics.number_control_points = segment_size
    
    segment.analyses.extend( analyses.takeoff )
    
    segment.altitude_end          = 0.0 * Units.ft
    segment.altitude_start        = 10000.0 * Units.ft
    segment.equivalent_air_speed  = 170.0 * Units.kts
    segment.throttle              = 0.15
    segment.temperature_deviation = 0.0
    
    
    # add to misison
    mission_7.append_segment(segment)       
    
    
    missions.takeoff_accel = mission_1
    missions.climb_accel   = mission_2
    missions.takeoff_climb = mission_3
    missions.climb_climb   = mission_4
    missions.term_descent  = mission_6
    missions.flap_descent  = mission_7

    return missions  



def write_mission_data(results,vehicle,trajectory_type,count):
    

    starting_traj = 0
    ending_traj = 1
    
    segment_size = 16
    
    segment_tot = ending_traj-starting_traj
    segment_mat = np.zeros([segment_tot*segment_size,15])
    
    #DATASET  NO #TOW #weight #xpos #zpos #speed #thrust #cdi  #cdp  #cdc  #cd #cl #drag #lift
    #for i in range(len(results.segments)):
    base_density = 1.225
    for i in range(starting_traj,ending_traj):    
        for j in range(len(results.segments[i].conditions.weights.total_mass)):
            segment_num = count
            mission_point = segment_size*(i-starting_traj) + j
            
            
            time      = results.segments[i].conditions.frames.inertial.time[j,0]
            altitude  = results.segments[i].conditions.freestream.altitude[j,0]
            density   = results.segments[i].conditions.freestream.density[j,0]
            velocity  = results.segments[i].conditions.freestream.velocity[j,0]
            cas       = velocity * np.sqrt(density/base_density)
            lift      = -results.segments[i].conditions.frames.wind.lift_force_vector[j,2]
            drag      = -results.segments[i].conditions.frames.wind.drag_force_vector[j,0]
            thrust    = results.segments[i].conditions.frames.body.thrust_force_vector[j,0]
            
            mach_number = results.segments[i].conditions.freestream.mach_number[j,0] 
            temperature = results.segments[i].conditions.freestream.temperature[j,0] 
                        
            mass = results.segments[i].conditions.weights.total_mass[j,0]
            mass_rate = results.segments[i].conditions.weights.vehicle_mass_rate[j,0]
            
            pressure = results.segments[i].conditions.freestream.pressure[j,0] 
            
            segment_mat[segment_size*(i-starting_traj)+j][0] = segment_num
            segment_mat[segment_size*(i-starting_traj)+j][1] = mission_point
            segment_mat[segment_size*(i-starting_traj)+j][2] = time
            segment_mat[segment_size*(i-starting_traj)+j][3] = altitude
            segment_mat[segment_size*(i-starting_traj)+j][4] = cas
            segment_mat[segment_size*(i-starting_traj)+j][5] = density
            segment_mat[segment_size*(i-starting_traj)+j][6] = velocity
            segment_mat[segment_size*(i-starting_traj)+j][7] = mach_number
            segment_mat[segment_size*(i-starting_traj)+j][8] = temperature
            #segment_mat[segment_size*(i-starting_traj)+j][9] = delta_isa (this is modified in the main function since it is not part of the results) 
            segment_mat[segment_size*(i-starting_traj)+j][10] = lift
            segment_mat[segment_size*(i-starting_traj)+j][11] = drag
            segment_mat[segment_size*(i-starting_traj)+j][12] = thrust
            segment_mat[segment_size*(i-starting_traj)+j][13] = mass_rate
            segment_mat[segment_size*(i-starting_traj)+j][14] = pressure
            
            
            # Construct matrix


    return segment_mat





# ----------------------------------------------------------------------
#   Call Main
# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    base_filename = '737800_profile_test'
    
    main(base_filename)
