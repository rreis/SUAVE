#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3


def read_nas_file(mesh_filename):


    no_of_dvs_scale = 1.0
    no_of_beams = 0
    scaling_factor = 1.0

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
    no_of_points = 0
    no_of_elements = 0

        
    for line in file:
        
        
        if (line[0:6]=='PSHELL'):
            no_of_materials = no_of_materials +1
#            start = line.find(' ')
#            end = line.find('\n')
#            no_of_elements= int(line[start:end])
#            #print no_of_elements
#            element_pres = 1
#            elemlist = [ CTRIA3() for i in range(no_of_elements)]


        if (line[0:5]=='GRID*'):
            no_of_points = no_of_points +1
            
            
        if (line[0:6]=='CTRIA3') or (line[0:6]=='CQUAD4'):
            no_of_elements = no_of_elements +1
                
                
                
    file.close()
    

    no_of_loc_materials = no_of_materials/no_of_dvs_scale
    rem_no =  no_of_materials % no_of_dvs_scale
    if (rem_no != 0 ):
        no_of_loc_materials = no_of_loc_materials+1
    
    no_of_materials = no_of_loc_materials
    

    print 'no of points ' , no_of_points
    print 'no of elements ' , no_of_elements
    print 'no of materials ' , no_of_materials
    
    pointlist = [ grid() for i in range(no_of_points)]
    elemlist = [ CTRIA3() for i in range(no_of_elements+no_of_beams)]
    
    point_count =0
    element_count =0
    
    file = open(mesh_filename, 'r')
    
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
            
            
#            if (pointlist[point_count].x1 <= 0.):#and(pointlist[point_count].x1 >= -0.5):
#                print pointlist[point_count].x1, pointlist[point_count].x2,pointlist[point_count].x3

            pointlist[point_count].cp = 0
            pointlist[point_count].cd = 0
            pointlist[point_count].in_stress_von_mises = 0.0
            pointlist[point_count].fin_stress_von_mises = 0.0
            pointlist[point_count].thickness = 0.0
            #print pointlist[point_count].x1,pointlist[point_count].x2,pointlist[point_count].x3
            
            
            
            
            point_count = point_count +1
                

        
        


        
        if (line[0:6]=='CTRIA3'):
            
            element_break= [int(s) for s in line.split() if s.isdigit()]
            
            elemlist[element_count].type='CTRIA3'
            elemlist[element_count].eid=element_count+1
            elemlist[element_count].g[0]=element_break[2]
            elemlist[element_count].g[1]=element_break[3]
            elemlist[element_count].g[2]=element_break[4]
            elemlist[element_count].theta=0.0
            elemlist[element_count].pid=element_break[1]
            elemlist[element_count].thickness = 0.0
            elemlist[element_count].fin_stress_von_mises = 0.0
            elemlist[element_count].in_stress_von_mises = 0.0
            
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



    
    file.close()

    return no_of_materials,no_of_points,no_of_elements,pointlist,elemlist

    











