# weight_estimation.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#


import numpy as np
import shutil
import argparse
from mpi4py import MPI
from baseclasses import *
import tacs
from tacs import *
#from repostate import *
#from pyoptsparse import *
from pyOpt import *


from pyOpt import SNOPT
#from pyOpt import NSGA2
#from pyOpt import COBYLA

from classes.aircraft import aircraft
from classes.aircraft import wing_section
from classes.aircraft import wing
from classes.aircraft import fuselage
#
#from pyFSI.functions.geometry_generation import geometry_generation
#from pyFSI.functions.compute_aircraft_loads import compute_aerodynamic_loads
#from pyFSI.functions.setup_nastran_interface import setup_nastran_interface
#from pyFSI.functions.regenerate_geomach_bdf import regenerate_geomach_bdf
#from pyFSI.class_str.solution_classes.sol200 import sol200
#from pyFSI.output.write_tecplot_file import write_tecplot_file
#
#from pyFSI.output.write_tecplot_file import write_tecplot_file
#from pyFSI.classes.structural_dvs import structural_dvs
#from pyFSI.functions.regenerate_geomach_bdf_spanwise import regenerate_geomach_bdf_spanwise

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

        shutil.copy2("strut_braced_str.bdf", self.filename.geomach_output_orig)
        shutil.copy2("strut_braced_str", self.output_folder + "strut_braced_str.dat")


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
        
        s200.write_tacs_load_file(self.filename.tacs_load)
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
            self.run_tacs_optimization(in_vals)




    def run_tacs_optimization(self,in_vals):
        aircraft =  self.aircraft
        filenames = self.filename
        shell_element_lists_redone = aircraft.shell_element_lists_redone
        
        s200 = self.s200
        s101_output_filename = self.output_folder + "CRM_wing_baseline_s101.bdf"
        s200.write_sol_101_file(s101_output_filename)
        
#        comm = MPI.COMM_WORLD
#        comm.Barrier()
        #execfile(self.filename.tacs_optimization_driver)
            
            
                    
        # ================================================================
        #                   INPUT INFORMATION
        # ================================================================
        parser = argparse.ArgumentParser()
        #parser.add_argument("--opt", help="optimizer to use", type=str, default='snopt')
        #parser.add_argument('--optOptions', type=str, help='Options for the optimizer', default="{}")
        args = parser.parse_args()
        #exec('optOptions=%s'% args.optOptions)

#        outputDirectory =  '../weight_estimation_framework'
#        bdfFile = '../weight_estimation_framework/CRM_wing_str.bdf'
#        loadfile = "../weight_estimation_framework/geomach_tacs_load_crm_wing.txt"



        
        outputDirectory =  self.output_folder #'../weight_estimation_framework'
        bdfFile = filenames.geomach_output # "../weight_estimation_framework/" + filenames.geomach_output
        loadfile = filenames.tacs_load # "../weight_estimation_framework/" + filenames.tacs_load   #geomach_tacs_load_crm_wing.txt"
        #structSetup = '../weight_estimation_framework/tacs/python/setup_structure_fsi_opt4.py'
        #forcefile = 'forces_truss_braced_aircraft'

        gcomm = comm = MPI.COMM_WORLD
        loadFactor = 1.5 #2.5
        KSWeight = 80.0
        #SPs = [StructProblem('lc0',loadFile='../weight_estimation_framework/geomach_tacs_load_crm_wing.txt',evalFuncs=['mass','ks0'])]
        SPs = [StructProblem('lc0',loadFile=loadfile,evalFuncs=['mass','ks0'])]
        numLoadCases = 1 #len(SPs)
        structOptions = {'transferSize':0.5,
            'transferGaussOrder':3}


        #setting up the structure to output data


        # Run common structural setup

        # ---------------------------------------------------
        # Setup Structural problem
        # ---------------------------------------------------
        # Material properties
        rho_2024 = 2780.
        E_2024 = 73.9e9 #73.1e9
        ys_2024 = 420.0e6
        nu = 0.33
        t = .02
        tMin = 0.0016 # 1/16"
        tMax = 0.030
        kcorr = 5.0/6.0

        #nDvs      = 251
        #scaleList = [ float() for dv in range(nDvs)]
        #for i in range(0,nDvs):
        #    scaleList[i] = 1.05*tMax
        comm = MPI.COMM_WORLD
        loc_group = comm.Get_group()
        loc_rank = comm.Get_rank()
        loc_rank_array = [loc_rank]
        new_loc_group = MPI.Group.Incl(loc_group,loc_rank_array)
        loc_comm = comm.Create(new_loc_group)


        FEASolver = pytacs.pyTACS(bdfFile, comm=loc_comm, options=structOptions)
        pressure = 50000

        #locally import the load from the fluid file (maybe su2)

        #locally import the load from the fluid file (maybe su2)





        ncoms = FEASolver.nComp

        t_List = self.design_variables_init

        for i in range(0,ncoms):
            
            dv_name = 'stru_'+str(i)
            FEASolver.addDVGroup(dv_name, include = i)
        #t_List[i] = 0.02

        #t_List[0] = 0.02124
        #t_List[1] = 0.01953
        #t_List[2] = 0.0016
        #t_List[3] = 0.00464
        #t_List[4] = 0.00160
        #t_List[5] = 0.02429
        #t_List[6] = 0.00160





        def conCallBack(dvNum, compDescripts, userDescript, specialDVs,iter, **kargs):
            con = constitutive.isoFSDTStiffness(rho_2024, E_2024, nu, kcorr,ys_2024,t_List[iter] , dvNum, tMin, tMax)
            #con = constitutive.isoFSDTStiffness(rho_2024, E_2024, nu, kcorr,ys_2024,shell_element_lists_redone[iter].t , dvNum, shell_element_lists_redone[iter].t_min, shell_element_lists_redone[iter].t_max)
            #con = constitutive.isoFSDTStiffness(rho_2024, E_2024, nu, kcorr,ys_2024, t, dvNum, tMin, tMax)
            scale = [100.0]
            return con, scale




        FEASolver.createTACSAssembler(conCallBack)


        # --------------- Add Functions -------------------------
        # Mass Functions
        FEASolver.addFunction('mass', functions.StructuralMass)



        # KS Functions
        ks0 = FEASolver.addFunction('ks0', functions.AverageKSFailure, KSWeight=KSWeight, loadFactor=loadFactor)
            




        #execfile(structSetup)






        #FEASolver.addFunction('MS0', tacs.functions.MaxFailure)


        def obj(x):
            '''Evaluate the objective and constraints'''
            funcs = {}

            in_time = MPI.Wtime()
            
            FEASolver.setDesignVars(x)
            for i in range(numLoadCases):
                FEASolver(SPs[i])
                FEASolver.evalFunctions(SPs[i], funcs)
            if comm.rank == 0:
                print funcs


            fin_time = MPI.Wtime()
            
            print "Obj_time : ",fin_time-in_time

            f = funcs['lc0_mass']/1.0


            g = [funcs['lc0_ks0']]
            #g = [funcs['lc0_MS0']]
            
            fail = 0
            return f, g, fail
        #return funcs, False

        def sens(x, f,g):
            '''Evaluate the objective and constraint sensitivities'''
            funcsSens = {}
                      
            FEASolver.setDesignVars(x)
            for i in range(numLoadCases):
                FEASolver(SPs[i])
                FEASolver.evalFunctionsSens(SPs[i], funcsSens)

            #print funcsSens
            #extract the actual data
            df1 = funcsSens['lc0_mass'][FEASolver.varSet]
            g1 = funcsSens['lc0_ks0'][FEASolver.varSet]

            df = [0.0]*len(df1)
            for i  in range(0,len(df1)):
                df[i] = df1[i]


            dg = []

            dg = np.zeros([1,len(g1)])
            
            for i  in range(0,len(g1)):
                dg[0][i] = g1[i]

            fail = 0
            return df, dg, fail
        #return funcsSens, False



        #Run an initial solution


        # Depending on the user supplied options generate the
        # write_flag
        writeNodes = 1
        writeDisplacements = 1
        writeStrains = 1
        writeStresses = 1
        writeExtras = 0
        writeCoordinateFrame = 0
        writeDesignVariables = 0

        print "Options"
        print FEASolver.getOption('writeNodes')
        print FEASolver.getOption('writeDisplacements')
        print FEASolver.getOption('writeStrains')
        print FEASolver.getOption('writeStresses')
        print FEASolver.getOption('writeExtras')
        print FEASolver.getOption('writeCoordinateFrame')
        print FEASolver.getOption('writeDesignVariables')


        #FEASolver.getOption('writeNodes',True)
        #FEASolver.setOption('writeDisplacements',True)
        #FEASolver.setOption('writeStrains',True)
        #FEASolver.setOption('writeStresses',True)
        #FEASolver.setOption('writeExtras',False)
        #FEASolver.setOption('writeCoordinateFrame',False)
        #FEASolver.setOption('writeDesignVariables',False)





        write_flag = 0

        #if (writeNodes == 1):
        if FEASolver.getOption('writeNodes'):
            write_flag += FEASolver.elements.TACSElement.OUTPUT_NODES

        #if (writeDisplacements == 1):
        if FEASolver.getOption('writeDisplacements'):
            write_flag += FEASolver.elements.TACSElement.OUTPUT_DISPLACEMENTS

        #if (writeStrains == 1):
        if FEASolver.getOption('writeStrains'):
            write_flag += FEASolver.elements.TACSElement.OUTPUT_STRAINS

        #if (writeStresses == 1):
        if FEASolver.getOption('writeStresses'):
            write_flag += FEASolver.elements.TACSElement.OUTPUT_STRESSES

        #if (writeExtras == 1):
        if FEASolver.getOption('writeExtras'):
            write_flag += FEASolver.elements.TACSElement.OUTPUT_EXTRAS

        #if (writeCoordinateFrame == 1):
        if FEASolver.getOption('writeCoordinateFrame'):
            write_flag += FEASolver.elements.TACSElement.OUTPUT_COORDINATES

        #if (writeDesignVariables == 1):
        if FEASolver.getOption('writeDesignVariables'):
            write_flag += FEASolver.elements.TACSElement.OUTPUT_DESIGN_VARIABLES



        FEASolver(SPs[0])


        displacements_file_name = self.output_folder  + 'optimization_initialize.txt' #'../weight_estimation_framework/optimization_initialize.txt'

        elem_type = FEASolver.elements.SHELL
        output_data = FEASolver.structure.extract_outputs(FEASolver.curLoadCase, elem_type,write_flag,displacements_file_name)

        visualize_forces_tacs = self.output_folder + "visualize_forces_crm_wing_design.f5"

        FEASolver.writeForcesFile(SPs[0], visualize_forces_tacs)
        FEASolver.writeSolution()
        tacs_initial_bdf = self.output_folder + "crm_wing_design_tacs_initial.bdf"
        FEASolver.writeBDF(tacs_initial_bdf)
        crm_wing_element_stresses = self.output_folder + "crm_wing_design_tacs_initial_stress.txt"
        FEASolver.structure.write_element_stresses(crm_wing_element_stresses,FEASolver.curLoadCase)




        # Set up the optimization problem
        optProb = Optimization('Mass min', obj)
        optProb.addObj('lc0_mass')
        FEASolver.addVariablesPyOpt(optProb)

        for i in range(numLoadCases):
            for j in xrange(1):
                optProb.addCon('%s_ks%d'% (SPs[i].name, j), upper=1.0)
        if comm.rank == 0:
            print optProb
        #optProb.printSparsity()




        # Instantiate Optimizer (SNOPT) & Solve Problem
        
        snopt = SNOPT()
        #snopt.setOption('iprint',-1)
#        snopt.setOption('Nonderivative linesearch')
#        snopt.setOption('Major feasibility tolerance',1.0e-6)
#        snopt.setOption('Major optimality tolerance',1.0e-6)
#        snopt.setOption('Minor feasibility tolerance',1.0e-6)
        [obj_fun, x_dvs, inform] = snopt(optProb,sens_type=sens)
        #print optProb.solution(0)
        snopt_out_file = self.output_folder + "strut_braced_full_airc_span_2_opt_pySNOPT.txt"
        optProb.write2file(outfile=snopt_out_file, disp_sols=False, solutions=[0])





#        # Instantiate Optimizer (NSGA2) & Solve Problem
#        
#        nsga2 = NSGA2(pll_type='POA')
#        #snopt.setOption('iprint',-1)
#        [obj_fun, x_dvs, inform] = nsga2(optProb)
#        #print optProb.solution(0)
#        optProb.write2file(outfile='strut_braced_full_airc_span_2_opt_pySNOPT.txt', disp_sols=False, solutions=[0])

        
        
        
        
        
#        # Instantiate Optimizer (COBYLA) & Solve Problem
#        
#        cobyla = COBYLA(pll_type='POA')
#        #snopt.setOption('iprint',-1)
#        [obj_fun, x_dvs, inform] = cobyla(optProb)
#        #print optProb.solution(0)
#        optProb.write2file(outfile='strut_braced_full_airc_span_2_opt_pySNOPT.txt', disp_sols=False, solutions=[0])










        #Getting the final solution
        FEASolver.setDesignVars(x_dvs)
        FEASolver(SPs[i])


        elem_type = FEASolver.elements.SHELL
        #output_data = FEASolver.structure.extract_outputs(FEASolver.curLoadCase, elem_type,write_flag,displacements_file_name)


        tacs_f5_visualize = self.output_folder + "visualize_forces_crm_wing_design.f5"
        FEASolver.writeForcesFile(SPs[0], tacs_f5_visualize)
        
        tacs_forces_bdf_visualize = self.output_folder + "visualize_forces_crm_wing_design.bdf"
        FEASolver.writeBDFForces(SPs[0], tacs_forces_bdf_visualize)
        FEASolver.writeSolution()
        
        tacs_final_design_bdf = self.output_folder + "crm_wing_design_tacs_final.bdf"
        FEASolver.writeBDF(tacs_final_design_bdf)
        
        tacs_element_stresses_output = self.output_folder + "crm_wing_design_tacs_final_stress.txt"
        FEASolver.structure.write_element_stresses(tacs_element_stresses_output,FEASolver.curLoadCase)


        
        
        
        
        
        self.primary_structure_weight = obj_fun
                                       
        print "Primary structure weight : ",self.primary_structure_weight
                                                                                              
        self.design_variables = x_dvs
        
                                                                                              
        for i in range(0,len(x_dvs)):
            s200.shell_element_list[i].t=x_dvs[i]

        for i in range (0,len(s200.elemlist_quad)):
            s200.elemlist_quad[i].thickness = x_dvs[s200.elemlist_quad[i].pid-1]
    
            for j in range(0,4):
                s200.pointlist[s200.elemlist_quad[i].g[j]-1].thickness = x_dvs[s200.elemlist_quad[i].pid-1]


        #-------update the primal element mesh------------------------------------

        self.design_iters = self.design_iters + 1



#        for i in range(0,len(self.aircraft.structural_mesh_shell_map)):
#            self.structural_mesh_global_element_thicknesses[i] = s200.shell_element_list[int(self.aircraft.structural_mesh_shell_map[i])-1].t
#            aircraft.shell_element_lists_redone[i].t = self.structural_mesh_global_element_thicknesses[i]
#            aircraft.shell_element_lists_redone[i].t_min = aircraft.shell_element_lists_redone[i].t*(1.0-0.8)
#            aircraft.shell_element_lists_redone[i].t_max = aircraft.shell_element_lists_redone[i].t*(1.0+0.2)
#            
#        aircraft.shell_element_lists_redone_int = 1
#            #print "t : ",self.structural_mesh_global_element_thicknesses[i]



        self.visualize_structural_optimization_results()





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
