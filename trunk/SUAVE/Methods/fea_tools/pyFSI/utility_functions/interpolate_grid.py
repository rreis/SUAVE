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


#def interpolate_grid(pointlist,pointlist_fl,no_of_points,constrained_grid_points,no_of_constrained_grid_points):

def interpolate_grid(pointlist,pointlist_fl,no_of_points):
    
    

    min_d= (pointlist[0].x1-pointlist_fl.x1)**2 + (pointlist[0].x2-pointlist_fl.x2)**2 + (pointlist[0].x3-pointlist_fl.x3)**2
    min_point = 0
    

    
    for i in range(1,no_of_points):
        
        
        
        d = (pointlist[i].x1-pointlist_fl.x1)**2 + (pointlist[i].x2-pointlist_fl.x2)**2 + (pointlist[i].x3-pointlist_fl.x3)**2
        
        if(d<min_d):
            min_d =d
            min_point = i
        

#        if ((pointlist[i].x1 <= 0)):  #and(pointlist[i].x1 >= -0.5)):
#            print pointlist[i].x1,pointlist[i].x2,pointlist[i].x2


    
            
            #        if(str_point_1==fl_point_1f)and(str_point_2==fl_point_2f)and(str_point_3==fl_point_3f):
    
    
    
    #print "min d : ",min_d
    pointlist[min_point].pressure=pointlist_fl.pressure

    pointlist[min_point].f1=pointlist_fl.f1
    pointlist[min_point].f2=pointlist_fl.f2
    pointlist[min_point].f3=pointlist_fl.f3
    pointlist[min_point].fl_gridpt=pointlist_fl.id
    
    pointlist_fl.str_grid = pointlist[min_point].id
    
    force =  pointlist[min_point].id
    


    return force






    
    









    
    















    







