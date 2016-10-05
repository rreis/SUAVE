
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Data, Data_Exception, Data_Warning
from SUAVE.Analyses import Analysis, Results
from External import External

#path to external framework
import sys
#sys.path.append('')



#from SUAVE.Methods.fea_tools import geometry_generation
from SUAVE.Methods.fea_tools.weight_estimation import FEA_Weight
from SUAVE.Methods.fea_tools.weight_estimation import Filenames

# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------

class UADF(External):
    """ SUAVE.Analyses.External.UADF()
    """
    def __defaults__(self):
        self.tag = 'weights'
        self.vehicle  = Data()
        self.settings = Data()
        self.external = None

        
        
    def evaluate(self,conditions=None):
        
        #call Geomach driver from weight estimation framework
        print "Calling geometry from weight estimation framework"
        self.external.import_from_suave(self.vehicle)
        
#        filenames = Filenames()
#        
#        filenames.Nastran_sol200 = "CRM_wing_baseline_opt.bdf"
#        filenames.geomach_output = "CRM_wing_str.bdf"
#        filenames.geomach_structural_surface_grid_points = "pt_str_surf.dat"
#        filenames.geomach_stl_mesh = "CRM_wing.stl"
#        filenames.tacs_load = "geomach_tacs_load_crm_wing.txt"
#        filenames.aero_load = None
#        filenames.tacs_optimization_driver = "design_run_fsi_crm_wing.py"
#        CRM_wing = FEA_Weight(filenames)
#        self.vehicle.external = CRM_wing

        return Results()
    
    
    def finalize(self):
        
        
        return
        