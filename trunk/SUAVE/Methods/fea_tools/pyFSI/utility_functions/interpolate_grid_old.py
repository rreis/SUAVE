#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format
from pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from pyFSI.class_str.io.nastran_datatype_write_formats import str_form


def interpolate_grid(pointlist,pointlist_fl,no_of_points,constrained_grid_points,no_of_constrained_grid_points):
    
    
    
#    str_point_1 =str(pointlist[i].x1)
#    str_point_2 =str(pointlist[i].x2)
#    str_point_3 =str(pointlist[i].x3)
#    
#    len_1 = len(str_point_1)
#    len_2 = len(str_point_2)
#    len_3 = len(str_point_3)
#    
#    
#    fl_point_1 =str(pointlist_fl.x1)
#    fl_point_2 =str(pointlist_fl.x1)
#    fl_point_3 =str(pointlist_fl.x1)
#    
#    fl_point_1c =fl_point_1[0:len_1]
#    fl_point_2c =fl_point_2[0:len_2]
#    fl_point_3c =fl_point_3[0:len_3]

    
    
    
    for i in range(0,no_of_points):
        
        
        str_point_1 =str(pointlist[i].x1)
        str_point_2 =str(pointlist[i].x2)
        str_point_3 =str(pointlist[i].x3)
    
        len_1 = len(str_point_1)
        len_2 = len(str_point_2)
        len_3 = len(str_point_3)
        
        

        
        
        fl_point_1 =str(pointlist_fl.x1)
        fl_point_2 =str(pointlist_fl.x2)
        fl_point_3 =str(pointlist_fl.x3)
        
        
        len_1f = len(fl_point_1)
        len_2f = len(fl_point_2)
        len_3f= len(fl_point_3)
        
        
        
        
#        if(len_1==len_1f):
#        
#            fl_point_1c = fl_point_1
#        
#  
#        else:
#            fl_point_1c =fl_point_1[0:len_1-1]
#            if(int(fl_point_1[len_1])>=5):
#                fl_point_1c2=str( int(fl_point_1[len_1-1])+1)
#            else:
#                fl_point_1c2=str( int(fl_point_1[len_1-1]))
#            
#            fl_point_1c = fl_point_1c + fl_point_1c2
#        
#
#
#        if(len_2==len_2f):
#            
#            fl_point_2c = fl_point_2
#
#
#        else:
#
#
#            fl_point_2c =fl_point_2[0:len_2-1]
#            if(int(fl_point_2[len_2])>=5):
#                fl_point_2c2=str( int(fl_point_2[len_2-1])+1)
#            else:
#                fl_point_2c2=str( int(fl_point_2[len_2-1]))
#
#            fl_point_2c = fl_point_2c + fl_point_2c2
#        
#
#
#
#
#        if(len_3==len_3f):
#            
#            fl_point_3c = fl_point_3
#
#
#        else:
#
#
#            fl_point_3c =fl_point_3[0:len_3-1]
#            if(int(fl_point_3[len_3])>=5):
#                fl_point_3c2=str( int(fl_point_3[len_3-1])+1)
#            else:
#                fl_point_3c2=str( int(fl_point_3[len_3-1]))
#
#            fl_point_3c = fl_point_3c + fl_point_3c2

        
        
        fl_point_1f =(fl_point_1[0:len_1])
        fl_point_2f =(fl_point_2[0:len_2])
        fl_point_3f =(fl_point_3[0:len_3])

#print fl_point_2
        
        
    
    #if(pointlist[i].x1==pointlist_fl.x1)and(pointlist[i].x2==pointlist_fl.x2)and(pointlist[i].x3==pointlist_fl.x3):
    
    
    #print str_point_1, fl_point_1c
    
            
        if(str_point_1==fl_point_1f)and(str_point_2==fl_point_2f)and(str_point_3==fl_point_3f):
    
    
            pointlist[i].pressure=pointlist_fl.pressure

            pointlist[i].f1=pointlist_fl.f1
            pointlist[i].f2=pointlist_fl.f2
            pointlist[i].f3=pointlist_fl.f3
            pointlist[i].fl_gridpt=pointlist_fl.id
            
            
        
        
            force=1
            break
        

        else:
            
            
            pointlist[i].pressure=0.00
                
            pointlist[i].f1=0.00
            pointlist[i].f2=0.00
            pointlist[i].f3=0.00
            pointlist[i].fl_gridpt=0
            force =0
                
                
                
                
           
    constr = 0
    for i in range(0,no_of_constrained_grid_points):
        
        if(pointlist_fl.id==constrained_grid_points[i]):
            
            

            constr = 1
            
            




    return force,constr

    
    









    
    















    







