#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format
from pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from pyFSI.class_str.io.nastran_datatype_write_formats import str_form
from pyFSI.utility_functions.nearest_element import nearest_element
from pyFSI.class_str.load_disp_bc.class_structure import FORCE
import numpy


#def interpolate_grid(pointlist,pointlist_fl,no_of_points,constrained_grid_points,no_of_constrained_grid_points):

def interpolate_grid_closest_element(elemlist_str,no_of_elements_str,no_of_points_str,pointlist,pointlist_fl,no_of_points_fl):
 
 #find the centroid of all the elements
 
    for i in range (0,no_of_elements_str):
        if(elemlist_str[i].type=='CQUAD4'):
            elemlist_str[i].centroid1 = (pointlist[elemlist_str[i].g1-1].x1 + pointlist[elemlist_str[i].g2-1].x1 + pointlist[elemlist_str[i].g3-1].x1 + pointlist[elemlist_str[i].g4-1].x1)/4.0
            elemlist_str[i].centroid2 = (pointlist[elemlist_str[i].g1-1].x2 + pointlist[elemlist_str[i].g2-1].x2 + pointlist[elemlist_str[i].g3-1].x2 + pointlist[elemlist_str[i].g4-1].x2)/4.0
            elemlist_str[i].centroid3 = (pointlist[elemlist_str[i].g1-1].x3 + pointlist[elemlist_str[i].g2-1].x3 + pointlist[elemlist_str[i].g3-1].x3 + pointlist[elemlist_str[i].g4-1].x3)/4.0
            
            
        elif(elemlist_str[i].type=='CTRIA3'):
            elemlist_str[i].centroid1 = (pointlist[elemlist_str[i].g1-1].x1 + pointlist[elemlist_str[i].g2-1].x1 + pointlist[elemlist_str[i].g3-1].x1 )/3.0
            elemlist_str[i].centroid2 = (pointlist[elemlist_str[i].g1-1].x2 + pointlist[elemlist_str[i].g2-1].x2 + pointlist[elemlist_str[i].g3-1].x2 )/3.0
            elemlist_str[i].centroid3 = (pointlist[elemlist_str[i].g1-1].x3 + pointlist[elemlist_str[i].g2-1].x3 + pointlist[elemlist_str[i].g3-1].x3 )/3.0


        elemlist_str[i].f1 = 0.0
        elemlist_str[i].f2 = 0.0
        elemlist_str[i].f3 = 0.0
        elemlist_str[i].area = 0.0
            




 
    load_list = [ FORCE() for i in range(no_of_elements_str)]
    load_list_int = [ FORCE() for i in range(no_of_elements_str)]
 
    
    for i in range(0,no_of_elements_str):
        elemlist_str[i].pressure=0.0
    
        elemlist_str[i].f1=0.0
        elemlist_str[i].f2=0.0
        elemlist_str[i].f3=0.0
        elemlist_str[i].fl_gridpt=0
    
    
    
    #find the nearest centroid
    
    #transfer  loads
    
    #loop over the fluid points
    for i in range(0,no_of_points_fl):

#find the closest structural points

        closest_point = nearest_element(elemlist_str,pointlist_fl[i],no_of_elements_str)

        elemlist_str[closest_point].pressure=elemlist_str[closest_point].pressure + pointlist_fl[i].pressure
        
        elemlist_str[closest_point].f1=elemlist_str[closest_point].f1 + pointlist_fl[i].f1
        elemlist_str[closest_point].f2=elemlist_str[closest_point].f2 + pointlist_fl[i].f2
        elemlist_str[closest_point].f3=elemlist_str[closest_point].f3 + pointlist_fl[i].f3
        elemlist_str[closest_point].fl_gridpt=pointlist_fl[i].id
        elemlist_str[closest_point].area = pointlist_fl[i].area





    coord_system=0
    
    load_count = 0

    for i in range(0,no_of_elements_str):

            load_list[load_count].type='FORCE'
            load_list[load_count].sid=1
            load_list[load_count].g=elemlist_str[i].eid #pointlist_fl[pcount].id
            load_list[load_count].cid=coord_system
            load_list[load_count].f= 1.0
            load_list[load_count].n1=elemlist_str[i].f1
            load_list[load_count].n2=elemlist_str[i].f2
            load_list[load_count].n3=elemlist_str[i].f3
            load_list[load_count].area = elemlist_str[i].area
            load_count = load_count +1



    return load_list,load_count
    















    







