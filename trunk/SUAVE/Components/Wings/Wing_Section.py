

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np

from SUAVE.Core import Data, Data_Exception, Data_Warning
from SUAVE.Components import Component, Physical_Component, Lofted_Body, Mass_Properties
from Airfoils import Airfoil

# ------------------------------------------------------------
#   Wing
# ------------------------------------------------------------

#class Wing_Section(Lofted_Body):
    
class Wing_Section:
    def __init__(self):

        self.tag = 'wing_section'
        self.type = ' '
        self.root_chord  = 0.0
        self.tip_chord   = 0.0
        self.mid_chord   = 0.0
        self.root_origin = [0.0,0.0,0.0]
        self.tip_origin  = [0.0,0.0,0.0]
        self.mid_origin  = [0.0,0.0,0.0]
        self.span        = 0.0
        self.sweep       = 0.0


