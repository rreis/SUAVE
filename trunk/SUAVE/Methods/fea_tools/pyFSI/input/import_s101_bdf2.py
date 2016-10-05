#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#Anil Variyar

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
#from pyFSI.class_str.solution_classes.sol200 import sol200
#from pyFSI.class_str.solution_classes.sol101 import sol101

from pyFSI.input.read_bdf_file_force import read_bdf_file_force


def import_s101_bdf(input_bdf,s101):

    #read the bdf
    [elemlist,pointlist,no_of_points,no_of_elements,material_list,no_of_materials,shell_element_list,no_of_shell_elements,constrained_grid_point_list,no_of_constrained_grid_points,load_list,no_of_grid_points_w_load] = read_bdf_file_force(input_bdf,1.0)


    #read the force files

    #s101 = sol101()

    #remove the specified elements and create a new elements list

    #create a new sol200 object

    s101.times = 600
    s101.sol = 101
    s101.case_control_def=1
    s101.load_type=1
    s101.spc_type=1


    s101.elemlist = elemlist
    s101.pointlist = pointlist
    s101.material_list = material_list
    s101.shell_element_list = shell_element_list
    s101.constrained_grid_point_list = constrained_grid_point_list
    s101.load_list = load_list

    s101.no_of_points = no_of_points
    s101.no_of_elements = no_of_elements
    s101.no_of_materials = no_of_materials
    s101.no_of_shell_elements = no_of_shell_elements
    s101.no_of_constrained_grid_points = no_of_constrained_grid_points
    s101.no_of_original_elements = no_of_elements
    s101.no_of_grid_points_w_load = no_of_grid_points_w_load
    s101.no_of_beam_elements = 0





    #build the s101 material and element list
    s101.case_control_def=1
        
    #--case control section options--


    s101.DESOBJ = 1

    #--Bulk data section options---

    #--if load_type=0 set default value
    #  if load_type=1 set value at boundaries
    #  if load_type=2 import load values from file

    s101.load_type =1

    int_pressure =1566.0
    s101.spc_type=1


    #--------material data-------------
    #no_of_materials = 1
    #material_list = [ MAT1() for i in range(no_of_materials)]

    for i in range(0,s101.no_of_materials):
        s101.material_list[i].type='MAT1'
        s101.material_list[i].mid=i+1
        s101.material_list[i].e=73.9e9 #70e9
        s101.material_list[i].nu=0.33
        s101.material_list[i].rho=2780.0

    #---------material element data--------

    #---shell elements------------------

    #no_of_shell_elements=no_of_materials
    #shell_element_list = [ PSHELL() for i in range(no_of_shell_elements)]


    #--shell materials
    for i in range(0,s101.no_of_shell_elements):
        
        #    shell_element_list[i].type='PSHELL'
        #    shell_element_list[i].pid=i+1
        s101.shell_element_list[i].mid1=1
        #s101.shell_element_list[i].t=0.02
        s101.shell_element_list[i].mid2=1
        s101.shell_element_list[i].mid3=1




    s101.case_control_def=1

    #case control
    s101.case_control_analysis_type=  'STATICS'




    print "Done importing bdf"#

    #return s101


