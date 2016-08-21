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
from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing

import copy, time


# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main(base_filename,plot_flag = False):
    
 
    
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
    
    mass_loops = np.zeros(3)
    mass_loops[0] = maximum_mass
    mass_loops[1] = reference_mass
    mass_loops[2] = minimum_mass
    
    
    segment_speed_loop_climb   = np.zeros(3)
    segment_speed_loop_descent = np.zeros(3)
    
    segment_speed_loop_climb[0] = 290.0 * Units.kts
    segment_speed_loop_climb[1] = 280.0 * Units.kts
    segment_speed_loop_climb[2] = 300.0 * Units.kts
    
    segment_speed_loop_descent[0] = 290.0 * Units.kts
    segment_speed_loop_descent[1] = 280.0 * Units.kts
    segment_speed_loop_descent[2] = 300.0 * Units.kts    
    
    isa_loop = np.zeros(2)
    isa_loop[0] = 10.0
    isa_loop[1] = 20.0
    
    vehicle_inputs = Data()
    
    segment3 = Data()
    segment4 = Data()
    segment5 = Data()
    
    count = 0
    
    # Standard values
    
    segment3.altitude_end   = 30000.0 * Units.ft  
    
    segment4.air_speed      = 230.412 
    segment4.distance       = 3933.65  
    
    segment5.altitude_end   = 10000.0 * Units.ft   
    
    mission_inputs = Data()
    mission_inputs.segment3 = segment3
    mission_inputs.segment4 = segment4  

    # ----------------------------------------------------------------------
    # ISA climb (9 segments, 3 masses and 3 speeds)
    print 'ISA climb segments:'
    for imass in range(0,len(mass_loops)):
            for iseg in range(0,len(segment_speed_loop_climb)):
                
                # Primary inputs
                vehicle_inputs.tow = mass_loops[imass]
                mission_inputs.delta_isa = 0.0
                segment3.equivalent_air_speed      = segment_speed_loop_climb[iseg]
                segment5.equivalent_air_speed      = segment_speed_loop_descent[0]     
            
                mission_inputs.segment3 = segment3
                mission_inputs.segment5 = segment5
            
                configs, analyses,vehicle = full_setup(mission_inputs,vehicle_inputs)
                
                simple_sizing(configs)
                
                configs.finalize()
                analyses.finalize()
                
                # mission analysis

                print count+1,vehicle_inputs.tow,segment3.equivalent_air_speed/Units.kts,segment5.equivalent_air_speed/Units.kts,mission_inputs.delta_isa
                
                mission = analyses.missions.base
                results = mission.evaluate()
                
 
                
                segment_mat = write_mission_data(results,vehicle,"climb",count)
                if count == 0:
                    mission_mat = segment_mat*1.
                else:
                    mission_mat = np.vstack([mission_mat,segment_mat])
                count  = count + 1
                plot_mission(results)
             
    climb_ISA_mat = mission_mat*1.0   
    count = 0
               
    # ----------------------------------------------------------------------     
    # ISA descent (3 segments, reference mass and 3 speeds)
    print 'ISA descent segments:'
    for iseg in range(0,len(segment_speed_loop_descent)):
          
        # Primary inputs      
        vehicle_inputs.tow = reference_mass
        mission_inputs.delta_isa = 0.0
        segment3.equivalent_air_speed      = segment_speed_loop_climb[0]
        segment5.equivalent_air_speed      = segment_speed_loop_descent[iseg] #170.0  
    
        mission_inputs.segment3 = segment3
        mission_inputs.segment5 = segment5
    
        configs, analyses,vehicle = full_setup(mission_inputs,vehicle_inputs)
        
        simple_sizing(configs)
        
        configs.finalize()
        analyses.finalize()
        
        print count+1,vehicle_inputs.tow,segment3.equivalent_air_speed/Units.kts,segment5.equivalent_air_speed/Units.kts,mission_inputs.delta_isa        
        
        # mission analysis
        mission = analyses.missions.base
        results = mission.evaluate()
        
        segment_mat = write_mission_data(results,vehicle,"descent",count)
        if count == 0:
            mission_mat = segment_mat*1.
        else:
            mission_mat = np.vstack([mission_mat,segment_mat])
        count  = count + 1 
        plot_mission(results)
                    
    descent_mat = mission_mat*1.0   
    count = 0    
        
    # ----------------------------------------------------------------------            
    # non-ISA climb (6 segments, 3 masses and 2 non-ISA temperatures)
    print 'non-ISA climb segments:'
    for imass in range(0,len(mass_loops)):
        for k in range(0,len( isa_loop)):
                
            # Primary inputs
            vehicle_inputs.tow = mass_loops[imass]
            mission_inputs.delta_isa = isa_loop[k]          
            segment3.equivalent_air_speed      = segment_speed_loop_climb[0]
            segment5.equivalent_air_speed      = segment_speed_loop_descent[0]
                
            mission_inputs.segment3 = segment3
            mission_inputs.segment5 = segment5
        
            configs, analyses,vehicle = full_setup(mission_inputs,vehicle_inputs)
            
            simple_sizing(configs)
            
            configs.finalize()
            analyses.finalize()
            
            print count+1,vehicle_inputs.tow,segment3.equivalent_air_speed/Units.kts,segment5.equivalent_air_speed/Units.kts,mission_inputs.delta_isa             
            
            # mission analysis
            mission = analyses.missions.base
            results = mission.evaluate()
            
            segment_mat = write_mission_data(results,vehicle,"climb",count)
            segment_mat[:,9] = isa_loop[k]
            if count == 0:
                mission_mat = segment_mat*1.
            else:
                mission_mat = np.vstack([mission_mat,segment_mat])
            count  = count + 1
            plot_mission(results)
                    
    climb_nonISA_mat = mission_mat*1.0   
    count = 0             
         
    # ----------------------------------------------------------------------           
    # ISA cruise (1 segment, reference mass and speed)
    print 'ISA cruise segment:'
                
    # Primary Inputs
    vehicle_inputs.tow = reference_mass
    mission_inputs.delta_isa = 0.0
    segment3.equivalent_air_speed      = segment_speed_loop_climb[0]
    segment5.equivalent_air_speed      = segment_speed_loop_descent[0]

    mission_inputs.segment3 = segment3
    mission_inputs.segment5 = segment5

    configs, analyses,vehicle = full_setup(mission_inputs,vehicle_inputs)
    
    simple_sizing(configs)
    
    configs.finalize()
    analyses.finalize()
    
    print count+1,vehicle_inputs.tow,segment3.equivalent_air_speed/Units.kts,segment5.equivalent_air_speed/Units.kts,mission_inputs.delta_isa     
    
    # mission analysis
    mission = analyses.missions.base
    results = mission.evaluate()
    
    segment_mat = write_mission_data(results,vehicle,"cruise",count)
    mission_mat = segment_mat*1.    
                    
    cruise_mat = mission_mat*1.0   
    plot_mission(results)
    # ----------------------------------------------------------------------
    
    #np.save('climb_ISA.npy',climb_ISA_mat)
    #np.save('climb_nonISA.npy',climb_nonISA_mat)
    #np.save('descent.npy',descent_mat)
    #np.save('cruise.npy',cruise_mat)
    
    np.save('bada3_' + base_filename + '_climbISA.npy',climb_ISA_mat)
    np.save('bada3_' + base_filename + '_climbNonISA.npy',climb_nonISA_mat)
    np.save('bada3_' + base_filename + '_descent.npy',descent_mat)
    np.save('bada3_' + base_filename + '_cruise.npy',cruise_mat)
    
    if plot_flag == True:
        plt.show()    
                    
    return (climb_ISA_mat,climb_nonISA_mat,descent_mat,cruise_mat)




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
    mission  = mission_setup(configs_analyses,mission_inputs)
    missions_analyses = missions_setup(mission)

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

    fuselage.areas.side_projected  = 142.1948
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
    #   BADA Data
    # ------------------------------------------------------------------     
    
    vehicle.BADA = Data()
    bd = vehicle.BADA
    
    bd.badaAirplaneId = '737800T2'   # used for all sections
    
    bd.mfgDescription = 'B737-800T    with NA engines'                        
    bd.numEngines = '2' 
    bd.engineTypeCode = 'J' 
    bd.wakeCategory = 'M' 
    bd.referenceAircraftMass = '65.3' 
    bd.minAircraftMass = '41.15' 
    bd.maxAircraftMass = '78.3' 
    bd.maxPayloadMass = '20.3' 
    bd.weightGradient = '0.26974' 
    bd.maxOperatingSpeed = '340' 
    bd.maxOperatingMachNumber = '0.82' 
    bd.maxOperatingAltitude = '41000' 
    bd.maxAltitudeAtMaxTakeoffWeight = '34982' 
    bd.temperatureGradientOnMaximumAltitude = '-54.1' 
    bd.wingSurfaceArea = '124.65' 
    bd.buffetOnsetLiftCoeff = '1.2454' 
    bd.buffetingGradient = '0.55567' 
    bd.machDragCoeff = '0' 
    
    bd.altitudeCount = [] 
    bd.distanceMean = [] 
    bd.distanceStddev = [] 
    bd.distanceLow = [] 
    bd.distanceHigh = [] 
    bd.altitude = []
    
    # Base values may be listed in vehicle file
    bd.altitudeCount.append('26415')
    bd.distanceMean.append('1191.3')
    bd.distanceStddev.append('502.7')
    bd.distanceLow.append('201.6')
    bd.distanceHigh.append('4253.6')
    bd.altitude.append('35000')    
    
    bd.massRangeValue = [] 
    bd.companyCode1 = [] 
    bd.companyCode2 = [] 
    bd.companyName = [] 
    bd.aircraftVersion = [] 
    bd.engine = [] 
    bd.climbSpeedBelowTransitionAltitude = [] 
    bd.climbSpeedAboveTransitionAltitude = [] 
    bd.climbMachNumber = [] 
    bd.cruiseSpeedBelowTransitionAltitude = [] 
    bd.cruiseSpeedAboveTransitionAltitude = [] 
    bd.cruiseMachNumber = [] 
    bd.descentSpeedUnderTransitionAltitude = [] 
    bd.descentSpeedOverTransitionAltitude = [] 
    bd.descentMachNumber = [] 
    
    # Base values may be listed in vehicle file
    bd.massRangeValue.append('AV')
    bd.companyCode1.append('***')
    bd.companyCode2.append('**')
    bd.companyName.append('201.6')
    bd.aircraftVersion.append('4253.6')
    bd.engine.append('*******')
    bd.climbSpeedBelowTransitionAltitude.append('300')
    bd.climbSpeedAboveTransitionAltitude.append('300')
    bd.climbMachNumber.append('0.78')
    bd.cruiseSpeedBelowTransitionAltitude.append('280')
    bd.cruiseSpeedAboveTransitionAltitude.append('280')
    bd.cruiseMachNumber.append('0.78')
    bd.descentSpeedUnderTransitionAltitude.append('290')
    bd.descentSpeedOverTransitionAltitude.append('290')
    bd.descentMachNumber.append('0.78')    
    
    bd.descentAlt = '1000' 
    bd.descentSpeed = '280' 
    bd.descentMach = '0.78' 
    
    bd.description = 'export' 
    bd.airframeModel = 'Boeing 737-800T Series' 
    bd.engineCode = '4CM039' 
    bd.engineModCode = 'NONE' 
    bd.anpAirplaneId = '737800T' 
    
    bd.transEnergyShare = '0.3'     
    
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
    analyses.takeoff.aerodynamics.settings.drag_coefficient_increment = 0.0000
    
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
    
def mission_setup(analyses,inputs):
    
    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------
    
    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'the_mission'
    
    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  inputs.delta_isa
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    
    mission.airport = airport
    
    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments
    
    # base segment
    base_segment = Segments.Segment()    
    
    
    # ------------------------------------------------------------------
    #   Climb
    # ------------------------------------------------------------------    
    
    segment = Segments.Climb.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "climb_3"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_start = 10000.0 * Units.ft
    segment.altitude_end = inputs.segment3.altitude_end
    segment.equivalent_air_speed    = inputs.segment3.equivalent_air_speed
    segment.throttle       = 1.0
    segment.temperature_deviation = inputs.delta_isa
    
    # add to mission
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------    
    #   Cruise
    # ------------------------------------------------------------------    
    
    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.air_speed  = inputs.segment4.air_speed
    segment.distance   = 3933.65 * Units.km
    segment.temperature_deviation = inputs.delta_isa
        
    mission.append_segment(segment)
    
    
    # ------------------------------------------------------------------    
    #   Descent
    # ------------------------------------------------------------------    
    
    segment = Segments.Descent.Constant_Throttle_Constant_EAS(base_segment)
    segment.tag = "descent_1"
    
    segment.analyses.extend( analyses.cruise )
    
    segment.altitude_end = 10000.0 * Units.ft # 5.0   * Units.km
    segment.equivalent_air_speed    = inputs.segment5.equivalent_air_speed
    segment.throttle     = .15
    segment.temperature_deviation = inputs.delta_isa
    
    # add to mission
    mission.append_segment(segment)
    
    # ------------------------------------------------------------------    
    #   Mission definition complete    
    # ------------------------------------------------------------------
    
    return mission



# ----------------------------------------------------------------------
#   Various Missions
# ----------------------------------------------------------------------
    
def missions_setup(base_mission):

    # the mission container
    missions = SUAVE.Analyses.Mission.Mission.Container()
    
    # ------------------------------------------------------------------
    #   Base Mission
    # ------------------------------------------------------------------
    
    missions.base = base_mission

    return missions  



def write_mission_data(results,vehicle,trajectory_type,count):
    

    starting_traj = 0
    ending_traj = 0
    
    
    if(trajectory_type == "climb"):
        starting_traj = 0
        ending_traj = 1
        
        
    elif(trajectory_type == "cruise"):
        starting_traj = 1
        ending_traj = 2
        
        
    elif(trajectory_type == "descent"):
        starting_traj = 2
        ending_traj = 3
    
    segment_tot = ending_traj-starting_traj
    segment_mat = np.zeros([segment_tot*16,14])
    
    postive_climb = True
    
    #DATASET  NO #TOW #weight #xpos #zpos #speed #thrust #cdi  #cdp  #cdc  #cd #cl #drag #lift
    #for i in range(len(results.segments)):
    for i in range(starting_traj,ending_traj):    
        for j in range(len(results.segments[i].conditions.weights.total_mass)):
            segment_num = count
            mission_point = 16*(i-starting_traj) + j
            
            time   = results.segments[i].conditions.frames.inertial.time[j,0]
            altitude = results.segments[i].conditions.freestream.altitude[j,0] / Units.ft
            if j == 0:
                altitude_p = results.segments[i].conditions.freestream.altitude[j+1,0] / Units.ft
                time_p     = results.segments[i].conditions.frames.inertial.time[j+1,0]
                climb_rate = (altitude_p-altitude)/(time_p-time) * Units.min
            elif j == 15:
                altitude_m = results.segments[i].conditions.freestream.altitude[j-1,0] / Units.ft
                time_m     = results.segments[i].conditions.frames.inertial.time[j-1,0]   
                climb_rate = (altitude-altitude_m)/(time-time_m) * Units.min
            else:
                altitude_p = results.segments[i].conditions.freestream.altitude[j+1,0] / Units.ft
                time_p     = results.segments[i].conditions.frames.inertial.time[j+1,0]   
                altitude_m = results.segments[i].conditions.freestream.altitude[j-1,0] / Units.ft
                time_m     = results.segments[i].conditions.frames.inertial.time[j-1,0]  
                climb_rate = (altitude_p-altitude_m)/(time_p-time_m) * Units.min    
            #climb_rate = -results.segments[i].conditions.frames.inertial.velocity_vector[j,2] / (Units.ft/Units.min) # need new info on units used here
            density    = results.segments[i].conditions.freestream.density[j,0]
            velocity = results.segments[i].conditions.freestream.velocity[j,0] / Units.kts
            mach_number = results.segments[i].conditions.freestream.mach_number[j,0] 
            temperature = results.segments[i].conditions.freestream.temperature[j,0] 
                        
            mass = results.segments[i].conditions.weights.total_mass[j,0]
            mass_rate = results.segments[i].conditions.weights.vehicle_mass_rate[j,0]
            
            thrust    = results.segments[i].conditions.frames.body.thrust_force_vector[j,0]
            
            segment_mat[16*(i-starting_traj)+j][0] = segment_num
            segment_mat[16*(i-starting_traj)+j][1] = mission_point
            segment_mat[16*(i-starting_traj)+j][2] = time
            segment_mat[16*(i-starting_traj)+j][3] = altitude
            segment_mat[16*(i-starting_traj)+j][4] = climb_rate
            if (climb_rate < 0) and (trajectory_type == "climb"):
                postive_climb = False
            segment_mat[16*(i-starting_traj)+j][5] = density
            segment_mat[16*(i-starting_traj)+j][6] = velocity
            segment_mat[16*(i-starting_traj)+j][7] = mach_number
            segment_mat[16*(i-starting_traj)+j][8] = temperature
            #segment_mat[16*(i-starting_traj)+j][9] = delta_isa (this is modified in the main function since it is not part of the results) 
            segment_mat[16*(i-starting_traj)+j][10] = mass
            segment_mat[16*(i-starting_traj)+j][11] = mass_rate
            segment_mat[16*(i-starting_traj)+j][12] = 1 # indicates constant airspeed segments (all currently included are constant airspeed)
            segment_mat[16*(i-starting_traj)+j][13] = thrust
            
    #fig = plt.figure("Rate of Climb")
    #axes = fig.add_subplot(1,1,1)
    #axes.plot( segment_mat[16*0:16*1,2] , segment_mat[16*0:16*1,4], 'r-' )
    #axes.set_xlabel('Mission Time (s)')
    #axes.set_ylabel('Rate of Climb (fpm)')
    #axes.grid(True)
    #axes.legend(['AEDT Provided Climb','AEDT Provided Descent','Calculated Climb','Calculated Descent'])  
    #axes.legend(['SUAVE Provided Climb','Calculated Climb'])      
            
    #plt.show()
            # Construct matrix


    if postive_climb == False:
        print 'Warning: Negative climb rate in climb segment', segment_num
    return segment_mat



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
    
    #print 'Ending Mass: ' + str(mass[-1] * Units.lb) + ' kg'

# ----------------------------------------------------------------------
#   Call Main
# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    base_filename = '737800_profile_test'
    
    plot_flag = True
    
    main(base_filename,plot_flag)