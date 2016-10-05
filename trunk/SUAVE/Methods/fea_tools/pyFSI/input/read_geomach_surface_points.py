#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
#-----------
#---function to convert integers to required nastran format

def read_geomach_surface_points(load_filename):

    no_of_points=0
        #print load_filename
        
    file2 = open(load_filename, 'r')
    
    #skip 3 lines
    
    
    for line in file2:
        no_of_points=no_of_points+1
    
    file2.close()
    
    no_of_points=no_of_points-1-2
    
    pointlist = [ grid() for i in range(no_of_points)]
    

    
    file2 = open(load_filename, 'r')
    count = 0
    pcount = 0
    #----------each zone has a separate material-----
    for line in file2:
        count=count+1;
        if(count>3):
            #point_no= [float(s) for s in line.split() if s.isdigit()]
            
            
            point_no = line.split(' ')
            
            if(point_no[0]!='zone'):
            
                pointlist[pcount].type='GRID'
                
                pointlist[pcount].id=pcount+1 #int(point_no[0])
                # pointlist[pcount].id=pointlist[pcount].id+1
                pointlist[pcount].x[0]=float(point_no[0])
                pointlist[pcount].x[1]=float(point_no[1])
                pointlist[pcount].x[2]=float(point_no[2])
                
                pointlist[pcount].cp=0
                pointlist[pcount].cd=0
            

		
            
            
                pcount=pcount+1
    
    

    file2.close()





    return pointlist[0:pcount]









