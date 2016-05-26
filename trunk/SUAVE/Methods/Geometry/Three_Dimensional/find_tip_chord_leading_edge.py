#find_tip_chord_leading_edge.py
#
#Created:  May 2016 by M. Vegh

# compute_chord_length_from_span_location.py

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------


import numpy as np
# ----------------------------------------------------------------------
#  Compute Chord Length from Span Location
# ---------------------------------------------------------------------- 



def find_tip_chord_leading_edge(wing):
    '''
    Computes the chord length given a location along the half-span.
    Assumes linear variation of chord with span
    '''    
    rc    = wing.chords.root
    tc    = wing.chords.tip
    b     = wing.spans.projected
    sweep = wing.sweep
    y_offset = (rc/4.)-(2./b)*np.tan(sweep)-tc/4.
    return y_offset