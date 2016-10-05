#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
##--imports---
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy

from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
from SUAVE.Methods.fea_tools.pyFSI.class_str.elements.class_structure import CTRIA3
from SUAVE.Methods.fea_tools.pyFSI.class_str.material.class_structure import PSHELL
from SUAVE.Methods.fea_tools.pyFSI.class_str.material.class_structure import PBARL
from SUAVE.Methods.fea_tools.pyFSI.class_str.material.class_structure import MAT1
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import FORCE
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import PLOAD
from SUAVE.Methods.fea_tools.pyFSI.class_str.load_disp_bc.class_structure import SPC
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.class_structure import SU2_import

from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import str_form

from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_forms
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_forms
#from SUAVE.Methods.fea_tools.pyFSI.utility_functions.pressure_interpolation import pressure_interpolation

#from SUAVE.Methods.fea_tools.pyFSI.utility_functions.print_equation import print_equation


from SUAVE.Methods.fea_tools.pyFSI.input.read_nas_file import read_nas_file
#from SUAVE.Methods.fea_tools.pyFSI.utility_functions.interpolate_grid import interpolate_grid
#from SUAVE.Methods.fea_tools.pyFSI.output.write_tecplot_file import write_tecplot_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_constraints import read_constraints

from SUAVE.Methods.fea_tools.pyFSI.input.read_beam import read_beam
from SUAVE.Methods.fea_tools.pyFSI.input.read_beam_numbers import read_beam_numbers

from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file import read_opt_f06_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file_stress import read_opt_f06_file_stress
#from SUAVE.Methods.fea_tools.pyFSI.input.read_geomach_nas_file import read_geomach_nas_file

#from SUAVE.Methods.fea_tools.pyFSI.utility_functions.interpolate_grid_brown import interpolate_grid_brown


#-----------
#---function to convert integers to required nastran format

def read_su2_surface_file_euler(load_filename):

    no_of_points=0
        #print load_filename
        
    file2 = open(load_filename, 'r')
    
    for line in file2:
        no_of_points=no_of_points+1
    
    file2.close()
    
    no_of_points=no_of_points-1
    
    pointlist = [ grid() for i in range(no_of_points)]
    
    local_to_glob_points = [ int for i in range(no_of_points)]
    
    no_of_grid_points_w_load=no_of_points
    coord_system=0
    load_list = [ FORCE() for i in range(no_of_points)]
    pcount=0
    fcount=0
    count=0
    max_glob_point=0
    
    file2 = open(load_filename, 'r')
    
    #----------each zone has a separate material-----
    for line in file2:
        count=count+1;
        if(count>1):
            #point_no= [float(s) for s in line.split() if s.isdigit()]
            
            
            point_no = line.split(',')
            
            pointlist[pcount].type='GRID'
            
            local_to_glob_points[pcount]=int(point_no[0])+1
            pointlist[pcount].global_to_loc =int(point_no[0])+1
            if(int(point_no[0])>max_glob_point):
                max_glob_point=int(point_no[0])
            pointlist[pcount].id=pcount+1 #int(point_no[0])
            # pointlist[pcount].id=pointlist[pcount].id+1
            pointlist[pcount].x[0]=float(point_no[1])
            pointlist[pcount].x[1]=float(point_no[2])
            pointlist[pcount].x[2]=float(point_no[3])
            
            pointlist[pcount].cp=0
            pointlist[pcount].cd=0
            pointlist[pcount].pressure=float(point_no[4])
#            pointlist[pcount].f[0]=float(point_no[6])
#            pointlist[pcount].f[1]=float(point_no[7])
#            pointlist[pcount].f[2]=float(point_no[8])
            #force_mag = numpy.sqrt(pointlist[pcount].f[0]**2 +pointlist[pcount].f[1]**2+pointlist[pcount].f[2]**2)
            
            pointlist[pcount].pcoeff = float(point_no[5])
            #pointlist[pcount].area = force_mag / pointlist[pcount].pcoeff
            

            pcount=pcount+1
    
    
    file2.close()




    max_glob_point = max_glob_point+1


    global_to_loc_points = [ int for i in range(max_glob_point+1)]

    for i in range(0,no_of_points):
        
        global_to_loc_points[local_to_glob_points[i]]=i+1



#    return no_of_points,pointlist,load_list,global_to_local_points,local_to_global_points



    return pointlist,no_of_points,local_to_glob_points,global_to_loc_points





