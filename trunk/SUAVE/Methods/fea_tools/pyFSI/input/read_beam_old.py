#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CBAR
import numpy


def read_beam(conn_filename,pointlistg,no_of_pointsg,scaling_factor,no_of_elements,,no_of_materials):
    
    
    max_glob_point=0;
    
    element_count=0
    element_pres =0
    count=0
    pcount=0
    no_of_beam_elements = 0
    no_of_points=0
    elemlist =[]
    
    
    
    #----------each zone has a separate material-----
    
    no_of_materials = 0
    no_of_points = 0
    no_of_elements = 0
    no_of_beams = 0
    
    
    
    file = open(conn_filename, 'r')
    
    for line in file:
        
        no_of_beams = no_of_beams + 1
        loc_no_points =int(line)
        no_of_points = loc_no_points + no_of_points
        for i in range(0,loc_no_points):
            
            for line in file:
                break
        
    file.close()
        
    pointlist = [ grid() for i in range(no_of_points)]
    beam_start = [grid() for i in range(no_of_beams)]
    beam_end  = [grid() for i in range(no_of_beams)]
    
    beam_startl = [int() for i in range(no_of_beams)]
    beam_endl  = [int() for i in range(no_of_beams)]
    
    
    file = open(conn_filename, 'r')
    point_count = 0
    local_pcount = 0
    beam_count = 0

    
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
                
                if(local_pcount==loc_no_points-1):

                    beam_end[beam_count].x1 = pointlist[point_count].x1
                    beam_end[beam_count].x2 = pointlist[point_count].x2
                    beam_end[beam_count].x3 = pointlist[point_count].x3

                
                point_count = point_count + 1
                local_pcount = local_pcount + 1
                break

        print beam_start[beam_count].x1, beam_end[beam_count].x1
        beam_count=beam_count+1
        
                    
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





    for i in range(0,no_of_beams):
        print beam_startl[i],beam_endl[i]




    beamlist = [ CBAR() for i in range(no_of_beams)]

    for i in range(0,no_of_beams):
        beamlist[i].eid=no_of_elements+i
        beamlist[i].pid=0
        beamlist[i].ga=beam_startl[i]
        beamlist[i].gb=beam_endl[i]
        beamlist[i].x1 = 0.0
        beamlist[i].x2 = 1.0
        beamlist[i].x3 = 0.0




    return no_of_beams,beamlist









