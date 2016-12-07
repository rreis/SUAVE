# build_geomach_geometry.py
#
# Created:  ### ####, M. Vegh
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import SUAVE
from SUAVE.Methods.Geometry.Three_Dimensional.find_tip_chord_leading_edge import find_tip_chord_leading_edge
import numpy as np


# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------

def translate_to_geomach_geometry(wing):
    """ 
    transforms the global SUAVE coordinates into GEOMACH's coordinate system,
    which is used to build up a bunch of section-wise geometry parameters
    
    Inputs:
        wing
        
    Outputs:
        wing.root_origin
        wing.tip_origin
    """
    
    coords                       = wing.origin
    wing.root_origin             = np.array([coords[0], coords[2], coords[1]])
    coords                       = wing.tip_origin
    wing.tip_origin              = np.array([coords[0], coords[2], coords[1]])
    for section in wing.wing_sections:
        coords               = section.root_origin
        section.root_origin  = np.array([coords[0], coords[2], coords[1]])
        coords               = section.tip_origin
        section.tip_origin   = np.array([coords[0], coords[2], coords[1]])
        print dir(section)
    return