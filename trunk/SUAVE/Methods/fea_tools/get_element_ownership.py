import numpy as np



#--imports---
import re
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import math


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
from SUAVE.Methods.fea_tools.pyFSI.input.read_bdf_file import read_bdf_file


#read the file

#mark the existing components

#combine them, write the map

#write out the bdf file

#end with a max case where each element is a design variable

#for external components group by j

def get_element_ownership(bdf_structural_meshfile,aircraft):
    scaling_factor = 1.0
    elemlist,pointlist,no_of_points,no_of_elements,material_list,no_of_materials,shell_element_list,no_of_shell_elements,constrained_grid_point_list,no_of_constrained_grid_points = read_bdf_file(bdf_structural_meshfile,scaling_factor)


#    for i in range(0,len(shell_element_list)):
#        print shell_element_list[i].name

    element_map = np.zeros(no_of_shell_elements)
    dv_breakdown = aircraft.dv_breakdown
    
    #class in aircraft that has the number of dvs
    no_of_dvs = dv_breakdown.total
    new_element_map = dv_breakdown.new_element_map
    shell_element_list_new = dv_breakdown.shell_element_list_new
    no_of_shell_elements_new = len(shell_element_list_new)
    
    
    aircraft.loads_marked = 1
    
    #loop over the wings

    
    no_of_dvs = 0


    #store the shell elements in a map
        #based on the tags combine the elements

    for i in range(0,len(shell_element_list)):
        name = shell_element_list[i].name
        name_s = name.split(':')
        current_element_id = shell_element_list[i].pid
        breakv = 0
        
        for wing in dv_breakdown.wings:
            
                    
            if (name_s[0] == wing.upper.tag[0]) and (name_s[1] == wing.upper.tag[1]):
                wing.upper.no_of_elements += 1
                wing.upper.new_element_nos.append(current_element_id)
                wing.upper.element_tags.append(name)
                breakv = 1
                break
        
        
            
            if (name_s[0] == wing.lower.tag[0]) and (name_s[1] == wing.lower.tag[1]):
                wing.lower.no_of_elements += 1
                wing.lower.new_element_nos.append(current_element_id)
                wing.lower.element_tags.append(name)
                breakv = 1
                break
            

            if (name_s[0] == wing.tip.tag[0]) and (name_s[1] == wing.tip.tag[1]):
                wing.tip.no_of_elements += 1
                wing.tip.new_element_nos.append(current_element_id)
                wing.tip.element_tags.append(name)
                breakv = 1
                break
            
            
            if (name_s[0] == wing.spars.tag[0]) and (name_s[1] == wing.spars.tag[1]):
                wing.spars.no_of_elements += 1
                wing.spars.new_element_nos.append(current_element_id)
                wing.spars.element_tags.append(name)
                breakv = 1
                break


            if (name_s[0] == wing.ribs.tag[0]) and (name_s[1] == wing.ribs.tag[1]):
                wing.ribs.no_of_elements += 1
                wing.ribs.new_element_nos.append(current_element_id)
                wing.ribs.element_tags.append(name)
                breakv = 1
                break



#            if (name_s[0] == wing.internal.tag[0]) and (name_s[1] == wing.internal.tag[1]):
#                wing.internal.no_of_elements += 1
#                wing.internal.element_nos.append(current_element_id)
#                wing.internal.element_tags.append(name)
#                breakv = 1
#                break

        
        
        
        if(breakv==0):
            #loop over the fuselages
            for fuse in dv_breakdown.fuselages:
                
                
                if (name_s[0] == fuse.top.tag[0]) and (name_s[1] == fuse.top.tag[1]):
                    fuse.top.no_of_elements += 1
                    fuse.top.new_element_nos.append(current_element_id)
                    fuse.top.element_tags.append(name)
                    breakv = 1
                    break
                
                
                if (name_s[0] == fuse.bottom.tag[0]) and (name_s[1] == fuse.bottom.tag[1]):
                    fuse.bottom.no_of_elements += 1
                    fuse.bottom.new_element_nos.append(current_element_id)
                    fuse.bottom.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.left.tag[0]) and (name_s[1] == fuse.left.tag[1]):
                    fuse.left.no_of_elements += 1
                    fuse.left.new_element_nos.append(current_element_id)
                    fuse.left.element_tags.append(name)
                    breakv = 1
                    break
                

                if (name_s[0] == fuse.right.tag[0]) and (name_s[1] == fuse.right.tag[1]):
                    fuse.right.no_of_elements += 1
                    fuse.right.new_element_nos.append(current_element_id)
                    fuse.right.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.front.tag[0]) and (name_s[1] == fuse.front.tag[1]):
                    fuse.front.no_of_elements += 1
                    fuse.front.new_element_nos.append(current_element_id)
                    fuse.front.element_tags.append(name)
                    breakv = 1
                    break
                

                if (name_s[0] == fuse.rear.tag[0]) and (name_s[1] == fuse.rear.tag[1]):
                    fuse.rear.no_of_elements += 1
                    fuse.rear.new_element_nos.append(current_element_id)
                    fuse.rear.element_tags.append(name)
                    breakv = 1
                    break
                

                if (name_s[0] == fuse.r1.tag[0]) and (name_s[1] == fuse.r1.tag[1]):
                    fuse.r1.no_of_elements += 1
                    fuse.r1.new_element_nos.append(current_element_id)
                    fuse.r1.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.r2.tag[0]) and (name_s[1] == fuse.r2.tag[1]):
                    fuse.r2.no_of_elements += 1
                    fuse.r2.new_element_nos.append(current_element_id)
                    fuse.r2.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.r3.tag[0]) and (name_s[1] == fuse.r3.tag[1]):
                    fuse.r3.no_of_elements += 1
                    fuse.r3.new_element_nos.append(current_element_id)
                    fuse.r3.element_tags.append(name)
                    breakv = 1
                    break
                
                
                if (name_s[0] == fuse.r4.tag[0]) and (name_s[1] == fuse.r4.tag[1]):
                    fuse.r4.no_of_elements += 1
                    fuse.r4.new_element_nos.append(current_element_id)
                    fuse.r4.element_tags.append(name)
                    breakv = 1
                    break

                
                
                if (name_s[0] == fuse.l1.tag[0]) and (name_s[1] == fuse.l1.tag[1]):
                    fuse.l1.no_of_elements += 1
                    fuse.l1.new_element_nos.append(current_element_id)
                    fuse.l1.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.l2.tag[0]) and (name_s[1] == fuse.l2.tag[1]):
                    fuse.l2.no_of_elements += 1
                    fuse.l2.new_element_nos.append(current_element_id)
                    fuse.l2.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.l3.tag[0]) and (name_s[1] == fuse.l3.tag[1]):
                    fuse.l3.no_of_elements += 1
                    fuse.l3.new_element_nos.append(current_element_id)
                    fuse.l3.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.l4.tag[0]) and (name_s[1] == fuse.l4.tag[1]):
                    fuse.l4.no_of_elements += 1
                    fuse.l4.new_element_nos.append(current_element_id)
                    fuse.l4.element_tags.append(name)
                    breakv = 1
                    break



        if(breakv==0):
        #loop over the intersections
            for intersection in dv_breakdown.intersections:
                if (name_s[0] ==  intersection.dv.tag[0]) and (name_s[1] ==  intersection.dv.tag[1]):
                    intersection.dv.no_of_elements += 1
                    intersection.dv.new_element_nos.append(current_element_id)
                    intersection.dv.element_tags.append(name)
                    breakv = 1
                    break


        if(breakv==0):
            #loop over the miscellaneous
            for misc in dv_breakdown.miscellaneous:
                if (name_s[0] ==  misc.dv.tag[0]) and (name_s[1] ==  misc.dv.tag[1]):
                    misc.dv.no_of_elements += 1
                    misc.dv.new_element_nos.append(current_element_id)
                    misc.dv.element_tags.append(name)
                    breakv = 1
                    break

