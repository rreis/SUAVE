#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3

def read_s101_f06_file(filename,pointlist,elemlist):

    no_of_elements = len(elemlist)
    no_of_points = len(pointlist)

    file = open(filename,"r")
    
    displacement_count=0
    point_count=1
    point_no = 1
    element_count=0
    for line in file:
        if (line[45:82]=='D I S P L A C E M E N T   V E C T O R'):
            displacement_count=displacement_count+1
            #print line



            skip_count=0
            for i in range(0,2):
                for line in file:
                    skip_count=skip_count+1
                    break
                
            for j in range(0,no_of_points):


                if((j)%50==0)and(j!=0):
                    for k in range(0,7):
                        for line in file:
                            #print line
                            temp_count=0
                            break
                for line in file:
                    #print line
                    point_no = int(line[0:14])
                    disp1 = float(line[25:40])
                    disp2 = float(line[41:55])
                    disp3 = float(line[56:71])
                    rot1  = float(line[71:86])
                    rot2  = float(line[86:101])
                    rot3  = float(line[101:114])
                    point_count = point_count+1
                    #print j+1
                    
                    pointlist[point_no-1].t1=disp1
                    pointlist[point_no-1].t2=disp2
                    pointlist[point_no-1].t3=disp3
                    
                    pointlist[point_no-1].rot1=rot1
                    pointlist[point_no-1].rot2=rot2
                    pointlist[point_no-1].rot3=rot3
                    
#                                            pointlist[point_no-1].r1=in_rot1
#                                            pointlist[point_no-1].r2=in_rot2
#                                            pointlist[point_no-1].r3=in_rot3

                    break




            break


    for line in file:
        print line
        if (line[25:40]=='S T R E S S E S'):  #27:42
            
            
            displacement_count=displacement_count+1
            #print line
                
                
                
            skip_count=0
            for i in range(0,2):
                for line in file:
                    skip_count=skip_count+1
                    break
                                    
            for j in range(0,no_of_elements):
                                        
                                        
                if((j)%16==0)and(j!=0):
                    for k in range(0,7):
                        for line in file:
                            #print line
                            temp_count=0
                            break
                for line in file:
                    #print line
                    element_no = int(line[1:9])
                    stress_x = float(line[30:43])
                    stress_y = float(line[44:58])
                    stress_xy = float(line[59:73])
                    angle = float(line[76:84])
                    stress_major = float(line[87:100])
                    stress_minor = float(line[102:116])
                    stress_von_mises = float(line[118:131])
                    element_count = element_count+1
                    #print 'element_no-1',element_no-1
                    #print elemlist[element_no-1].eid
                    for line in file:
                        break
                    elemlist[element_no-1].in_stress_x=stress_x
                    elemlist[element_no-1].in_stress_y=stress_y
                    elemlist[element_no-1].in_stress_xy=stress_xy
                    elemlist[element_no-1].in_angle=angle
                    elemlist[element_no-1].in_stress_major=stress_major
                    elemlist[element_no-1].in_stress_minor=stress_minor
                    elemlist[element_no-1].in_stress_von_mises=stress_von_mises
                    
                    break




                                                                                                
                                                                                                


#                                    break
#                                
#                                
#                            for line in file:
        if (line[27:42]=='S T R E S S E S'):  #25:40
            
            #print 'Helloooooo'
            displacement_count=displacement_count+1
            #print line
                
                
                
            skip_count=0
            for i in range(0,2):
                for line in file:
                    skip_count=skip_count+1
                    break
                                    
            for j in range(0,no_of_elements):
                                        
                                        
                if((j)%16==0)and(j!=0):
                    for k in range(0,7):
                        for line in file:
                            #print line
                            temp_count=0
                            break
                for line in file:
                    #print line
                    element_no = int(line[1:9])
                    stress_x = float(line[30:43])
                    stress_y = float(line[44:58])
                    stress_xy = float(line[59:73])
                    angle = float(line[76:84])
                    stress_major = float(line[87:100])
                    stress_minor = float(line[102:116])
                    stress_von_mises = float(line[118:131])
                    element_count = element_count+1
                    #print 'element_no-1',element_no-1
                    #print elemlist[element_no-1].eid
                    for line in file:
                        break
                    elemlist[element_no-1].in_stress_x=stress_x
                    elemlist[element_no-1].in_stress_y=stress_y
                    elemlist[element_no-1].in_stress_xy=stress_xy
                    elemlist[element_no-1].in_angle=angle
                    elemlist[element_no-1].in_stress_major=stress_major
                    elemlist[element_no-1].in_stress_minor=stress_minor
                    elemlist[element_no-1].in_stress_von_mises=stress_von_mises
                    
                    break
    
        


    file.close()
