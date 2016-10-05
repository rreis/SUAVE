# regenerate_geomach_bdf_spanwise.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

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
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.compute_centroid import compute_centroid

#read the file

#mark the existing components

#combine them, write the map

#write out the bdf file

#end with a max case where each element is a design variable

#for external components group by j

def regenerate_geomach_bdf_spanwise(bdf_structural_meshfile,bdf_structural_meshfile_new,aircraft):
    scaling_factor = 1.0
    
    if (aircraft.structural_mesh_added==0):
        elemlist,pointlist,no_of_points,no_of_elements,material_list,no_of_materials,shell_element_list,no_of_shell_elements,constrained_grid_point_list,no_of_constrained_grid_points = read_bdf_file(bdf_structural_meshfile,scaling_factor)
    
    
        aircraft.structural_mesh_points = pointlist
        aircraft.structural_mesh_elements = elemlist
        aircraft.structural_mesh_material_list = material_list
        aircraft.structural_mesh_shell_element_list = shell_element_list
        aircraft.structural_mesh_constrained_grid_point_list = constrained_grid_point_list

        aircraft.structural_mesh_added = 1
    
    
    else:

        pointlist = aircraft.structural_mesh_points
        elemlist = aircraft.structural_mesh_elements
        material_list = aircraft.structural_mesh_material_list
        shell_element_list = aircraft.structural_mesh_shell_element_list
        constrained_grid_point_list = aircraft.structural_mesh_constrained_grid_point_list

        no_of_points = len(pointlist)
        no_of_elements = len(elemlist)
        no_of_materials = len(material_list)
        no_of_shell_elements = len(shell_element_list)
        no_of_constrained_grid_points = len(constrained_grid_point_list)
        print "structural mesh added : ",aircraft.structural_mesh_added



    compute_centroid(elemlist,pointlist)

    print "elem map : no of shell elements : ",no_of_shell_elements
    element_map = np.zeros(no_of_shell_elements)
    dv_breakdown = aircraft.dv_breakdown
    
    #class in aircraft that has the number of dvs
    no_of_dvs = dv_breakdown.total
    new_element_map = dv_breakdown.new_element_map
    shell_element_list_new = dv_breakdown.shell_element_list_new
    no_of_shell_elements_new = len(shell_element_list_new)
    
    
    aircraft.loads_marked = 0 #1
    
    #loop over the wings

    
    no_of_dvs = 0
    
    
#    print dv_breakdown.wings[1].upper.tag[0],dv_breakdown.wings[1].lower.tag[0],dv_breakdown.wings[1].tip.tag[0]
#    
#    print dv_breakdown.wings[1].upper.tag[1],dv_breakdown.wings[1].lower.tag[1],dv_breakdown.wings[1].tip.tag[1]
#    
#    print dv_breakdown.wings[1].upper.required_no_of_elements,dv_breakdown.wings[1].lower.required_no_of_elements,dv_breakdown.wings[1].tip.required_no_of_elements

    
    print "-------------------------------------------------------------------"
    print "-------------------------------------------------------------------"


    #store the shell elements in a map
        #based on the tags combine the elements
        
        
    


#------------------element_partition-----------------------------------------------------------



    for i in range(0,len(shell_element_list)):
        name = shell_element_list[i].name
        name_s = name.split(':')
        current_element_id = shell_element_list[i].pid
        breakv = 0
        
        #print name_s
        
        for wing in dv_breakdown.wings:
            
                    
            if (name_s[0] == wing.upper.tag[0]) and (name_s[1] == wing.upper.tag[1]):
                wing.upper.no_of_elements += 1
                wing.upper.element_nos.append(current_element_id)
                wing.upper.element_tags.append(name)
                breakv = 1
                break
        
        
            
            if (name_s[0] == wing.lower.tag[0]) and (name_s[1] == wing.lower.tag[1]):
                wing.lower.no_of_elements += 1
                wing.lower.element_nos.append(current_element_id)
                wing.lower.element_tags.append(name)
                breakv = 1
                break
            

            if (name_s[0] == wing.tip.tag[0]) and (name_s[1] == wing.tip.tag[1]):
                wing.tip.no_of_elements += 1
                wing.tip.element_nos.append(current_element_id)
                wing.tip.element_tags.append(name)
                breakv = 1
                break
            
            
            if (name_s[0] == wing.spars.tag[0]) and (name_s[1] == wing.spars.tag[1]):
                wing.spars.no_of_elements += 1
                wing.spars.element_nos.append(current_element_id)
                wing.spars.element_tags.append(name)
                breakv = 1
                break


            if (name_s[0] == wing.ribs.tag[0]) and (name_s[1] == wing.ribs.tag[1]):
                wing.ribs.no_of_elements += 1
                wing.ribs.element_nos.append(current_element_id)
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
                    fuse.top.element_nos.append(current_element_id)
                    fuse.top.element_tags.append(name)
                    breakv = 1
                    break
                
                
                if (name_s[0] == fuse.bottom.tag[0]) and (name_s[1] == fuse.bottom.tag[1]):
                    fuse.bottom.no_of_elements += 1
                    fuse.bottom.element_nos.append(current_element_id)
                    fuse.bottom.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.left.tag[0]) and (name_s[1] == fuse.left.tag[1]):
                    fuse.left.no_of_elements += 1
                    fuse.left.element_nos.append(current_element_id)
                    fuse.left.element_tags.append(name)
                    breakv = 1
                    break
                

                if (name_s[0] == fuse.right.tag[0]) and (name_s[1] == fuse.right.tag[1]):
                    fuse.right.no_of_elements += 1
                    fuse.right.element_nos.append(current_element_id)
                    fuse.right.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.front.tag[0]) and (name_s[1] == fuse.front.tag[1]):
                    fuse.front.no_of_elements += 1
                    fuse.front.element_nos.append(current_element_id)
                    fuse.front.element_tags.append(name)
                    breakv = 1
                    break
                

                if (name_s[0] == fuse.rear.tag[0]) and (name_s[1] == fuse.rear.tag[1]):
                    fuse.rear.no_of_elements += 1
                    fuse.rear.element_nos.append(current_element_id)
                    fuse.rear.element_tags.append(name)
                    breakv = 1
                    break
                

                if (name_s[0] == fuse.r1.tag[0]) and (name_s[1] == fuse.r1.tag[1]):
                    fuse.r1.no_of_elements += 1
                    fuse.r1.element_nos.append(current_element_id)
                    fuse.r1.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.r2.tag[0]) and (name_s[1] == fuse.r2.tag[1]):
                    fuse.r2.no_of_elements += 1
                    fuse.r2.element_nos.append(current_element_id)
                    fuse.r2.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.r3.tag[0]) and (name_s[1] == fuse.r3.tag[1]):
                    fuse.r3.no_of_elements += 1
                    fuse.r3.element_nos.append(current_element_id)
                    fuse.r3.element_tags.append(name)
                    breakv = 1
                    break
                
                
                if (name_s[0] == fuse.r4.tag[0]) and (name_s[1] == fuse.r4.tag[1]):
                    fuse.r4.no_of_elements += 1
                    fuse.r4.element_nos.append(current_element_id)
                    fuse.r4.element_tags.append(name)
                    breakv = 1
                    break

                
                
                if (name_s[0] == fuse.l1.tag[0]) and (name_s[1] == fuse.l1.tag[1]):
                    fuse.l1.no_of_elements += 1
                    fuse.l1.element_nos.append(current_element_id)
                    fuse.l1.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.l2.tag[0]) and (name_s[1] == fuse.l2.tag[1]):
                    fuse.l2.no_of_elements += 1
                    fuse.l2.element_nos.append(current_element_id)
                    fuse.l2.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.l3.tag[0]) and (name_s[1] == fuse.l3.tag[1]):
                    fuse.l3.no_of_elements += 1
                    fuse.l3.element_nos.append(current_element_id)
                    fuse.l3.element_tags.append(name)
                    breakv = 1
                    break

                
                if (name_s[0] == fuse.l4.tag[0]) and (name_s[1] == fuse.l4.tag[1]):
                    fuse.l4.no_of_elements += 1
                    fuse.l4.element_nos.append(current_element_id)
                    fuse.l4.element_tags.append(name)
                    breakv = 1
                    break



        if(breakv==0):
        #loop over the intersections
            for intersection in dv_breakdown.intersections:
                if (name_s[0] ==  intersection.dv.tag[0]) and (name_s[1] ==  intersection.dv.tag[1]):
                    intersection.dv.no_of_elements += 1
                    intersection.dv.element_nos.append(current_element_id)
                    intersection.dv.element_tags.append(name)
                    breakv = 1
                    break


        if(breakv==0):
            #loop over the miscellaneous
            for misc in dv_breakdown.miscellaneous:
                if (name_s[0] ==  misc.dv.tag[0]) and (name_s[1] ==  misc.dv.tag[1]):
                    misc.dv.no_of_elements += 1
                    misc.dv.element_nos.append(current_element_id)
                    misc.dv.element_tags.append(name)
                    breakv = 1
                    break



    

    print "wing element numbers upper : "
    print "lwing : ",dv_breakdown.wings[0].upper.element_nos
    print "lstrut : ",dv_breakdown.wings[1].upper.element_nos

    print "element check : "
    
    wing_upper_count = 0

    for i in range(0,len(elemlist)):

        breakv = 0
        
        
        for wing in dv_breakdown.wings:
            
                    
            if (elemlist[i].pid in wing.upper.element_nos):
                #print wing_upper_count,elemlist[i].pid
                wing_upper_count = wing_upper_count + 1
                wing.upper.fea_element_nos.append(i)
                breakv = 1
                break
        
        
            
            if (elemlist[i].pid in wing.lower.element_nos):
                wing.lower.fea_element_nos.append(i)
                breakv = 1
                break
            

            if (elemlist[i].pid in wing.tip.element_nos):
                wing.tip.fea_element_nos.append(i)
                breakv = 1
                break
            
            
            if (elemlist[i].pid in wing.spars.element_nos):
                wing.spars.fea_element_nos.append(i)
                breakv = 1
                break


            if (elemlist[i].pid in wing.ribs.element_nos):
                wing.ribs.fea_element_nos.append(i)
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
                
                if (elemlist[i].pid in fuse.top.element_nos):
                    fuse.top.fea_element_nos.append(i)
                    breakv = 1
                    break
                
                
                if (elemlist[i].pid in fuse.bottom.element_nos):
                    fuse.bottom.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                if (elemlist[i].pid in fuse.left.element_nos):
                    fuse.left.fea_element_nos.append(i)
                    breakv = 1
                    break
                

                if (elemlist[i].pid in fuse.right.element_nos):
                    fuse.right.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                if (elemlist[i].pid in fuse.front.element_nos):
                    fuse.front.fea_element_nos.append(i)
                    breakv = 1
                    break
                

                if (elemlist[i].pid in fuse.rear.element_nos):
                    fuse.rear.fea_element_nos.append(i)
                    breakv = 1
                    break
                

                if (elemlist[i].pid in fuse.r1.element_nos):
                    fuse.r1.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                if (elemlist[i].pid in fuse.r2.element_nos):
                    fuse.r2.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                if (elemlist[i].pid in fuse.r3.element_nos):
                    fuse.r3.fea_element_nos.append(i)
                    breakv = 1
                    break
                
                
                if (elemlist[i].pid in fuse.r4.element_nos):
                    fuse.r4.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                
                if (elemlist[i].pid in fuse.l1.element_nos):
                    fuse.l1.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                if (elemlist[i].pid in fuse.l2.element_nos):
                    fuse.l2.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                if (elemlist[i].pid in fuse.l3.element_nos):
                    fuse.l3.fea_element_nos.append(i)
                    breakv = 1
                    break

                
                if (elemlist[i].pid in fuse.l4.element_nos):
                    fuse.l4.fea_element_nos.append(i)
                    breakv = 1
                    break



        if(breakv==0):
        #loop over the intersections
            for intersection in dv_breakdown.intersections:
                if (elemlist[i].pid in intersection.dv.element_nos):
                    intersection.dv.fea_element_nos.append(i)
                    breakv = 1
                    break


        if(breakv==0):
            #loop over the miscellaneous
            for misc in dv_breakdown.miscellaneous:
                if (elemlist[i].pid in misc.dv.element_nos):
                    misc.dv.fea_element_nos.append(i)
                    breakv = 1
                    break

            



    print "-------------------------------------------------------------------"
    print "-------------------------------------------------------------------"
    print "wings upper : ",len(dv_breakdown.wings[0].upper.fea_element_nos)

    #mapping------------------------------
    dv_count = 0
    shell_name_lists  = [str() for i in range(no_of_shell_elements)]
    shell_element_lists_redone  = [PSHELL() for i in range(no_of_shell_elements)]
    #shell_name_lists_count = 0
    
    #compute the element centroids
    
    local_dv_value = 0
    
    for iwing in range(0,len(aircraft.main_wing)):
    
        wing_tip_z = aircraft.main_wing[iwing].tip_origin[2]
        wing_root_z = aircraft.main_wing[iwing].root_origin[2]
    
        wing_span = wing_tip_z - wing_root_z
    
        #number_of_sections = dv_breakdown.wings[iwing].structural_dv
        number_of_sections = aircraft.main_wing[iwing].structural_dv
    
        spanwise_sections = np.zeros(number_of_sections+1)
        
        section_span = float(wing_span)/float(number_of_sections)
        
        wing = dv_breakdown.wings[iwing]
        
        for ielem in range(0,len(wing.upper.fea_element_nos)):
            ielems = wing.upper.fea_element_nos[ielem]
            local_pid = min(int(math.floor(float(elemlist[ielems].centroid[2] - wing_root_z)/float(section_span))),wing.upper.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            #print ielem #wing.upper.tag[0],elemlist[ielems].pid,local_dv_value + local_pid
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,wing.upper.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = wing.upper.tag[0]+ ":" + wing.upper.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03            
        local_dv_value +=  wing.upper.required_no_of_elements        
            
            
        for ielem in range(0,len(wing.lower.fea_element_nos)):
            ielems = wing.lower.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[2] - wing_root_z)/section_span)),wing.lower.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,wing.lower.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = wing.lower.tag[0]+ ":" + wing.lower.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03          
        local_dv_value +=  wing.lower.required_no_of_elements    


        for ielem in range(0,len(wing.tip.fea_element_nos)):
            ielems = wing.tip.fea_element_nos[ielem]
            elemlist[ielems].pid = local_dv_value #+ min(int(math.floor((elemlist[ielem].centroid[2] - wing_root_z)/section_span)),wing.lower.dv_value)
        for i in range(0,1):
            shell_name_lists[local_dv_value+i] = wing.tip.tag[0]+ ":" + wing.tip.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  1 #wing.upper.dv_value

        
        for ielem in range(0,len(wing.spars.fea_element_nos)):
            ielems = wing.spars.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[2] - wing_root_z)/section_span)),wing.spars.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,wing.spars.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = wing.spars.tag[0]+ ":" + wing.spars.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  wing.spars.required_no_of_elements

        
        for ielem in range(0,len(wing.ribs.fea_element_nos)):
            ielems = wing.ribs.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[2] - wing_root_z)/section_span)),wing.ribs.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,wing.ribs.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = wing.ribs.tag[0]+ ":" + wing.ribs.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  wing.ribs.required_no_of_elements 


    for ifus in range(0,len(aircraft.fuselage)):
    
        fus_tip_z = aircraft.fuselage[ifus].tip_origin[0]
        fus_root_z = aircraft.fuselage[ifus].root_origin[0]
    
        fus_length = fus_tip_z - fus_root_z
    
        number_of_sections = aircraft.fuselage[ifus].structural_dv
    
        spanwise_sections = np.zeros(number_of_sections+1)
        
        section_span = float(fus_length)/float(number_of_sections)
        
        fus = dv_breakdown.fuselages[ifus]
        
        
        for ielem in range(0,len(fuse.top.fea_element_nos)):
            ielems = fuse.top.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.top.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.top.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.top.tag[0]+ ":" + fuse.top.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.top.required_no_of_elements        
            

        for ielem in range(0,len(fuse.bottom.fea_element_nos)):
            ielems = fuse.bottom.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.bottom.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.bottom.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.bottom.tag[0]+ ":" + fuse.bottom.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.bottom.required_no_of_elements   


        for ielem in range(0,len(fuse.left.fea_element_nos)):
            ielems = fuse.left.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.left.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.left.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.left.tag[0]+ ":" + fuse.left.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.left.required_no_of_elements   

        for ielem in range(0,len(fuse.right.fea_element_nos)):
            ielems = fuse.right.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.right.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.right.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.right.tag[0]+ ":" + fuse.right.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.right.required_no_of_elements         
        

        for ielem in range(0,len(fuse.front.fea_element_nos)):
            ielems = fuse.front.fea_element_nos[ielem]
            elemlist[ielems].pid = local_dv_value #+ min(int(math.floor((elemlist[ielem].centroid[0] - fus_root_z)/section_span)),fus.right.dv_value)
        for i in range(0,1):
            shell_name_lists[local_dv_value+i] = fuse.front.tag[0]+ ":" + fuse.front.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  1 #fus.right.dv_value 


        for ielem in range(0,len(fuse.rear.fea_element_nos)):
            ielems = fuse.rear.fea_element_nos[ielem]
            elemlist[ielems].pid = local_dv_value #+ min(int(math.floor((elemlist[ielem].centroid[0] - fus_root_z)/section_span)),fus.right.dv_value)
        for i in range(0,1):
            shell_name_lists[local_dv_value+i] = fuse.rear.tag[0]+ ":" + fuse.rear.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  1 #fus.right.dv_value         


        for ielem in range(0,len(fuse.r1.fea_element_nos)):
            ielems = fuse.r1.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.r1.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.r1.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.r1.tag[0]+ ":" + fuse.r1.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.r1.required_no_of_elements

        for ielem in range(0,len(fuse.r2.fea_element_nos)):
            ielems = fuse.r2.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.r2.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.r2.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.r2.tag[0]+ ":" + fuse.r2.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.r2.required_no_of_elements         
        
        for ielem in range(0,len(fuse.r3.fea_element_nos)):
            ielems = fuse.r3.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.r3.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.r3.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.r3.tag[0]+ ":" + fuse.r3.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.r3.required_no_of_elements         

        for ielem in range(0,len(fuse.r4.fea_element_nos)):
            ielems = fuse.r4.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.r4.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.r4.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.r4.tag[0]+ ":" + fuse.r4.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.r4.required_no_of_elements         

        
        for ielem in range(0,len(fuse.l1.fea_element_nos)):
            ielems = fuse.l1.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.l1.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.l1.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.l1.tag[0]+ ":" + fuse.l1.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.l1.required_no_of_elements


        for ielem in range(0,len(fuse.l2.fea_element_nos)):
            ielems = fuse.l2.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.l2.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.l2.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.l2.tag[0]+ ":" + fuse.l2.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.l2.required_no_of_elements        
        

        for ielem in range(0,len(fuse.l3.fea_element_nos)):
            ielems = fuse.l3.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.l3.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.l3.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.l3.tag[0]+ ":" + fuse.l3.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.l3.required_no_of_elements         


        for ielem in range(0,len(fuse.l4.fea_element_nos)):
            ielems = fuse.l4.fea_element_nos[ielem]
            local_pid = min(int(math.floor((elemlist[ielems].centroid[0] - fus_root_z)/section_span)),fus.l4.required_no_of_elements)
            if(local_pid < 0):
                local_pid = 0
            elemlist[ielems].pid = local_dv_value + local_pid
        for i in range(0,fuse.l4.required_no_of_elements):
            shell_name_lists[local_dv_value+i] = fuse.l4.tag[0]+ ":" + fuse.l4.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value +=  fus.l4.required_no_of_elements         

        
    
    
    for iint in range(0,len(dv_breakdown.intersections)):
        intersections = dv_breakdown.intersections[iint]
        for ielem in range(0,len(intersections.dv.fea_element_nos)):
            ielems = intersections.dv.fea_element_nos[ielem]
            elemlist[ielems].pid = local_dv_value #+ min(int(math.floor((elemlist[ielem].centroid[0] - fus_root_z)/section_span)),fus.l4.required_no_of_elements)
        for i in range(0,1):
            shell_name_lists[local_dv_value+i] = intersections.dv.tag[0]+ ":" + intersections.dv.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value += 1 #fus.l4.required_no_of_elements         
    
    
    for imisc in range(0,len(dv_breakdown.miscellaneous)):
        miscellaneous = dv_breakdown.miscellaneous[imisc]
        for ielem in range(0,len(miscellaneous.dv.fea_element_nos)):
            ielems = miscellaneous.dv.fea_element_nos[ielem]
            elemlist[ielems].pid = local_dv_value #+ min(int(math.floor((elemlist[ielem].centroid[0] - fus_root_z)/section_span)),fus.l4.required_no_of_elements)
        for i in range(0,1):
            shell_name_lists[local_dv_value+i] = miscellaneous.dv.tag[0]+ ":" + miscellaneous.dv.tag[1] + ":"+ str(i)+":"
            shell_element_lists_redone[local_dv_value+i].pid = local_dv_value+i
            shell_element_lists_redone[local_dv_value+i].t = 0.02
            shell_element_lists_redone[local_dv_value+i].t_min = 0.0016
            shell_element_lists_redone[local_dv_value+i].t_max = 0.03         
        local_dv_value += 1 #fus.l4.required_no_of_elements         
    
    
    
    



    no_of_shell_elements_new = local_dv_value #int(np.amax(element_map))  #dv_count+1

    #aircraft.structural_mesh_shell_map = element_map

    if(aircraft.shell_element_lists_redone_int == 0):
        aircraft.shell_element_lists_redone = shell_element_lists_redone


    #print no_of_shell_elements_new

#    for i in range(0,len(element_map)):
#        if (element_map[i]==0):
#            print i,element_map[i]



    #rename the old file to a new file,
    #os.rename(bdf_structural_meshfile, bdf_structural_meshfile+".old")


#---write a bdf file for geomach-------------------------------------------------------------------

    fo = open(bdf_structural_meshfile_new,"wb")
    #---------Executive_control_section----------------------------------------
    fo.write("$ Generated by ICEMCFD -  NASTRAN Interface Vers.  4.6.1 \n")
    fo.write("$ Nastran input deck \n")
    fo.write("SOL 103 \n")
    #fo.write("\n")
    
    fo.write("CEND \n")
    #fo.write("\n")
    fo.write("$\n")
    fo.write("BEGIN BULK \n")
        
    #write shell element data
    #------------writing element property data------
    for i in range(0, no_of_shell_elements_new):
        
        fo.write("$CDSCRPT");
        fo.write(str_form('        '));
        fo.write(str_form('        '));
        #fo.write(int_form(shell_element_list_new[i].pid));
        fo.write(int_form(i+1));
        #print int_form(shell_element_list_new[i].pid)
        fo.write(str_form('        '));
        fo.write(str_form(shell_name_lists[i]));
        #fo.write(str_form(shell_element_list_new[i].name));
        fo.write("\n");


    fo.write("$\n")
    fo.write("$       grid data              0  \n")


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
        fo.write(str_form('        '));
        fo.write(int_forms(pointlist[i].cd));
        
        #    fo.write(int_form(pointlist[i].ps));
        #    fo.write(int_form(pointlist[i].seid));
        fo.write("\n");


    #------------writing element data------
    #fo.write("$write element data\n")
    
    #--write to the grid points-

    for i in range(0,no_of_elements):
        
        fo.write(str_form(elemlist[i].type));
        fo.write(int_form(elemlist[i].eid));
        #fo.write(int_form(int(element_map[elemlist[i].pid-1])));
        fo.write(int_form(elemlist[i].pid+1));
        fo.write(int_form(elemlist[i].g[0]));
        fo.write(int_form(elemlist[i].g[1]));
        fo.write(int_form(elemlist[i].g[2]));
        
        if(elemlist[i].type=='CQUAD4'):
            fo.write(int_form(elemlist[i].g[3]));
    
    
        #        fo.write(int_form(global_to_loc_points[elemlist[i].g[0]]));
        #        fo.write(int_form(global_to_loc_points[elemlist[i].g[1]]));
        #        fo.write(int_form(global_to_loc_points[elemlist[i].g[2]]));
        
        #print elemlist[i].g[0],elemlist[i].g[1],elemlist[i].g[2]
        #print global_to_loc_points[elemlist[i].g[0]],elemlist[i].g[1],elemlist[i].g[2]
        
        
        fo.write("\n")



        #-----------------spc data------------
        #fo.write("$spc data\n")
    for i in range(0,no_of_constrained_grid_points):
        #        fo.write(str_form(constrained_grid_point_list[i].type));
        #        fo.write(int_form(constrained_grid_point_list[i].sid));
        #        #fo.write(int_form(constrained_grid_point_list[i].g[0]));
        #
        #        fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
        #        fo.write(int_form(constrained_grid_point_list[i].c1));
        #        fo.write(float_form(constrained_grid_point_list[i].d1));
        
        fo.write(str_form("SPC"));
        #fo.write(str_form('        '));
        #fo.write(format('         '));
        #fo.write(str_form(constrained_grid_point_list[i].type));
        fo.write(int_form(constrained_grid_point_list[i].sid));
        fo.write(int_form(constrained_grid_point_list[i].g1))
        fo.write(int_form(constrained_grid_point_list[i].c1));
        fo.write(float_form(0.0));
        
        #fo.write(float_form(constrained_grid_point_list[i].d1));
        
        
        fo.write("\n");

    fo.write("END BULK")

