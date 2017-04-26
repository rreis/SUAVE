import numpy as np
from SUAVE.Core import Data

def aircraft_total(state,settings,geometry):

    total_length = geometry.wings.main_wing.total_length
    CL           = state.conditions.aerodynamics.lift_coefficient
    Sref         = geometry.wings.main_wing.areas.reference
    AR           = geometry.wings.main_wing.aspect_ratio
    vehicle_ref  = geometry.reference_area
    mach         = state.conditions.freestream.mach_number
    t_c_w        = geometry.wings.main_wing.thickness_to_chord
    e = .9
    

    CDp = Sref*0.0055/100.
    CDi = CL*CL/(np.pi*e*AR)
    
    ARL = total_length**2/Sref
    x = np.pi*ARL/4
    beta = np.sqrt(mach**2-1.)
    CDwl = CL**2*x/4*(np.sqrt(1.+(beta/x)**2)-1.)
    CDwv = 4.*t_c_w**2*(beta**2+2.*x**2)/(beta**2+x**2)**1.5
    
    CDwl = CDwl*vehicle_ref/Sref
    CDwv = CDwv*vehicle_ref/Sref
    
    CD = CDp + CDi + CDwl + CDwv    
    CD_vehicle = CD

    state.conditions.aerodynamics.drag_coefficient = CD_vehicle
    state.conditions.aerodynamics.drag_breakdown = Data()
    state.conditions.aerodynamics.drag_breakdown.total = CD_vehicle
    state.conditions.aerodynamics.drag_breakdown.parasite = Data()
    state.conditions.aerodynamics.drag_breakdown.parasite['main_wing'] = Data()
    state.conditions.aerodynamics.drag_breakdown.parasite['main_wing'].parasite_drag_coefficient = CDp*Sref/vehicle_ref
    state.conditions.aerodynamics.drag_breakdown.parasite.total = CDp
    state.conditions.aerodynamics.drag_breakdown.compressible = Data()
    state.conditions.aerodynamics.drag_breakdown.compressible.total_volume = CDwl+CDwv
    state.conditions.aerodynamics.drag_breakdown.compressible.volume_wave = CDwv
    state.conditions.aerodynamics.drag_breakdown.compressible.lift_wave   = CDwl
    state.conditions.aerodynamics.drag_breakdown.induced                  = CDi
    
    
    return CD_vehicle