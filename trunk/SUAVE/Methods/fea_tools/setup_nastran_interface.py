# setup_nastran_interface.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

import numpy as np



#--imports---
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy


from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
from SUAVE.Methods.fea_tools.pyFSI.class_str.elements.class_structure import CTRIA3
from SUAVE.Methods.fea_tools.pyFSI.class_str.material.class_structure import PSHELL
from SUAVE.Methods.fea_tools.pyFSI.class_str.material.class_structure import PBARL
from SUAVE.Methods.fea_tools.pyFSI.class_str.material.class_structure import MAT1
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import FORCE
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import PLOAD
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import SPC
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.class_structure import SU2_import

from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import str_form

from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_forms
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_forms
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.pressure_interpolation import pressure_interpolation


from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DCONSTR
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DCONADD
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DRESP
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DRESP1
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DRESP2
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DDVAL
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DEQUATN
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DESVAR
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DVPREL1
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DVCREL1
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DVGRID
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DLINK
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DOPTPRM

from SUAVE.Methods.fea_tools.pyFSI.utility_functions.print_equation import print_equation


from SUAVE.Methods.fea_tools.pyFSI.input.read_nas_file import read_nas_file
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.interpolate_grid import interpolate_grid
from SUAVE.Methods.fea_tools.pyFSI.output.write_tecplot_file import write_tecplot_file
from SUAVE.Methods.fea_tools.pyFSI.output.write_tecplot_file_str import write_tecplot_file_str
from SUAVE.Methods.fea_tools.pyFSI.input.read_beam_numbers import read_beam_numbers
from SUAVE.Methods.fea_tools.pyFSI.input.read_constraints import read_constraints
from SUAVE.Methods.fea_tools.pyFSI.input.read_su2_surface_file import read_su2_surface_file

from SUAVE.Methods.fea_tools.pyFSI.input.read_beam import read_beam
from SUAVE.Methods.fea_tools.pyFSI.input.read_beam_numbers import read_beam_numbers
from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file import read_opt_f06_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file_stress import read_opt_f06_file_stress
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.interpolate_grid_brown import interpolate_grid_brown

from SUAVE.Methods.fea_tools.pyFSI.input.read_geomach_structural_file import read_geomach_structural_file

from SUAVE.Methods.fea_tools.pyFSI.class_str.solution_classes.sol200 import sol200
#from python_nastran_io.class_str.solution_classes.sol101 import sol101
#-----------
#---function to convert integers to required nastran format
from SUAVE.Methods.fea_tools.pyFSI.output.write_tacs_load_file import write_tacs_load_file
from SUAVE.Methods.fea_tools.mark_loading_points import mark_loading_points
#from SUAVE.Methods.fea_tools.setup_aero_pointwise import setup_aero_pointwise


#from SUAVE.Methods.fea_tools.pyFSI.functions.generate_panel_mesh import generate_panel_mesh

def setup_nastran_interface(s200,geomach_structural_mesh,load_mesh_type,load_filename,output_filename,aircraft,loads_scale_factor):


#Write a nastran file





    read_write_option =0 #if 0 then write if 1 then read
    write_su2_def_file=0  #if 1 then write su2 def file if 0 dont write

    use_option=2

    dynamic_pressure = 20716.20

    mesh_import = 1

    load_type ='PRESSURE'


    mesh_filename = geomach_structural_mesh #'conventional_str4.bdf'
    #load_filename = 'surface_flow_geomach_ncrm2.csv'

    opt_filename = 'nasa_crm_wing_str_bounds_001_2_5_29_4.f06'

    su2_def_file = 'plate_bwb_mesh_motion.dat'

    conn_filename = 'nasa_crm_coarse_constrained_gp.dat'

    tecplot_file_orig = 'conventional_str4.plt'

    beam_file =  'ncrm_beam.dat' #'beam_constraint.dat' #

    tecplot_file_deformed ='nasa_crm_wing_str_bounds_001_2_5_29_4.plt'

    scaling_factor = 1.0

    no_of_dvs_scale = 10

    #output_filename = "geomach_ncrm_str6.bdf"

    #--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

    max_glob_point=0;
    #file = open(mesh_filename, 'r')
    element_count=0
    element_pres =0
    count=0
    pcount=0
    no_of_elements = 0
    no_of_points=0
    elemlist =[]

    no_of_materials = 0
    no_of_shell_elements = 0
    no_of_points = 0
    no_of_elements = 0
    no_of_constraint_points = 0
    no_of_beams = 0
    no_of_beam_elements = 0



#    load_list = [ FORCE() for i in range(1)]
#
#    load_list[0].type='FORCE'
#    load_list[0].sid=1
#    load_list[0].g=1234
#    load_list[0].cid=0
#    load_list[0].f= 1.0
#    load_list[0].n=[1.0,1000.0,1.0]





    #---older code form----------------
    # Read BDF data---
    #filetype = "su2_euler"
    #s200 = sol200()
    s200.times = 600
    s200.sol =200
    s200.case_control_def=1
    s200.load_type=1
    s200.spc_type=1
    s200.read_bdf(mesh_filename)



    mark_loading_points(aircraft,s200.elemlist,s200.pointlist,mesh_filename)
    
    #setup_aero_pointwise(aircraft,s200.elemlist,s200.pointlist)
    #generate_panel_mesh(s200.elemlist,s200.pointlist,aircraft)

    s200.compute_nastran_loads()
    #s200.specify_loads(load_list)

    #--case control section options--

    s200.case_control_def=1

    #--case control section options--


    s200.DESOBJ = 1

    #--Bulk data section options---

    #--if load_type=0 set default value
    #  if load_type=1 set value at boundaries
    #  if load_type=2 import load values from file

    s200.load_type =1

    int_pressure =1566.0
    s200.spc_type=1

    s200.specify_constraint(2,0.0)

    #--------material data-------------
    #no_of_materials = 1
    #material_list = [ MAT1() for i in range(no_of_materials)]

    for i in range(0,s200.no_of_materials):
        s200.material_list[i].type='MAT1'
        s200.material_list[i].mid=i+1
        s200.material_list[i].e=73.9e9 #70e9
        s200.material_list[i].nu=0.33
        s200.material_list[i].rho=2780.0

    #---------material element data--------

    #---shell elements------------------

    #no_of_shell_elements=no_of_materials
    #shell_element_list = [ PSHELL() for i in range(no_of_shell_elements)]


    #--shell materials
    for i in range(0,s200.no_of_shell_elements):
        
        #    shell_element_list[i].type='PSHELL'
        #    shell_element_list[i].pid=i+1
        s200.shell_element_list[i].mid1=1
        s200.shell_element_list[i].t=0.02
        s200.shell_element_list[i].mid2=1
        s200.shell_element_list[i].mid3=1



    #for i in range(0,no_of_elements):
    #    elemlist[i].pid=1



    #------ADDING CONSTRAINTS----------------

    ##--disp type 1
    #spc_type=1
    #no_of_constrained_grid_points=28 #36  #4 #18 #28
    #
    #
    ##---transform the constrained grid points
    #
    #[no_of_constrained_grid_points,constrained_grid_points]= read_constraints(conn_filename,pointlist,no_of_points,scaling_factor)
    #
    #local_dof_constr=123456
    #local_disp_value=0.0
    #constrained_grid_point_list = [ SPC() for i in range(no_of_constrained_grid_points)]
    #
    #for i in range(0,no_of_constrained_grid_points):
    #  #    constrained_grid_points[i]=pointlist_fl[constrained_grid_points[i]].str_grid
    #  constrained_grid_point_list[i].type='SPC1'
    #  constrained_grid_point_list[i].sid=1
    #  constrained_grid_point_list[i].g1=pointlist_fl[constrained_grid_points[i]].str_grid
    #  constrained_grid_point_list[i].c1= 123456 #local_dof_constr
    #  constrained_grid_point_list[i].d1= 0.0  #local_disp_value

    #------------------Design optimization part-----------------------

    #-------Define the analysis disciplines to be used


    s200.case_control_def=1

    #case control
    s200.case_control_analysis_type=  'STATICS'


    #Define the design variables
    #bulk data

    #DESVAR
    s200.no_of_design_variables=s200.no_of_shell_elements#+no_of_beam_elements
    design_var_list = [ DESVAR() for i in range(s200.no_of_design_variables)]

    for i in range(0,s200.no_of_design_variables):
        design_var_list[i].type = 'DESVAR'
        design_var_list[i].id = i+1
        design_var_list[i].label = 'desvar1'
        design_var_list[i].xinit = 0.02
        design_var_list[i].xlb = 0.001
        design_var_list[i].xub = 0.5
        design_var_list[i].delxv =0.5

    s200.design_var_list = design_var_list

    #---view the mesh---------------

    s200.no_of_property_types= s200.no_of_shell_elements #+ no_of_beam_elements

    design_ppties_list = [ DVPREL1() for i in range(s200.no_of_property_types)]

    for i in range(0,s200.no_of_shell_elements):
        design_ppties_list[i].type = 'DVPREL1'
        design_ppties_list[i].id = i+1
        design_ppties_list[i].type2 = 'PSHELL'
        design_ppties_list[i].pid = i+1
        design_ppties_list[i].fid = 'T'
        design_ppties_list[i].pmin =0.001
        design_ppties_list[i].pmax =0.5
        design_ppties_list[i].c0 =0.0
        design_ppties_list[i].dvid1 = i+1
        design_ppties_list[i].coef1 = 1.0

    s200.design_ppties_list = design_ppties_list

    #----------beam elements

    #no_of_property_types=no_of_design_variables
    #design_ppties_list = [ DVPREL1() for i in range(no_of_property_types)]

    for i in range(s200.no_of_shell_elements,s200.no_of_shell_elements + no_of_beam_elements):
        design_ppties_list[i].type = 'DVPREL1'
        design_ppties_list[i].id =  i+1
        design_ppties_list[i].type2 = 'PBARL'
        design_ppties_list[i].pid =  i+1
        design_ppties_list[i].fid = 'DIM1'
        design_ppties_list[i].pmin =0.001
        design_ppties_list[i].pmax =0.5
        design_ppties_list[i].c0 =0.0
        design_ppties_list[i].dvid1 = i+1
        design_ppties_list[i].coef1 = 1.0

    s200.design_ppties_list = design_ppties_list


    ##--changing the bounds for the dvs
    ##
    #for i in range(0,s200.no_of_shell_elements):
    #
    #    if(i<93):
    #        design_var_list[i].xub = 0.008
    #        design_ppties_list[i].pmax =0.008
    #        design_var_list[i].xinit = 0.002
    #


    #---Define the deisgn responses-----------------

    #bulk data
    #DRESP1
    #DRESP1
    s200.no_of_dresp1 = 7
    s200.no_of_dresp2 = 2
    s200.no_of_equations = 2
    s200.no_of_constraints = 2
    s200.no_of_dconadd = 1


    dresp1_list = [ DRESP1() for i in range(s200.no_of_dresp1)]
    dresp2_list = [ DRESP2() for i in range(s200.no_of_dresp2)]
    equation_list = [ DEQUATN() for i in range(s200.no_of_equations)]
    constraint_list = [ DCONSTR() for i in range(s200.no_of_constraints)]
    dconadd_list = [ DCONADD() for i in range(s200.no_of_dconadd)]


    #DRESP1 Weight
    dresp1_list[0].type = 'DRESP1'
    dresp1_list[0].id = 1   #unique identification number
    dresp1_list[0].label='Wt'        # user defined label
    dresp1_list[0].rtype = 'WEIGHT'     # response type
    dresp1_list[0].ptype ='0'    # used to identify the property type (ELEM, PBAR,PSHELL)
    dresp1_list[0].region  =0  #region identifier for constraint screening
    dresp1_list[0].atta =0     #response attributes
    dresp1_list[0].attb =0
    dresp1_list[0].att1 = 0
    dresp1_list[0].no_of_points = 0


    #DRESP1 Displacement -x
    dresp1_list[1].type = 'DRESP1'
    dresp1_list[1].id = 2   #unique identification number
    dresp1_list[1].label='xDisp'        # user defined label
    dresp1_list[1].rtype = 'DISP'     # response type
    dresp1_list[1].ptype  = '0'   # used to identify the property type (ELEM, PBAR,PSHELL)
    dresp1_list[1].region =0   #region identifier for constraint screening
    dresp1_list[1].atta  =1     #response attributes
    dresp1_list[1].attb  =0
    dresp1_list[1].att1  = list(range(1,s200.no_of_points-1)) #5
    dresp1_list[1].no_of_points = len(list(range(1,s200.no_of_points-1)))

    #DRESP1 Displacement -y
    dresp1_list[2].type = 'DRESP1'
    dresp1_list[2].id = 3   #unique identification number
    dresp1_list[2].label='yDisp'        # user defined label
    dresp1_list[2].rtype = 'DISP'     # response type
    dresp1_list[2].ptype  ='0'   # used to identify the property type (ELEM, PBAR,PSHELL)
    dresp1_list[2].region =0   #region identifier for constraint screening
    dresp1_list[2].atta  =2     #response attributes
    dresp1_list[2].attb =0
    dresp1_list[2].att1  = list(range(1,s200.no_of_points-1)) #5
    dresp1_list[2].no_of_points = len(list(range(1,s200.no_of_points-1)))

    #DRESP1 Displacement -z
    dresp1_list[3].type = 'DRESP1'
    dresp1_list[3].id = 4   #unique identification number
    dresp1_list[3].label='zDisp'        # user defined label
    dresp1_list[3].rtype = 'DISP'     # response type
    dresp1_list[3].ptype ='0'   # used to identify the property type (ELEM, PBAR,PSHELL)
    dresp1_list[3].region =0   #region identifier for constraint screening
    dresp1_list[3].atta  =3     #response attributes
    dresp1_list[3].attb = 0
    dresp1_list[3].att1  = list(range(1,s200.no_of_points-1)) #5
    dresp1_list[3].no_of_points = len(list(range(1,s200.no_of_points-1)))

    #DRESP2 mag disp
    dresp2_list[0].type = 'DRESP2'
    dresp2_list[0].id = 5   #unique identification number
    dresp2_list[0].label ='magdisp'       # user defined label
    dresp2_list[0].eqid =1    # equation id
    dresp2_list[0].region  =0   #region identifier for constraint screening
    dresp2_list[0].method  ='0'    # method to be used on fun
    dresp2_list[0].c1  =0     #constants used
    dresp2_list[0].c2 = 0
    dresp2_list[0].c3 = 0
    dresp2_list[0].associated ='DRESP1' # value associated with (like "DRESP1"
    dresp2_list[0].nr1=2
    dresp2_list[0].nr2=3
    dresp2_list[0].nr3=4


    #stress-----------

    #DRESP1 Stress -x
    dresp1_list[4].type = 'DRESP1'
    dresp1_list[4].id = 6   #unique identification number
    dresp1_list[4].label='majStr'        # user defined label
    dresp1_list[4].rtype = 'STRESS'     # response type
    dresp1_list[4].ptype  = 'ELEM'   # used to identify the property type (ELEM, PBAR,PSHELL)
    dresp1_list[4].region =0   #region identifier for constraint screening
    dresp1_list[4].atta  =7     #stress item code
    dresp1_list[4].attb  =0
    dresp1_list[4].att1  = list(range(1,s200.no_of_elements)) #5
    dresp1_list[4].no_of_points = len(list(range(1,s200.no_of_elements)))

    #DRESP1 Stress -y
    dresp1_list[5].type = 'DRESP1'
    dresp1_list[5].id = 7   #unique identification number
    dresp1_list[5].label='minStr'        # user defined label
    dresp1_list[5].rtype = 'STRESS'     # response type
    dresp1_list[5].ptype  ='ELEM'   # used to identify the property type (ELEM, PBAR,PSHELL)
    dresp1_list[5].region =0   #region identifier for constraint screening
    dresp1_list[5].atta  =8     #response attributes
    dresp1_list[5].attb =0
    dresp1_list[5].att1  = list(range(1,s200.no_of_elements)) #5
    dresp1_list[5].no_of_points = len(list(range(1,s200.no_of_elements)))

    #DRESP1 Stress -z
    dresp1_list[6].type = 'DRESP1'
    dresp1_list[6].id = 8   #unique identification number
    dresp1_list[6].label='vmStr'        # user defined label
    dresp1_list[6].rtype = 'STRESS'     # response type
    dresp1_list[6].ptype ='ELEM'   # used to identify the property type (ELEM, PBAR,PSHELL)
    dresp1_list[6].region =0   #region identifier for constraint screening
    dresp1_list[6].atta  =9     #response attributes
    dresp1_list[6].attb = 0
    dresp1_list[6].att1  = list(range(1,s200.no_of_elements)) #5
    dresp1_list[6].no_of_points = len(list(range(1,s200.no_of_elements)))

    #DRESP2 mag Stress
    dresp2_list[1].type = 'DRESP2'
    dresp2_list[1].id = 9   #unique identification number
    dresp2_list[1].label ='maxStr'       # user defined label
    dresp2_list[1].eqid =2    # equation id
    dresp2_list[1].region  =0   #region identifier for constraint screening
    dresp2_list[1].method  ='0'    # method to be used on fun
    dresp2_list[1].c1  =0     #constants used
    dresp2_list[1].c2 = 0
    dresp2_list[1].c3 = 0
    dresp2_list[1].associated ='DRESP1' # value associated with (like "DRESP1"
    dresp2_list[1].nr1=6
    dresp2_list[1].nr2=7
    dresp2_list[1].nr3=8
    
    
    
#    dresp2_list[2].type = 'DRESP2'
#    dresp2_list[2].id = 10   #unique identification number
#    dresp2_list[2].label ='KSStr1'       # user defined label
#    dresp2_list[2].eqid =3    # equation id
#    dresp2_list[2].region  =0   #region identifier for constraint screening
#    dresp2_list[2].method  ='0'    # method to be used on fun
#    dresp2_list[2].c1  =0     #constants used
#    dresp2_list[2].c2 = 0
#    dresp2_list[2].c3 = 0
#    dresp2_list[2].associated ='DRESP1' # value associated with (like "DRESP1"
#    dresp2_list[2].nr1=8
#    dresp2_list[2].nr2=0
#    dresp2_list[2].nr3=0
#    
#    
#    dresp2_list[3].type = 'DRESP2'
#    dresp2_list[3].id = 11   #unique identification number
#    dresp2_list[3].label ='KSStr2'       # user defined label
#    dresp2_list[3].eqid = 0     # equation id
#    dresp2_list[3].region  =0   #region identifier for constraint screening
#    dresp2_list[3].method  ='SUM'    # method to be used on fun
#    dresp2_list[3].c1  =0     #constants used
#    dresp2_list[3].c2 = 0
#    dresp2_list[3].c3 = 0
#    dresp2_list[3].associated ='DRESP2' # value associated with (like "DRESP1"
#    dresp2_list[3].nr1=10
#    dresp2_list[3].nr2=0
#    dresp2_list[3].nr3=0
#    
#    
#    
#    dresp2_list[4].type = 'DRESP2'
#    dresp2_list[4].id = 12   #unique identification number
#    dresp2_list[4].label ='KSStrF'       # user defined label
#    dresp2_list[4].eqid = 4     # equation id
#    dresp2_list[4].region  =0   #region identifier for constraint screening
#    dresp2_list[4].method  ='0'    # method to be used on fun
#    dresp2_list[4].c1  =0     #constants used
#    dresp2_list[4].c2 = 0
#    dresp2_list[4].c3 = 0
#    dresp2_list[4].associated ='DRESP2' # value associated with (like "DRESP1"
#    dresp2_list[4].nr1=11
#    dresp2_list[4].nr2=0
#    dresp2_list[4].nr3=0

    s200.dresp1_list = dresp1_list
    s200.dresp2_list = dresp2_list


    #Equation to compute max disp
    equation_list[0].type = 'DEQATN'
    equation_list[0].id = 1   #unique equation identification number
    equation_list[0].equation = 'MAG(xDisp,yDisp,zDisp) = SQRT(xDisp**2 + yDisp**2 + zDisp**2 )'       # equation


    #Equation to compute max stress
    equation_list[1].type = 'DEQATN'
    equation_list[1].id = 2   #unique equation identification number
    equation_list[1].equation = 'MAXSTR(majStr,minStr,vmStr) = MAX(majStr , minStr , vmStr )'       # equation

#    #Adding a KS function
#    #Equation to compute max stress
#    #Equation to compute max stress
#    equation_list[2].type = 'DEQATN'
#    equation_list[2].id = 3   #unique equation identification number
#    equation_list[2].equation = 'KS1(vmStr) = (80.0*EXP(vmStr))'
#    
#    equation_list[3].type = 'DEQATN'
#    equation_list[3].id = 4   #unique equation identification number
#    equation_list[3].equation = 'KS(SvmStr) = LOG(SvmStr)/80.0'

#    equation_list[4].type = 'DEQATN'
#    equation_list[4].id = 5   #unique equation identification number
#    equation_list[4].equation = 'KSSUM(xi) = SUM(xi)'

#    
#    equation_list[3].type = 'DEQATN'
#    equation_list[3].id = 4   #unique equation identification number
#    equation_list[3].equation = 'KS(vmStr) = LOG(SUM(80*EXP(vmStr)))/80'


    s200.equation_list = equation_list


    #---Define the constraints-------------

    #case control

    #-----displacement constraint
    constraint_list[0].type = 'DCONSTR'
    constraint_list[0].dcid = 1   #design constrain set identification number
    constraint_list[0].rid =5       #DRESPi entry identification number
    constraint_list[0].lallow =10e-10    #lower bound on the response quantity
    #constraint_list[0].lid                #set identi of a TABLEDi entry that suplies the lower bound as a fun of freq
    constraint_list[0].uallow = 5.01    #upper bound on the response quantity
    #constraint_list[0].uid                #set identification of a Tabledi entry that supplies the upper bound as a fun of freq
    #constraint_list[0].lowfq              #low end of the freq range in Hz
    #constraint_list[0].highfq             #high end of freq range in hz
    #DESGLB
    #DESSUB
    #DRSPAN

    #bulk data
    #DCONSTR
    #DCONADD



    #---------stress constraint------------------
    constraint_list[1].type = 'DCONSTR'
    constraint_list[1].dcid = 2   #design constrain set identification number
    constraint_list[1].rid = 8       #DRESPi entry identification number
    constraint_list[1].lallow =10e-10    #lower bound on the response quantity
    #constraint_list[1].lid                #set identi of a TABLEDi entry that suplies the lower bound as a fun of freq
    constraint_list[1].uallow = 420e6    #upper bound on the response quantity
    
    
#    #---------stress constraint------------------
#    constraint_list[2].type = 'DCONSTR'
#    constraint_list[2].dcid = 3   #design constrain set identification number
#    constraint_list[2].rid = 12       #DRESPi entry identification number
#    constraint_list[2].lallow =10e-10    #lower bound on the response quantity
#    #constraint_list[1].lid                #set identi of a TABLEDi entry that suplies the lower bound as a fun of freq
#    constraint_list[2].uallow = 420e6    #upper bound on the response quantity


    s200.constraint_list = constraint_list


    dconadd_list[0].type = 'DCONADD'
    dconadd_list[0].dcid = 25
    dconadd_list[0].dc1 = 1
    dconadd_list[0].dc2 = 2

    s200.dconadd_list = dconadd_list

    #---------Provide necessary parameter overrides----
    #bulk data
    #DOPTPRM
    #DSCREEN
    #DTABLE


    opt_parameters = DOPTPRM()

    opt_parameters.type = 'DOPTPRM'
    opt_parameters.param1 = 'DESMAX'
    opt_parameters.val1 = 50
    opt_parameters.param2 = 'MXLAGM1'
    opt_parameters.val2 = 50
    
    s200.opt_parameters = opt_parameters



    s200.write_sol(output_filename)

    print "Done writing bdf"#

    #write_tecplot_file_str(s101.pointlist,s101.elemlist,tecplot_file_orig,s101.no_of_points,s101.no_of_elements)




