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


def nearest_element(elemlist,point,no_of_elements):
    
    

    min_d= (elemlist[0].centroid1-point.x1)**2 + (elemlist[0].centroid2-point.x2)**2 + (elemlist[0].centroid3-point.x3)**2
    min_point = 0
    

    
    for i in range(1,no_of_elements):
        
        
        
        d = (elemlist[i].centroid1-point.x1)**2 + (elemlist[i].centroid1-point.x2)**2 + (elemlist[i].centroid1-point.x3)**2
        
        if(d<min_d):
            min_d =d
            min_point = i
        

    


    return min_point






    
    









    
    















    







