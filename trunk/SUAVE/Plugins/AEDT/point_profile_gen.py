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
        
    simple_sizing(configs)
        
    configs.finalize()
    analyses.finalize()
    
    count = 1
    
    mission = analyses.missions.SUAVE_climb
    results_climb = mission.evaluate()
    SUAVE_climb_mat = write_mission_data(results_climb,vehicle,mission,'D')
    
    mission = analyses.missions.SUAVE_descent
    results_descent = mission.evaluate()
    SUAVE_descent_mat = write_mission_data(results_descent,vehicle,mission,'A')    
    
    np.save('points_' + base_filename + '_SUAVE_climb.npy',SUAVE_climb_mat)
    np.save('points_' + base_filename + '_SUAVE_descent.npy',SUAVE_descent_mat)    
    
                    
    return results_climb,results_descent




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
    vehicle.mass_properties.operating_empty           = 62746.4   # kg
    vehicle.mass_properties.takeoff                   = inputs.tow #79015.8   # kg
    vehicle.mass_properties.max_zero_fuel             = 0.9 * vehicle.mass_properties.max_takeoff
    vehicle.mass_properties.cargo                     = 10000.  * Units.kilogram   
    
    vehicle.mass_properties.center_of_gravity         = [60 * Units.feet, 0, 0]  # Not correct
    vehicle.mass_properties.moments_of_inertia.tensor = [[10 ** 5, 0, 0],[0, 10 ** 6, 0,],[0,0, 10 ** 7]] # Not Correct
    
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
    
    wing.aspect_ratio            = 6.16      #
    wing.sweep                   = 30 * Units.deg
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.4
    wing.span_efficiency         = 0.9
    
    wing.spans.projected         = 14.146      #

    wing.chords.root             = 3.28
    wing.chords.tip              = 1.31    
    wing.chords.mean_aerodynamic = 8.0

    wing.areas.reference         = 32.488    #
    
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
    
    wing.aspect_ratio            = 1.91      #
    wing.sweep                   = 25 * Units.deg
    wing.thickness_to_chord      = 0.08
    wing.taper                   = 0.25
    wing.span_efficiency         = 0.9
    
    wing.spans.projected         = 7.877      #    

    wing.chords.root             = 6.60
    wing.chords.tip              = 1.65
    wing.chords.mean_aerodynamic = 8.0
    
    wing.areas.reference         = 32.488    #
    
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
    
    #fuselage.number_coach_seats    = vehicle.passengers
    fuselage.seats_abreast         = 6
    fuselage.seat_pitch            = 1
    
    fuselage.fineness.nose         = 1.6
    fuselage.fineness.tail         = 2.
    
    fuselage.lengths.nose          = 6.4
    fuselage.lengths.tail          = 8.0
    fuselage.lengths.cabin         = 28.85 #44.0
    fuselage.lengths.total         = 38.02 #58.4
    fuselage.lengths.fore_space    = 6.
    fuselage.lengths.aft_space     = 5.    
    
    fuselage.width                 = 3.74 #4.
    
    fuselage.heights.maximum       = 3.74  #4.    #
    fuselage.heights.at_quarter_length          = 3.74 # Not correct
    fuselage.heights.at_three_quarters_length   = 3.74 # Not correct
    fuselage.heights.at_wing_root_quarter_chord = 3.74 # Not correct

    fuselage.areas.side_projected  = 3.74* 38.02 #4.* 59.8 #  Not correct
    fuselage.areas.wetted          = 446.718 #688.64
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
    
    an.anpAirplaneId = '737800T'
    
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
    
    an.profile.append(Data())
    an.profile[0].operationType = 'A'
    an.profile[0].profileGroupId = 'STANDARD'
    an.profile[0].profileStageLength = '1'
    an.profile[0].weight = '131700'
    an.profile[0].profilePoints = Data()
    an.profile[0].profilePoints.point = []
    an.profile[0].profilePoints.point.append(Data())
    an.profile[0].profilePoints.point[0].pointNum = '1'
    an.profile[0].profilePoints.point[0].distance = '-144240'
    an.profile[0].profilePoints.point[0].altitude = '6000'
    an.profile[0].profilePoints.point[0].speed = '272.3'
    an.profile[0].profilePoints.point[0].thrustSet = '345'
    an.profile[0].profilePoints.point[0].opMode = 'A'
    an.profile[0].profilePoints.point.append(Data())
    an.profile[0].profilePoints.point[1].pointNum = '2'
    an.profile[0].profilePoints.point[1].distance = '-135360'
    an.profile[0].profilePoints.point[1].altitude = '5542'
    an.profile[0].profilePoints.point[1].speed = '270.5'
    an.profile[0].profilePoints.point[1].thrustSet = '332'
    an.profile[0].profilePoints.point[1].opMode = 'A'
    
    an.profile.append(Data())
    an.profile[1].operationType = 'D'
    an.profile[1].profileGroupId = 'STANDARD'
    an.profile[1].profileStageLength = '1'
    an.profile[1].weight = '133300'
    an.profile[1].procedureSteps = Data()
    an.profile[1].procedureSteps.step = []
    an.profile[1].procedureSteps.step.append(Data())
    an.profile[1].procedureSteps.step[0].stepNum = '1'
    an.profile[1].procedureSteps.step[0].flapId = 'T_05'
    an.profile[1].procedureSteps.step[0].stepType = 'T'
    an.profile[1].procedureSteps.step[0].thrustType = 'T'
    an.profile[1].procedureSteps.step[0].param1 = '0'
    an.profile[1].procedureSteps.step[0].param2 = '0'
    an.profile[1].procedureSteps.step[0].param3 = '0'
    an.profile[1].procedureSteps.step.append(Data())
    an.profile[1].procedureSteps.step[1].stepNum = '2'
    an.profile[1].procedureSteps.step[1].flapId = 'T_05'
    an.profile[1].procedureSteps.step[1].stepType = 'T'
    an.profile[1].procedureSteps.step[1].thrustType = 'T'
    an.profile[1].procedureSteps.step[1].param1 = '1000'
    an.profile[1].procedureSteps.step[1].param2 = '0'
    an.profile[1].procedureSteps.step[1].param3 = '0'    
    
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

def mission_setup_SUAVE_climb(analyses,inputs):
    
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
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "climb_1"

    segment.analyses.extend( analyses.takeoff )

    segment.altitude_start = 0.0 
    segment.altitude_end   = 1500.0   * Units.ft
    segment.equivalent_air_speed = 170.0 * Units.kts
    segment.throttle       = 1.0

    # add to misison
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Speed, constant segment angle 
    # ------------------------------------------------------------------    

    segment = Segments.Climb.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "climb_2"

    segment.analyses.extend( analyses.cruise )

    segment.altitude_end   = 10000.0   * Units.ft
    segment.equivalent_air_speed = 250.0 * Units.kts
    segment.throttle       = 0.8

    # add to mission
    mission.append_segment(segment)
    
    segment.settings.root_finder = scipy.optimize.fsolve
    
    return mission

def mission_setup_SUAVE_descent(analyses,inputs):
    
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
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "descent_2"

    segment.analyses.extend( analyses.cruise )

    segment.altitude_start = 10000.0  * Units.ft
    segment.altitude_end   = 1500.0   * Units.ft
    segment.equivalent_air_speed = 250.0 * Units.kts
    segment.throttle       = 0.15

    # add to mission
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------
    #   Third Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "descent_3"

    segment.analyses.extend( analyses.takeoff )

    segment.altitude_end   = 0.0   * Units.ft
    segment.equivalent_air_speed = 170.0 * Units.kts
    segment.throttle       = 0.15

    # add to mission
    mission.append_segment(segment)    


    # ------------------------------------------------------------------
    #   Mission definition complete    
    # ------------------------------------------------------------------

    return mission    

def missions_setup(analyses,inputs):

    # the mission container
    missions = SUAVE.Analyses.Mission.Mission.Container()

    missions.SUAVE_climb   = mission_setup_SUAVE_climb(analyses, inputs)
    missions.SUAVE_descent = mission_setup_SUAVE_descent(analyses, inputs)

    return missions  



def write_mission_data(results,vehicle,mission,opMode):
    
    if opMode == 'A':
        opMode = 0
    elif opMode == 'D':
        opMode = 1
    elif opMode == 'L':
        opMode = 2
    else:
        print 'Warning: invalid opMode'

    starting_traj = 0
    ending_traj = len(results.segments)
    
    segment_size = 16
    
    try:
        delta_isa = mission.delta_isa
    except AttributeError:
        delta_isa = 0.0
    
    atmos = SUAVE.Analyses.Atmospheric.US_Standard_1976() 
    ref_data = atmos.compute_values(0,delta_isa)
    ref_temp = ref_data.temperature[:,0]
    ref_rho  = ref_data.density[:,0]    
    airport_elevation = mission.airport.altitude
    
    segment_tot = ending_traj-starting_traj
    segment_mat = np.zeros([segment_tot*segment_size,14])

    tot_dist = 0.0
    old_time = 0.0
    vel_old  = 0.0 # This works because the initial distance is always 0

    for i in range(starting_traj,ending_traj):    
        for j in range(len(results.segments[i].conditions.weights.total_mass)):
            mission_point = segment_size*(i-starting_traj) + j
            
            atmos = SUAVE.Analyses.Atmospheric.US_Standard_1976() 
            ref_data = atmos.compute_values(0)
            ref_temp = ref_data.temperature[:,0]
            ref_rho  = ref_data.density[:,0]                        
            
            altitude  = results.segments[i].conditions.freestream.altitude[j,0] - airport_elevation
            
            airspeed  = results.segments[i].conditions.freestream.velocity[j,0]
            TAS       = airspeed
            
            time      = results.segments[i].conditions.frames.inertial.time[j,0]
            vel_x     = results.segments[i].conditions.frames.inertial.velocity_vector[j,0]
            tot_dist  += (vel_x+vel_old)/2.*(time-old_time)
            old_time  = time*1.
            vel_old   = vel_x*1.
            
            thrust    = results.segments[i].conditions.frames.body.thrust_force_vector[j,0]
            density   = results.segments[i].conditions.freestream.density[j,0]
            net_c_thrust = thrust/(density/ref_rho)/vehicle.propulsors.turbo_fan.number_of_engines
    
            mass = results.segments[i].conditions.weights.total_mass[j,0]
            
            segment_mat[segment_size*(i-starting_traj)+j][0] = time
            segment_mat[segment_size*(i-starting_traj)+j][1] = opMode
            segment_mat[segment_size*(i-starting_traj)+j][2] = altitude / Units.ft
            segment_mat[segment_size*(i-starting_traj)+j][3] = tot_dist / Units.ft
            segment_mat[segment_size*(i-starting_traj)+j][4] = TAS / Units.kts
            segment_mat[segment_size*(i-starting_traj)+j][5] = net_c_thrust / Units.lbf 
            segment_mat[segment_size*(i-starting_traj)+j][6] = mass / Units.lb
            
            # Construct matrix


    return segment_mat


def plot_mission(results,line_style='bo-'):
    
    axis_font = {'fontname':'Arial', 'size':'14'}    

    # ------------------------------------------------------------------
    #   Aerodynamics
    # ------------------------------------------------------------------


    fig = plt.figure("Aerodynamic Forces",figsize=(8,6))
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        Lift   = -segment.conditions.frames.wind.lift_force_vector[:,2]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0] / Units.lbf
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0] / Units.lbf
        eta  = segment.conditions.propulsion.throttle[:,0]
        mdot   = segment.conditions.weights.vehicle_mass_rate[:,0]
        thrust =  segment.conditions.frames.body.thrust_force_vector[:,0]
        sfc    = 3600. * mdot / 0.1019715 / thrust	


        axes = fig.add_subplot(2,1,1)
        axes.plot( time , Thrust , line_style )
        axes.set_ylabel('Thrust (lbf)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(2,1,2)
        axes.plot( time , mdot , line_style )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('mdot (kg/s)',axis_font)
        axes.grid(True)	


    # ------------------------------------------------------------------
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    fig = plt.figure("Aerodynamic Coefficients",figsize=(8,10))
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        CLift  = segment.conditions.aerodynamics.lift_coefficient[:,0]
        CDrag  = segment.conditions.aerodynamics.drag_coefficient[:,0]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]
        aoa = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        l_d = CLift/CDrag


        axes = fig.add_subplot(3,1,1)
        axes.plot( time , CLift , line_style )
        axes.set_ylabel('Lift Coefficient',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , l_d , line_style )
        axes.set_ylabel('L/D',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,3)
        axes.plot( time , aoa , 'ro-' )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('AOA (deg)',axis_font)
        axes.grid(True)

    # ------------------------------------------------------------------
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    fig = plt.figure("Drag Components",figsize=(8,10))
    axes = plt.gca()
    for i, segment in enumerate(results.segments.values()):

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        drag_breakdown = segment.conditions.aerodynamics.drag_breakdown
        cdp = drag_breakdown.parasite.total[:,0]
        cdi = drag_breakdown.induced.total[:,0]
        cdc = drag_breakdown.compressible.total[:,0]
        cdm = drag_breakdown.miscellaneous.total[:,0]
        cd  = drag_breakdown.total[:,0]

        if line_style == 'bo-':
            axes.plot( time , cdp , 'ko-', label='CD parasite' )
            axes.plot( time , cdi , 'bo-', label='CD induced' )
            axes.plot( time , cdc , 'go-', label='CD compressibility' )
            axes.plot( time , cdm , 'yo-', label='CD miscellaneous' )
            axes.plot( time , cd  , 'ro-', label='CD total'   )
            if i == 0:
                axes.legend(loc='upper center')            
        else:
            axes.plot( time , cdp , line_style )
            axes.plot( time , cdi , line_style )
            axes.plot( time , cdc , line_style )
            axes.plot( time , cdm , line_style )
            axes.plot( time , cd  , line_style )            

    axes.set_xlabel('Time (min)')
    axes.set_ylabel('CD')
    axes.grid(True)

    # ------------------------------------------------------------------
    #   Altitude, sfc, vehicle weight
    # ------------------------------------------------------------------

    fig = plt.figure("Altitude_sfc_weight",figsize=(8,10))
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        CLift  = segment.conditions.aerodynamics.lift_coefficient[:,0]
        CDrag  = segment.conditions.aerodynamics.drag_coefficient[:,0]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]
        aoa    = segment.conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        l_d    = CLift/CDrag
        mass   = segment.conditions.weights.total_mass[:,0] / Units.lb
        altitude = segment.conditions.freestream.altitude[:,0] / Units.ft
        mdot   = segment.conditions.weights.vehicle_mass_rate[:,0]
        thrust =  segment.conditions.frames.body.thrust_force_vector[:,0]
        sfc    = 3600. * mdot / 0.1019715 / thrust	

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , altitude , line_style )
        axes.set_ylabel('Altitude (ft)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,3)
        axes.plot( time , sfc , line_style )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('sfc (lb/lbf-hr)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , mass , 'ro-' )
        axes.set_ylabel('Weight (lb)',axis_font)
        axes.grid(True)
        
    plt.show()


    return


# ----------------------------------------------------------------------
#   Call Main
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
    
    print 'Ending Mass: ' + str(mass[-1] * Units.lb) + ' kg'
     
    plt.show()

if __name__ == '__main__':
    
    base_filename = '737800_SUAVE_profile'
    
    climb, descent = main(base_filename)
    
    plot_mission(climb)
    plot_mission(descent)