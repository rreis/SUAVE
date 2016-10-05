#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import str_form
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.nearest_point import nearest_point
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import FORCE
import numpy


#def interpolate_grid(pointlist,pointlist_fl,no_of_points,constrained_grid_points,no_of_constrained_grid_points):

def interpolate_grid_brown(pointlist_fl,pointlist_str,elemlist_str):
    
    print "Interpolating mesh"
 
    no_of_points_str = len(pointlist_str)
    no_of_points_fl = len(pointlist_fl)
 
 
    load_list = [ FORCE() for i in range(no_of_points_str)]
    load_list_int = [ FORCE() for i in range(no_of_points_str)]
    
    
    for i in range(0,no_of_points_str):
        pointlist_str[i].pressure=0.0
    
        pointlist_str[i].f[0]=0.0
        pointlist_str[i].f[1]=0.0
        pointlist_str[i].f[2]=0.0
        pointlist_str[i].fl_gridpt=0
    
    
    
    #loop over the fluid points
    for i in range(0,no_of_points_fl):

#find the closest structural points

        closest_point = nearest_point(pointlist_str,pointlist_fl[i],no_of_points_str)

        pointlist_str[closest_point].pressure=pointlist_str[closest_point].pressure + pointlist_fl[i].pressure
        
        pointlist_str[closest_point].f[0]=pointlist_str[closest_point].f[0] + pointlist_fl[i].f[0]
        pointlist_str[closest_point].f[1]=pointlist_str[closest_point].f[1] + pointlist_fl[i].f[1]
        pointlist_str[closest_point].f[2]=pointlist_str[closest_point].f[2] + pointlist_fl[i].f[2]
        pointlist_str[closest_point].fl_gridpt=pointlist_fl[i].id
#pointlist_str[closest_point].area = pointlist_fl[i].area



#loop over the fluid points
    for i in range(0,no_of_points_str):
    
    #find the closest structural points
    
        
        pointlist_str[i].f[0]=4.5*pointlist_str[closest_point].f[0]
        pointlist_str[i].f[1]=4.5*pointlist_str[closest_point].f[1]
        pointlist_str[i].f[2]=4.5*pointlist_str[closest_point].f[2]




#    coord_system=0
#    
#    load_count = 0
#
#    for i in range(0,no_of_points_str):
#
#        if(pointlist_str[i].f1!=0 or pointlist_str[i].f2!=0 or pointlist_str[i].f3!=0 ):
#
#            load_list[load_count].type='FORCE'
#            load_list[load_count].sid=1
#            load_list[load_count].g=pointlist_str[i].id #pointlist_fl[pcount].id
#            load_list[load_count].cid=coord_system
#            load_list[load_count].f= 1.0
#            load_list[load_count].n1=pointlist_str[i].f1
#            load_list[load_count].n2=pointlist_str[i].f2
#            load_list[load_count].n3=pointlist_str[i].f3
#            load_list[load_count].area = pointlist_str[i].area
#            load_count = load_count +1



#   return load_list,load_count
    















    







