import numpy as np

def aircraft_total(state,settings,geometry):

    # unpack
    AoA         = state.conditions.aerodynamics.angle_of_attack
    CL          = AoA*2.*np.pi
    vehicle_ref = geometry.reference_area
    Sref        = geometry.wings.main_wing.areas.reference
    CL_vehicle  = CL*vehicle_ref/Sref
    
    state.conditions.aerodynamics.lift_coefficient = CL_vehicle

    return CL_vehicle