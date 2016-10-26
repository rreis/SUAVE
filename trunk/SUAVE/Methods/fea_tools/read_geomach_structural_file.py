# read_geomach_structural_file.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#Read a geomach bdf file

from class_structure import grid
from class_structure import CTRIA3
from pyFSI.class_str.material.class_structure import PSHELL
from pyFSI.class_str.material.class_structure import MAT1
from pyFSI.class_str.load_disp_bc.class_structure import SPC

#--imports---
import re
import numpy




def read_geomach_structural_file(mesh_filename,scaling_factor):
    
    
    max_glob_point=0;
    file = open(mesh_filename, 'r')
    element_count=0
    element_pres =0
    count=0
    pcount=0
    no_of_elements = 0
    no_of_points=0
    elemlist =[]
    


    #----------each zone has a separate material-----

    no_of_materials = 0
    no_of_shell_elements = 0
    no_of_points = 0
    no_of_elements = 0
    no_of_constraint_points = 0

        
    for line in file:
        
        
        if (line[0:8]=='$CDSCRPT'):
            no_of_shell_elements = no_of_shell_elements +1
#            start = line.find(' ')
#            end = line.find('\n')
#            no_of_elements= int(line[start:end])
#            #print no_of_elements
#            element_pres = 1
#            elemlist = [ CTRIA3() for i in range(no_of_elements)]


        if (line[0:5]=='GRID*'):
            no_of_points = no_of_points +1
            
            
        if (line[0:6]=='CTRIA3')or(line[0:6]=='CQUAD4'):
            no_of_elements = no_of_elements +1

        if (line[0:3]=='SPC'):
            no_of_constraint_points = no_of_constraint_points +1

        if (line[0:4]=='MAT1'):
            no_of_materials = no_of_materials +1
    
    
                
    file.close()


    if(no_of_materials==0):
        no_of_materials = 1;


#    no_of_loc_materials = no_of_materials/10
#    rem_no =  no_of_materials % 10
#    if (rem_no != 0 ):
#        no_of_loc_materials = no_of_loc_materials+1
#    
#    no_of_materials = no_of_loc_materials



    
    pointlist = [ grid() for i in range(no_of_points)]
    elemlist = [ CTRIA3() for i in range(no_of_elements)]
    material_list = [ MAT1() for i in range(no_of_materials)]
    shell_element_list = [ PSHELL() for i in range(no_of_shell_elements)]
    constrained_grid_point_list = [ SPC() for i in range(no_of_constraint_points)]
    

    
    file = open(mesh_filename, 'r')
    point_count = 0
    element_count=0
    material_count=0
    shell_count =0
    constraint_count=0
    
    
    for line in file:
        
        
#        if (line[0:6]=='PSHELL'):
#            no_of_materials = no_of_materials +1
#        #            start = line.find(' ')
#        #            end = line.find('\n')
#        #            no_of_elements= int(line[start:end])
#        #            #print no_of_elements
#        #            element_pres = 1
#        #            elemlist = [ CTRIA3() for i in range(no_of_elements)]

        
        if (line[0:5]=='GRID*'):

            point_1 = float(line[40:56])
            point_2 = float(line[56:72])

#            point_1 = line[41:56]
#            point_2 = line[57:72]

            for line in file:
                point_3 = float(line[8:24])
#                point_3 = line[9:24]
                break


            pointlist[point_count].type = 'GRID'
            pointlist[point_count].id = point_count + 1
            pointlist[point_count].x[0] = point_1*scaling_factor
            pointlist[point_count].x[1] = point_2*scaling_factor
            pointlist[point_count].x[2] = point_3*scaling_factor
            pointlist[point_count].t[0] = 0.0
            pointlist[point_count].t[1] = 0.0
            pointlist[point_count].t[2] = 0.0
            pointlist[point_count].thickness =0.0
            pointlist[point_count].in_stress_von_mises = 0.0
            pointlist[point_count].fin_stress_von_mises = 0.0
            
#            if (pointlist[point_count].x1 <= 0.):#and(pointlist[point_count].x1 >= -0.5):
#                print pointlist[point_count].x1, pointlist[point_count].x2,pointlist[point_count].x3

            pointlist[point_count].cp = 0
            pointlist[point_count].cd = 0
            
            #print pointlist[point_count].x1,pointlist[point_count].x2,pointlist[point_count].x3
            
            
            
            
            point_count = point_count +1
                

        
        


        
        if (line[0:6]=='CTRIA3'):
            
            element_break= [int(s) for s in line.split() if s.isdigit()]
            
            elemlist[element_count].type='CTRIA3'
            elemlist[element_count].eid=element_count+1 #element_break[0] #element_count+1
            elemlist[element_count].g[0]=element_break[2]
            elemlist[element_count].g[1]=element_break[3]
            elemlist[element_count].g[2]=element_break[4]
            elemlist[element_count].theta=0.0
            elemlist[element_count].pid=element_break[1]
            elemlist[element_count].thickness = 0.0
            
            element_count = element_count +1



        if (line[0:6]=='CQUAD4'):
    
            element_break= [int(s) for s in line.split() if s.isdigit()]
        
            elemlist[element_count].type='CQUAD4'
            elemlist[element_count].eid=element_count+1 #element_break[0]
            elemlist[element_count].g[0]=element_break[2]
            elemlist[element_count].g[1]=element_break[3]
            elemlist[element_count].g[2]=element_break[4]
            elemlist[element_count].g[3]=element_break[5]
            elemlist[element_count].theta=0.0
            elemlist[element_count].pid=element_break[1]
            elemlist[element_count].thickness = 0.0
            
            element_count = element_count +1



        if (line[0:4]=='MAT1'):
    
        
            material_list[material_count].type='MAT1'
            material_list[material_count].mid=material_count+1
            material_list[material_count].e=line[14:24]
            material_list[material_count].nu=element_break[31:40]
            material_list[material_count].rho=element_break[41:48]

            
            material_count = material_count +1


        if (line[0:8]=='$CDSCRPT'):
    
    
            shell_element_list[shell_count].type='PSHELL'
            shell_element_list[shell_count].pid=shell_count+1
#            material_list[element_count].mid1=line[14:24]
#            material_list[element_count].t=element_break[31:40]
#            material_list[element_count].rho=element_break[41:48]

            
            shell_count = shell_count +1



        if (line[0:3]=='SPC'):
    
    
            constrained_grid_point_list[constraint_count].type='SPC1'
            constrained_grid_point_list[constraint_count].sid=int(line[9:16])
            constrained_grid_point_list[constraint_count].g1=int(line[17:24])
            constrained_grid_point_list[constraint_count].c1=int(line[25:32])
            constrained_grid_point_list[constraint_count].d1=float(line[33:40])
            

            
            
            constraint_count = constraint_count +1




    file.close()





    print 'no of points ' , no_of_points
    print 'no of elements ' , no_of_elements



#return elemlist

    return elemlist,pointlist,no_of_points,no_of_elements,constrained_grid_point_list,shell_element_list










