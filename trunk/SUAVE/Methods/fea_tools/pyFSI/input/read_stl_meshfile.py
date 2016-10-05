#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3

import numpy as np

#-----------
#---function to convert integers to required nastran format

def read_stl_meshfile(stl_filename):

#stl_filename = 'cp_str.stl'

    #get the number of elements

    file= open(stl_filename,"r")



    element_count = 0

    for line in file:

        line_break = line.split()

#if((line_break[0]=='facet') and (line_break[1]=='normal')):
        if((line_break[0]=='outer') and (line_break[1]=='loop')):
#        if (line[0:12]=='facet normal'):
            element_count = element_count +1


    element_list = [ CTRIA3() for i in range(element_count)]



    file.close()



    file= open(stl_filename,"r")


    for line in file:
        "reading file"
        break

    for i in range(0,element_count):
        
        for line in file:
            point_no = line.split('l')
            normal_val = point_no[1].split(' ')


            normal = [float() for mno in range(3)]
            no_of_el = 3 #len(normal_val)

            loc_el_count =0
            loc_el_non_c =0
            for lel in range(0,no_of_el):
                if (normal_val[lel]==''):

                    loc_el_non_c = 0
                else:
 
                    normal[loc_el_count] = float(normal_val[lel])
                    loc_el_count =  loc_el_count + 1
                
            
            #normal[0] = float(normal_val[0])
            #normal[1] = float(normal_val[1])
            #normal[2] = float(normal_val[2])
            element_list[i].normal_g = normal

            break

        for line in file:
            loc_count =0
            break

    # element_list[i].v =[nodes() for mno in range(3)]
        v =[grid() for mno in range(3)]
        for j in range(0,3):
            for line in file:
                point_no = line.split(' ')
                no_of_el = len(point_no)
                loc_el_count =0
                loc_el_non_c =0
                for lel in range(0,no_of_el):
                    
                    if ((point_no[lel]=='')or (point_no[lel]=='vertex')):
                        loc_el_non_c = 0
                    else:
                        if(loc_el_count==0):
                            v[j].n1=float(point_no[lel])
                        if(loc_el_count==1):
                            v[j].n2=float(point_no[lel])                        

                        if(loc_el_count==2):
                            v[j].n3=float(point_no[lel])  
                            
                        loc_el_count =  loc_el_count + 1
                
                
                #v[j].n1=float(point_no[1])
                #v[j].n2=float(point_no[2])
                #v[j].n3=float(point_no[3])
                break


        element_list[i].v = v

        for k in range(0,2):
            for line in file:
                loc_count =0
                break


    file.close()


    for i in range(0,element_count):
        centroid = [float() for mno in range(3)]
        
        centroid[0] = (element_list[i].v[0].n1 + element_list[i].v[1].n1 + element_list[i].v[2].n1)/3.0
        centroid[1] = (element_list[i].v[0].n2 + element_list[i].v[1].n2 + element_list[i].v[2].n2)/3.0
        centroid[2] = (element_list[i].v[0].n3 + element_list[i].v[1].n3 + element_list[i].v[2].n3)/3.0
        

        
        element_list[i].centroid = centroid
        element_list[i].no_of_neighbours = 0
        element_list[i].neighbours = 0
        element_list[i].vel = [ float() for mno in range(3)]
        element_list[i].Cp = 0.

        
        side1=  np.sqrt((element_list[i].v[1].n1-element_list[i].v[0].n1)**2 + (element_list[i].v[1].n2-element_list[i].v[0].n2)**2 + (element_list[i].v[1].n3-element_list[i].v[0].n3)**2 )
        side2=  np.sqrt((element_list[i].v[2].n1-element_list[i].v[1].n1)**2 + (element_list[i].v[2].n2-element_list[i].v[1].n2)**2 + (element_list[i].v[2].n3-element_list[i].v[1].n3)**2 )
        side3=  np.sqrt((element_list[i].v[0].n1-element_list[i].v[2].n1)**2 + (element_list[i].v[0].n2-element_list[i].v[2].n2)**2 + (element_list[i].v[0].n3-element_list[i].v[2].n3)**2 )
        ss =  (side1 + side2 + side3)/2.0
        
        area = np.sqrt(ss*(ss-side1)*(ss-side2)*(ss-side3))
        
        element_list[i].Sarea = area
    
    

    return element_list,element_count
