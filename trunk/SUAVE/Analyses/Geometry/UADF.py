# weight_estimation.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from SUAVE.Core import Data, Data_Exception, Data_Warning
from SUAVE.Analyses import Analysis, Results
from Geometry import Geometry

#path to external framework
import sys
#sys.path.append('/home/anilvariyar/Desktop/weight_estimation_framework')
#
#import SUAVE.Methods.fea_tools.pyFSI
#import weight_estimation
#
#
#from SUAVE.Methods.fea_tools.pyFSI.functions.geometry_generation import geometry_generation
#from weight_estimation import FEA_Weight
#from weight_estimation import Filenames

# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------

class UADF(Geometry):
    """ SUAVE.Analyses.Geometry.Geometry()
    """
    def __defaults__(self):
        self.tag    = 'geometry'
        self.features = Data()
        self.vehicle  = Data()
        self.settings = Data()
        self.external = None
        
        
    def evaluate(self,condtitions=None):
        
        #call Geomach driver from weight estimation framework
        print "Calling geometry from weight estimation framework"
        
        
        self.external.compute_geometry()

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

        
        return Results()
    
        