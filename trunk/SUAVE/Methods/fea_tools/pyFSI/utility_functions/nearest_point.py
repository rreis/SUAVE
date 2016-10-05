#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format
from pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from pyFSI.class_str.io.nastran_datatype_write_formats import str_form
import numpy


def nearest_point(pointlist,point,no_of_points):
    
    

    min_d= (pointlist[0].x[0]-point.x[0])**2 + (pointlist[0].x[1]-point.x[1])**2 + (pointlist[0].x[2]-point.x[2])**2
    min_point = 0
    

    
    for i in range(1,no_of_points):
        
        
        
        d = (pointlist[i].x[0]-point.x[0])**2 + (pointlist[i].x[1]-point.x[1])**2 + (pointlist[i].x[2]-point.x[2])**2
        
        if(d<min_d):
            min_d =d
            min_point = i
        

    


    return min_point






    
    









    
    















    







