#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3


def read_nas_file(conn_filename):


    max_glob_point=0;
    file = open(conn_filename, 'r')
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

        
    for line in file:
      
      
        loc_no_points =int(line)
        for i in range(0,loc_no_points):

          for line in file:

            point = 2
            break
        
        
        
        
        
        
        
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
            
            
        if (line[0:6]=='CTRIA3'):
            no_of_elements = no_of_elements +1
                
                
                
    file.close()
    
    
    print 'no of points ' , no_of_points
    print 'no of elements ' , no_of_elements
    print 'no of materials ' , no_of_materials
    
    pointlist = [ grid() for i in range(no_of_points)]
    elemlist = [ CTRIA3() for i in range(no_of_elements)]
    
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

            point_1 = float(line[41:56])
            point_2 = float(line[57:72])

#            point_1 = line[41:56]
#            point_2 = line[57:72]

            for line in file:
                point_3 = float(line[9:24])
#                point_3 = line[9:24]
                break


            pointlist[point_count].type = 'GRID'
            pointlist[point_count].id = point_count + 1
            pointlist[point_count].x1 = point_1
            pointlist[point_count].x2 = point_2
            pointlist[point_count].x3 = point_3
            
            pointlist[point_count].cp = 0
            pointlist[point_count].cd = 0
            
            #print pointlist[point_count].x1,pointlist[point_count].x2,pointlist[point_count].x3
            
            
            
            
            point_count = point_count +1
                

        
        


        
        if (line[0:6]=='CTRIA3'):
            
            element_break= [int(s) for s in line.split() if s.isdigit()]
            
            elemlist[element_count].type='CTRIA3'
            elemlist[element_count].eid=element_count+1
            elemlist[element_count].g1=element_break[2]
            elemlist[element_count].g2=element_break[3]
            elemlist[element_count].g3=element_break[4]
            elemlist[element_count].theta=0.0
            elemlist[element_count].pid=element_break[1]
            
            element_count = element_count +1





    
    file.close()
    
    return no_of_materials,no_of_points,no_of_elements,pointlist,elemlist

    
    
    
    
    
    
    
            



#            for line in file:
#                
#                element_no= [int(s) for s in line.split() if s.isdigit()]
#                #print element_no
#                elemlist[count].type='CTRIA3'
#                elemlist[count].eid=count+1
#                elemlist[count].g1=element_no[1]+1
#                elemlist[count].g2=element_no[2]+1
#                elemlist[count].g3=element_no[3]+1
#                elemlist[count].theta=0.0
#                
#                count = count +1
#                if(count==no_of_elements):
#                    break
#        
#        
#        if (line[0:5]=='NPOIN'):
#            start = line.find(' ')
#            end = line.find('\n')
#            no_of_points= int(line[start:end])
#            #print no_of_points
#            element_pres = 1
#            pointlist = [ grid() for i in range(no_of_points)]
#            
#            max_glob_point=0
#            
#            for line in file:
#                
#                point_no= [float(s) for s in line.split() if s.isdigit()]
#                point_no = re.findall(r'[\d\.\d]+', line)
#                #print point_no
#                pointlist[pcount].type='GRID'
#                pointlist[pcount].id=pcount+1
#                pointlist[pcount].x1=float(point_no[0])
#                pointlist[pcount].x2=float(point_no[1])
#                pointlist[pcount].x3=float(point_no[2])
#                
#                
#                pointlist[pcount].cp=0
#                pointlist[pcount].cd=0
#                
#                
#                pcount = pcount +1
#                if(pcount==no_of_points):
#                    break




    file.close()


    print 'no of points ' , no_of_points
    print 'no of elements ' , no_of_elements
    print 'no of materials ' , no_of_materials


#return elemlist












