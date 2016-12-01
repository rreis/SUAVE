# full_setup.py
#
# Created:  SUave Team, Aug 2014
# Modified:

""" setup file for a mission with a E190
"""


# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Units

import numpy as np
import pylab as plt

import copy, time, os

from SUAVE.Core import (
Data, Container, Data_Exception, Data_Warning,
)

# the analysis functions

from SUAVE.Methods.Performance  import payload_range

from SUAVE.Methods.Propulsion.turbofan_sizing import turbofan_sizing
from SUAVE.Methods.Geometry.Three_Dimensional.find_tip_chord_leading_edge import find_tip_chord_leading_edge

from SUAVE.Methods.fea_tools.geomach_geometry import geometry_generation
from SUAVE.Methods.fea_tools.weight_estimation import FEA_Weight
from SUAVE.Methods.fea_tools.weight_estimation import Filenames
# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------

def main():

    # define the problem
    configs, analyses = full_setup()

    configs.finalize()
    analyses.finalize()    
    

    # mission analysis
    mission = analyses.missions
    #results = mission.evaluate()
    
    configs.base.type ='Conventional'
    external = analyses.configs.base.external
    aircraft_external = external.evaluate()
    
    #geometry computation
    geometry = analyses.configs.base.geometry
    aircraft_geometry = geometry.evaluate()
    
    #weight analysis
    weights = analyses.configs.base.weights
    breakdown = weights.evaluate()
    
    #mission analysis
    mission = analyses.missions
    results = mission.evaluate()

    #geometry_generation(configs.base,0,0,'E190.stl') #two dummy variables in script right now
    #setup_nastran(configs.base)
    
    # plt the old results
    #plot_mission(results)
    

    return

'''    
def setup_nastran(vehicle):
    external = SUAVE.Analyses.External.UADF()
    
    filenames = Filenames()
    
    filenames.Nastran_sol200 = "conventional_opt.bdf"
    filenames.Nastran_f06 = "conventional_opt.f06"
    filenames.geomach_output = "conventional_str.bdf"
    filenames.geomach_structural_surface_grid_points = "pt_str_surf.dat"
    filenames.geomach_stl_mesh = 'conventional.stl'
    filenames.tacs_load = "geomach_tacs_load_conventional.txt"
    filenames.aero_load = "geomach_load_aero.txt"
    filenames.tacs_optimization_driver = "geomach_tacs_opt_driver.txt"
    local_dir = os.getcwd()
    SBW_wing = FEA_Weight(filenames,local_dir)
    
    #the nastran path on zion" 
    SBW_wing.nastran_path ="/opt/MSC.Software/NASTRAN/bin/msc20131"  #"nastran" #"nast20140"
    external.vehicle  = vehicle
    external.external = SBW_wing
    
    SBW_wing = FEA_Weight(filenames,local_dir)
    analyses.append(external)
    return
    
'''    
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

    analyses = SUAVE.Analyses.Analysis.Container()
    analyses.configs  = configs_analyses
    analyses.missions = mission
   
    
    return configs, analyses


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
    #  External Module
    external = SUAVE.Analyses.External.UADF()
    
    filenames = Filenames()
    
    filenames.Nastran_sol200 = "conventional_opt.bdf"
    filenames.Nastran_f06 = "conventional_opt.f06"
    filenames.geomach_output = "conventional_str.bdf"
    filenames.geomach_structural_surface_grid_points = "pt_str_surf.dat"
    filenames.geomach_stl_mesh = 'conventional.stl'
    filenames.tacs_load = "geomach_tacs_load_conventional.txt"
    filenames.aero_load = "geomach_load_aero.txt"
    filenames.tacs_optimization_driver = "geomach_tacs_opt_driver.txt"
    local_dir = os.getcwd()
    SBW_wing = FEA_Weight(filenames,local_dir)
    
    #the nastran path on zion" 
    SBW_wing.nastran_path ="/opt/MSC.Software/NASTRAN/bin/msc20131"  #"nastran" #"nast20140"
    
    external.vehicle  = vehicle
    external.external = SBW_wing
    analyses.append(external)
    
    # ------------------------------------------------------------------
    #  Basic Geometry Relations
    sizing = SUAVE.Analyses.Sizing.Sizing()
    sizing.features.vehicle = vehicle
    
    analyses.append(sizing)
    
    # Geometry specify
    geometry = SUAVE.Analyses.Geometry.UADF()
    #geometry = SUAVE.Analyses.Geometry.Geometry()
    geometry.vehicle = vehicle
    geometry.external = external.external
    analyses.append(geometry)
    
    # ------------------------------------------------------------------
    #  Weights
    #weights = SUAVE.Analyses.Weights.Weights()
    
    weights = SUAVE.Analyses.Weights.UADF()
    weights.vehicle = vehicle
    weights.external = external.external
    analyses.append(weights)

#    # ------------------------------------------------------------------
#    #  Basic Geometry Relations
#    sizing = SUAVE.Analyses.Sizing.Sizing()
#    sizing.features.vehicle = vehicle
#    analyses.append(sizing)
#
#    # ------------------------------------------------------------------
#    #  Weights
#    weights = SUAVE.Analyses.Weights.Weights()
#    weights.vehicle = vehicle
#    analyses.append(weights)

    # ------------------------------------------------------------------
    #  Aerodynamics Analysis
    aerodynamics = SUAVE.Analyses.Aerodynamics.Fidelity_Zero()
    aerodynamics.geometry = vehicle
    aerodynamics.settings.drag_coefficient_increment = 0.0000
    aerodynamics.settings.aircraft_span_efficiency_factor = 1.0
    analyses.append(aerodynamics)

    # ------------------------------------------------------------------
    #  Stability Analysis
    stability = SUAVE.Analyses.Stability.Fidelity_Zero()
    stability.geometry = vehicle
    analyses.append(stability)

    # ------------------------------------------------------------------
    #  Energy Analysis
    energy  = SUAVE.Analyses.Energy.Energy()
    energy.network=vehicle.propulsors
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
    vehicle.tag = 'Embraer_E190'

    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------

    # mass properties
    vehicle.mass_properties.max_takeoff               = 51800.   # kg
    vehicle.mass_properties.operating_empty           = 27837.   # kg
    vehicle.mass_properties.takeoff                   = 50989. #51800.   # kg
    vehicle.mass_properties.max_zero_fuel             = 40900.   # kg
    vehicle.mass_properties.cargo                     = 0.0 * Units.kg
    vehicle.mass_properties.max_payload               = 13063. * Units.kg
    vehicle.mass_properties.max_fuel                  = 12971.
    
    # envelope properties
    vehicle.envelope.ultimate_load = 3.5
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area         = 92.00
    vehicle.passengers             = 114
    vehicle.systems.control        = "fully powered"
    vehicle.systems.accessories    = "medium range"
    
    vehicle.wing_fea = [0,1,2]
    vehicle.fuselage_fea = [0]
    vehicle.no_of_intersections = 3
    vehicle.no_of_miscellaneous = 4
    vehicle.fea_type = "Conventional"
    vehicle.miscellaneous_tag=["lwing_i_i1","lwing_i_i2","fus_Misc_1","fus_Misc_2"]
    vehicle.intersection_tag=["lwing_fuse","ltail_fuse","vtail_fuse"]
    dv_val = 12
    
    # ------------------------------------------------------------------
    #   Main Wing
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'main_wing'

    wing.aspect_ratio            = 8.4
    wing.sweep                   = 23.0 * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.28
    wing.span_efficiency         = 1.0

    wing.spans.projected         = 27.8

    wing.chords.root             = 5.203
    wing.chords.tip              = 1.460
    wing.chords.mean_aerodynamic = 3.680

    wing.areas.reference         = 92.0
    wing.areas.wetted            = 2.0 * wing.areas.reference
    wing.areas.exposed           = 0.8 * wing.areas.wetted
    wing.areas.affected          = 0.6 * wing.areas.wetted

    wing.twists.root             = 2.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees

    wing.origin                  = [14.5,0,-0.5]
    wing.aerodynamic_center      = [3,0,0]

    

    wing.vertical                = False
    wing.symmetric               = True

    wing.dynamic_pressure_ratio  = 1.0
    
   
    #new nastran parameters
    wing.geometry_tag = "lwing"
    wing.airfoil                 = "rae2012"
    wing.element_area            = 0.25
    wing.sizing_lift             = vehicle.mass_properties.max_takeoff*2.5*9.81/2.0
    
    
    
    wing.root_origin             = wing.origin#[10.0,1.5,1.88849]
    wing.tip_origin              = find_tip_chord_leading_edge(wing)+wing.origin
   
    wing.fuel_load = 10000.0
    wing.max_x = 20.0
    wing.max_y = 20.0
    wing.max_z = 0.6*wing.tip_origin[2]
    wing.load_scaling = 1.0
    
    wing.structural_dv           = dv_val #1
    wing.strut_presence          = 0
    wing.strut_location          = 0.5
    wing.strut_section           = 1 #int(float(wing.strut_location)/float(0.05))
    wing.lv_location             = 0.2
    
    #note: NASTRAN uses x, z, y as coordinate system
    #wing_planform(wing)
    wing.no_of_sections          = 2
    wing_section = [SUAVE.Components.Wings.Wing_Section() for mnw in range(wing.no_of_sections)]
    wing_section[0].type = 'wing_section'
    wing_section[0].root_chord  = wing.chords.root
    wing_section[0].tip_chord   = 0.5*(wing.chords.root + wing.chords.tip)
    #wing_section[0].mid_chord   = 0.0 #mid chord and mid origin are depecrated
    coords = wing.root_origin 
    wing_section[0].root_origin = np.array([coords[0], coords[2],coords[1]])
    coords = wing.tip_origin
    wing_section[0].tip_origin  =np.array([coords[0], coords[2], coords[1]])
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    wing_section[0].span        = wing_section[0].tip_origin[1] - wing_section[0].root_origin[1]
    wing_section[0].sweep       = np.arctan((wing_section[0].tip_origin[2]- wing_section[0].root_origin[2])/(wing_section[0].tip_origin[0]- wing_section[0].root_origin[0]))
    
    wing_section[1].type =  'wing_section'
    wing_section[1].root_chord = 0.5*(wing.chords.root + wing.chords.tip)
    wing_section[1].tip_chord = wing.chords.tip
    wing_section[1].root_origin = [0.0,0.0,0.0] #why?
    wing_section[1].tip_origin = [0.0,0.0,0.0]
    wing_section[1].span = 0.0
    wing_section[1].sweep = 0.0

    wing.wing_sections = wing_section

   
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Horizontal Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'horizontal_stabilizer'

    wing.aspect_ratio            = 5.5
    wing.sweep                   = 34.5 * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.11
    wing.span_efficiency         = 0.9

    wing.spans.projected         = 11.958

    wing.chords.root             = 3.5
    wing.chords.tip              = 0.883
    wing.chords.mean_aerodynamic = 2.3840

    wing.areas.reference         = 26.0
    wing.areas.wetted            = 2.0 * wing.areas.reference
    wing.areas.exposed           = 0.8 * wing.areas.wetted
    wing.areas.affected          = 0.6 * wing.areas.wetted

    wing.twists.root             = 2.0 * Units.degrees
    wing.twists.tip              = 2.0 * Units.degrees

    wing.origin                  = [33.,0,0]
    wing.aerodynamic_center      = [2.,0,0]
    
   

    wing.vertical                = False
    wing.symmetric               = True

    wing.dynamic_pressure_ratio                     = 0.9
    
    #nastran parameters
    wing.geometry_tag = "ltail"
    wing.root_origin             = wing.origin
    wing.tip_origin              = wing.origin+find_tip_chord_leading_edge(wing)
    
    wing.airfoil                 = "rae2012"
    wing.element_area            = 0.25
    wing.vertical                = 0
    wing.sizing_lift             = 0.0*vehicle.mass_properties.max_takeoff*2.5*9.81/2.0
    wing.fuel_load = 0.
    wing.max_x = 200.0
    wing.max_y = 200.0
    wing.max_z = 0.6*wing.tip_origin[2]
    wing.load_scaling = 1.1
    
    wing.structural_dv           = dv_val #1
    wing.strut_presence          = 0
    wing.strut                   = 0
    
    
    #wingsections
    
    wing.no_of_sections          = 1
    
    
    wing_section = [SUAVE.Components.Wings.Wing_Section() for mnw in range(wing.no_of_sections)]
    
    wing_section[0].type = 'wing_section'
    wing_section[0].root_chord  = wing.chords.root
    wing_section[0].tip_chord   = wing.chords.tip
    wing_section[0].mid_chord   = 0.0
    coords = wing.root_origin
    wing_section[0].root_origin = np.array([coords[0], coords[2], coords[1]])
    coords = wing.tip_origin
    wing_section[0].tip_origin  = np.array([coords[0], coords[2], coords[1]])
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    
    
    wing_section[0].span        = wing_section[0].tip_origin[2] - wing_section[0].root_origin[2]
    wing_section[0].sweep       = np.arctan((wing_section[0].tip_origin[2]- wing_section[0].root_origin[2])/(wing_section[0].tip_origin[0]- wing_section[0].root_origin[0]))
    
    
    
    wing.wing_sections = wing_section
    
    
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'vertical_stabilizer'

    wing.aspect_ratio            = 1.7      #
    wing.sweep                   = 35. * Units.deg
    wing.thickness_to_chord      = 0.11
    wing.taper                   = 0.31
    wing.span_efficiency         = 0.9

    wing.spans.projected         = 5.270     #

    wing.chords.root             = 4.70
    wing.chords.tip              = 1.45
    wing.chords.mean_aerodynamic = 3.36

    wing.areas.reference         = 16.0    #
    wing.areas.wetted            = 2.0 * wing.areas.reference
    wing.areas.exposed           = 0.8 * wing.areas.wetted
    wing.areas.affected          = 0.6 * wing.areas.wetted

    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees
    

    wing.origin                  = [31.,0,1.]
    wing.aerodynamic_center      = [2.,0,0]

    wing.vertical                = True
    wing.symmetric               = False
    
    
    #new nastran parameters
    wing.geometry_tag = "vtail"
    wing.airfoil                 = "rae2012"
    wing.root_origin             = wing.origin
    
    wing.tip_origin              = wing.origin+find_tip_chord_leading_edge(wing)
    wing.sizing_lift             = 0.0*vehicle.mass_properties.max_takeoff*2.5*9.81/2.0
    wing.sizing_lift             = 0.0*vehicle.mass_properties.max_takeoff*2.5*9.81/2.0
    wing.element_area            = 0.25
    wing.dynamic_pressure_ratio                     = 1.0
    wing.fuel_load = 0.
    wing.max_x = 200.0
    wing.max_y = 200.0
    wing.max_z = 0.6*wing.tip_origin[2]
    wing.load_scaling = 1.1
    
    wing.structural_dv           = dv_val #1
    wing.strut_presence          = 0
    wing.strut                   = 0
    
    
    
    
    #wingsections
    wing.no_of_sections          = 1
    wing_section = [SUAVE.Components.Wings.Wing_Section() for mnw in range(wing.no_of_sections)]
    
    wing_section[0].type = 'wing_section'
    wing_section[0].root_chord  = wing.chords.root
    wing_section[0].tip_chord   = wing.chords.tip
    #wing_section[0].mid_chord   = 0.0
    coords = wing.root_origin 
    wing_section[0].root_origin = np.array([coords[0], coords[2], coords[1]])
    coords = wing.tip_origin
    wing_section[0].tip_origin  = np.array([coords[0], coords[2], coords[1]])
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    wing_section[0].span        = wing_section[0].tip_origin[1] - wing_section[0].root_origin[1]
   
    wing_section[0].sweep       = np.arctan((wing_section[0].tip_origin[2]- wing_section[0].root_origin[2])/(wing_section[0].tip_origin[0]- wing_section[0].root_origin[0]))
    wing.wing_sections = wing_section

    
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------

    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'fuselage'

    fuselage.number_coach_seats    = vehicle.passengers
    fuselage.seats_abreast         = 4
    fuselage.seat_pitch            = 0.7455

    fuselage.fineness.nose         = 2.0
    fuselage.fineness.tail         = 3.0

    fuselage.lengths.nose          = 4.27
    fuselage.lengths.tail          = 36.24-24.57
    #fuselage.lengths.cabin         = 21.24
    fuselage.lengths.cabin         = 25.91
    fuselage.lengths.total         = 36.24
    fuselage.lengths.fore_space    = 0.
    fuselage.lengths.aft_space     = 0.

    fuselage.width                 = 3.18

    fuselage.heights.maximum       = 3.35    #
    fuselage.heights.at_quarter_length          =  3.35
    fuselage.heights.at_three_quarters_length   =  3.35
    fuselage.heights.at_wing_root_quarter_chord = 3.35 

    fuselage.areas.side_projected  = 239.20
    fuselage.areas.wetted          = 327.01
    fuselage.areas.front_projected = 8.0110

    fuselage.effective_diameter    = 3.18

    fuselage.differential_pressure = 10**5 * Units.pascal    # Maximum differential pressure
    
    #new nastran parameters
    fuselage.geometry_tag = "fuse"
    fuselage.root_origin = [0.0,0.0,0.0]
    fuselage.tip_origin = [fuselage.lengths.total,0.0,0.0]
    fuselage.structural_dv         = 3 #dv_val #1

    
    
    # add to vehicle
    vehicle.append_component(fuselage)

    # ------------------------------------------------------------------
    #  Turbofan Network
    # ------------------------------------------------------------------    


    #initialize the gas turbine network
    gt_engine                   = SUAVE.Components.Energy.Networks.Turbofan()
    gt_engine.tag               = 'turbofan'

    gt_engine.number_of_engines = 2.0
    gt_engine.bypass_ratio      = 5.4
    gt_engine.engine_length     = 2.71
    gt_engine.nacelle_diameter  = 2.05
    #gt_engine.nacelle_length  =
    
    
    #gt_engine.nacelle_diameter  = 1.1*1.5 #CFM 56
    #gt_engine.engine_length     = 2.5
    
    
    #compute engine areas)
    Amax    = (np.pi/4.)*gt_engine.nacelle_diameter**2.
    Awet    = 1.1*np.pi*gt_engine.nacelle_diameter*gt_engine.engine_length # 1.1 is simple coefficient
    
    #Assign engine areas

    gt_engine.areas.wetted  = Awet
    
    #set the working fluid for the network
    working_fluid               = SUAVE.Attributes.Gases.Air

    #add working fluid to the network
    gt_engine.working_fluid = working_fluid


    #Component 1 : ram,  to convert freestream static to stagnation quantities
    ram = SUAVE.Components.Energy.Converters.Ram()
    ram.tag = 'ram'

    #add ram to the network
    gt_engine.ram = ram


    #Component 2 : inlet nozzle
    inlet_nozzle = SUAVE.Components.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag = 'inlet nozzle'

    inlet_nozzle.polytropic_efficiency = 0.98
    inlet_nozzle.pressure_ratio        = 0.98 #	turbofan.fan_nozzle_pressure_ratio     = 0.98     #0.98

    #add inlet nozzle to the network
    gt_engine.inlet_nozzle = inlet_nozzle


    #Component 3 :low pressure compressor    
    low_pressure_compressor = SUAVE.Components.Energy.Converters.Compressor()    
    low_pressure_compressor.tag = 'lpc'

    low_pressure_compressor.polytropic_efficiency = 0.91
    low_pressure_compressor.pressure_ratio        = 1.9    

    #add low pressure compressor to the network    
    gt_engine.low_pressure_compressor = low_pressure_compressor



    #Component 4 :high pressure compressor  
    high_pressure_compressor = SUAVE.Components.Energy.Converters.Compressor()    
    high_pressure_compressor.tag = 'hpc'

    high_pressure_compressor.polytropic_efficiency = 0.91
    high_pressure_compressor.pressure_ratio        = 10.0   

    #add the high pressure compressor to the network    
    gt_engine.high_pressure_compressor = high_pressure_compressor


    #Component 5 :low pressure turbine  
    low_pressure_turbine = SUAVE.Components.Energy.Converters.Turbine()   
    low_pressure_turbine.tag='lpt'

    low_pressure_turbine.mechanical_efficiency = 0.99
    low_pressure_turbine.polytropic_efficiency = 0.93

    #add low pressure turbine to the network    
    gt_engine.low_pressure_turbine = low_pressure_turbine



    #Component 5 :high pressure turbine  
    high_pressure_turbine = SUAVE.Components.Energy.Converters.Turbine()   
    high_pressure_turbine.tag='hpt'

    high_pressure_turbine.mechanical_efficiency = 0.99
    high_pressure_turbine.polytropic_efficiency = 0.93

    #add the high pressure turbine to the network    
    gt_engine.high_pressure_turbine = high_pressure_turbine 


    #Component 6 :combustor  
    combustor = SUAVE.Components.Energy.Converters.Combustor()   
    combustor.tag = 'Comb'

    combustor.efficiency                = 0.99 
    combustor.alphac                    = 1.0     
    combustor.turbine_inlet_temperature = 1500
    combustor.pressure_ratio            = 0.95
    combustor.fuel_data                 = SUAVE.Attributes.Propellants.Jet_A()    

    #add the combustor to the network    
    gt_engine.combustor = combustor



    #Component 7 :core nozzle
    core_nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    core_nozzle.tag = 'core nozzle'

    core_nozzle.polytropic_efficiency = 0.95
    core_nozzle.pressure_ratio        = 0.99    

    #add the core nozzle to the network    
    gt_engine.core_nozzle = core_nozzle


    #Component 8 :fan nozzle
    fan_nozzle = SUAVE.Components.Energy.Converters.Expansion_Nozzle()   
    fan_nozzle.tag = 'fan nozzle'

    fan_nozzle.polytropic_efficiency = 0.95
    fan_nozzle.pressure_ratio        = 0.99

    #add the fan nozzle to the network
    gt_engine.fan_nozzle = fan_nozzle



    #Component 9 : fan   
    fan = SUAVE.Components.Energy.Converters.Fan()   
    fan.tag = 'fan'

    fan.polytropic_efficiency = 0.93
    fan.pressure_ratio        = 1.7    

    #add the fan to the network
    gt_engine.fan = fan    

    #Component 10 : thrust (to compute the thrust)
    thrust = SUAVE.Components.Energy.Processes.Thrust()       
    thrust.tag ='compute_thrust'

    #total design thrust (includes all the engines)
    thrust.total_design             = 37278.0* Units.N #Newtons

    #design sizing conditions
    altitude      = 35000.0*Units.ft
    mach_number   = 0.78 
    isa_deviation = 0.

    # add thrust to the network
    gt_engine.thrust = thrust

    #size the turbofan
    turbofan_sizing(gt_engine,mach_number,altitude)   

    # add  gas turbine network gt_engine to the vehicle
    vehicle.append_component(gt_engine)      
    
    fuel                    =SUAVE.Components.Physical_Component()
    vehicle.fuel            =fuel
    
    fuel.mass_properties.mass=vehicle.mass_properties.max_takeoff-vehicle.mass_properties.max_zero_fuel
    fuel.origin                           =vehicle.wings.main_wing.mass_properties.center_of_gravity     
    fuel.mass_properties.center_of_gravity=vehicle.wings.main_wing.aerodynamic_center
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
#   Define the Mission
# ----------------------------------------------------------------------
def mission_setup(analyses):

    # ------------------------------------------------------------------
    #   Initialize the Mission
    # ------------------------------------------------------------------

    mission = SUAVE.Analyses.Mission.Sequential_Segments()
    mission.tag = 'embraer_e190ar test mission'

    # atmospheric model
    atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    planet = SUAVE.Attributes.Planets.Earth()

    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()

    mission.airport = airport

    # unpack Segments module
    Segments = SUAVE.Analyses.Mission.Segments    


    # ------------------------------------------------------------------
    #   First Climb Segment: Constant Speed, Constant Throttle
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed()
    segment.tag = "climb_250kcas"

    # connect vehicle configuration
    segment.analyses.extend( analyses.takeoff )

    # define segment attributes
    segment.atmosphere     = atmosphere
    segment.planet         = planet

    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 3.048 * Units.km
    segment.air_speed      = 250.0 * Units.knots
    segment.throttle       = 1.0

    # add to misison
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Second Climb Segment: Constant Speed, Constant Throttle
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed()
    segment.tag = "climb_280kcas"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 32000. * Units.ft
    segment.air_speed    = 350.0  * Units.knots
    segment.throttle     = 1.0

    # dummy for post process script
    segment.climb_rate   = 0.1

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Third Climb Segment: Constant Speed, Constant Climb Rate
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Throttle_Constant_Speed()
    segment.tag = "climb_final"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 35000. * Units.ft
    segment.air_speed    = 390.0  * Units.knots
    segment.throttle     = 1.0

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude()
    segment.tag = "cruise"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere = atmosphere
    segment.planet     = planet

    segment.air_speed  = 450. * Units.knots #230.  * Units['m/s']
    ## 35kft:
    # 415. => M = 0.72
    # 450. => M = 0.78
    # 461. => M = 0.80
    ## 37kft:
    # 447. => M = 0.78
    segment.distance   = 2100. * Units.nmi

    # add to mission
    mission.append_segment(segment)

    # ------------------------------------------------------------------
    #   First Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "descent_m0_77"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 9.31  * Units.km
    segment.air_speed    = 440.0 * Units.knots
    segment.descent_rate = 2600. * Units['ft/min']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "descent_290kcas"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 3.657 * Units.km
    segment.air_speed    = 365.0 * Units.knots
    segment.descent_rate = 2300. * Units['ft/min']

    # append to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate()
    segment.tag = "descent_250kcas"

    # connect vehicle configuration
    segment.analyses.extend( analyses.cruise )

    # segment attributes
    segment.atmosphere   = atmosphere
    segment.planet       = planet

    segment.altitude_end = 0.0   * Units.km
    segment.air_speed    = 250.0 * Units.knots
    segment.descent_rate = 1500. * Units['ft/min']

    # append to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Mission definition complete
    # ------------------------------------------------------------------

    return mission

#: def define_mission()


# ----------------------------------------------------------------------
#   Plot Mission
# ----------------------------------------------------------------------

def plot_mission(results,line_style='bo-'):

    # ------------------------------------------------------------------
    #   Throttle
    # ------------------------------------------------------------------
    plt.figure("Throttle History")
    axes = plt.gca()
    for i in range(len(results.segments)):
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        eta  = results.segments[i].conditions.propulsion.throttle[:,0]
        axes.plot(time, eta, line_style)
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Throttle')
    axes.grid(True)


    # ------------------------------------------------------------------
    #   Angle of Attack
    # ------------------------------------------------------------------

    plt.figure("Angle of Attack History")
    axes = plt.gca()
    for i in range(len(results.segments)):
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        aoa = results.segments[i].conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        axes.plot(time, aoa, line_style)
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Angle of Attack (deg)')
    axes.grid(True)


    # ------------------------------------------------------------------
    #   Fuel Burn Rate
    # ------------------------------------------------------------------
    plt.figure("Fuel Burn Rate")
    axes = plt.gca()
    for i in range(len(results.segments)):
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        mdot = results.segments[i].conditions.weights.vehicle_mass_rate[:,0]
        axes.plot(time, mdot, line_style)
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Fuel Burn Rate (kg/s)')
    axes.grid(True)


##    # ------------------------------------------------------------------
##    #   Engine SFC
##    # ------------------------------------------------------------------
##    plt.figure("Engine SFC")
##    axes = plt.gca()
##    for i in range(len(results.segments)):
##        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
##        mdot = results.segments[i].conditions.weights.vehicle_mass_rate[:,0] * 360.
##        Thrust = results.segments[i].conditions.frames.body.thrust_force_vector[:,0] / 9.81
##        sfc = np.divide(mdot,Thrust)
##        axes.plot(time, sfc, line_style)
##    axes.set_xlabel('Time (mins)')
##    axes.set_ylabel('Engine SFC (kg/kg)')
##    axes.grid(True)


    # ------------------------------------------------------------------
    #   Altitude
    # ------------------------------------------------------------------
    plt.figure("Altitude")
    axes = plt.gca()
    for i in range(len(results.segments)):
        time     = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        altitude = results.segments[i].conditions.freestream.altitude[:,0] / Units.km
        axes.plot(time, altitude, line_style)
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Altitude (km)')
    axes.grid(True)


    # ------------------------------------------------------------------
    #   Vehicle Mass
    # ------------------------------------------------------------------
    plt.figure("Vehicle Mass")
    axes = plt.gca()
    for i in range(len(results.segments)):
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        mass = results.segments[i].conditions.weights.total_mass[:,0]
        axes.plot(time, mass, line_style)
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Vehicle Mass (kg)')
    axes.grid(True)


    # ------------------------------------------------------------------
    #   Aerodynamics
    # ------------------------------------------------------------------
    fig = plt.figure("Aerodynamic Forces")
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        Lift   = -segment.conditions.frames.wind.lift_force_vector[:,2]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]

        axes = fig.add_subplot(4,1,1)
        axes.plot( time , Lift , line_style )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Lift (N)')
        axes.grid(True)

        axes = fig.add_subplot(4,1,2)
        axes.plot( time , Drag , line_style )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Drag (N)')
        axes.grid(True)

        axes = fig.add_subplot(4,1,3)
        axes.plot( time , Thrust , line_style )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Thrust (N)')
        axes.grid(True)

        try:
            Pitching_moment = segment.conditions.stability.static.cm_alpha[:,0]
            axes = fig.add_subplot(4,1,4)
            axes.plot( time , Pitching_moment , line_style )
            axes.set_xlabel('Time (min)')
            axes.set_ylabel('Pitching_moment (~)')
            axes.grid(True)            
        except:
            pass 

    # ------------------------------------------------------------------
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    fig = plt.figure("Aerodynamic Coefficients")
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        CLift  = segment.conditions.aerodynamics.lift_coefficient[:,0]
        CDrag  = segment.conditions.aerodynamics.drag_coefficient[:,0]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , CLift , line_style )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('CL')
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , CDrag , line_style )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('CD')
        axes.grid(True)

        axes = fig.add_subplot(3,1,3)
        axes.plot( time , Drag   , line_style )
        axes.plot( time , Thrust , 'ro-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Drag and Thrust (N)')
        axes.grid(True)


    # ------------------------------------------------------------------
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    fig = plt.figure("Drag Components")
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
            axes.plot( time , cdp , 'ko-', label='CD_P' )
            axes.plot( time , cdi , 'bo-', label='CD_I' )
            axes.plot( time , cdc , 'go-', label='CD_C' )
            axes.plot( time , cdm , 'yo-', label='CD_M' )
            axes.plot( time , cd  , 'ro-', label='CD'   )
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

    return

def check_results(new_results,old_results):

    # check segment values
    check_list = [
        'segments.cruise.conditions.aerodynamics.angle_of_attack',
        'segments.cruise.conditions.aerodynamics.drag_coefficient',
        'segments.cruise.conditions.aerodynamics.lift_coefficient',
        #'segments.cruise.conditions.stability.static.cm_alpha',
        'segments.cruise.conditions.stability.static.cn_beta',
        'segments.cruise.conditions.propulsion.throttle',
        'segments.cruise.conditions.weights.vehicle_mass_rate',
    ]

    # do the check
    for k in check_list:
        print k

        old_val = np.max( old_results.deep_get(k) )
        new_val = np.max( new_results.deep_get(k) )
        err = (new_val-old_val)/old_val
        print 'Error at Max:' , err
        assert np.abs(err) < 1e-6 , 'Max Check Failed : %s' % k

        old_val = np.min( old_results.deep_get(k) )
        new_val = np.min( new_results.deep_get(k) )
        err = (new_val-old_val)/old_val
        print 'Error at Min:' , err
        assert np.abs(err) < 1e-6 , 'Min Check Failed : %s' % k        

        print ''

    ## check high level outputs
    #def check_vals(a,b):
        #if isinstance(a,Data):
            #for k in a.keys():
                #err = check_vals(a[k],b[k])
                #if err is None: continue
                #print 'outputs' , k
                #print 'Error:' , err
                #print ''
                #assert np.abs(err) < 1e-6 , 'Outputs Check Failed : %s' % k  
        #else:
            #return (a-b)/a

    ## do the check
    #check_vals(old_results.output,new_results.output)

    return


    
def load_results():
    return SUAVE.Input_Output.SUAVE.load('results_mission_E190_constThr.res')

def save_results(results):
    SUAVE.Input_Output.SUAVE.archive(results,'results_mission_E190_constThr.res')
    return


if __name__ == '__main__':
    main()
    #plt.show()
