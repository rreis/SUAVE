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

def find_tip_chord_leading_edge(wing):
    '''
    Computes the location of the leading edge of the tip chord relative to the
    leading edge of the wing
    '''    
    rc    = wing.chords.root
    tc    = wing.chords.tip
    b     = wing.spans.projected
    sweep = wing.sweep
    y_offset = (rc/4.)-(2./b)*np.tan(sweep)-tc/4.
    return y_offset