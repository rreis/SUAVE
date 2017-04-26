# Fidelity_Zero.py
#
# Created:  
# Modified: Feb 2016, Andrew Wendorff

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Data
from Markup import Markup
from SUAVE.Analyses import Process
import numpy as np

# default Aero Results
from Results import Results

# the aero methods
from SUAVE.Methods.Aerodynamics import MF_Aero_Test_Fidelity as Methods
from Process_Geometry import Process_Geometry
from Vortex_Lattice import Vortex_Lattice

# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------
class MF_Aero_Test_Fidelity(Markup):
    
    def __defaults__(self):
        
        self.tag    = 'fidelity_zero_markup'
        
        ## available from Markup
        #self.geometry = Data()
        #self.settings = Data()
        
        #self.process = Process()
        #self.process.initialize = Process()
        #self.process.compute = Process()        
    
        # correction factors
        settings = self.settings
        settings.fuselage_lift_correction           = 1.14
        settings.trim_drag_correction_factor        = 1.02
        settings.wing_parasite_drag_form_factor     = 1.1
        settings.fuselage_parasite_drag_form_factor = 2.3
        settings.oswald_efficiency_factor           = None
        settings.viscous_lift_dependent_drag_factor = 0.38
        settings.drag_coefficient_increment         = 0.0000
        settings.spoiler_drag_increment             = 0.00 
        settings.maximum_lift_coefficient           = np.inf 
        
        # vortex lattice configurations
        settings.number_panels_spanwise  = 5
        settings.number_panels_chordwise = 1
        
        
        # build the evaluation process
        compute = self.process.compute
        
        # these methods have interface as
        # results = function(state,settings,geometry)
        # results are optional
        
        # first stub out empty functions
        # then implement methods
        # then we'll figure out how to connect to a mission
        
        compute.lift = Process()

        compute.lift.inviscid_wings                = SUAVE.Methods.skip
        compute.lift.vortex                        = SUAVE.Methods.skip
        compute.lift.compressible_wings            = SUAVE.Methods.skip
        compute.lift.fuselage                      = SUAVE.Methods.skip
        compute.lift.total                         = Methods.Lift.aircraft_total
        
        compute.drag = Process()
        compute.drag.parasite                      = SUAVE.Methods.skip
        compute.drag.parasite.wings                = SUAVE.Methods.skip
        compute.drag.parasite.wings.wing           = SUAVE.Methods.skip
        compute.drag.parasite.fuselages            = SUAVE.Methods.skip
        compute.drag.parasite.fuselages.fuselage   = SUAVE.Methods.skip
        compute.drag.parasite.propulsors           = SUAVE.Methods.skip
        compute.drag.parasite.propulsors.propulsor = SUAVE.Methods.skip
        compute.drag.parasite.pylons               = SUAVE.Methods.skip
        compute.drag.parasite.total                = SUAVE.Methods.skip
        compute.drag.induced                       = SUAVE.Methods.skip
        compute.drag.compressibility               = SUAVE.Methods.skip
        compute.drag.compressibility.wings         = SUAVE.Methods.skip
        compute.drag.compressibility.wings.wing    = SUAVE.Methods.skip
        compute.drag.compressibility.total         = SUAVE.Methods.skip
        compute.drag.miscellaneous                 = SUAVE.Methods.skip
        compute.drag.untrimmed                     = SUAVE.Methods.skip
        compute.drag.trim                          = SUAVE.Methods.skip
        compute.drag.spoiler                       = SUAVE.Methods.skip
        compute.drag.total                         = Methods.Drag.aircraft_total
        
        
    def initialize(self):
        #self.process.compute.lift.inviscid_wings.geometry = self.geometry
        #self.process.compute.lift.inviscid_wings.initialize()
        pass
        
    finalize = initialize