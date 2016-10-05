#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
import numpy as np
import math

#---function to convert integers to required nastran format
from pyFSI.class_str.load_disp_bc.class_structure import PLOAD
from pyFSI.class_str.elements.class_structure import CTRIA3


#read in a set of elements, check if they are valid then return an updated elemlist list
#check for skewness

def check_mesh_quality(elemlist,pointlist):

#valid_element count
    valid_element_count =0
#    quad_previous_point = [3,0,1,2]
#    quad_next_point = [1,2,3,0]
#    max_tolerance = 180.0*np.pi/180.0
#    min_tolerance = 1.0*np.pi/180.0

    #for element edges
    edge_point1 = [0,1,2,3]
    edge_point2 = [1,2,3,0]    
    min_edgelength_tolerance = 1e-5*2.0
    


#loop over the elements


    for element in elemlist:


        valid = 0
        if (element.type == 'CTRIA3'):
            print
        
        #compute the centroid
        
        
        
        
        elif (element.type == 'CQUAD4'):

            
            #check the element edge size
            
            #loop over the points
            element.valid = 1
            
            #print "Element : ",element.eid
            
            for int_p in range(0,4):


                edge_1 = np.array(pointlist[element.g[edge_point1[int_p]]-1].x)
                edge_2 = np.array(pointlist[element.g[edge_point2[int_p]]-1].x)
                


                edge_length = np.linalg.norm(edge_1 - edge_2)
                
            
                
                if ((edge_length<min_edgelength_tolerance)):
                    element.valid = 0
                    print edge_length
                    
                    
            if (element.valid == 1):
                valid_element_count +=1            
            
            
            

#print "new_elements : ",valid_element_count,"old elements : ",len(elemlist)

    #create a new elemlist with the valid element

    elemlist_valid = [ CTRIA3() for i in range(valid_element_count)]
    
    valid_element_count = 0
    for i in range(0,len(elemlist)):
        if(elemlist[i].valid == 1):
            
            #update the properties
            elemlist_valid[valid_element_count].type = elemlist[i].type
            elemlist_valid[valid_element_count].eid = valid_element_count
            elemlist_valid[valid_element_count].g[0] =elemlist[i].g[0]
            elemlist_valid[valid_element_count].g[1] =elemlist[i].g[1]
            elemlist_valid[valid_element_count].g[2] =elemlist[i].g[2]
            
            if(elemlist[i].type == 'CQUAD4'):

                elemlist_valid[valid_element_count].g[3] =elemlist[i].g[3]


            valid_element_count += 1



    print "Done checking mesh quality"

    return elemlist_valid












    







