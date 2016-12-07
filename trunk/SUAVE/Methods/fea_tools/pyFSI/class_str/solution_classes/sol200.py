#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#---Class structure for this----------------------
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import str_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_forms
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_forms
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.print_equation import print_equation
from SUAVE.Methods.fea_tools.pyFSI.input.read_su2_surface_file_euler import read_su2_surface_file_euler
from SUAVE.Methods.fea_tools.pyFSI.input.read_su2_surface_file_euler_f import read_su2_surface_file_euler_f
from SUAVE.Methods.fea_tools.pyFSI.input.read_bdf_file import read_bdf_file
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import FORCE
from SUAVE.Methods.fea_tools.pyFSI.output.write_tacs_load_file import write_tacs_load_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file import read_opt_f06_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file_stress import read_opt_f06_file_stress
from SUAVE.Methods.fea_tools.pyFSI.output.write_tecplot_file import write_tecplot_file
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.split_mesh import split_mesh
from SUAVE.Methods.fea_tools.pyFSI.input.import_s200_bdf import import_s200_bdf
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import SPC
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.compute_centroid import compute_centroid
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.compute_normal import compute_normal
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import PLOAD
from SUAVE.Methods.fea_tools.pyFSI.output.visualize_tacs_results import visualize_tacs_results


class sol200:
    def __init__(self):
        self.pointlist=[]
        self.pointlist_fl=[]
        self.load_list=[]
        self.elemlist=[]
        self.case_control_def=[]
        self.DESOBJ=None
        self.load_type=None
        self.material_list=[]
        self.shell_element_list=[]
        self.beam_element_list=[]
        self.spc_type=None
        self.constrained_grid_point_list=[]
        self.case_control_def=None
        self.case_control_analysis_type=None
        self.design_var_list=[]
        self.dresp1_list=[]
        self.dresp2_list=[]
        self.constraint_list=[]
        self.dconadd_list=[]
        self.opt_parameters=[]
   
        
        self.no_of_points=0
        self.no_of_elements=0
        self.no_of_beams=0
        self.no_of_shell_elements=0
        self.no_of_beam_elements=0
        self.no_of_materials=0
        self.no_of_constrained_grid_points=0
        self.no_of_grid_points_w_load=0
        self.no_of_design_variables=0
        self.no_of_property_types=0
        self.no_of_dresp1=0
        self.no_of_dresp2=0
        self.no_of_equations=0
        self.no_of_constraints=0
        self.no_of_dconadd=0
        self.times = 600
        self.sol =200
        self.split_mesh = 0
        
        self.output_filename=None
        
    def __defaults__(self):
        print "default values"

    def read_bdf(self,mesh_filename):
    
        [elemlist,pointlist,no_of_points,no_of_elements,material_list,no_of_materials,shell_element_list,no_of_shell_elements,constrained_grid_point_list,no_of_constrained_grid_points] = read_bdf_file(mesh_filename,1.0)
        
        
        self.elemlist_quad = elemlist
        
        if (self.split_mesh == 1):
            elemlist_tria = split_mesh(elemlist)
            self.elemlist = elemlist_tria
            self.no_of_elements = len(elemlist_tria)
        else:
            self.elemlist = elemlist
            self.no_of_elements = no_of_elements
        
        
        
        compute_centroid(self.elemlist,pointlist)
        compute_normal(self.elemlist,pointlist)
        
        node_element_count = [ int() for i in range(no_of_points)]
        
        for i in range(0,no_of_points):
            node_element_count[i] = 0
        
        
        
        for i in range(0,len(self.elemlist_quad)):
            if (self.elemlist_quad[i].type == "CQUAD4"):
                for j in range(0,4):
                    node_element_count[self.elemlist_quad[i].g[j]-1]+=1
        
            elif (self.elemlist_quad[i].type == "CTRIA3"):
                for j in range(0,3):
                    node_element_count[self.elemlist_quad[i].g[j]-1]+=1
        
        
        
        self.node_element_count = node_element_count
        
        
        self.pointlist = pointlist
        self.material_list = material_list
        self.shell_element_list = shell_element_list
        self.constrained_grid_point_list = constrained_grid_point_list
        
        
        self.no_of_points = no_of_points
        self.no_of_materials = no_of_materials
        self.no_of_shell_elements = no_of_shell_elements
        self.no_of_constrained_grid_points = no_of_constrained_grid_points
    


    def read_load_file(self,loads_filename,filetype):
    
        if (filetype == "su2_euler"):
            pointlist_fl,no_of_points_fl,local_to_global_points_fl,global_to_local_points_fl =  read_su2_surface_file_euler(loads_filename)
            
            self.pointlist_fl = pointlist_fl
            self.no_of_points_fl = no_of_points_fl
            self.local_to_global_points_fl = local_to_global_points_fl
            self.global_to_local_points_fl = global_to_local_points_fl



        if (filetype == "su2_euler_f"):
            pointlist_fl,no_of_points_fl,local_to_global_points_fl,global_to_local_points_fl =  read_su2_surface_file_euler_f(loads_filename)
        
            self.pointlist_fl = pointlist_fl
            self.no_of_points_fl = no_of_points_fl
            self.local_to_global_points_fl = local_to_global_points_fl
            self.global_to_local_points_fl = global_to_local_points_fl



            

    def compute_nastran_loads(self):
    #interpolate_loads(self.pointlist_fl,self.pointlist,self.elemlist)
    
        no_of_points_str = self.no_of_points
        pointlist_str = self.pointlist
        
        coord_system=0
        
        load_count = 0
        
        load_list = [ FORCE() for i in range(no_of_points_str)]
        for i in range(0,no_of_points_str):
            
            if(np.abs(pointlist_str[i].f[0])>=0.0000001 or np.abs(pointlist_str[i].f[1])>=0.0000001 or np.abs(pointlist_str[i].f[2])>=0.0000001 ):
                
                load_list[load_count].type='FORCE'
                load_list[load_count].sid=1
                load_list[load_count].g=pointlist_str[i].id #pointlist_fl[pcount].id
                load_list[load_count].cid=coord_system
                load_list[load_count].f= 1.0
                load_list[load_count].n1=pointlist_str[i].f[0]
                load_list[load_count].n2=pointlist_str[i].f[1]
                load_list[load_count].n3=pointlist_str[i].f[2]
                load_list[load_count].area = pointlist_str[i].area
                load_count = load_count +1


#        pressure_load_count = 0
#        no_of_elements_str = len(self.elemlist)
#        pressure_load = [ PLOAD() for i in range(no_of_elements_str)]
#        for i in range(0,no_of_elements_str):
#        
#            if(np.abs(self.elemlist[i].pressure)>=0.0000001):
#                
#                pressure_load[pressure_load_count].type='FORCE'
#                pressure_load[pressure_load_count].sid=1
#                pressure_load[pressure_load_count].p=pointlist_str[i].id #pointlist_fl[pcount].id
#                pressure_load[pressure_load_count].cid=coord_system
#                pressure_load[pressure_load_count].f= 1.0
#                pressure_load[pressure_load_count].n1=pointlist_str[i].f[0]
#                pressure_load[pressure_load_count].n2=pointlist_str[i].f[1]
#                pressure_load[pressure_load_count].n3=pointlist_str[i].f[2]
#                pressure_load[pressure_load_count].area = pointlist_str[i].area
#                pressure_load_count = pressure_load_count +1


        self.load_list = load_list
        self.no_of_grid_points_w_load = load_count





    def specify_loads(self,specified_loads):
        self.load_list = specified_loads
        self.no_of_grid_points_w_load = len(specified_loads)
    
    def scale_loads(self,scale):
        
        for i in range(0,len(self.pointlist)):
            self.pointlist[i].f[0]=scale*self.pointlist[i].f[0]
            self.pointlist[i].f[1]=scale*self.pointlist[i].f[1]
            self.pointlist[i].f[2]=scale*self.pointlist[i].f[2]
    
    
    def specify_constraint(self,coordinate,value):
        
        constrained_points = []
        
        for i in range(0,len(self.pointlist)):
            if((self.pointlist[i].x[coordinate] >= value - 0.000001) and (self.pointlist[i].x[coordinate] <= value + 0.000001)):
                constrained_points.append(self.pointlist[i].id)
        
        constrained_grid_point_list = [ SPC() for i in range(len(constrained_points))]
        
        for i in range(0,len(constrained_grid_point_list)):
            constrained_grid_point_list[i].type = 'SPC1'
            constrained_grid_point_list[i].sid = 1
            constrained_grid_point_list[i].g1 = constrained_points[i]
            constrained_grid_point_list[i].c1 = 123456
            constrained_grid_point_list[i].d1 = 0.0
        
        self.constrained_grid_point_list = constrained_grid_point_list
        self.no_of_constrained_grid_points = len(constrained_grid_point_list)
    
    


    def import_full_s200_bdf(self,filename):
        import_s200_bdf(filename,self)
    
    def read_tacs_results(self,filename,tecplot_file_orig):
        read_tacs_displacement_file(self.pointlist,filename)
        visualize_tacs_results(self.pointlist,self.elemlist,tecplot_file_orig)
    

    def initialize(self,output_filename):
        print "Initializing"
    


    def visualize_loading(self,tacs_load_tecplot):
        #-----writing the headers-----
        pointlist = self.pointlist
        elemlist = self.elemlist
        npoint = len(pointlist)
        nelem = len(elemlist)
        
        
        mesh_def2 = open(tacs_load_tecplot,"wb")
        
        mesh_def2.write("TITLE = \"Visualization of structural solution\"")
        mesh_def2.write("\n")
        mesh_def2.write("VARIABLES = \"x\", \"y\", \"z\", \"force x\",\"force y\",\"force z\",")
        mesh_def2.write("\n")
        mesh_def2.write("ZONE NODES=")
        mesh_def2.write(format(npoint))
        mesh_def2.write(", ELEMENTS=")
        mesh_def2.write(format(nelem))
        #    mesh_def.write("\n")
        mesh_def2.write(", DATAPACKING=POINT, ZONETYPE=FEQUADRILATERAL")
        mesh_def2.write("\n")
        
        
        #---------writing the points----------------------
        # Write x coordinates.
        
        
        
        for i in range(0,npoint):
            mesh_def2.write(format(pointlist[i].x[0]))
            mesh_def2.write("\t")
            mesh_def2.write(format(pointlist[i].x[1]))
            mesh_def2.write("\t")
            mesh_def2.write(format(pointlist[i].x[2]))
            mesh_def2.write("\t")
            mesh_def2.write(format(pointlist[i].f[0]))
            mesh_def2.write("\t")
            mesh_def2.write(format(pointlist[i].f[1]))
            mesh_def2.write("\t")
            mesh_def2.write(format(pointlist[i].f[2]))
            mesh_def2.write("\n")
        
        
        #----------writing the elements----------------------
        
        # Write the element connectivity (1-based).
        
        for i in range(0,nelem):
            mesh_def2.write(format(elemlist[i].g[0]))
            mesh_def2.write("  ")
            mesh_def2.write(format(elemlist[i].g[1]))
            mesh_def2.write("  ")
            mesh_def2.write(format(elemlist[i].g[2]))
            mesh_def2.write("  ")
            if(elemlist[i].type=='CTRIA3'):
                
                mesh_def2.write(format(elemlist[i].g[2]))
                mesh_def2.write("\n")
            
            if(elemlist[i].type=='CQUAD4'):
                
                mesh_def2.write(format(elemlist[i].g[3]))
                mesh_def2.write("\n")


        mesh_def2.close()
                
                


    def write_tacs_load_file(self,tacs_load_filename):
        write_tacs_load_file(self.pointlist,self.elemlist,tacs_load_filename,self.node_element_count)
    
    def write_sol_101_file(self,output_filename):
        #----------------writing the output to the file----------------------------------------------
        #------open the file-------
        fo = open(output_filename,"wb")
        
        
        
        #---------Executive_control_section----------------------------------------
        
        fo.write("SOL ")
        fo.write(format(101))
        fo.write("\n")
        
        fo.write("TIME ")
        fo.write(format(self.times))
        fo.write("\n")
        
        fo.write("CEND")
        fo.write("\n")
        
        
        #-----------Case_control_section------------------------------------------
        
        #--load case--
        
        
        if(self.case_control_def==1):
            fo.write("DISPLACEMENT = ALL")
            fo.write("\n")
            fo.write("ELFORCE = ALL")
            fo.write("\n")
            fo.write("ELSTRESS = ALL")
            
            fo.write("\n")
        
        fo.write("LOAD = ")
        fo.write(format(self.load_type))
        fo.write("\n")
        
        fo.write("SPC = ")
        fo.write(format(self.spc_type))
        fo.write("\n")
        
        
        #-------------------Bulk Data Section--------------------------------------
        
        fo.write("BEGIN BULK\n")
        
        #---------------writing grid data------
        fo.write("PARAM    POST    0\n")
        
        #-------loop over the points-----------
        fo.write("$write grid data\n")
        
        #--write to the grid points-
        
#        for i in range(0,self.no_of_points):
#            
#            fo.write(str_form(self.pointlist[i].type));
#            fo.write(int_form(self.pointlist[i].id));
#            fo.write(int_form(self.pointlist[i].cp));
#            fo.write(float_form(self.pointlist[i].x[0]));
#            fo.write(float_form(self.pointlist[i].x[1]));
#            fo.write(float_form(self.pointlist[i].x[2]));
#            fo.write(int_form(self.pointlist[i].cd));
#            
#            #    fo.write(int_form(self.pointlist[i].ps));
#            #    fo.write(int_form(self.pointlist[i].seid));
#            fo.write("\n");

        
        #------------16 point string----------------
        
        for i in range(0,self.no_of_points):
            
            fo.write(str_form('GRID*'));
            fo.write(int_forms(self.pointlist[i].id));
            fo.write(int_forms(self.pointlist[i].cp));
            fo.write(float_forms(self.pointlist[i].x[0]));
            fo.write(float_forms(self.pointlist[i].x[1]));
            fo.write(str_form('*G'+str(self.pointlist[i].id)))
            fo.write("\n");
            fo.write(str_form('*G'+str(self.pointlist[i].id)))
            fo.write(float_forms(self.pointlist[i].x[2]));
            fo.write(int_forms(self.pointlist[i].cd));
            
            #    fo.write(int_form(pointlist[i].ps));
            #    fo.write(int_form(pointlist[i].seid));
            fo.write("\n");
        
        
        
        #------------writing element data------
        fo.write("$write element data\n")
        
        #--write to the grid points-
        

        
        for i in range(0,self.no_of_elements):
            
            
            
            
            fo.write(str_form(self.elemlist[i].type));
            fo.write(int_form(self.elemlist[i].eid));
            fo.write(int_form(self.elemlist[i].pid));
            fo.write(int_form(self.elemlist[i].g[0]));
            fo.write(int_form(self.elemlist[i].g[1]));
            fo.write(int_form(self.elemlist[i].g[2]));
            
            if(self.elemlist[i].type=='CQUAD4'):
                fo.write(int_form(self.elemlist[i].g[3]));
            
            
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[0]]));
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[1]]));
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[2]]));
            
            #print elemlist[i].g[0],elemlist[i].g[1],elemlist[i].g[2]
            #print global_to_loc_points[elemlist[i].g[0]],elemlist[i].g[1],elemlist[i].g[2]
            
            
            fo.write("\n")
        
        
        
        
        
        
        
        
        
        #------------writing element property data------
        fo.write("$write element property\n")
        for i in range(0, self.no_of_shell_elements):
            
            fo.write(str_form(self.shell_element_list[i].type));
            fo.write(int_form(self.shell_element_list[i].pid));
            fo.write(int_form(self.shell_element_list[i].mid1));
            fo.write(float_form(self.shell_element_list[i].t));
            fo.write(int_form(self.shell_element_list[i].mid2));
            fo.write(str_form('        '));
            fo.write(int_form(self.shell_element_list[i].mid3));
            
            
            
            
            fo.write("\n");
        
        
        
        #------------writing material data------
        fo.write("$material property\n")
        
        for i in range(0, self.no_of_materials):
            fo.write(str_form(self.material_list[i].type));
            fo.write(int_form(self.material_list[i].mid));
            fo.write(float_form(self.material_list[i].e));
            fo.write("        ");
            fo.write(float_form(self.material_list[i].nu));
            fo.write(float_form(self.material_list[i].rho));
            
            fo.write("\n");
        
        #-----------------spc data------------
        fo.write("$spc data\n")
        for i in range(0,self.no_of_constrained_grid_points):
            #        fo.write(str_form(constrained_grid_point_list[i].type));
            #        fo.write(int_form(constrained_grid_point_list[i].sid));
            #        #fo.write(int_form(constrained_grid_point_list[i].g[0]));
            #
            #        fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
            #        fo.write(int_form(constrained_grid_point_list[i].c1));
            #        fo.write(float_form(constrained_grid_point_list[i].d1));
            
            fo.write(str_form(self.constrained_grid_point_list[i].type));
            fo.write(int_form(self.constrained_grid_point_list[i].sid));
            #fo.write(int_form(constrained_grid_point_list[i].g[0]));
            
            fo.write(int_form(self.constrained_grid_point_list[i].c1));
            #fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
            
            fo.write(int_form(self.constrained_grid_point_list[i].g1))
            
            #fo.write(float_form(constrained_grid_point_list[i].d1));
            
            
            fo.write("\n");
        
        
        #-----------------load data------------
        fo.write("$load data\n")
        
        #   if(load_type =='FORCE'):
        
        for i in range(0, self.no_of_grid_points_w_load):
            fo.write(str_form("FORCE*"));
            fo.write(int_forms(self.load_list[i].sid));
            #fo.write(int_form(load_list[i].g));
            #fo.write(int_form(global_to_loc_points[load_list[i].g]));
            fo.write(int_forms(self.load_list[i].g));
            
            
            fo.write(int_forms(self.load_list[i].cid));
            fo.write(float_forms(self.load_list[i].f));
            fo.write(str_form('*F'+str(self.load_list[i].sid)))
            fo.write("\n");
            
            fo.write(str_form('*F'+str(self.load_list[i].sid)))
            fo.write(float_forms(self.load_list[i].n1));
            fo.write(float_forms(self.load_list[i].n2));
            fo.write(float_forms(self.load_list[i].n3));
            fo.write("\n");
        
        
        ##short format
#        for i in range(0, self.no_of_grid_points_w_load):
#            fo.write(str_form(self.load_list[i].type));
#            fo.write(int_form(self.load_list[i].sid));
#            #fo.write(int_form(load_list[i].g));
#            #fo.write(int_form(global_to_loc_points[load_list[i].g]));
#            fo.write(int_form(self.load_list[i].g));
#            
#            
#            fo.write(int_form(self.load_list[i].cid));
#            fo.write(float_form(self.load_list[i].f));
#            
#            fo.write(float_form(self.load_list[i].n1));
#            fo.write(float_form(self.load_list[i].n2));
#            fo.write(float_form(self.load_list[i].n3));
#            fo.write("\n");

        
        #if(load_type =='PRESSURE'):
        
        #    for i in range(0, no_of_elements):
        #        fo.write(str_form(self.pressure_load[i].type));
        #        fo.write(int_form(self.pressure_load[i].sid));
        #
        #        fo.write(float_form(self.pressure_load[i].p));
        #       
        #       
        #        fo.write(int_form(self.pressure_load[i].g[0]));
        #        fo.write(int_form(self.pressure_load[i].g[1]));
        #        fo.write(int_form(self.pressure_load[i].g[2]));
        #
        #        fo.write("\n");
        
        
        #------------------
        fo.write("ENDDATA");
        
        #--------close the file----------------
        
        fo.close();
         


    def write_sol(self,output_filename):
        
        print "Writing bdf file"
        
        pointlist = self.pointlist
        pointlist_fl = self.pointlist_fl
        load_list = self.load_list
        elemlist = self.elemlist
        case_control_def = self.case_control_def
        DESOBJ = self.DESOBJ
        load_type = self.load_type
        material_list = self.material_list
        shell_element_list = self.shell_element_list
        beam_element_list = self.beam_element_list
        spc_type = self.spc_type
        constrained_grid_point_list = self.constrained_grid_point_list
        case_control_def = self.case_control_def
        case_control_analysis_type = self.case_control_analysis_type
        design_var_list = self.design_var_list
        dresp1_list = self.dresp1_list
        dresp2_list = self.dresp2_list
        equation_list  = self.equation_list
        constraint_list = self.constraint_list
        dconadd_list = self.dconadd_list
        opt_parameters  = self.opt_parameters
        design_ppties_list =  self.design_ppties_list
        
        no_of_points = self.no_of_points
        no_of_elements = self.no_of_elements
        no_of_beams = self.no_of_beams
        no_of_shell_elements = self.no_of_shell_elements
        no_of_beam_elements = self.no_of_beam_elements
        no_of_materials = self.no_of_materials
        no_of_constrained_grid_points = self.no_of_constrained_grid_points
        no_of_grid_points_w_load = self.no_of_grid_points_w_load
        no_of_design_variables = self.no_of_design_variables
        no_of_property_types = self.no_of_property_types
        no_of_dresp1 = self.no_of_dresp1
        no_of_dresp2 = self.no_of_dresp2
        no_of_equations = self.no_of_equations
        no_of_constraints = self.no_of_constraints
        no_of_dconadd = self.no_of_dconadd
        
        output_filename =  output_filename


        sol=  self.sol
        times= self.times
        
        
        fo = open(output_filename,"wb")
    
    
    
        #---------Executive_control_section----------------------------------------

        fo.write("SOL ")
        fo.write(format(sol))
        fo.write("\n")
    
        fo.write("TIME ")
        fo.write(format(times))
        fo.write("\n")
        
        fo.write("GEOMCHECK Q4_IAMAX=180.0,Q4_SKEW=0.0,Q4_TAPER=3.0\n")
        fo.write("GEOMCHECK Q4_IAMIN=0.5,Q4_WARP=0.3\n")
    
        fo.write("CEND")
        fo.write("\n")
    
    
    
        #-----------Case_control_section------------------------------------------
    
        #--load case--
    
    
        if(case_control_def==1):
            fo.write("DISPLACEMENT = ALL")
            fo.write("\n")
            fo.write("ELFORCE = ALL")
            fo.write("\n")
            fo.write("ELSTRESS = ALL")
            fo.write("\n")
    
        fo.write("LOAD = ")
        fo.write(format(load_type))
        fo.write("\n")
    
        fo.write("SPC = ")
        fo.write(format(spc_type))
        fo.write("\n")
    
    
        #--------Design optimization related variables---------
    
        fo.write("ANALYSIS = ")
        fo.write(format(case_control_analysis_type))
        fo.write("\n")
    
    
        fo.write("DESOBJ(MIN) = ")
        fo.write(format(DESOBJ))
        fo.write("\n")
    
    
        fo.write("DESSUB = ")
        fo.write(format(dconadd_list[0].dcid))
        fo.write("\n")
        #-------------------Bulk Data Section--------------------------------------
    
        fo.write("BEGIN BULK\n")
    
        #---------------writing grid data------
        fo.write("PARAM    POST    0\n")
        fo.write("PARAM, BAILOUT, -1\n")
    
        #-------loop over the points-----------
        fo.write("$write grid data\n")
    
        #--write to the grid points-
    
    #    for i in range(0,no_of_points):
    #        
    #        fo.write(str_form(pointlist[i].type));
    #        fo.write(int_form(pointlist[i].id));
    #        fo.write(int_form(pointlist[i].cp));
    #        fo.write(float_form(pointlist[i].x[0]));
    #        fo.write(float_form(pointlist[i].x[1]));
    #        fo.write(float_form(pointlist[i].x[2]));
    #        fo.write(int_form(pointlist[i].cd));
    #
    #    #    fo.write(int_form(pointlist[i].ps));
    #    #    fo.write(int_form(pointlist[i].seid));
    #        fo.write("\n");
    
    
    
        #------------16 point string----------------
    
        for i in range(0,no_of_points):
            
            fo.write(str_form('GRID*'));
            fo.write(int_forms(pointlist[i].id));
            fo.write(int_forms(pointlist[i].cp));
            fo.write(float_forms(pointlist[i].x[0]));
            fo.write(float_forms(pointlist[i].x[1]));
            fo.write(str_form('*G'+str(pointlist[i].id)))
            fo.write("\n");
            fo.write(str_form('*G'+str(pointlist[i].id)))
            fo.write(float_forms(pointlist[i].x[2]));
            fo.write(int_forms(pointlist[i].cd));
    
            #    fo.write(int_form(pointlist[i].ps));
            #    fo.write(int_form(pointlist[i].seid));
            fo.write("\n");
    
    
    
        #------------writing element data------
        fo.write("$write element data\n")
        print 'no of  elem',no_of_elements
        #--write to the grid points-
    
        for i in range(0,no_of_elements):
            
            fo.write(str_form(elemlist[i].type));
            fo.write(int_form(elemlist[i].eid));
            fo.write(int_form(elemlist[i].pid));
            fo.write(int_form(elemlist[i].g[0]));
            fo.write(int_form(elemlist[i].g[1]));
            fo.write(int_form(elemlist[i].g[2]));
            
            if(self.elemlist[i].type=='CQUAD4'):
                fo.write(int_form(self.elemlist[i].g[3]));
    
    #        fo.write(int_form(global_to_loc_points[elemlist[i].g[0]]));
    #        fo.write(int_form(global_to_loc_points[elemlist[i].g[1]]));
    #        fo.write(int_form(global_to_loc_points[elemlist[i].g[2]]));
    
            #print elemlist[i].g[0],elemlist[i].g[1],elemlist[i].g[2]
            #print global_to_loc_points[elemlist[i].g[0]],elemlist[i].g[1],elemlist[i].g[2]
            
    
            fo.write("\n");
    
    
    #----------beam elements-----------
        for i in range(0,no_of_beams):
        
            fo.write(str_form(beamlist[i].type));
            fo.write(int_form(beamlist[i].eid));
            fo.write(int_form(beamlist[i].pid));
            fo.write(int_form(beamlist[i].ga));
            fo.write(int_form(beamlist[i].gb));
            fo.write(int_form(beamlist[i].x[0]));
            fo.write(int_form(beamlist[i].x[1]));
            fo.write(int_form(beamlist[i].x[2]));
            
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[0]]));
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[1]]));
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[2]]));
            
            #print elemlist[i].g[0],elemlist[i].g[1],elemlist[i].g[2]
            #print global_to_loc_points[elemlist[i].g[0]],elemlist[i].g[1],elemlist[i].g[2]
            
            
            fo.write("\n");
    
    
    
    
    
    
        #------------writing element property data------
        fo.write("$write element property\n")
        for i in range(0, no_of_shell_elements):
            
            fo.write(str_form(shell_element_list[i].type));
            fo.write(int_form(shell_element_list[i].pid));
            fo.write(int_form(shell_element_list[i].mid1));
            fo.write(float_form(shell_element_list[i].t));
            fo.write(int_form(shell_element_list[i].mid2));
            fo.write(str_form('        '));
            #fo.write(int_form(shell_element_list[i].mid3));
    
    
            
            
            fo.write("\n");
    
    
        fo.write("$write beam element property\n")
        for i in range(0, no_of_beam_elements):
            
            fo.write(str_form(beam_element_list[i].type));
            fo.write(int_form(beam_element_list[i].pid));
            fo.write(int_form(beam_element_list[i].mid));
            fo.write(str_form('        '));
            
            fo.write(str_form(beam_element_list[i].type2));
            fo.write("\n");
            fo.write(str_form('        '));
            fo.write(float_form(beam_element_list[i].dim1));
            fo.write(float_form(beam_element_list[i].dim2));
            
            
            
            
            
            
            fo.write("\n");
    
    
        #------------writing material data------
        fo.write("$material property\n")
    
        for i in range(0, no_of_materials):
            fo.write(str_form(material_list[i].type));
            fo.write(int_form(material_list[i].mid));
            fo.write(float_form(material_list[i].e));
            fo.write("        ");
            fo.write(float_form(material_list[i].nu));
            fo.write(float_form(material_list[i].rho));
    
            fo.write("\n");
    
        #-----------------spc data------------
        fo.write("$spc data\n")
        for i in range(0,no_of_constrained_grid_points):
    #        fo.write(str_form(constrained_grid_point_list[i].type));
    #        fo.write(int_form(constrained_grid_point_list[i].sid));
    #        #fo.write(int_form(constrained_grid_point_list[i].g[0]));
    #        
    #        fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
    #        fo.write(int_form(constrained_grid_point_list[i].c1));
    #        fo.write(float_form(constrained_grid_point_list[i].d1));
    
            fo.write(str_form(constrained_grid_point_list[i].type));
            fo.write(int_form(constrained_grid_point_list[i].sid));
            #fo.write(int_form(constrained_grid_point_list[i].g[0]));
            
            fo.write(int_form(constrained_grid_point_list[i].c1));
            #fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
            
            fo.write(int_form(constrained_grid_point_list[i].g1))
    
            #fo.write(float_form(constrained_grid_point_list[i].d1));
            
    
            
    
            fo.write("\n");
    
    
        #-----------------load data------------
        fo.write("$load data\n")
    
    #   if(load_type =='FORCE'):
    
        for i in range(0, no_of_grid_points_w_load):
            fo.write(str_form(load_list[i].type));
            fo.write(int_form(load_list[i].sid));
            #fo.write(int_form(load_list[i].g));
            #fo.write(int_form(global_to_loc_points[load_list[i].g]));
            fo.write(int_form(load_list[i].g));
    
            
            fo.write(int_form(load_list[i].cid));
            fo.write(float_form(load_list[i].f));
    
            fo.write(float_form(load_list[i].n1));
            fo.write(float_form(load_list[i].n2));
            fo.write(float_form(load_list[i].n3));
            fo.write("\n");
        
    
           
    #if(load_type =='PRESSURE'):
           
    #    for i in range(0, no_of_elements):
    #        fo.write(str_form(pressure_load[i].type));
    #        fo.write(int_form(pressure_load[i].sid));
    #
    #        fo.write(float_form(pressure_load[i].p));
    #       
    #       
    #        fo.write(int_form(pressure_load[i].g[0]));
    #        fo.write(int_form(pressure_load[i].g[1]));
    #        fo.write(int_form(pressure_load[i].g[2]));
    #
    #        fo.write("\n");
    
    
        #--------------Design optimization data-----------------------------------------
    
        #-----------------design variables------------
        fo.write("$ldesign variables\n")
    
        for i in range(0, no_of_design_variables):
            fo.write(str_form(design_var_list[i].type));
            fo.write(int_form(design_var_list[i].id));
            
            fo.write(str_form(design_var_list[i].label));
            fo.write(float_form(design_var_list[i].xinit));
            fo.write(float_form(design_var_list[i].xlb));
            fo.write(float_form(design_var_list[i].xub));
            fo.write(float_form(design_var_list[i].delxv));
            
            fo.write("\n");
    
    
        #-----------------design properties------------
        fo.write("$ldesign properties\n")
    
        for i in range(0, no_of_property_types):
            fo.write(str_form(design_ppties_list[i].type));
            fo.write(int_form(design_ppties_list[i].id));
            
            fo.write(str_form(design_ppties_list[i].type2));
            fo.write(int_form(design_ppties_list[i].pid));
            
            if (design_ppties_list[i].fid=='0'):
                fo.write(str_form('        '));
            else:
                fo.write(str_form(design_ppties_list[i].fid));
            
            
            
            fo.write(float_form(design_ppties_list[i].pmin));
            fo.write(float_form(design_ppties_list[i].pmax));
            fo.write(float_form(design_ppties_list[i].c0));
            fo.write("\n");
            fo.write(str_form('        '));
            fo.write(int_form(design_ppties_list[i].dvid1));
            fo.write(float_form(design_ppties_list[i].coef1));
            #---dvidi and coefi should be user defined lists
            
            fo.write("\n");
    
    
    
    
        #-----------------DRESP1 properties------------
        fo.write("$DRESP1\n")
    
        for i in range(0, no_of_dresp1):
            fo.write(str_form(dresp1_list[i].type));
            fo.write(int_form(dresp1_list[i].id));
            
            fo.write(str_form(dresp1_list[i].label));
            
            fo.write(str_form(dresp1_list[i].rtype));
            
            if (dresp1_list[i].ptype=='0'):
                fo.write(str_form('        '));
            else:
                fo.write(str_form(dresp1_list[i].ptype));
            
            
            if (dresp1_list[i].region==0):
                fo.write(int_form('        '));
            else:
                fo.write(int_form(dresp1_list[i].region));
            
            if (dresp1_list[i].atta==0):
                fo.write(int_form('        '));
            else:
                fo.write(int_form(dresp1_list[i].atta));
            
            
            if (dresp1_list[i].attb==0):
                fo.write(int_form('        '));
            else:
                fo.write(int_form(dresp1_list[i].attb));
            
            
            if (dresp1_list[i].no_of_points ==1):
    
                if (dresp1_list[i].att1==0):
                    fo.write(int_form('        '));
                else:
                    fo.write(int_form(dresp1_list[i].att1));
                
                fo.write("\n");

    
            else:
    
                if (dresp1_list[i].att1==0):
                    fo.write(int_form('        '));
                else:
                    fo.write(int_form(dresp1_list[i].att1[0]));
                
                
                fo.write("\n");
    
    
                loc_row_count = (dresp1_list[i].no_of_points-1)/8
                rem_elem = dresp1_list[i].no_of_points - 8*loc_row_count -1
    
                curr_pos=0
                for nrow in range(0,loc_row_count):
                    
                    fo.write(int_form('        '));
                    
                    for ncol in range(0,8):
                        fo.write(int_form(dresp1_list[i].att1[8*nrow +ncol +1]));
                        curr_pos =8*nrow +ncol + 1
    
                    fo.write("\n");
                
                if (curr_pos!=0):
                    fo.write(int_form('        '));
                    for ncol in range(0,rem_elem):
                        fo.write(int_form(dresp1_list[i].att1[curr_pos+ncol]));
                    fo.write("\n");
                        
                    
                    
                    
                    
        
    
            
            
            #att1 should be a user defined list
            #        fo.write("\n");
            #        fo.write(int_form(dresp1_list[i].att1));
            
            
            #fo.write("\n");
    
    
        #-----------------DRESP2 properties------------
        fo.write("$DRESP2\n")
    
        for i in range(0, no_of_dresp2):
            fo.write(str_form(dresp2_list[i].type));
            fo.write(int_form(dresp2_list[i].id));
            
            fo.write(str_form(dresp2_list[i].label));
            
            if (dresp2_list[i].eqid==0):
                #fo.write(str_form('        '));
                fo.write(str_form(dresp2_list[i].method));
            else:
                fo.write(int_form(dresp2_list[i].eqid));

            
            
            
            if (dresp2_list[i].region==0):
                fo.write(str_form('        '));
            else:
                fo.write(int_form(dresp2_list[i].region));
            
            
            if (dresp2_list[i].method=='0'):
                fo.write(str_form('        '));
            else:
                fo.write(str_form('        '));
                #fo.write(str_form(dresp2_list[i].method));
            
            if (dresp2_list[i].c1==0):
                fo.write(str_form('        '));
            else:
                fo.write(float_form(dresp2_list[i].c1));
            
            
            if (dresp2_list[i].c2==0):
                fo.write(str_form('        '));
            else:
                fo.write(float_form(dresp2_list[i].c2));
            
            
            if (dresp2_list[i].c3==0):
                fo.write(str_form('        '));
            else:
                fo.write(float_form(dresp2_list[i].c3));
            
            fo.write("\n");
            fo.write(str_form('        '));
            fo.write(str_form(dresp2_list[i].associated));
            
            #writing a list of dresps
            if(dresp2_list[i].nr1==0):


                loc_row_count = (dresp2_list[i].no_of_resp)/7
                rem_elem = dresp2_list[i].no_of_resp - 7*loc_row_count
                
                curr_pos=0
                for nrow in range(0,loc_row_count):
                    
                    if(nrow!=0):
                        fo.write(str_form('        '));
                        fo.write(str_form('        '));
                    
                    for ncol in range(0,7):
                        fo.write(int_form(dresp2_list[i].nr[7*nrow +ncol]));
                        curr_pos =7*nrow +ncol
                    
                    fo.write("\n");
                
                
                if (curr_pos!=0):
                    fo.write(str_form('        '));
                    fo.write(str_form('        '));
                    for ncol in range(0,rem_elem+1):
                        fo.write(int_form(dresp2_list[i].nr[curr_pos+ncol]));
                    fo.write("\n");
                        
                        
            else:
                fo.write(int_form(dresp2_list[i].nr1));
            
            
            
            if (dresp2_list[i].nr2==0):
                fo.write(str_form('        '));
            else:
                fo.write(int_form(dresp2_list[i].nr2));
            
            if (dresp2_list[i].nr3==0):
                fo.write(str_form('        '));
            else:
                fo.write(int_form(dresp2_list[i].nr3));
            
    
        #att1 should be a user defined list
        #        fo.write("\n");
        #        fo.write(int_form(dresp1_list[i].att1));
    
    
            fo.write("\n");
    
    
        ##-----------------DRESP2 properties------------
        #    fo.write("$DRESP2\n")
        #
        #    for i in range(0, no_of_dresp2):
        #        fo.write(str_form(dresp2_list[i].type));
        #        fo.write(int_form(dresp2_list[i].id));
        #
        #        fo.write(str_form(dresp2_list[i].label));
        #        fo.write(int_form(dresp2_list[i].eqid));
        #        fo.write(int_form(dresp2_list[i].region));
        #        fo.write(str_form(dresp2_list[i].method));
        #        fo.write(float_form(dresp2_list[i].c1));
        #        fo.write(float_form(dresp2_list[i].c2));
        #        fo.write(float_form(dresp2_list[i].c3));
        #
        #        fo.write("\n");
        #        fo.write(str_form('        '));
        #        fo.write(str_form(dresp2_list[i].associated));
        #
        #        fo.write(int_form(dresp2_list[i].nr1));
        #        fo.write(int_form(dresp2_list[i].nr2));
        #        fo.write(int_form(dresp2_list[i].nr3));
        #
        #    #att1 should be a user defined list
        #    #        fo.write("\n");
        #    #        fo.write(int_form(dresp1_list[i].att1));
        #
        #
        #    fo.write("\n");
    
        #-----------------equations properties------------
        fo.write("$DEQUATN\n")
    
        for i in range(0, no_of_equations):
            
            print_equation(equation_list[i],fo)
    
    
    
        #        fo.write(str_form(equation_list[i].type));
        #        fo.write(int_form(equation_list[i].id));
        #        fo.write(str_form(equation_list[i].equation));
        #        fo.write("\n")
        #        fo.write(str_form('        '))
    
    
    
        #-----------------constraint properties------------
        fo.write("$DCONSTR\n")
    
        for i in range(0, no_of_constraints):
            fo.write(str_form(constraint_list[i].type));
            fo.write(int_form(constraint_list[i].dcid));
            
            fo.write(int_form(constraint_list[i].rid));
            fo.write(float_form(constraint_list[i].lallow));
            
            fo.write(float_form(constraint_list[i].uallow));
    
    
            fo.write("\n");
    
    
        #-----------------constraint set properties------------
        fo.write("$DCONADD\n")
    
        for i in range(0, no_of_dconadd):
            fo.write(str_form(dconadd_list[i].type));
            fo.write(int_form(dconadd_list[i].dcid));
            
            
            
            fo.write(int_form(dconadd_list[i].dc1));
            
            if(dconadd_list[i].dc2!=0):
            
                fo.write(int_form(dconadd_list[i].dc2))
    
            fo.write("\n");
    
    
        #-----------------parameters properties------------
        fo.write("$Optimization params set\n")
    
    
        fo.write(str_form(opt_parameters.type));
        fo.write(str_form(opt_parameters.param1));
    
        fo.write(int_form(opt_parameters.val1));
#        fo.write(str_form(opt_parameters.param2));
#
#        fo.write(int_form(opt_parameters.val2));

        fo.write("\n");
    
    
    
        #------------------
        fo.write("ENDDATA");
    
        #--------close the file----------------
    
        fo.close();
            
            
        
        #def read_pyopt_results(design_variables_value,design_variables_name):
    def read_pyopt_results(aircraft_dv_filename):
#        file = open(pyopt_filename,"r")
#        
#        for line in file:
#            broken_line = line.split()
#            print broken_line

        no_of_dvs = self.no_of_shell_elements
        design_variables_value = np.zeros(no_of_dvs)

        file = open(aircraft_dv_filename,"r")
        for line in file:
            objective_line = line.split()
            objective = float(objective_line[1])
            break
        count = 0
        for line in file:
            variable = float(line)
            design_variables_value[count] = variable
            count = count + 1


        file.close()

        self.pyopt_dv_values = design_variables_value
        #self.pyopt_dv_name = design_variables_name
        pointlist = self.pointlist
        elemlist = self.elemlist
    
        #visualize the results
        mesh_def = open("visualize_dvs.plt","wb")
        #-----writing the headers-----
        
        
        mesh_def.write("TITLE = \"Visualization of CSM design variables\"")
        mesh_def.write("\n")
        mesh_def.write("VARIABLES = \"x\", \"y\", \"z\", \"thickness\",")
        mesh_def.write("\n")
        mesh_def.write("ZONE NODES=")
        mesh_def.write(format(npoint))
        mesh_def.write(", ELEMENTS=")
        mesh_def.write(format(nelem))
        #    mesh_def.write("\n")
        #mesh_def.write(", DATAPACKING=POINT, ZONETYPE=FEQUADRILATERAL")
        mesh_def.write(", DATAPACKING=BLOCK, ZONETYPE=FEQUADRILATERAL")
        mesh_def.write("\n")
        mesh_def.write(", VarLocation=([4-4]=CellCentered)")
        mesh_def.write("\n")
        
        
        #---------writing the points----------------------
        # Write x coordinates.
        
        
        
#        for i in range(0,npoint):
#            mesh_def.write(format(pointlist[i].x[0]))
#            mesh_def.write("\t")
#            mesh_def.write(format(pointlist[i].x[1]))
#            mesh_def.write("\t")
#            mesh_def.write(format(pointlist[i].x[2]))
#            mesh_def.write("\t")
#            mesh_def.write(format(pointlist[i].thickness))
#            mesh_def.write("\t")

        
        for i in range(0,npoint):
            mesh_def.write(format(pointlist[i].x[0]))
            mesh_def.write("\t")
        mesh_def.write("\n")
        
        for i in range(0,npoint):
            mesh_def.write(format(pointlist[i].x[1]))
            mesh_def.write("\t")
        mesh_def.write("\n")
            
        for i in range(0,npoint):
            mesh_def.write(format(pointlist[i].x[2]))
            mesh_def.write("\t")
        mesh_def.write("\n")
            
        for i in range(0,nelem):
            mesh_def.write(format(design_variables_value[elemlist[i].pid-1]))
            mesh_def.write("\t")
        mesh_def.write("\n")



        #----------writing the elements----------------------

        # Write the element connectivity (1-based).

        for i in range(0,nelem):
            mesh_def.write(format(elemlist[i].g[0]))
            mesh_def.write("  ")
            mesh_def.write(format(elemlist[i].g[1]))
            mesh_def.write("  ")
            mesh_def.write(format(elemlist[i].g[2]))
            mesh_def.write("  ")
            if(elemlist[i].type=='CTRIA3'):
                
                mesh_def.write(format(elemlist[i].g[2]))
                mesh_def.write("\n")
            
            if(elemlist[i].type=='CQUAD4'):
                
                mesh_def.write(format(elemlist[i].g[3]))
                mesh_def.write("\n")



    
    

#    def write_sol_100(self,output_filename):
#        def write_sol(self,output_filename):
#        print "ha"
#        
#        #----------------writing the output to the file----------------------------------------------
#        #------open the file-------
#        fo = open(output_filename,"wb")
#        
#        
#        
#        #---------Executive_control_section----------------------------------------
#        
#        fo.write("SOL ")
#        fo.write(format(self.sol))
#        fo.write("\n")
#        
#        fo.write("TIME ")
#        fo.write(format(self.times))
#        fo.write("\n")
#        
#        fo.write("CEND")
#        fo.write("\n")
#        
#        
#        
#        #-----------Case_control_section------------------------------------------
#        
#        #--load case--
#        
#        
#        if(self.case_control_def==1):
#            fo.write("DISPLACEMENT = ALL")
#            fo.write("\n")
#            fo.write("ELFORCE = ALL")
#            fo.write("\n")
#            fo.write("ELSTRESS = ALL")
#            
#            fo.write("\n")
#        
#        fo.write("LOAD = ")
#        fo.write(format(self.load_type))
#        fo.write("\n")
#        
#        fo.write("SPC = ")
#        fo.write(format(self.spc_type))
#        fo.write("\n")
#        
#        
#        #-------------------Bulk Data Section--------------------------------------
#        
#        fo.write("BEGIN BULK\n")
#        
#        #---------------writing grid data------
#        fo.write("PARAM    POST    0\n")
#        
#        #-------loop over the points-----------
#        fo.write("$write grid data\n")
#        
#        #--write to the grid points-
#        
#        #        for i in range(0,self.no_of_points):
#        #
#        #            fo.write(str_form(self.pointlist[i].type));
#        #            fo.write(int_form(self.pointlist[i].id));
#        #            fo.write(int_form(self.pointlist[i].cp));
#        #            fo.write(float_form(self.pointlist[i].x[0]));
#        #            fo.write(float_form(self.pointlist[i].x[1]));
#        #            fo.write(float_form(self.pointlist[i].x[2]));
#        #            fo.write(int_form(self.pointlist[i].cd));
#        #
#        #            #    fo.write(int_form(self.pointlist[i].ps));
#        #            #    fo.write(int_form(self.pointlist[i].seid));
#        #            fo.write("\n");
#        
#        
#        #------------16 point string----------------
#        
#        for i in range(0,self.no_of_points):
#            
#            fo.write(str_form('GRID*'));
#            fo.write(int_forms(self.pointlist[i].id));
#            fo.write(int_forms(self.pointlist[i].cp));
#            fo.write(float_forms(self.pointlist[i].x[0]));
#            fo.write(float_forms(self.pointlist[i].x[1]));
#            fo.write(str_form('*G'+str(self.pointlist[i].id)))
#            fo.write("\n");
#            fo.write(str_form('*G'+str(self.pointlist[i].id)))
#            fo.write(float_forms(self.pointlist[i].x[2]));
#            fo.write(int_forms(self.pointlist[i].cd));
#            
#            #    fo.write(int_form(pointlist[i].ps));
#            #    fo.write(int_form(pointlist[i].seid));
#            fo.write("\n");
#
#    #------------writing element data------
#    fo.write("$write element data\n")
#        
#        #--write to the grid points-
#        
#        
#        
#        for i in range(0,self.no_of_elements):
#            
#            fo.write(str_form(self.elemlist[i].type));
#            fo.write(int_form(self.elemlist[i].eid));
#            fo.write(int_form(self.elemlist[i].pid));
#            fo.write(int_form(self.elemlist[i].g[0]));
#            fo.write(int_form(self.elemlist[i].g[1]));
#            fo.write(int_form(self.elemlist[i].g[2]));
#            
#            if(self.elemlist[i].type=='CQUAD4'):
#                fo.write(int_form(self.elemlist[i].g[3]));
#            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[0]]));
#            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[1]]));
#            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[2]]));
#            
#            #print elemlist[i].g[0],elemlist[i].g[1],elemlist[i].g[2]
#            #print global_to_loc_points[elemlist[i].g[0]],elemlist[i].g[1],elemlist[i].g[2]
#            
#            
#            fo.write("\n")
#        
#        
#        
#        
#        
#        
#        
#        
#        
#        #------------writing element property data------
#        fo.write("$write element property\n")
#        for i in range(0, self.no_of_shell_elements):
#            
#            fo.write(str_form(self.shell_element_list[i].type));
#            fo.write(int_form(self.shell_element_list[i].pid));
#            fo.write(int_form(self.shell_element_list[i].mid1));
#            fo.write(float_form(self.shell_element_list[i].t));
#            fo.write(int_form(self.shell_element_list[i].mid2));
#            fo.write(str_form('        '));
#            fo.write(int_form(self.shell_element_list[i].mid3));
#            
#            
#            
#            
#            fo.write("\n");
#        
#        
#        
#        #------------writing material data------
#        fo.write("$material property\n")
#        
#        for i in range(0, self.no_of_materials):
#            fo.write(str_form(self.material_list[i].type));
#            fo.write(int_form(self.material_list[i].mid));
#            fo.write(float_form(self.material_list[i].e));
#            fo.write("        ");
#            fo.write(float_form(self.material_list[i].nu));
#            fo.write(float_form(self.material_list[i].rho));
#            
#            fo.write("\n");
#
##-----------------spc data------------
#fo.write("$spc data\n")
#    for i in range(0,self.no_of_constrained_grid_points):
#        #        fo.write(str_form(constrained_grid_point_list[i].type));
#        #        fo.write(int_form(constrained_grid_point_list[i].sid));
#        #        #fo.write(int_form(constrained_grid_point_list[i].g[0]));
#        #
#        #        fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
#        #        fo.write(int_form(constrained_grid_point_list[i].c1));
#        #        fo.write(float_form(constrained_grid_point_list[i].d1));
#        
#        fo.write(str_form(self.constrained_grid_point_list[i].type));
#            fo.write(int_form(self.constrained_grid_point_list[i].sid));
#            #fo.write(int_form(constrained_grid_point_list[i].g[0]));
#            
#            fo.write(int_form(self.constrained_grid_point_list[i].c1));
#            #fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
#            
#            fo.write(int_form(self.constrained_grid_point_list[i].g1))
#            
#            #fo.write(float_form(constrained_grid_point_list[i].d1));
#            
#            
#            fo.write("\n");
#        
#        
#        #-----------------load data------------
#        fo.write("$load data\n")
#        
#        #   if(load_type =='FORCE'):
#        
#        for i in range(0, self.no_of_grid_points_w_load):
#            fo.write(str_form(self.load_list[i].type));
#            fo.write(int_form(self.load_list[i].sid));
#            #fo.write(int_form(load_list[i].g));
#            #fo.write(int_form(global_to_loc_points[load_list[i].g]));
#            fo.write(int_form(self.load_list[i].g));
#            
#            
#            fo.write(int_form(self.load_list[i].cid));
#            fo.write(float_form(self.load_list[i].f));
#            print self.load_list[i].f
#            print float_form(self.load_list[i].f)
#            fo.write(float_form(self.load_list[i].n1));
#            fo.write(float_form(self.load_list[i].n2));
#            fo.write(float_form(self.load_list[i].n3));
#            fo.write("\n");
#
#
#    #if(load_type =='PRESSURE'):
#
#    #    for i in range(0, no_of_elements):
#    #        fo.write(str_form(self.pressure_load[i].type));
#    #        fo.write(int_form(self.pressure_load[i].sid));
#    #
#    #        fo.write(float_form(self.pressure_load[i].p));
#    #
#    #
#    #        fo.write(int_form(self.pressure_load[i].g[0]));
#    #        fo.write(int_form(self.pressure_load[i].g[1]));
#    #        fo.write(int_form(self.pressure_load[i].g[2]));
#    #
#    #        fo.write("\n");
#
#
#    #------------------
#    fo.write("ENDDATA");
#        
#        #--------close the file----------------
#        
#        fo.close();







    def read_sol(self,opt_filename,tecplot_file_orig):
        
        print "read_solution"
        

        
        #objective_list,no_of_design_runs,design_var_value,constraint_list = read_opt_f06_file(opt_filename,self.no_of_design_variables,self.elemlist,self.no_of_elements+self.no_of_beams)
        
        objective_list,no_of_design_runs,design_var_value,constraint_list = read_opt_f06_file(opt_filename,self.no_of_design_variables,self.elemlist,self.no_of_elements+self.no_of_beams)
        
        self.objective_list = objective_list

#        self.no_of_design_runs = no_of_design_runs
#        self.design_var_value = design_var_value
#        self.constraint_list = constraint_list
#        
#        for i in range(0,self.no_of_design_runs):
#            self.shell_element_list[i].t = self.design_var_value[i]
#        
#        
#        read_opt_f06_file_stress(opt_filename,self.no_of_design_variables,self.elemlist,self.no_of_elements,self.no_of_points,self.pointlist,self.no_of_beams,self.no_of_design_runs)
#    
#    
#        for i in range(0,self.no_of_elements):
#            self.pointlist[self.elemlist[i].g[0]-1].thickness = max(self.elemlist[i].thickness,self.pointlist[self.elemlist[i].g[0]-1].thickness)
#            self.pointlist[self.elemlist[i].g[1]-1].thickness = max(self.elemlist[i].thickness,self.pointlist[self.elemlist[i].g[1]-1].thickness)
#            self.pointlist[self.elemlist[i].g[2]-1].thickness = max(self.elemlist[i].thickness,self.pointlist[self.elemlist[i].g[2]-1].thickness)
#        
#        pointlist =  self.pointlist
#        elemlist = self.elemlist
#        
#        
#        write_tecplot_file(pointlist,elemlist,tecplot_file_orig,self.no_of_points,self.no_of_elements)
#    
#    
#    
#    
#        design_vars =[ int() for i in range(self.no_of_design_variables)]
#        design_runs =[ int() for i in range(self.no_of_design_runs+1)]
#    
#    
#        for i in range(0,self.no_of_design_variables):
#            design_vars[i]=i+1
#    
#        for i in range(0,self.no_of_design_runs):
#            design_runs[i]=i+1
#    
#        plt.figure(1)
#        axes = plt.gca()
#        axes.plot(design_runs,self.objective_list,'bo-')
#    #plt.plot(design_runs,objective_list,'-*')
#        plt.xlabel('no. of design runs')
#        plt.ylabel('Objective function (Aircraft structural weight in kg)')
#        plt.savefig('objective_strut_braced.png')
#        axes.grid(True)
#    
#        plt.figure(2)
#        for i in range(0,self.no_of_design_variables):
#            plt.plot(design_runs,self.design_var_value[i],'-*')
#    
#        plt.xlabel('no. of design runs')
#        plt.ylabel('Design variables (element thickness in m)')
#    #plt.legend( loc='upper left' )
#    
#        plt.savefig('design_variables_strut_braced.png')
#    
#    
#    
#        plt.figure(4)
#        plt.plot(design_runs,self.constraint_list,'-*')
#        plt.xlabel('no. of design runs')
#        plt.ylabel('Maximum constraint violation (stress)')
#        plt.savefig('constraint_strut_braced.png')
#        
#        plt.figure(5)
#        plt.plot(design_runs,np.log10(self.constraint_list),'-*')
#        plt.xlabel('no. of design runs')
#        plt.ylabel('log Maximum constraint violation (stress)')
#        plt.savefig('constraint_strut_braced_log.png')
#    
#    
#        fig = plt.figure(3)
#        
#        ax = Axes3D(fig)
#        
#        
#        for i in range (0,self.no_of_points):
#            
#            
#            ax.scatter(self.pointlist[i].x[0], self.pointlist[i].x[1], self.pointlist[i].x[2],c="red")
#            
#    
#            
#    # ax.scatter(pointlist[i].x[0], pointlist[i].x[1], pointlist[i].x[2],c="blue")
#    
#        #plt.axis('equal')
#    
#        plt.savefig('struct_braced.png',format='png')
#    
#    #plt.show()
#        plt.clf()



    


