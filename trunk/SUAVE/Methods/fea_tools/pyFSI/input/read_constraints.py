#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from pyFSI.class_str.grid.class_structure import grid



def read_constraints(conn_filename,pointlistg,no_of_pointsg,scaling_factor):
    
    
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
    
    
    
    file = open(conn_filename, 'r')
    
    for line in file:
        
        
        loc_no_points =int(line)
        no_of_points = loc_no_points + no_of_points
        for i in range(0,loc_no_points):
            
            for line in file:
                break
        
    file.close()
        
    pointlist = [ grid() for i in range(no_of_points)]
    
    
    
    
    
    file = open(conn_filename, 'r')
    point_count = 0
    
    for line in file:
        
        
        loc_no_points =int(line)
        #no_of_points = loc_no_points + no_of_points
        for i in range(0,loc_no_points):
            
            for line in file:
                
                pointlist[point_count].type = 'GRID'
                pointlist[point_count].id = point_count + 1
                pointlist[point_count].x1 = float(line[2:23])*scaling_factor
                pointlist[point_count].x2 = float(line[25:47])*scaling_factor
                pointlist[point_count].x3 = float(line[49:71])*scaling_factor
                point_count = point_count + 1
                break
                    
    file.close()
        
                    
                    
                    
    #-------------------getting the constraint grid point numbers----------
    
    no_of_constrained_grid_points = no_of_points
    
    constrained_grid_points = [ int() for i in range(no_of_constrained_grid_points)]
    
    
    for i in range(0,no_of_points):
        
        min_d= (pointlist[i].x1-pointlistg[0].x1)**2 + (pointlist[i].x2-pointlistg[0].x2)**2 + (pointlist[i].x3-pointlistg[0].x3)**2
        
        min_point = 0
        
        for j in range(1,no_of_pointsg):
            
            d= (pointlist[i].x1-pointlistg[j].x1)**2 + (pointlist[i].x2-pointlistg[j].x2)**2 + (pointlist[i].x3-pointlistg[j].x3)**2
            
            
            if(d<min_d):
                min_d =d
                min_point = j
        
        constrained_grid_points[i] = pointlistg[min_point].id
    
    print constrained_grid_points
    
    return no_of_constrained_grid_points,constrained_grid_points









