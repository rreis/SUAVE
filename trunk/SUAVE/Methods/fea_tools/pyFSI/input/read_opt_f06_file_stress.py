#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3
import re

def read_opt_f06_file_stress(opt_filename,no_of_design_variables,elemlist,no_of_elements,no_of_points,pointlist,no_of_beams,no_of_max_design_iters):
#def read_opt_f06_file_stress(opt_filename):

    max_glob_point=0;
    file = open(opt_filename, "r")
    element_count=0
    element_pres =0
    count=0
    point_count=1
#    no_of_elements = 42505
#    no_of_points=20380
    design_var_value1=[]
    design_var_value2=[]
    #no_of_max_design_iters = 14

    #[39:87]
    for line in file:
        count =0

#if ('E L E M E N T   G E O M E T R Y   T E S T   R E S U L T S   S U M M A R Y' in line):
            
        for line in file:
            if ('STATIC   ANALYSIS INITIATED.  DESIGN CYCLE NUMBER=' in line):
                print line
                line_val = [int(s) for s in line.split() if s.isdigit()]

                design_iter_no = int(line_val[0])
                #print design_iter_no,no_of_max_design_iters
                if (design_iter_no==1):
                    displacement_count=0
                    point_count=1
                    point_no=1
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
                                    point_count = point_count+1
                                    #print j+1
                                    
                                    pointlist[point_no-1].t1=disp1
                                    pointlist[point_no-1].t2=disp2
                                    pointlist[point_no-1].t3=disp3
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
        
        
        
        
                                                                                                                
                                                                                                                


                            break

            
            #--------extract the initial displacement and stress arrays
                    #count = 0
                    
                    #break
                   
                if (design_iter_no== no_of_max_design_iters):
                    displacement_count=0
                    point_count=1
                    point_no=1
                    
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
                                    point_count = point_count+1
                                    #print j+1
                                    
                                    pointlist[point_no-1].t1=disp1
                                    pointlist[point_no-1].t2=disp2
                                    pointlist[point_no-1].t3=disp3
#                                            pointlist[point_no-1].r1=fin_rot1
#                                            pointlist[point_no-1].r2=fin_rot2
#                                            pointlist[point_no-1].r3=fin_rot3
                                    break





                            break
                                
                    for line in file:
                        if (line[25:40]=='S T R E S S E S'):  #[27:42]
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
                                    print line
                                    element_no = int(line[1:9])
                                    stress_x = float(line[30:43])
                                    stress_y = float(line[44:58])
                                    stress_xy = float(line[59:73])
                                    angle = float(line[76:84])
                                    stress_major = float(line[87:100])
                                    stress_minor = float(line[102:116])
                                    stress_von_mises = float(line[118:131])
                                    element_count = element_count+1
                                    #print j+1
                                    for line in file:
                                        break
                                    
                                    
                                    elemlist[element_no-1].fin_stress_x=stress_x
                                    elemlist[element_no-1].fin_stress_y=stress_y
                                    elemlist[element_no-1].fin_stress_xy=stress_xy
                                    elemlist[element_no-1].fin_angle=angle
                                    elemlist[element_no-1].fin_stress_major=stress_major
                                    elemlist[element_no-1].fin_stress_minor=stress_minor
                                    elemlist[element_no-1].fin_stress_von_mises=stress_von_mises
                                    
                                    
                                    
                                    
                                    break
                            

                            
#                                    break
#
#                            for line in file:
                        if (line[27:42]=='S T R E S S E S'):  #[25:40]
                            displacement_count=displacement_count+1
                            #print line
                            print 'Helooooo'
                                                
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
                                    #print j+1
                                    for line in file:
                                        break
                                    
                                    
                                    elemlist[element_no-1].fin_stress_x=stress_x
                                    elemlist[element_no-1].fin_stress_y=stress_y
                                    elemlist[element_no-1].fin_stress_xy=stress_xy
                                    elemlist[element_no-1].fin_angle=angle
                                    elemlist[element_no-1].fin_stress_major=stress_major
                                    elemlist[element_no-1].fin_stress_minor=stress_minor
                                    elemlist[element_no-1].fin_stress_von_mises=stress_von_mises
                                    
                                    print stress_von_mises
                                    
                                    
                                    
                                    
                                    break
                            

                            
                            break


                    #extract the final displacemnt arrays
                    cout = 0
                    
                    #break
                    
                break



    for i in range(0,no_of_elements):
        

        
        pointlist[elemlist[i].g[0]-1].in_stress_von_mises = max(elemlist[i].in_stress_von_mises,pointlist[elemlist[i].g[0]-1].in_stress_von_mises)
        pointlist[elemlist[i].g[0]-1].fin_stress_von_mises = max(elemlist[i].fin_stress_von_mises,pointlist[elemlist[i].g[0]-1].fin_stress_von_mises)

        pointlist[elemlist[i].g[1]-1].in_stress_von_mises = max(elemlist[i].in_stress_von_mises,pointlist[elemlist[i].g[1]-1].in_stress_von_mises)
        pointlist[elemlist[i].g[1]-1].fin_stress_von_mises = max(elemlist[i].fin_stress_von_mises,pointlist[elemlist[i].g[1]-1].fin_stress_von_mises)

        pointlist[elemlist[i].g[2]-1].in_stress_von_mises = max(elemlist[i].in_stress_von_mises,pointlist[elemlist[i].g[2]-1].in_stress_von_mises)
        pointlist[elemlist[i].g[2]-1].fin_stress_von_mises = max(elemlist[i].fin_stress_von_mises,pointlist[elemlist[i].g[2]-1].fin_stress_von_mises)

        if (elemlist[i].type == 'CQUAD4'):
            pointlist[elemlist[i].g[3]-1].in_stress_von_mises = max(elemlist[i].in_stress_von_mises,pointlist[elemlist[i].g[3]-1].in_stress_von_mises)
            pointlist[elemlist[i].g[3]-1].fin_stress_von_mises = max(elemlist[i].fin_stress_von_mises,pointlist[elemlist[i].g[3]-1].fin_stress_von_mises)









