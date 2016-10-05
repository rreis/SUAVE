#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3


def read_su2_meshfile(mesh_filename):


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


        
    for line in file:
        
        
        if (line[0:5]=='NELEM'):
            start = line.find(' ')
            end = line.find('\n')
            no_of_elements= int(line[start:end])
            #print no_of_elements
            element_pres = 1
            elemlist = [ CTRIA3() for i in range(no_of_elements)]
            
            
            
            for line in file:
                
                element_no= [int(s) for s in line.split() if s.isdigit()]
                #print element_no
                elemlist[count].type='CTRIA3'
                elemlist[count].eid=count+1
                elemlist[count].g1=element_no[1]+1
                elemlist[count].g2=element_no[2]+1
                elemlist[count].g3=element_no[3]+1
                elemlist[count].theta=0.0
                
                count = count +1
                if(count==no_of_elements):
                    break
        
        
        if (line[0:5]=='NPOIN'):
            start = line.find(' ')
            end = line.find('\n')
            no_of_points= int(line[start:end])
            #print no_of_points
            element_pres = 1
            pointlist = [ grid() for i in range(no_of_points)]
            
            max_glob_point=0
            
            for line in file:
                
                point_no= [float(s) for s in line.split() if s.isdigit()]
                point_no = re.findall(r'[\d\.\d]+', line)
                #print point_no
                pointlist[pcount].type='GRID'
                pointlist[pcount].id=pcount+1
                pointlist[pcount].x1=float(point_no[0])
                pointlist[pcount].x2=float(point_no[1])
                pointlist[pcount].x3=float(point_no[2])
                
                
                pointlist[pcount].cp=0
                pointlist[pcount].cd=0
                
                
                pcount = pcount +1
                if(pcount==no_of_points):
                    break


        
#    #----------each zone has a separate material-----
#    for line in file:
#        
#        #--------importing the wall boundary condition
#        
#        if (line[0:16]=='MARKER_TAG= Wall'):
#            
#            
#            count=0
#            
#            line_count=0
#            
#            for line in file:
#                if(line_count==0):
#                    element_no= [int(s) for s in line.split() if s.isdigit()]
#                    no_of_elements=element_no[0]
#                    elemlist = [ CTRIA3() for i in range(no_of_elements)]
#                    line_count=line_count+1
#                else:
#                    element_no= [int(s) for s in line.split() if s.isdigit()]
#                    print element_no
#                    elemlist[count].type='CTRIA3'
#                    elemlist[count].eid=count+1
#                    elemlist[count].g1=element_no[1]+1
#                    elemlist[count].g2=element_no[2]+1
#                    elemlist[count].g3=element_no[3]+1
#                    
#                    count = count +1
#                if(count==no_of_elements):
#                    break


    file.close()


    return elemlist,pointlist












