# tube.py
# 
# Created:  Andrew Wendorff, Jan 2014
# Modified: Andrew Wendorff, Feb 2014       


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Core import Units
from SUAVE.Core import (
    Data, Container, Data_Exception, Data_Warning,
)

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------


def tube_secondary(S_fus, diff_p_fus, w_fus, h_fus, l_fus, Nlim, wt_zf, wt_wing, wt_propulsion, wing_c_r):
    """ weight = SUAVE.Methods.Weights.Correlations.Tube_Wing.tube(S_fus, diff_p_fus, w_fus, h_fus, l_fus, Nlim, wt_zf, wt_wing, wt_propulsion, wing_c_r)
        Calculate the weight of a fuselage in the state tube and wing configuration
        
        Inputs:
            S_fus - fuselage wetted area [meters**2]
            diff_p_fus - Maximum fuselage pressure differential [Pascal]
            w_fus - width of the fuselage [meters]
            h_fus - height of the fuselage [meters]
            l_fus - length of the fuselage [meters]
            Nlim - limit load factor at zero fuel weight of the aircraft [dimensionless]
            wt_zf - zero fuel weight of the aircraft [kilograms]
            wt_wing - weight of the wing of the aircraft [kilograms]
            wt_propulsion - weight of the entire propulsion system of the aircraft [kilograms]
            wing_c_r - wing root chord [meters]
            
        Outputs:
            weight - weight of the fuselage [kilograms]
            
        Assumptions:
            fuselage in a standard wing and tube configuration 
    """
    # unpack inputs
    

        
    #Calculate weight of wing for traditional aircraft vertical tail without rudder
    fuselage_weight = 0.0 * Units.lb # Convert from lbs to kg
    
    return fuselage_weight