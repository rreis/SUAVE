
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Core import Data, Data_Exception, Data_Warning


# default Aero Results
from SUAVE.Analyses import Analysis, Results

import numpy as np

# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------

class External(Analysis):
    """ SUAVE.Analyses.External.External()
    """
    def __defaults__(self):
        self.tag    = 'external'
        self.geometry = Data()
        self.settings = Data()
        
        
    def evaluate(self,state=None):
        print "Linking to an external module"
        return Results()

    __call__ = evaluate