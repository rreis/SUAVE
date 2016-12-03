# tut_mission_B737.py
# 
# Created:  Aug 2014, SUAVE Team
# Modified: Dec 2015, T. MacDonald

""" setup file for a mission with a concorde
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

from SUAVE.Methods.Propulsion.turbojet_sizing import turbojet_sizing
from SUAVE.Methods.Geometry.Two_Dimensional.Cross_Section.Propulsion import compute_turbofan_geometry
from SUAVE.Methods.Geometry.Three_Dimensional.find_tip_chord_leading_edge import find_tip_chord_leading_edge

from SUAVE.Methods.fea_tools.geomach_geometry import geometry_generation
from SUAVE.Methods.fea_tools.weight_estimation import FEA_Weight
from SUAVE.Methods.fea_tools.weight_estimation import Filenames
from SUAVE.Methods.fea_tools.build_geomach_geometry import build_geomach_geometry

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
    
    configs.base.type ='Supersonic'
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

    ## takeoff_analysis
    #analyses.takeoff.aerodynamics.settings.drag_coefficient_increment = 0.0000

    ## landing analysis
    #aerodynamics = analyses.landing.aerodynamics

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
    
    filenames.Nastran_sol200 = "supersonic_opt.bdf"
    filenames.Nastran_f06 = "supersonic_opt.f06"
    filenames.geomach_output = "supersonic_str.bdf"
    filenames.geomach_structural_surface_grid_points = "super_pt_str_surf.dat"
    filenames.geomach_stl_mesh = 'supersonic.stl'
    filenames.tacs_load = "geomach_tacs_load_supersonic.txt"
    filenames.aero_load = "geomach_load_aero_super.txt"
    filenames.tacs_optimization_driver = "geomach_tacs_opt_driver_super.txt"
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
    vehicle.tag = 'Concorde'    


    # ------------------------------------------------------------------
    #   Vehicle-level Properties
    # ------------------------------------------------------------------    

    # mass properties
    vehicle.mass_properties.max_takeoff               = 185000.   # kg
    vehicle.mass_properties.takeoff                   = 78700.   # kg
    #vehicle.mass_properties.max_zero_fuel             = 0.9 * vehicle.mass_properties.max_takeoff
    vehicle.mass_properties.cargo                     = 1000.  * Units.kilogram   

    # envelope properties
    vehicle.envelope.ultimate_load = 3.5
    vehicle.envelope.limit_load    = 1.5

    # basic parameters
    vehicle.reference_area         = 358.25     
    vehicle.passengers             = 100
    vehicle.systems.control        = "fully powered" 
    vehicle.systems.accessories    = "long range"

    #new nastran parameters
    vehicle.wing_fea = [0,2]
    vehicle.fuselage_fea = [0]
    vehicle.no_of_intersections = 2
    vehicle.no_of_miscellaneous = 4
    vehicle.fea_type = "Supersonic"
    vehicle.miscellaneous_tag=["lwing_i_i1","lwing_i_i2","fus_Misc_1","fus_Misc_2"]
    vehicle.intersection_tag=["lwing_fuse","vtail_fuse"]
    dv_val = 12




    # ------------------------------------------------------------------
    #  Fuselage
    # ------------------------------------------------------------------

    fuselage = SUAVE.Components.Fuselages.Fuselage()
    fuselage.tag = 'fuselage'

    fuselage.seats_abreast         = 4
    fuselage.seat_pitch            = 1

    fuselage.fineness.nose         = 4.3
    fuselage.fineness.tail         = 6.4

    #fuselage.lengths.nose          = 6.4
    #fuselage.lengths.tail          = 8.0
    #fuselage.lengths.cabin         = 28.85
    fuselage.lengths.total         = 61.66
    #fuselage.lengths.fore_space    = 6.
    #fuselage.lengths.aft_space     = 5.    

    fuselage.width                 = 2.88

    fuselage.heights.maximum       = 3.32
    fuselage.heights.at_quarter_length          = 3.32
    fuselage.heights.at_three_quarters_length   = 3.32
    fuselage.heights.at_wing_root_quarter_chord = 3.32

    #fuselage.areas.side_projected  = 142.1948
    fuselage.areas.wetted          = 523.
    fuselage.areas.front_projected = 7.55

    fuselage.effective_diameter    = 3.1 #4.0

    fuselage.differential_pressure = 7.4e4 * Units.pascal # Maximum differential pressure

    #new nastran parameters
    fuselage.geometry_tag = "fuse"
    fuselage.root_origin = [0.0,0.0,0.0]
    fuselage.tip_origin = [fuselage.lengths.total,0.0,0.0]
    fuselage.structural_dv         = 3 #dv_val #1

    
    
    
    # add to vehicle
    vehicle.append_component(fuselage)
    
    # ------------------------------------------------------------------        
    #   Main Wing
    # ------------------------------------------------------------------        

    wing = SUAVE.Components.Wings.Main_Wing()
    wing.tag = 'main_wing'

    wing.aspect_ratio            = 1.83
    wing.sweep                   = 59.5 * Units.deg
    wing.thickness_to_chord      = 0.03
    wing.taper                   = 0.
    wing.span_efficiency         = 0.74

    wing.spans.projected         = 25.6    

    wing.chords.root             = 33.8 * Units.meter
    wing.chords.tip              = 1.1 * Units.meter
    wing.chords.mean_aerodynamic = 18.4

    wing.areas.reference         = 358.25 

    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees

    wing.origin                  = [14., 0., -.8]
    wing.aerodynamic_center      = [35,0,0] #not really used here 
    

    wing.vertical                = False
    wing.symmetric               = True
    wing.high_lift               = True

    wing.dynamic_pressure_ratio  = 1.0
    
    #new nastran parameters (note nastran uses x, z, y coordinate system
    wing.geometry_tag = "lwing"
    wing.airfoil                 = "n65203.dat"
    wing.element_area            = 0.25
    wing.sizing_lift             = vehicle.mass_properties.max_takeoff*2.5*9.81/2.0
    build_geomach_geometry(wing)
    
    
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
    
    wing_section[0].root_origin = wing.root_origin
    wing_section[0].tip_origin  = wing.tip_origin
    '''
    #wing_section[0].mid_chord   = 0.0 #mid chord and mid origin are depecrated
    coords = wing.root_origin 
    wing_section[0].root_origin = np.array([coords[0], coords[2],coords[1]])
    coords = wing.tip_origin
    wing_section[0].tip_origin  =np.array([coords[0], coords[2], coords[1]])
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    '''
    
    wing_section[0].span        = wing_section[0].tip_origin[2] - wing_section[0].root_origin[2]
    wing_section[0].sweep       = 28.225 * Units.degrees
    
    wing_section[1].type =  'wing_section'
    wing_section[1].root_chord = wing_section[0].tip_chord
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

    wing.aspect_ratio            = 6.16
    wing.sweep                   = 40. * Units.deg
    wing.thickness_to_chord      = 0.08
    wing.taper                   = .955/4.7
    wing.span_efficiency         = 0.9

    wing.spans.projected         = 14.2

    wing.chords.root             = 4.7
    wing.chords.tip              = .955    
    wing.chords.mean_aerodynamic = 8.0

    wing.areas.reference         = 32.488

    wing.twists.root             = 0 * Units.degrees
    wing.twists.tip              = 0 * Units.degrees 

    wing.origin                  = [28.79,0,1.14]
    wing.aerodynamic_center      = [2,0,0]
    
    wing.tip_location            = find_tip_chord_leading_edge(wing)

    wing.vertical                = False 
    wing.symmetric               = True

    wing.dynamic_pressure_ratio  = 0.9  

    #nastran parameters
    wing.geometry_tag = "ltail"
    
    #convert coordinate system
    build_geomach_geometry(wing)
    #add in dihedral (remember nastran goes xzy, where z is up
    wing.tip_origin[1] = wing.root_origin[1]+np.tan(8.63*Units.degrees)*wing.spans.projected/2.
    
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
    '''
    # old way
    wing.no_of_sections          = 1
    
    
    wing_section = [SUAVE.Components.Wings.Wing_Section() for mnw in range(wing.no_of_sections)]
    
    wing_section[0].type = 'wing_section'
    wing_section[0].root_chord  = wing.chords.root
    wing_section[0].tip_chord   = wing.chords.tip
    wing_section[0].mid_chord   = 0.0
     
    wing_section[0].root_origin = wing.root_origin
    wing_section[0].tip_origin  = wing.tip_origin
    
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    
    
    wing_section[0].span        = wing_section[0].tip_origin[2] - wing_section[0].root_origin[2]
    wing_section[0].sweep       = np.arctan((wing_section[0].tip_origin[2]- wing_section[0].root_origin[2])/(wing_section[0].tip_origin[0]- wing_section[0].root_origin[0]))
    
    '''
    wing.no_of_sections          = 3
    
    
    wing_section = [SUAVE.Components.Wings.Wing_Section() for mnw in range(wing.no_of_sections)]
    
    wing_section[0].type = 'wing_section'
    wing_section[0].root_chord  = wing.chords.root
    wing_section[0].tip_chord   = wing.chords.tip
    wing_section[0].mid_chord   = 0.0
     
    wing_section[0].root_origin = wing.root_origin
    wing_section[0].tip_origin  = wing.tip_origin
    
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    
    
    wing_section[0].span        = .91*wing.spans.projected
    wing_section[0].sweep       = 38.42*Units.degrees
    
    wing_section[1].type =  'wing_section'
    wing_section[1].root_chord = .35*wing.chords.root
    wing_section[1].tip_chord = wing.chords.tip
    wing_section[1].root_origin = [0.0,0.0,0.0] #not being used
    wing_section[1].tip_origin = [0.0,0.0,0.0]
    wing_section[1].span = 0.0
    wing_section[1].sweep = 48.17*Units.degrees
    
    wing.wing_sections = wing_section
    
    
    # add to vehicle
    vehicle.append_component(wing)


    # ------------------------------------------------------------------
    #   Vertical Stabilizer
    # ------------------------------------------------------------------

    wing = SUAVE.Components.Wings.Wing()
    wing.tag = 'vertical_stabilizer'    

    wing.aspect_ratio            = 0.74
    wing.sweep                   = 60 * Units.deg
    wing.thickness_to_chord      = 0.04
    wing.taper                   = .14
    wing.span_efficiency         = 0.9

    wing.spans.projected         = 6.0

    wing.chords.root             = 14.5
    wing.chords.tip              = 2.7
    wing.chords.mean_aerodynamic = 8.66

    wing.areas.reference         = 33.91

    wing.twists.root             = 0.0 * Units.degrees
    wing.twists.tip              = 0.0 * Units.degrees  

    wing.origin                  = [42.,0,1.]
    
    wing.aerodynamic_center      = [50,0,0]   #not really used 
    
    wing.tip_location            = find_tip_chord_leading_edge(wing)

    wing.vertical                = True 
    wing.symmetric               = False
    wing.t_tail                  = False

    wing.dynamic_pressure_ratio  = 1.0

    #new nastran parameters
    wing.geometry_tag = "vtail"
    wing.airfoil                 = "rae2012"
    build_geomach_geometry(wing)
    
    
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
    
    
    
    '''
    #this is saved for a single wing section
    #wingsections
    wing.no_of_sections          = 1
    wing_section = [SUAVE.Components.Wings.Wing_Section() for mnw in range(wing.no_of_sections)]
    
    wing_section[0].type = 'wing_section'
    wing_section[0].root_chord  = wing.chords.root
    wing_section[0].tip_chord   = wing.chords.tip
    #wing_section[0].mid_chord   = 0.0
    wing_section[0].root_origin = wing.root_origin
    wing_section[0].tip_origin  = wing.tip_origin
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    wing_section[0].span        = wing_section[0].tip_origin[1] - wing_section[0].root_origin[1]
   
    wing_section[0].sweep       = np.arctan((wing_section[0].tip_origin[2]- wing_section[0].root_origin[2])/(wing_section[0].tip_origin[0]- wing_section[0].root_origin[0]))
    wing.wing_sections = wing_section
    '''
    wing.no_of_sections          = 2
    wing_section = [SUAVE.Components.Wings.Wing_Section() for mnw in range(wing.no_of_sections)]
    
    wing_section[0].type = 'wing_section'
    wing_section[0].root_chord  = wing.chords.root
    wing_section[0].tip_chord   = wing.chords.tip #not sure how this works
    #wing_section[0].mid_chord   = 0.0
    wing_section[0].root_origin = wing.root_origin
    wing_section[0].tip_origin  = wing.tip_origin
    #wing_section[0].mid_origin  = [0.0,0.0,0.0]
    wing_section[0].span        = .194*wing.spans.projected
    wing_section[0].sweep       = 63.63 * Units.degrees
    
    wing_section[1].root_chord = 0.54*wing.chords.root
    wing_section[1].tip_chord = wing.chords.tip
    wing_section[1].root_origin = [0.0,0.0,0.0] #why?
    wing_section[1].tip_origin = [0.0,0.0,0.0]
    wing_section[1].span = 0.
    wing_section[1].sweep = 30*Units.degrees

    wing.wing_sections = wing_section
    
    
    
    # add to vehicle
    vehicle.append_component(wing)

    # ------------------------------------------------------------------
    #   Turbojet Network
    # ------------------------------------------------------------------    
    
    #instantiate the gas turbine network
    turbojet = SUAVE.Components.Energy.Networks.Turbojet_Super()
    turbojet.tag = 'turbojet'

    # setup
    turbojet.number_of_engines = 4.0
    turbojet.engine_length     = 12.5
    turbojet.nacelle_diameter  = 1.60
    
    # working fluid
    turbojet.working_fluid = SUAVE.Attributes.Gases.Air()


    # ------------------------------------------------------------------
    #   Component 1 - Ram

    # to convert freestream static to stagnation quantities

    # instantiate
    ram = SUAVE.Components.Energy.Converters.Ram()
    ram.tag = 'ram'

    # add to the network
    turbojet.append(ram)


    # ------------------------------------------------------------------
    #  Component 2 - Inlet Nozzle

    # instantiate
    inlet_nozzle = SUAVE.Components.Energy.Converters.Compression_Nozzle()
    inlet_nozzle.tag = 'inlet_nozzle'

    # setup
    inlet_nozzle.polytropic_efficiency = 0.98
    inlet_nozzle.pressure_ratio        = 1.0

    # add to network
    turbojet.append(inlet_nozzle)


    # ------------------------------------------------------------------
    #  Component 3 - Low Pressure Compressor

    # instantiate 
    compressor = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag = 'low_pressure_compressor'

    # setup
    compressor.polytropic_efficiency = 0.91
    compressor.pressure_ratio        = 3.1    

    # add to network
    turbojet.append(compressor)


    # ------------------------------------------------------------------
    #  Component 4 - High Pressure Compressor

    # instantiate
    compressor = SUAVE.Components.Energy.Converters.Compressor()    
    compressor.tag = 'high_pressure_compressor'

    # setup
    compressor.polytropic_efficiency = 0.91
    compressor.pressure_ratio        = 5.0  

    # add to network
    turbojet.append(compressor)


    # ------------------------------------------------------------------
    #  Component 5 - Low Pressure Turbine

    # instantiate
    turbine = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag='low_pressure_turbine'

    # setup
    turbine.mechanical_efficiency = 0.99
    turbine.polytropic_efficiency = 0.93     

    # add to network
    turbojet.append(turbine)


    # ------------------------------------------------------------------
    #  Component 6 - High Pressure Turbine

    # instantiate
    turbine = SUAVE.Components.Energy.Converters.Turbine()   
    turbine.tag='high_pressure_turbine'

    # setup
    turbine.mechanical_efficiency = 0.99
    turbine.polytropic_efficiency = 0.93     

    # add to network
    turbojet.append(turbine)


    # ------------------------------------------------------------------
    #  Component 7 - Combustor

    # instantiate    
    combustor = SUAVE.Components.Energy.Converters.Combustor()   
    combustor.tag = 'combustor'

    # setup
    combustor.efficiency                = 0.99
    combustor.alphac                    = 1.0     
    combustor.turbine_inlet_temperature = 1450.
    combustor.pressure_ratio            = 1.0
    combustor.fuel_data                 = SUAVE.Attributes.Propellants.Jet_A()    

    # add to network
    turbojet.append(combustor)


    # ------------------------------------------------------------------
    #  Component 8 - Core Nozzle

    # instantiate
    nozzle = SUAVE.Components.Energy.Converters.Supersonic_Nozzle()   
    nozzle.tag = 'core_nozzle'

    # setup
    nozzle.polytropic_efficiency = 0.95
    nozzle.pressure_ratio        = 0.99    

    # add to network
    turbojet.append(nozzle)

    # ------------------------------------------------------------------
    #  Component 9 - Divergening Nozzle




    # ------------------------------------------------------------------
    #Component 10 : thrust (to compute the thrust)
    thrust = SUAVE.Components.Energy.Processes.Thrust()       
    thrust.tag ='compute_thrust'

    #total design thrust (includes all the engines)
    thrust.total_design             = 4*140000. * Units.N #Newtons

    # Note: Sizing builds the propulsor. It does not actually set the size of the turbojet
    #design sizing conditions
    altitude      = 0.0*Units.ft
    mach_number   = 0.01
    isa_deviation = 0.

    # add to network
    turbojet.thrust = thrust

    #size the turbojet
    turbojet_sizing(turbojet,mach_number,altitude)   

    # add  gas turbine network gt_engine to the vehicle
    vehicle.append_component(turbojet)      


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
    
    # write to OpenVSP
    #write(vehicle,base_config.tag)    

    ## ------------------------------------------------------------------
    ##   Cruise Configuration
    ## ------------------------------------------------------------------

    #config = SUAVE.Components.Configs.Config(base_config)
    #config.tag = 'cruise'

    #configs.append(config)
    
    ## write to OpenVSP
    #write(vehicle,config.tag)     


    ## ------------------------------------------------------------------
    ##   Takeoff Configuration
    ## ------------------------------------------------------------------

    #config = SUAVE.Components.Configs.Config(base_config)
    #config.tag = 'takeoff'

    #config.wings['main_wing'].flaps.angle = 20. * Units.deg
    #config.wings['main_wing'].slats.angle = 25. * Units.deg

    #config.V2_VS_ratio = 1.21
    #config.maximum_lift_coefficient = 2.

    #configs.append(config)
    
    ## write to OpenVSP
    #write(vehicle,config.tag)       


    ## ------------------------------------------------------------------
    ##   Landing Configuration
    ## ------------------------------------------------------------------

    #config = SUAVE.Components.Configs.Config(base_config)
    #config.tag = 'landing'

    #config.wings['main_wing'].flaps_angle = 30. * Units.deg
    #config.wings['main_wing'].slats_angle = 25. * Units.deg

    #config.Vref_VS_ratio = 1.23
    #config.maximum_lift_coefficient = 2.

    #configs.append(config)
    
    ## write to OpenVSP
    #write(vehicle,config.tag)       


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
    #   Aerodynamics
    # ------------------------------------------------------------------


    fig = plt.figure("Aerodynamic Forces",figsize=(8,6))
    for segment in results.segments.values():

        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        Lift   = -segment.conditions.frames.wind.lift_force_vector[:,2]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]*0.224808943
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]*0.224808943
        eta  = segment.conditions.propulsion.throttle[:,0]
        mdot   = segment.conditions.weights.vehicle_mass_rate[:,0]
        thrust =  segment.conditions.frames.body.thrust_force_vector[:,0]
        sfc    = 3600. * mdot / 0.1019715 / thrust	
        


        axes = fig.add_subplot(2,1,1)
        axes.plot( time , Thrust , line_style )
        #axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Thrust (lbf)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(2,1,2)
        axes.plot( time , eta , line_style )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('eta (lb/lbf-hr)',axis_font)
        axes.grid(True)	

        #plt.savefig("B737_engine.pdf")
        #plt.savefig("B737_engine.png")


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
        #axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Lift Coefficient',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , l_d , line_style )
        #axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('L/D',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,3)
        axes.plot( time , aoa , 'ro-' )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('AOA (deg)',axis_font)
        axes.grid(True)

        #plt.savefig("B737_aero.pdf")
        #plt.savefig("B737_aero.png")

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
            #axes.plot( time , cdi , line_style )
            #axes.plot( time , cdc , line_style )
            axes.plot( time , cdm , line_style )
            axes.plot( time , cd  , line_style )            

    axes.set_xlabel('Time (min)')
    axes.set_ylabel('CD')
    axes.grid(True)
    #plt.savefig("B737_drag.pdf")
    #plt.savefig("B737_drag.png")

    # ------------------------------------------------------------------
    #   Altitude,sfc,vehiclde weight
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
        mass   = segment.conditions.weights.total_mass[:,0]*2.20462
        altitude = segment.conditions.freestream.altitude[:,0] / Units.km *3.28084 *1000
        mdot   = segment.conditions.weights.vehicle_mass_rate[:,0]
        thrust =  segment.conditions.frames.body.thrust_force_vector[:,0]
        sfc    = 3600. * mdot / 0.1019715 / thrust
        mach   = segment.conditions.freestream.mach_number[:,0]


        axes = fig.add_subplot(3,1,1)
        axes.plot( time , altitude , line_style )
        #axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Altitude (ft)',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,3)
        axes.plot( time , mach , line_style )
        axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Mach Number',axis_font)
        axes.grid(True)

        axes = fig.add_subplot(3,1,2)
        axes.plot( time , mass , 'ro-' )
        #axes.set_xlabel('Time (min)',axis_font)
        axes.set_ylabel('Weight (lb)',axis_font)
        axes.grid(True)


        #plt.savefig("B737_mission.pdf")
        #plt.savefig("B737_mission.png")

    return

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

    ## ------------------------------------------------------------------
    ##   Landing Configuration
    ## ------------------------------------------------------------------
    #landing = configs.landing

    ## make sure base data is current
    #landing.pull_base()

    ## landing weight
    #landing.mass_properties.landing = 0.85 * base.mass_properties.takeoff

    ## diff the new data
    #landing.store_diff()

    # done!
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
    #   First Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_1"

    segment.analyses.extend( analyses.base )

    segment.altitude_start = 0.0   * Units.km
    segment.altitude_end   = 3.0   * Units.km
    segment.air_speed      = 125.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']

    # add to misison
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Climb Segment: constant Speed, constant segment angle 
    # ------------------------------------------------------------------    

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_2"

    segment.analyses.extend( analyses.base )

    segment.altitude_end   = 8.0   * Units.km
    segment.air_speed      = 190.0 * Units['m/s']
    segment.climb_rate     = 6.0   * Units['m/s']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Climb Segment: constant Mach, constant segment angle 
    # ------------------------------------------------------------------    

    segment = Segments.Climb.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "climb_3"

    segment.analyses.extend( analyses.base )

    segment.altitude_end = 10.668 * Units.km
    segment.air_speed    = 226.0  * Units['m/s']
    segment.climb_rate   = 3.0    * Units['m/s']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------    
    #   Cruise Segment: constant speed, constant altitude
    # ------------------------------------------------------------------    

    segment = Segments.Cruise.Constant_Speed_Constant_Altitude(base_segment)
    segment.tag = "cruise"

    segment.analyses.extend( analyses.base )

    segment.air_speed  = 230.412 * Units['m/s']
    segment.distance   = (3933.65 + 770 - 92.6) * Units.km
    
    segment.state.numerics.number_control_points = 10

    # add to mission
    mission.append_segment(segment)


# ------------------------------------------------------------------
#   First Descent Segment: consant speed, constant segment rate
# ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_1"

    segment.analyses.extend( analyses.base )

    segment.altitude_end = 8.0   * Units.km
    segment.air_speed    = 220.0 * Units['m/s']
    segment.descent_rate = 4.5   * Units['m/s']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Second Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_2"

    segment.analyses.extend( analyses.base )

    #analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.altitude_end = 6.0   * Units.km
    segment.air_speed    = 195.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Third Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_3"

    segment.analyses.extend( analyses.base )

    #analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.altitude_end = 4.0   * Units.km
    segment.air_speed    = 170.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']

    # add to mission
    mission.append_segment(segment)


    # ------------------------------------------------------------------
    #   Fourth Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_4"

    segment.analyses.extend( analyses.base )

    #analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00

    segment.altitude_end = 2.0   * Units.km
    segment.air_speed    = 150.0 * Units['m/s']
    segment.descent_rate = 5.0   * Units['m/s']


    # add to mission
    mission.append_segment(segment)



    # ------------------------------------------------------------------
    #   Fifth Descent Segment: consant speed, constant segment rate
    # ------------------------------------------------------------------

    segment = Segments.Descent.Constant_Speed_Constant_Rate(base_segment)
    segment.tag = "descent_5"

    segment.analyses.extend( analyses.base )
    #analyses.landing.aerodynamics.settings.spoiler_drag_increment = 0.00


    segment.altitude_end = 0.0   * Units.km
    segment.air_speed    = 145.0 * Units['m/s']
    segment.descent_rate = 3.0   * Units['m/s']


    # append to mission
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


    # ------------------------------------------------------------------
    #   Mission for Constrained Fuel
    # ------------------------------------------------------------------    
    fuel_mission = SUAVE.Analyses.Mission.Mission() #Fuel_Constrained()
    fuel_mission.tag = 'fuel'
    fuel_mission.range   = 1277. * Units.nautical_mile
    fuel_mission.payload   = 19000.
    missions.append(fuel_mission)    


    # ------------------------------------------------------------------
    #   Mission for Constrained Short Field
    # ------------------------------------------------------------------    
    short_field = SUAVE.Analyses.Mission.Mission(base_mission) #Short_Field_Constrained()
    short_field.tag = 'short_field'    

    #airport
    airport = SUAVE.Attributes.Airports.Airport()
    airport.altitude   =  0.0  * Units.ft
    airport.delta_isa  =  0.0
    airport.atmosphere = SUAVE.Attributes.Atmospheres.Earth.US_Standard_1976()
    airport.available_tofl = 1500.
    short_field.airport = airport    
    missions.append(short_field)



    # ------------------------------------------------------------------
    #   Mission for Fixed Payload
    # ------------------------------------------------------------------    
    payload = SUAVE.Analyses.Mission.Mission() #Payload_Constrained()
    payload.tag = 'payload'
    payload.range   = 2316. * Units.nautical_mile
    payload.payload   = 19000.
    missions.append(payload)


    # done!
    return missions  

if __name__ == '__main__': 
    main()    
    plt.show()

