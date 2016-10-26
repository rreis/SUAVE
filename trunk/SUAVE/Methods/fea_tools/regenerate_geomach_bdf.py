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

def regenerate_geomach_bdf(bdf_structural_meshfile,bdf_structural_meshfile_new,aircraft):
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

    for i in range(0,len(shell_element_list)):
        name = shell_element_list[i].name
        name_s = name.split(':')
        current_element_id = shell_element_list[i].pid
        breakv = 0
        
        print name_s
        
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

            

            
            




    print "-------------------------------------------------------------------"
    print "-------------------------------------------------------------------"

    #mapping------------------------------
    dv_count = 0
    shell_name_lists  = [str() for i in range(no_of_shell_elements)]
    shell_element_lists_redone  = [PSHELL() for i in range(no_of_shell_elements)]
    #shell_name_lists_count = 0
    
    

    for wing in dv_breakdown.wings:
        
        print wing.upper.tag[0],wing.upper.element_nos, wing.upper.no_of_elements

        #upper
        wing.upper.required_no_of_elements = max(min(wing.upper.no_of_elements,wing.upper.required_no_of_elements),1)
        dv_split = math.ceil(wing.upper.no_of_elements/wing.upper.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,wing.upper.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(wing.upper.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                
                #shell_name_lists[int(dv_value)] = "lwing:upp:" + str(int(dv_value) + 1)+":"
            
                shell_name_lists[int(dv_value)] = wing.upper.tag[0]+ ":" + wing.upper.tag[1] + ":"+ str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03
            
            dv_count = dv_count + wing.upper.required_no_of_elements
        
        
        #lower
        wing.lower.required_no_of_elements = max(min(wing.lower.no_of_elements,wing.lower.required_no_of_elements),1)
        dv_split = math.ceil(wing.lower.no_of_elements/wing.lower.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,wing.lower.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(wing.lower.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                wing.lower.new_element_nos.append(int(dv_value) + 1)
                shell_name_lists[int(dv_value)] = wing.lower.tag[0]+ ":" + wing.lower.tag[1]+ ":" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03              
            dv_count = dv_count + wing.lower.required_no_of_elements


        #tip
        wing.tip.required_no_of_elements = max(min(wing.tip.no_of_elements,wing.tip.required_no_of_elements),1)
        dv_split = math.ceil(wing.tip.no_of_elements/wing.tip.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,wing.tip.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(wing.tip.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = wing.tip.tag[0]+":" + wing.tip.tag[1]+ ":" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.024                
            dv_count = dv_count + wing.tip.required_no_of_elements
        

        #spars
        wing.spars.required_no_of_elements = max(min(wing.spars.no_of_elements,wing.spars.required_no_of_elements),1)
        dv_split = math.ceil(wing.spars.no_of_elements/wing.spars.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,wing.spars.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(wing.spars.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = wing.spars.tag[0]+":" + wing.spars.tag[1]+ ":" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.005
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.006         
            dv_count = dv_count + wing.spars.required_no_of_elements
        

        #ribs
        wing.ribs.required_no_of_elements = max(min(wing.ribs.no_of_elements,wing.ribs.required_no_of_elements),1)
        dv_split = math.ceil(wing.ribs.no_of_elements/wing.ribs.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,wing.ribs.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(wing.ribs.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = wing.ribs.tag[0]+":" + wing.ribs.tag[1] + ":" +  str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.002
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.0024               
            dv_count = dv_count + wing.ribs.required_no_of_elements


#        #internal
#        dv_split = math.ceil(wing.internal.no_of_elements/wing.internal.required_no_of_elements )
#        for i in range(0,wing.internal.no_of_elements):
#        dv_value = dv_count + math.floor(i/dv_split)
#            element_map[int(wing.internal.element_nos[i])-1] = new_element_map[dv_value]
#        dv_count = dv_count + wing.internal.required_no_of_elements




    #loop over the fuselages
    for fuse in dv_breakdown.fuselages:
        
        
        #top
        fuse.top.required_no_of_elements = max(min(fuse.top.no_of_elements,fuse.top.required_no_of_elements),1)
        dv_split = math.ceil(fuse.top.no_of_elements/fuse.top.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.top.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.top.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse:top:" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03               
            dv_count = dv_count + fuse.top.required_no_of_elements
        

        #bottom
        fuse.bottom.required_no_of_elements = max(min(fuse.bottom.no_of_elements,fuse.bottom.required_no_of_elements),1)
        dv_split = math.ceil(fuse.bottom.no_of_elements/fuse.bottom.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.bottom.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.bottom.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse:bot:" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03               
            
            fuse.bottom.new_element_nos.append(int(dv_value) + 1)
            
            dv_count = dv_count + fuse.bottom.required_no_of_elements

        #left
        fuse.left.required_no_of_elements = max(min(fuse.left.no_of_elements,fuse.left.required_no_of_elements),1)
        dv_split = math.ceil(fuse.left.no_of_elements/fuse.left.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.left.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.left.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse:lft:" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03             
            dv_count = dv_count + fuse.left.required_no_of_elements
        

        #right
        fuse.right.required_no_of_elements = max(min(fuse.right.no_of_elements,fuse.right.required_no_of_elements),1)
        dv_split = math.ceil(fuse.right.no_of_elements/fuse.right.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.right.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.right.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse:rght:" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03             
            dv_count = dv_count + fuse.right.required_no_of_elements
        

        #front
        fuse.front.required_no_of_elements = max(min(fuse.front.no_of_elements,fuse.front.required_no_of_elements),1)
        dv_split = math.ceil(fuse.front.no_of_elements/fuse.front.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.front.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.front.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_f::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03         
            dv_count = dv_count + fuse.front.required_no_of_elements
        

        #rear
        fuse.rear.required_no_of_elements = max(min(fuse.rear.no_of_elements,fuse.rear.required_no_of_elements),1)
        dv_split = math.ceil(fuse.rear.no_of_elements/fuse.rear.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.rear.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.rear.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_r::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03            
            dv_count = dv_count + fuse.rear.required_no_of_elements


        #r1
        fuse.r1.required_no_of_elements = max(min(fuse.r1.no_of_elements,fuse.r1.required_no_of_elements),1)
        dv_split = math.ceil(fuse.r1.no_of_elements/fuse.r1.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.r1.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.r1.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_r1::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007               
            dv_count = dv_count + fuse.r1.required_no_of_elements
        
        #r2
        fuse.r2.required_no_of_elements = max(min(fuse.r2.no_of_elements,fuse.r2.required_no_of_elements),1)
        dv_split = math.ceil(fuse.r2.no_of_elements/fuse.r2.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.r2.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.r2.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_r2::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007               
            dv_count = dv_count + fuse.r2.required_no_of_elements
        

        #r3
        fuse.r3.required_no_of_elements = max(min(fuse.r3.no_of_elements,fuse.r3.required_no_of_elements),1)
        dv_split = math.ceil(fuse.r3.no_of_elements/fuse.r3.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.r3.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.r3.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_r3::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007               
            dv_count = dv_count + fuse.r3.required_no_of_elements
        
        
        #r4
        fuse.r4.required_no_of_elements = max(min(fuse.r4.no_of_elements,fuse.r4.required_no_of_elements),1)
        dv_split = math.ceil(fuse.r4.no_of_elements/fuse.r4.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.r4.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.r4.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_r4::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007          
            dv_count = dv_count + fuse.r4.required_no_of_elements
        

        #l1
        fuse.l1.required_no_of_elements = max(min(fuse.l1.no_of_elements,fuse.l1.required_no_of_elements),1)
        dv_split = math.ceil(fuse.l1.no_of_elements/fuse.l1.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.l1.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.l1.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_l1::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007             
            dv_count = dv_count + fuse.l1.required_no_of_elements
        

        #l2
        fuse.l2.required_no_of_elements = max(min(fuse.l2.no_of_elements,fuse.l2.required_no_of_elements),1)
        dv_split = math.ceil(fuse.l2.no_of_elements/fuse.l2.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.l2.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.l2.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_l2::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007              
            dv_count = dv_count + fuse.l2.required_no_of_elements
        

        #l3
        fuse.l3.required_no_of_elements = max(min(fuse.l3.no_of_elements,fuse.l3.required_no_of_elements),1)
        dv_split = math.ceil(fuse.l3.no_of_elements/fuse.l3.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.l3.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.l3.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_l3::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007               
            dv_count = dv_count + fuse.l3.required_no_of_elements
        

        #l4
        fuse.l4.required_no_of_elements = max(min(fuse.l4.no_of_elements,fuse.l4.required_no_of_elements),1)
        dv_split = math.ceil(fuse.l4.no_of_elements/fuse.l4.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,fuse.l4.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(fuse.l4.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "fuse_l4::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.007
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.007              
            dv_count = dv_count + fuse.l4.required_no_of_elements
        

    


    #loop over the intersections
    for intersection in dv_breakdown.intersections:
        
        #top
        intersection.dv.required_no_of_elements = max(min(intersection.dv.no_of_elements,intersection.dv.required_no_of_elements),1)
        dv_split = math.ceil(intersection.dv.no_of_elements/intersection.dv.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,intersection.dv.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(intersection.dv.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "intersection::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03               
            dv_count = dv_count + intersection.dv.required_no_of_elements
        


    #loop over the miscellaneous
    for misc in dv_breakdown.miscellaneous:
        
        #top
        misc.dv.required_no_of_elements = max(min(misc.dv.no_of_elements,misc.dv.required_no_of_elements),1)
        dv_split = math.ceil(misc.dv.no_of_elements/misc.dv.required_no_of_elements )
        if(dv_split>0):
            for i in range(0,misc.dv.no_of_elements):
                dv_value = dv_count + math.floor(i/dv_split)
                element_map[int(misc.dv.element_nos[i])-1] = int(dv_value) + 1  #new_element_map[dv_value]
                shell_name_lists[int(dv_value)] = "miscellaneous::" + str(int(dv_value) + 1)+":"
                shell_element_lists_redone[int(dv_value)].pid = int(dv_value)
                shell_element_lists_redone[int(dv_value)].t = 0.02
                shell_element_lists_redone[int(dv_value)].t_min = 0.0016
                shell_element_lists_redone[int(dv_value)].t_max = 0.03             
            dv_count = dv_count + misc.dv.required_no_of_elements
        


    no_of_shell_elements_new = int(np.amax(element_map))  #dv_count+1

    aircraft.structural_mesh_shell_map = element_map

    if(aircraft.shell_element_lists_redone_int == 0):
        aircraft.shell_element_lists_redone = shell_element_lists_redone


    print no_of_shell_elements_new

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
        fo.write(int_form(int(element_map[elemlist[i].pid-1])));
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

