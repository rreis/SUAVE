# as2_fc_full_setup.py
# 
# Created:  Tim MacDonald, 1/27/15
# Modified: Tim MacDonald, 1/27/15

""" evaluate a mission with an AS2
"""


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
import time
from SUAVE.Core import Units

import numpy as np
import scipy as sp
from scipy import integrate
import pylab as plt

from SUAVE.Core import (
Data, Container, Data_Exception, Data_Warning,
)

import copy, time

# ----------------------------------------------------------------------
#   Vehicle Setup
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

    return configs, analyses

# ----------------------------------------------------------------------
#   Define the Vehicle
# ----------------------------------------------------------------------

def vehicle_setup():

    # ------------------------------------------------------------------
    #   Initialize the Vehicle
    # ------------------------------------------------------------------    

    vehicle = SUAVE.Vehicle()
    vehicle.tag = 'Aerion AS2'


    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    

    # mass properties
    # ------------------------------------------------------------------
    # Vehicle-level Properties
    # ------------------------------------------------------------------

    n_select = 3
    if n_select == 0:
        vehicle_propellant = SUAVE.Attributes.Propellants.Jet_A()
        vehicle.mass_properties.max_takeoff     = 53000 # kg
        vehicle.mass_properties.operating_empty = 22500 # kg
        vehicle.mass_properties.takeoff         = 52000 # kg
    elif n_select == 1:
        vehicle_propellant = SUAVE.Attributes.Propellants.Jet_A()
        vehicle.mass_properties.max_takeoff     = 73000 # kg
        vehicle.mass_properties.operating_empty = 42000 # kg
        vehicle.mass_properties.takeoff         = 72000 # kg
    elif n_select == 2:
        vehicle_propellant = SUAVE.Attributes.Propellants.Liquid_Natural_Gas()
        vehicle.mass_properties.max_takeoff     = 67000 # kg
        vehicle.mass_properties.operating_empty = 42000 # kg
        vehicle.mass_properties.takeoff         = 66000 # kg
    elif n_select == 3:
        vehicle_propellant = SUAVE.Attributes.Propellants.Liquid_H2()
        vehicle.mass_properties.max_takeoff     = 53000 # kg
        vehicle.mass_properties.operating_empty = 42000 # kg
        vehicle.mass_properties.takeoff         = 52000 # kg
        # mass properties
        # 53000 / 22500 base weight
        # 71000 / 40500 with fuel cell using Jet A
        # 65000 / 40500 with fuel cell using LNG
        # 51000 / 40500 with fuel cell using LH2

    vehicle.mass_properties.center_of_gravity         = [26.3 * Units.feet, 0, 0]
    vehicle.mass_properties.moments_of_inertia.tensor = [[10 ** 5, 0, 0],[0, 10 ** 6, 0,],[0,0, 10 ** 7]] # Not Correct

    # envelope properties
    vehicle.envelope.ultimate_load = 3.5
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area       = 124.862       
    vehicle.passengers           = 8
    vehicle.systems.control      = "fully powered" 
    vehicle.systems.accessories  = "long range"


    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------        

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'main_wing'
    wing.areas.reference = 125.4    #
    wing.aspect_ratio    = 3.63     #
    wing.spans.projected = 21.0     #
    wing.sweep           = 0 * Units.deg
    wing.symmetric       = True
    wing.thickness_to_chord = 0.03
    wing.taper           = 0.7

    # size the wing planform
    SUAVE.Geometry.Two_Dimensional.Planform.wing_planform(wing)

    # size the wing planform ----------------------------------
    # These can be determined by the wing sizing function
    # Note that the wing sizing function will overwrite span
    wing.chords.root  = 12.9
    wing.chords.tip   = 1.0
    wing.areas.wetted = wing.areas.reference*2.0 
    # The span that would normally be overwritten here doesn't match
    # ---------------------------------------------------------    

    wing.chords.mean_aerodynamic = 7.0
    wing.areas.exposed = 0.8*wing.areas.wetted
    wing.areas.affected = 0.6*wing.areas.wetted
    wing.span_efficiency = 0.74
    wing.twists.root = 0.0*Units.degrees
    wing.twists.tip  = 2.0*Units.degrees
    wing.origin             = [20,0,0]
    wing.aerodynamic_center = [3,0,0]     
    wing.vertical = False

    wing.high_lift    = False                 #
    wing.high_mach    = True
    wing.vortex_lift  = False
    wing.transition_x_upper = 0.9
    wing.transition_x_lower = 0.9
    wing.dynamic_pressure_ratio  = 1.0

    #print wing
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------        
    #   Horizontal Stabilizer
    # ------------------------------------------------------------------        

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'horizontal_stabilizer'


    wing.areas.reference = 24.5     #
    wing.aspect_ratio    = 2.0      #
    wing.spans.projected = 7.0      #
    wing.sweep           = 0 * Units.deg
    wing.symmetric       = True
    wing.thickness_to_chord = 0.03
    wing.taper           = 0.5

    # size the wing planform
    SUAVE.Geometry.Two_Dimensional.Planform.wing_planform(wing)

    wing.chords.mean_aerodynamic = 3.0
    wing.areas.exposed = 0.8*wing.areas.wetted
    wing.areas.affected = 0.6*wing.areas.wetted
    wing.span_efficiency = 0.74
    wing.twists.root = 0.0*Units.degrees
    wing.twists.tip  = 2.0*Units.degrees
    wing.vertical = False

    wing.high_lift    = False                 #
    wing.high_mach    = True
    wing.vortex_lift  = False
    wing.transition_x_upper = 0.9
    wing.transition_x_lower = 0.9
    wing.dynamic_pressure_ratio  = 1.0

    #print wing
    # add to vehicle
    vehicle.append_component(wing)    


    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'vertical_stabilizer'    

    wing.areas.reference = 33.91    #
    wing.aspect_ratio    = 1.3      #
    wing.spans.projected = 3.5      #
    wing.sweep           = 45 * Units.deg
    wing.symmetric       = False
    wing.thickness_to_chord = 0.04
    wing.taper           = 0.5

    # size the wing planform
    SUAVE.Geometry.Two_Dimensional.Planform.wing_planform(wing)

    wing.chords.mean_aerodynamic = 4.2
    wing.areas.exposed = 1.0*wing.areas.wetted
    wing.areas.affected = 0.0*wing.areas.wetted
    wing.span_efficiency = 0.9
    wing.twists.root = 0.0*Units.degrees
    wing.twists.tip  = 0.0*Units.degrees

    wing.vertical   = True 
    wing.t_tail     = False
    wing.eta         = 1.0

    wing.high_lift    = False                 #
    wing.high_mach    = True
    wing.vortex_lift  = False
    wing.vertical = True
    wing.transition_x_upper = 0.9
    wing.transition_x_lower = 0.9 
    wing.dynamic_pressure_ratio  = 1.0


    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------

    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'fuselage'

    fuselage.number_coach_seats = 0
    fuselage.seats_abreast = 2
    fuselage.seat_pitch = 0
    fuselage.fineness.nose = 4.0
    fuselage.fineness.tail = 4.0
    fuselage.lengths.fore_space = 16.3
    fuselage.lengths.aft_space  = 16.3
    fuselage.width = 2.35
    fuselage.heights.maximum = 2.55
    fuselage.heights.at_quarter_length          = 4. # Not correct
    fuselage.heights.at_three_quarters_length   = 4. # Not correct
    fuselage.heights.at_wing_root_quarter_chord = 4. # Not correct

    fuselage.areas.side_projected  = 4.* 59.8 #  Not correct
    fuselage.areas.front_projected = 12.57

    fuselage.effective_diameter    = 4.0

    fuselage.differential_pressure = 10**5 * Units.pascal    # Maximum differential pressure

    # size fuselage planform
    SUAVE.Geometry.Two_Dimensional.Planform.fuselage_planform(fuselage)

    fuselage.areas.wetted = 615.0

    # add to vehicle
    vehicle.append_component(fuselage)


    # ------------------------------------------------------------------
    # Ducted Fan / Fuel Cell Model
    # ------------------------------------------------------------------

    net = SUAVE.Components.Energy.Networks.Fuel_Cell_Network()

    net.tag        = 'turbo_fan'
    net.fuel_cell  = Data()
    net.motor	   = Data()
    net.propulsor  = Data()
    net.propellant = vehicle_propellant
    net.fuel_cell.propellant = vehicle_propellant
    net.fuel_cell.efficiency = 0.8
    net.fuel_cell.max_mdot = 1.0
    net.motor.efficiency = 0.95
    net.propulsor.A0 = (.5)**2*np.pi
    net.engine_length = 8.0
    net.number_of_engines    = 3.0
    net.nacelle_diameter = (.5)*2

    # vehicle.append_component(net)

    # ------------------------------------------------------------------
    #   Simple Propulsion Model
    # ------------------------------------------------------------------     

    vehicle.propulsors.append(net)
    #vehicle.propulsion_model = net


    # ------------------------------------------------------------------
    #   Vehicle Definition Complete
    # ------------------------------------------------------------------

    return vehicle

# ----------------------------------------------------------------------
#   Define the Configurations
# ----------------------------------------------------------------------

def configs_setup(vehicle):

############################ Not updated 1/27/15 ################    

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

    # no equations!
    ## config.mass_properties.landing = 0.85 * vehicle.mass_properties.takeoff

    configs.append(config)


    # done!
    return configs 

#############################^^^^^ Not updated 1/27/15 ###########

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
    analyses.takeoff.aerodynamics.drag_coefficient_increment = 0.1000

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
    aerodynamics = SUAVE.Analyses.Aerodynamics.Supersonic_Zero()
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Stability Analysis
    stability = SUAVE.Analyses.Stability.Fidelity_Zero()
    stability.geometry = vehicle
    analyses.append(stability)

    # ------------------------------------------------------------------
    #  Propulsion Analysis
    propulsion = SUAVE.Analyses.Energy.Propulsion()
    propulsion.vehicle = vehicle
    analyses.append(propulsion)

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

def mission_setup(analyses):


    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Analyses.Missions.Mission()
    mission.tag = 'the_mission'

    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()

    mission.airport = airport    

    # unpack Segments module
    Segments = SUAVE.Analyses.Missions.Segments

        # base segment
    base_segment = Segments.Segment()

    # ------------------------------------------------------------------
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    
    # was previously climb 6
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )


    segment.altitude_start = 0.0    * Units.km
    segment.altitude_end = 3.05     * Units.km
    segment.air_speed    = 128.6    * Units['m/s']
    segment.climb_rate   = 4000    * Units['ft/min']

    # add to mission
    mission.append_segment(segment)     

    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    
    # was previously climb 7
    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2"


    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise ) 

    segment.altitude_end = 4.57     * Units.km
    segment.air_speed    = 205.8    * Units['m/s']
    segment.climb_rate   = 1000    * Units['ft/min']

    # add to mission
    mission.append_segment(segment) 

    # ------------------------------------------------------------------
    #   Third Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    
    # was previously climb 8
    segment = Segments.Climb.Linear_Mach_Constant_Rate(base_segment)
    #segment = SUAVE.Attributes.Missions.Segments.Climb.Linear_Mach_Constant_Rate()
    segment.tag = "climb_3"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    segment.altitude_end = 9.77 * Units.km # 
    segment.mach_number_start = 0.64
    segment.mach_number_end  = 1.0 
    segment.climb_rate   = 1000    * Units['ft/min']

    # add to mission
    mission.append_segment(segment)  

    # ------------------------------------------------------------------
    #   Fourth Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    
    # was climb 9
    segment = Segments.Climb.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "climb_4"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    segment.altitude_end = 12.95 * Units.km # 51000 ft
    segment.mach_number_start = 1.0
    segment.mach_number_end  = 1.22
    segment.climb_rate   = 1000    * Units['ft/min']

    # add to mission
    mission.append_segment(segment)  

    # ------------------------------------------------------------------
    #   Fifth Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    
    # was climb 10
    segment = Segments.Climb.Linear_Mach_Constant_Rate(base_segment)
    segment.tag = "climb_5"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )


    segment.altitude_end = 15.54 * Units.km # 51000 ft
    segment.mach_number_start = 1.22
    segment.mach_number_end  = 1.4
    segment.climb_rate   = 200    * Units['ft/min']

    # add to mission
    mission.append_segment(segment) 


    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------    

    segment = Segments.Cruise.Constant_Mach_Constant_Altitude(base_segment)
    #segment = SUAVE.Attributes.Missions.Segments.Cruise.Constant_Mach_Constant_Altitude()
    segment.tag = "cruise"

    segment.analyses.extend( analyses.cruise )


    segment.altitude   = 15.54  * Units.km     # Optional
    segment.mach       = 1.4
    # 1687 for 3000 nmi

    desired_range = 2000.0
    cruise_dist = desired_range - 1313.0
    segment.distance   = cruise_dist * Units.nmi

    mission.append_segment(segment)

    # ------------------------------------------------------------------    
    #   First Descent Segment: constant mach, constant descent rate
    # ------------------------------------------------------------------    

    segment = Segments.Descent.Linear_Mach_Constant_Rate(base_segment)
    #segment = SUAVE.Attributes.Missions.Segments.Descent.Linear_Mach_Constant_Rate()
    segment.tag = "descent_1"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )


    segment.altitude_end = 6.8  * Units.km
    segment.mach_number_start = 1.4
    segment.mach_number_end = 1.0
    segment.descent_rate = 5.0   * Units['m/s']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------    
    #   Second Descent Segment: constant mach, constant descent rate
    # ------------------------------------------------------------------    

    segment = Segments.Descent.Linear_Mach_Constant_Rate(base_segment)
    #segment = SUAVE.Attributes.Missions.Segments.Descent.Linear_Mach_Constant_Rate()
    segment.tag = "descent_2"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )


    segment.altitude_end = 3.0  * Units.km
    segment.mach_number_start = 1.0
    segment.mach_number_end = 0.65
    segment.descent_rate = 5.0   * Units['m/s']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------    
    #   Third Descent Segment: constant mach, constant descent rate
    # ------------------------------------------------------------------    
        # was descent 3

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )   

    segment.altitude_end = 0.0   * Units.km
    segment.air_speed    = 130.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']

    # append to mission
    mission.append_segment(segment)       


    # ------------------------------------------------------------------    
    #   Mission definition complete    
    # ------------------------------------------------------------------

    return mission

#: def define_mission()    

def missions_setup(base_mission):

    # the mission container
    missions = SUAVE.Analyses.Missions.Mission.Container()

    # ------------------------------------------------------------------
    #   Base Mission
    # ------------------------------------------------------------------

    missions.base = base_mission


    # ------------------------------------------------------------------
    #   Mission for Constrained Fuel
    # ------------------------------------------------------------------    

    fuel_mission = SUAVE.Analyses.Missions.Mission() #Fuel_Constrained()
    fuel_mission.tag = 'fuel'
    fuel_mission.mission = base_mission
    missions.append(fuel_mission)


    # ------------------------------------------------------------------
    #   Mission for Constrained Short Field
    # ------------------------------------------------------------------

    short_field = SUAVE.Analyses.Missions.Mission() #Short_Field_Constrained()
    short_field.tag = 'short_field'
    short_field.mission = base_mission
    missions.append(short_field)


    # ------------------------------------------------------------------
    #   Mission for Fixed Payload
    # ------------------------------------------------------------------    

    payload = SUAVE.Analyses.Missions.Mission() #Payload_Constrained()
    payload.tag = 'payload'
    payload.mission = base_mission
    missions.append(payload)


    # done!
    return missions    