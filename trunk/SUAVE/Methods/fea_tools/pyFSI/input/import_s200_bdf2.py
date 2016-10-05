#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

import numpy as np

#Import SUAVE
#Import GeoMACH
#Import PanelCode
#Import python nastran interface

#Create the necessary data structure - similar to suave
#Interface file to suave
#Interface for GeoMACH
#Interface for panel code
#Interface to python_nastran


from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3
from pyFSI.class_str.material.class_structure import PSHELL
from pyFSI.class_str.material.class_structure import PBARL
from pyFSI.class_str.material.class_structure import MAT1
from pyFSI.class_str.load_disp_bc.class_structure import FORCE
from pyFSI.class_str.load_disp_bc.class_structure import PLOAD
from pyFSI.class_str.load_disp_bc.class_structure import SPC
from pyFSI.class_str.io.class_structure import SU2_import

from pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from pyFSI.class_str.io.nastran_datatype_write_formats import str_form

from pyFSI.class_str.io.nastran_datatype_write_formats import float_forms
from pyFSI.class_str.io.nastran_datatype_write_formats import int_forms
from pyFSI.utility_functions.pressure_interpolation import pressure_interpolation


from pyFSI.class_str.optimization.constraints.class_structure import DCONSTR
from pyFSI.class_str.optimization.constraints.class_structure import DCONADD
from pyFSI.class_str.optimization.constraints.class_structure import DRESP
from pyFSI.class_str.optimization.constraints.class_structure import DRESP1
from pyFSI.class_str.optimization.constraints.class_structure import DRESP2
from pyFSI.class_str.optimization.constraints.class_structure import DDVAL
from pyFSI.class_str.optimization.constraints.class_structure import DEQUATN
from pyFSI.class_str.optimization.constraints.class_structure import DESVAR
from pyFSI.class_str.optimization.constraints.class_structure import DVPREL1
from pyFSI.class_str.optimization.constraints.class_structure import DVCREL1
from pyFSI.class_str.optimization.constraints.class_structure import DVGRID
from pyFSI.class_str.optimization.constraints.class_structure import DLINK
from pyFSI.class_str.optimization.constraints.class_structure import DOPTPRM

from pyFSI.utility_functions.print_equation import print_equation
from pyFSI.class_str.solution_classes.sol200 import sol200

from pyFSI.input.read_bdf_file_force import read_bdf_file_force


def import_s200_bdf(input_bdf):

    #read the bdf
    [elemlist,pointlist,no_of_points,no_of_elements,material_list,no_of_materials,shell_element_list,no_of_shell_elements,constrained_grid_point_list,no_of_constrained_grid_points,load_list,no_of_grid_points_w_load] = read_bdf_file_force(input_bdf,1.0)


    #read the force files

    s200 = sol200()

    #remove the specified elements and create a new elements list

    #create a new sol200 object

    s200.times = 600
    s200.sol =200
    s200.case_control_def=1
    s200.load_type=1
    s200.spc_type=1


    s200.elemlist = elemlist
    s200.pointlist = pointlist
    s200.material_list = material_list
    s200.shell_element_list = shell_element_list
    s200.constrained_grid_point_list = constrained_grid_point_list
    s200.load_list = load_list

    s200.no_of_points = no_of_points
    s200.no_of_elements = no_of_elements
    s200.no_of_materials = no_of_materials
    s200.no_of_shell_elements = no_of_shell_elements
    s200.no_of_constrained_grid_points = no_of_constrained_grid_points
    s200.no_of_original_elements = no_of_elements
    s200.no_of_grid_points_w_load = no_of_grid_points_w_load
    s200.no_of_beam_elements = 0





    #build the s200 material and element list
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

    for i in range(s200.no_of_shell_elements,s200.no_of_shell_elements + s200.no_of_beam_elements):
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



    #---Define the deisgn responses-----------------

    #bulk data
    #DRESP1
    s200.no_of_dresp1 = 7
    s200.no_of_dresp2 = 2
    s200.no_of_equations = 2
    s200.no_of_constraints =2
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
    constraint_list[1].rid =8       #DRESPi entry identification number
    constraint_list[1].lallow =10e-10    #lower bound on the response quantity
    #constraint_list[1].lid                #set identi of a TABLEDi entry that suplies the lower bound as a fun of freq
    constraint_list[1].uallow = 420e6    #upper bound on the response quantity


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




    print "Done importing bdf"#

    return s200


