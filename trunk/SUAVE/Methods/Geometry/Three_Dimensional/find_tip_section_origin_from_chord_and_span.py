#find_tip_chord_leading_edge.py
#
#Created:  May 2016 by M. Vegh



# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np


# ----------------------------------------------------------------------
#  find_tip_chord_leading_edge
# ---------------------------------------------------------------------- 

def find_tip_section_origin_from_chord_and_span(wing_section):
    '''
    Computes the location of the leading edge of the tip chord relative to the
    leading edge of the wing
    '''    
    rc    = wing_section.root_chord
    tc    = wing_section.tip_chord
    b     = wing_section.span
    sweep = wing_section.sweep
    if wing.vertical:
        x_offset = (rc/4.)+b*np.tan(sweep)-tc/4.
        y_offset = 0.
        z_offset = b
    else:
        x_offset = (rc/4.)+(b)*np.tan(sweep)-tc/4.
        y_offset = b
        z_offset = 0.        
    
    return np.array([x_offset,y_offset,z_offset])