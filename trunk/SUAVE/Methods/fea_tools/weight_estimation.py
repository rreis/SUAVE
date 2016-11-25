# weight_estimation.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#


import numpy as np
import shutil
import argparse
from mpi4py import MPI
#from baseclasses import *
#import tacs
#from tacs import *
#from repostate import *
#from pyoptsparse import *
#from pyOpt import *


#from pyOpt import SNOPT
#from pyOpt import NSGA2
#from pyOpt import COBYLA

from classes.aircraft import aircraft
from classes.aircraft import wing_section
from classes.aircraft import wing
from classes.aircraft import fuselage
#
from SUAVE.Methods.fea_tools.geomach_geometry import geometry_generation
from SUAVE.Methods.fea_tools.compute_aircraft_loads import compute_aerodynamic_loads
from SUAVE.Methods.fea_tools.setup_nastran_interface import setup_nastran_interface
from SUAVE.Methods.fea_tools.regenerate_geomach_bdf import regenerate_geomach_bdf
from SUAVE.Methods.fea_tools.pyFSI.class_str.solution_classes.sol200 import sol200
from SUAVE.Methods.fea_tools.pyFSI.output.write_tecplot_file import write_tecplot_file

from SUAVE.Methods.fea_tools.pyFSI.output.write_tecplot_file import write_tecplot_file
from SUAVE.Methods.fea_tools.classes.structural_dvs import structural_dvs
from SUAVE.Methods.fea_tools.regenerate_geomach_bdf_spanwise import regenerate_geomach_bdf_spanwise

#path to external framework
import sys
#sys.path.append('/home/anilvariyar/Desktop/weight_estimation_framework')
#sys.path.append('/home/anilvar/weight_estimation_framework')


class FEA_Weight:

    def __init__(self,filenames,output_folder = None):
        self.type = "FEA based weight estimation"
        self.geometry = None
        self.fea_mesh = None
        self.aircraft = None
        self.aero = None
        self.tacs = None
        self.nastran = None
        self.primary_structure_weight = None
        self.design_variables_fin  = None
        self.design_variables_init = None
        self.load_type = "low_fidelity_aero"
        self.s200 = sol200()
        self.structural_mesh_global_element_thicknesses = None
        self.design_iters = 0
        self.init_dv_list = None
        self.output_folder = output_folder
        self.output_folder = self.output_folder + str('/')

        self.filename = filenames
        
        self.filename.geomach_output_root = self.filename.geomach_output
        self.filename.Nastran_sol200 = self.output_folder + self.filename.Nastran_sol200
        self.filename.geomach_output = self.output_folder + self.filename.geomach_output
        self.filename.geomach_structural_surface_grid_points = self.output_folder + self.filename.geomach_structural_surface_grid_points
        self.filename.geomach_stl_mesh = self.output_folder + self.filename.geomach_stl_mesh
        self.filename.tacs_load = self.output_folder + self.filename.tacs_load
        self.filename.tacs_optimization_driver = self.output_folder + self.filename.tacs_optimization_driver
        


        
        self.filename.geomach_output_orig = self.filename.geomach_output
    
        rank = 0
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
    
        temp_output = self.filename.geomach_output.split('.')
        #print self.filename.geomach_output,temp_output
        
        self.filename.geomach_output = temp_output[0] + ("_") + str(rank) + ".bdf"
    
        #print "orig file :",self.filename.geomach_output_orig,"new file : ",self.filename.geomach_output
    
    
    
        temp_load = self.filename.tacs_load.split('.')
        self.filename.tacs_load = temp_load[0] + ("_") + str(rank) + ".txt"
    
    
    

#        self.filename['Nastran_sol200'] = filenames['Nastran_sol200']
#        self.filename['geomach_output'] = filenames['geomach_output']
#        self.filename['geomach_structural_surface_grid_points'] = filenames['geomach_structural_surface_grid_points']
#        self.filename['geomach_stl_mesh'] = filenames['geomach_stl_mesh']
#        self.filename['tacs_load']      = filenames['tacs_load']
#        self.filename['aero_load']      = filenames['aero_load']
#        self.filename['tacs_optimization_driver'] = filenames['tacs_optimization_driver']




    def supply_init_dvs(self,dv_list):
        self.init_dv_list = dv_list
    

    def import_from_suave(self,aircraft_model):
        self.aircraft = aircraft()
        self.aircraft.import_from_suave(aircraft_model)
        self.aircraft.compute()


    def setup_aircraft(self,aircraft):
        self.aircraft = aircraft


    def compute_geometry(self):
        aircraft = self.aircraft
        geometry_generation(aircraft,self.filename.geomach_output_orig,self.filename.geomach_structural_surface_grid_points,self.filename.geomach_stl_mesh)

        #shutil.copy2("conventional_str.bdf", self.filename.geomach_output_orig)
        #shutil.copy2("conventional_str", self.output_folder + "conventional_str.dat")


#        shutil.copy2(self.filename.geomach_output_root, self.filename.geomach_output_orig)
#        filename1_split = self.filename.geomach_output_root.split('.')
#        filename1 = filename1_split[0]
#        filename2 = filename1_split[0] + ".dat"
#        shutil.copy2(filename1, self.output_folder + filename2)

        print
    
    
    def compute_aerodynamics(self):
        print
    
    
    def deform_mesh(self):
        
        #read in input parameters
        
        #deform the mesh by calling the deforming methodology
        
        #regenerate the geomach bdf file
        
        #
        
        print
    
    
    def setup_design_problem(self,recompute_dvs,split_mesh):
        aircraft=self.aircraft
        
        
        if(recompute_dvs>0):
            regenerate_geomach_bdf_spanwise(self.filename.geomach_output_orig,self.filename.geomach_output,aircraft)
            #regenerate_geomach_bdf(self.filename.geomach_output_orig,self.filename.geomach_output,aircraft)
            
            if (self.design_iters == 0):
                self.structural_mesh_global_element_thicknesses = np.zeros(len(self.aircraft.structural_mesh_shell_element_list))
        
        s200 = self.s200
        s200.split_mesh = split_mesh
        loads_scale_factor = 1.0
        setup_nastran_interface(s200,self.filename.geomach_output,self.load_type,self.filename.aero_load,self.filename.Nastran_sol200,aircraft,loads_scale_factor)
        
        #s200.write_tacs_load_file(self.filename.tacs_load)
        tacs_load_tecplot = self.output_folder + "visualize_s200_loads.plt"
        s200.visualize_loading(tacs_load_tecplot)
        for i in range(0,len(aircraft.main_wing)):
            print "wing loading ",i," : ",aircraft.main_wing[i].tag," : ",aircraft.main_wing[i].total_force
    
    

        self.design_variables_init = np.zeros(s200.no_of_design_variables)
        
        if (self.design_iters == 0):
            
            if(self.init_dv_list is not None):
                for i in range(0,s200.no_of_design_variables):
                    s200.design_var_list[i].xinit = self.init_dv_list[i]
                    self.design_variables_init[i] = s200.design_var_list[i].xinit
            
            else:
            
                for i in range(0,s200.no_of_design_variables):
                    self.design_variables_init[i] = s200.design_var_list[i].xinit

        else:
            
            for i in range(0,len(self.structural_mesh_global_element_thicknesses)):
#            structural_mesh_global_element_thicknesses
#            for i in range(0,len(self.aircraft.structural_mesh_shell_map)):
                s200.design_var_list[int(self.aircraft.structural_mesh_shell_map[i])-1].xinit = self.structural_mesh_global_element_thicknesses[i]
                self.design_variables_init[int(self.aircraft.structural_mesh_shell_map[i])-1] = s200.design_var_list[int(self.aircraft.structural_mesh_shell_map[i])-1].xinit


                #print "dv : ",int(self.aircraft.structural_mesh_shell_map[i])-1," ",self.structural_mesh_global_element_thicknesses[i]," ",self.design_variables_init[int(self.aircraft.structural_mesh_shell_map[i])-1]


    def setup_loading(self,method):
        #method 0 for low fidelity, 1 for panel method
        print



    def preprocess_for_tacs(self):
        aircraft= self.aircraft
        s200.write_tacs_load_file(self.filename.tacs_load)
        print
    
    
    
    def preprocess_for_nastran(self):
        print




    def evaluate_weight(self,fea_code):
        aircraft =  self.aircraft
        
        #fea code 0 for nastran, 1 for tacs
        if(fea_code==0):
            print

        elif(fea_code == 1):
            in_vals = 0.0
            self.run_Nastran_optimization(in_vals)




    def run_Nastran_optimization(self,in_vals):
        
        import sys
        import time
        import subprocess
        
        #system calls to Nastran
        
        log_file = "log_filename.txt"
        err_file = "err_file.txt"
        
        filenames_array = [log_file,err_file,self.nastran_filename]
        
        #remove existing files from the directory
        for f in filenames_array:
            try:
                os.remove(f)
                except OSError:
                    pass

        
        aswing_call = self.nastran_path+" "+"nastran"
        
        #1st set the operating conditions
        icond = 0
        commands = []

        
        with redirect.output(log_file,err_file):
            
            ctime = time.ctime() # Current date and time stamp

            
            nastran_run = subprocess.Popen([aswing_call,self.nastran_filename],stdout=sys.stdout,stderr=sys.stderr,stdin=subprocess.PIPE)
            
            nastran_run.wait()
            
            exit_status = nastran_run.returncode
            ctime = time.ctime()
            sys.stdout.write("\nProcess finished: {0}\nExit status: {1}\n".format(ctime,exit_status))


        pass




    def visualize_structural_optimization_results(self,filename=None):
        
        aircraft =  self.aircraft
        s200 =self.s200

        if (filename==None):
            filename = self.output_folder + "tacs_element_thicknesses.plt"
        
        #write_tecplot_file(s200.pointlist,s200.elemlist_quad,filename,s200.no_of_points,len(s200.elemlist_quad))
        
        write_tecplot_file(s200.pointlist,s200.elemlist,filename,len(s200.pointlist),len(s200.elemlist_quad))

        s101_output_filename_fin = self.output_folder + "CRM_wing_baseline_s101_fin.bdf"
        s200.write_sol_101_file(s101_output_filename_fin)
        
        
        print



    def update_the_origin_structural_element(self):
    
        print
    
    
    def update_the_dvs(self,dv_value):
        aircraft = self.aircraft
        
        aircraft.dv_breakdown.wings[0].upper.required_no_of_elements = dv_value #14
        aircraft.dv_breakdown.wings[0].upper.element_nos[:] = []
        aircraft.dv_breakdown.wings[0].upper.element_tags[:] = []
        aircraft.dv_breakdown.wings[0].upper.no_of_elements = 0
        
        aircraft.dv_breakdown.wings[0].lower.required_no_of_elements = dv_value #14
        aircraft.dv_breakdown.wings[0].lower.element_nos[:] = []
        aircraft.dv_breakdown.wings[0].lower.element_tags[:] = []
        aircraft.dv_breakdown.wings[0].lower.no_of_elements = 0
        
        
        aircraft.dv_breakdown.wings[0].tip.required_no_of_elements = dv_value #14
        aircraft.dv_breakdown.wings[0].tip.element_nos[:] = []
        aircraft.dv_breakdown.wings[0].tip.element_tags[:] = []
        aircraft.dv_breakdown.wings[0].tip.no_of_elements = 0
        
        
        aircraft.dv_breakdown.wings[0].spars.required_no_of_elements = dv_value #14
        aircraft.dv_breakdown.wings[0].spars.element_nos[:] = []
        aircraft.dv_breakdown.wings[0].spars.element_tags[:] = []
        aircraft.dv_breakdown.wings[0].spars.no_of_elements = 0
        
        
        aircraft.dv_breakdown.wings[0].ribs.required_no_of_elements = dv_value #14
        aircraft.dv_breakdown.wings[0].ribs.element_nos[:] = []
        aircraft.dv_breakdown.wings[0].ribs.element_tags[:] = []
        aircraft.dv_breakdown.wings[0].ribs.no_of_elements = 0
        
        
        aircraft.dv_breakdown.miscellaneous[0].dv.required_no_of_elements = 1 #dv_value #14
        aircraft.dv_breakdown.miscellaneous[0].dv.element_nos[:] = []
        aircraft.dv_breakdown.miscellaneous[0].dv.element_tags[:] = []
        aircraft.dv_breakdown.miscellaneous[0].dv.no_of_elements = 0
        
        
        aircraft.dv_breakdown.miscellaneous[1].dv.required_no_of_elements = 1 #dv_value #14
        aircraft.dv_breakdown.miscellaneous[1].dv.element_nos[:] = []
        aircraft.dv_breakdown.miscellaneous[1].dv.element_tags[:] = []
        aircraft.dv_breakdown.miscellaneous[1].dv.no_of_elements = 0
        
        

        aircraft.dv_breakdown.compute_structural_dvs()


    def FFD_deform_structure(self):
        print
                                                                                                  
                                                                                                  
                                                                                                  
    __call__ = evaluate_weight







class Filenames:
    
    def __init__(self):

        self.Nastran_sol200 = "CRM_wing_baseline_opt.bdf"
        self.geomach_output = "CRM_wing_str.bdf"
        self.geomach_structural_surface_grid_points = "pt_str_surf.dat"
        self.geomach_stl_mesh = "CRM_wing.stl"
        self.tacs_load = "geomach_tacs_load_crm_wing.txt"
        self.aero_load = None
        self.tacs_optimization_driver = "design_run_fsi_crm_wing.py"
