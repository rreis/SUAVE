#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format

def read_msh_meshfile(load_filename):

    no_of_points=0
        #print load_filename
        
    file2 = open(load_filename, 'r')
    
    for line in file2:
        no_of_points=no_of_points+1
    
    file2.close()
    
    no_of_points=no_of_points-1
    
    pointlist = [ grid() for i in range(no_of_points)]
    
    local_to_glob_points = [ int for i in range(no_of_points)]
    
    no_of_grid_points_w_load=no_of_points
    coord_system=0
    load_list = [ FORCE() for i in range(no_of_points)]
    pcount=0
    fcount=0
    count=0
    max_glob_point=0
    
    file2 = open(load_filename, 'r')
    
    #----------each zone has a separate material-----
    for line in file2:
        count=count+1;
        if(count>1):
            #point_no= [float(s) for s in line.split() if s.isdigit()]
            
            
            point_no = line.split(',')
            
            pointlist[pcount].type='GRID'
            
            local_to_glob_points[pcount]=int(point_no[0])+1
            pointlist[pcount].global_to_loc =int(point_no[0])+1
            if(int(point_no[0])>max_glob_point):
                max_glob_point=int(point_no[0])
            pointlist[pcount].id=pcount+1 #int(point_no[0])
            # pointlist[pcount].id=pointlist[pcount].id+1
            pointlist[pcount].x1=float(point_no[1])
            pointlist[pcount].x2=float(point_no[2])
            pointlist[pcount].x3=float(point_no[3])
            
            pointlist[pcount].cp=0
            pointlist[pcount].cd=0
            
            
            
            #            if((pointlist[pcount].id != constrained_grid_points[0]) and (pointlist[pcount].id != constrained_grid_points[1]) and (pointlist[pcount].id != constrained_grid_points[2]) and (pointlist[pcount].id != constrained_grid_points[3])):
            load_list[fcount].type='FORCE'
            load_list[fcount].sid=1
            load_list[fcount].g=pointlist[pcount].id
            load_list[fcount].cid=coord_system
            load_list[fcount].f=float(point_no[4])
            load_list[fcount].n1=1.0
            load_list[fcount].n2=0.0
            load_list[fcount].n3=0.0
            
            fcount=fcount+1
            
            
            pcount=pcount+1
    
    
    file2.close()




    max_glob_point = max_glob_point+1
    print max_glob_point

    global_to_loc_points = [ int for i in range(max_glob_point+1)]

    for i in range(0,no_of_points):
        
        global_to_loc_points[local_to_glob_points[i]]=i+1
        print


    return no_of_points,pointlist,load_list,global_to_local_points,local_to_global_points









