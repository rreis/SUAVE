#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--imports---
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy

#from class_str.grid.class_structure import grid
#from class_str.elements.class_structure import CTRIA3
#from class_str.material.class_structure import PSHELL
#from class_str.material.class_structure import PBARL
#from class_str.material.class_structure import MAT1
#from class_str.load_disp_bc.class_structure import FORCE
#from class_str.load_disp_bc.class_structure import PLOAD
#from class_str.load_disp_bc.class_structure import SPC
#from class_str.io.class_structure import SU2_import
#
#from class_str.io.nastran_datatype_write_formats import float_form
#from class_str.io.nastran_datatype_write_formats import int_form
#from class_str.io.nastran_datatype_write_formats import str_form
#
#from class_str.io.nastran_datatype_write_formats import float_forms
#from class_str.io.nastran_datatype_write_formats import int_forms
##from utility_functions.pressure_interpolation import pressure_interpolation
#
##from utility_functions.print_equation import print_equation
#
#
#from input.read_nas_file import read_nas_file
##from utility_functions.interpolate_grid import interpolate_grid
##from output.write_tecplot_file import write_tecplot_file
#from input.read_constraints import read_constraints
#
#from input.read_beam import read_beam
#from input.read_beam_numbers import read_beam_numbers
#
#from input.read_opt_f06_file import read_opt_f06_file
#from input.read_opt_f06_file_stress import read_opt_f06_file_stress
##from input.read_geomach_nas_file import read_geomach_nas_file
#
##from utility_functions.interpolate_grid_brown import interpolate_grid_brown


#-----------
#---function to convert integers to required nastran format

def read_tacs_displacement_file(pointlist,displacement_filename):

    no_of_points=len(pointlist)
        #print load_filename
        
        
    file2 = open(displacement_filename, 'r')
    
    for i in range(0,no_of_points):
    
        for line in file2:
            disp_data = line.split()
            loc_point = int(disp_data[0])
#            if(pointlist[loc_point].id - loc_point !=1):
#                print loc_point , pointlist[loc_point].id
            pointlist[loc_point].t[0] = float(disp_data[4])
            pointlist[loc_point].t[1] = float(disp_data[5])
            pointlist[loc_point].t[2] = float(disp_data[6])
            
            pointlist[loc_point].s[0] = float(disp_data[7])
            pointlist[loc_point].s[1] = float(disp_data[8])
            pointlist[loc_point].s[2] = float(disp_data[9])
            pointlist[loc_point].s[3] = float(disp_data[10])
            pointlist[loc_point].s[4] = float(disp_data[11])
            pointlist[loc_point].s[5] = float(disp_data[12])
            pointlist[loc_point].s[6] = float(disp_data[13])
            pointlist[loc_point].s[7] = float(disp_data[14])
            break
    
    file2.close()
    



