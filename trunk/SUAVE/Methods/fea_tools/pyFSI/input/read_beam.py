#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CBAR
import numpy


def read_beam(conn_filename,pointlistg,no_of_pointsg,scaling_factor,no_of_elements,no_of_materials):
    
    
    max_glob_point=0;
    
    element_count=0
    element_pres =0
    count=0
    pcount=0
    no_of_beam_elements = 0
    no_of_points=0
    elemlist =[]
    
    
    
    #----------each zone has a separate material-----
    
    # no_of_materials = 0
    no_of_points = 0
    #no_of_elements = 0
    no_of_beams = 0
    no_of_beam_materials = 0
    
    
    
    file = open(conn_filename, 'r')
    
    for line in file:
        
        no_of_beam_materials = no_of_beam_materials + 1
        loc_no_points =int(line)
        no_of_beams = no_of_beams + loc_no_points-1
        no_of_points = loc_no_points + no_of_points
        for i in range(0,loc_no_points):
            
            for line in file:
                break
        
    file.close()
    
    print 'no_of_beams' , no_of_beams
    print 'no_of_points' , no_of_points
    print 'no_of_beam materials' , no_of_beam_materials
        
    pointlist = [ grid() for i in range(no_of_points)]
    beam_start = [grid() for i in range(no_of_beams)]
    beam_end  = [grid() for i in range(no_of_beams)]

    
    beam_startl = [int() for i in range(no_of_beams)]
    beam_endl  = [int() for i in range(no_of_beams)]
    beam_material = [int() for i in range(no_of_beams)]
    
    
    file = open(conn_filename, 'r')
    point_count = 0
    local_pcount = 0
    beam_count = 0
    material_count = 0

    
    for line in file:
        
        local_pcount = 0
        loc_no_points =int(line)
        #no_of_points = loc_no_points + no_of_points
        for i in range(0,loc_no_points):
            
            for line in file:
                
                pointlist[point_count].type = 'GRID'
                pointlist[point_count].id = point_count + 1
                pointlist[point_count].x1 = float(line[2:23])*scaling_factor
                pointlist[point_count].x2 = float(line[25:47])*scaling_factor
                pointlist[point_count].x3 = float(line[49:71])*scaling_factor
                

                
                if(local_pcount==0):
                    
                    beam_start[beam_count].x1 = pointlist[point_count].x1
                    beam_start[beam_count].x2 = pointlist[point_count].x2
                    beam_start[beam_count].x3 = pointlist[point_count].x3
                    beam_material[beam_count] = material_count
                    beam_count = beam_count+1
                
                if(local_pcount==loc_no_points-1):

                    beam_end[beam_count-1].x1 = pointlist[point_count].x1
                    beam_end[beam_count-1].x2 = pointlist[point_count].x2
                    beam_end[beam_count-1].x3 = pointlist[point_count].x3
                
                if((local_pcount!=0)and(local_pcount!=loc_no_points-1)):
                    beam_start[beam_count].x1 = pointlist[point_count].x1
                    beam_start[beam_count].x2 = pointlist[point_count].x2
                    beam_start[beam_count].x3 = pointlist[point_count].x3
                    beam_material[beam_count] = material_count
                
                    beam_end[beam_count-1].x1 = pointlist[point_count].x1
                    beam_end[beam_count-1].x2 = pointlist[point_count].x2
                    beam_end[beam_count-1].x3 = pointlist[point_count].x3
                    beam_count = beam_count+1
                


                point_count = point_count + 1
                local_pcount = local_pcount + 1
                print beam_count
                
                
                break

#print beam_start[beam_count].x1, beam_end[beam_count].x1
#beam_count=beam_count+1
        material_count= material_count+1
        
                    
    file.close()
        
                    
                    
                    
    #-------------------getting the constraint grid point numbers----------

    print "\n"

    no_of_constrained_grid_points = no_of_points
    
    constrained_grid_points = [ int() for i in range(no_of_constrained_grid_points)]
    
    
    for i in range(0,no_of_beams):
        
        min_d= (beam_start[i].x1-pointlistg[0].x1)**2 + (beam_start[i].x2-pointlistg[0].x2)**2 + (beam_start[i].x3-pointlistg[0].x3)**2

        
        
        for j in range(0,no_of_pointsg):
            
            d= (beam_start[i].x1-pointlistg[j].x1)**2 + (beam_start[i].x2-pointlistg[j].x2)**2 + (beam_start[i].x3-pointlistg[j].x3)**2
            
            
        
            

            
            if(d<min_d):
                min_d =d
                min_point = j

        beam_startl[i] = pointlistg[min_point].id



#---------end value-------------------------------

    for i in range(0,no_of_beams):
        
        min_d= (beam_end[i].x1-pointlistg[0].x1)**2 + (beam_end[i].x2-pointlistg[0].x2)**2 + (beam_end[i].x3-pointlistg[0].x3)**2
        
        
        
        for j in range(1,no_of_pointsg):
            
            d= (beam_end[i].x1-pointlistg[j].x1)**2 + (beam_end[i].x2-pointlistg[j].x2)**2 + (beam_end[i].x3-pointlistg[j].x3)**2
            
            
            
            
            
            
            if(d<min_d):
                min_d =d
                min_point = j
        
        beam_endl[i] = pointlistg[min_point].id





#    for i in range(0,no_of_beams):
#        print beam_startl[i],beam_endl[i]


    redundant_beams = 0
    local_beam_count =0

    beamlist = [ CBAR() for i in range(no_of_beams)]

    for i in range(0,no_of_beams):
        
        if(beam_startl[i]!=beam_endl[i]):
           
  
            beamlist[local_beam_count].type='CBAR'
            beamlist[local_beam_count].eid=no_of_elements+local_beam_count+1
            beamlist[local_beam_count].pid=no_of_materials + beam_material[i]+1
            beamlist[local_beam_count].ga=beam_startl[i]
            beamlist[local_beam_count].gb=beam_endl[i]
            beamlist[local_beam_count].x1 = 0.0
            beamlist[local_beam_count].x2 = 1.0
            beamlist[local_beam_count].x3 = 0.0
            local_beam_count = local_beam_count +1
           
        else:
           redundant_beams = redundant_beams+1

    no_of_beams = no_of_beams - redundant_beams

#    no_of_materials = no_of_materials + no_of_beams



#----------reducing the number of beams by  a factor 10
    no_of_loc_beam_materials = no_of_beam_materials/10
    rem_no =  no_of_beam_materials % 10
    if (rem_no != 0 ):
        no_of_loc_beam_materials = no_of_loc_beam_materials+1

    no_of_beam_materials = no_of_loc_beam_materials




    for i in range(0,no_of_beams):
    
        local_pid = beamlist[i].pid
        #        if(local_pid % 10 == 0):
        material_no = no_of_materials + beam_material[i]/10 +1
        beamlist[i].pid=material_no


    print no_of_beam_materials

    return no_of_beams,beamlist,no_of_beam_materials









