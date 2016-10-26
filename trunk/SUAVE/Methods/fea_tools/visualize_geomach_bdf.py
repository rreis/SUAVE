# rvisualize_geomach_bdf.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#visualize a geomach bdf file

from write_tecplot_file import write_tecplot_file
from read_geomach_structural_file import read_geomach_structural_file



def visualize_geomach_geometry(bdf_filename,tecplot_filename):

    elemlist,pointlist,no_of_points,no_of_elements,constrained_grid_point_list,shell_element_list = read_geomach_structural_file(bdf_filename,1.)


    write_tecplot_file(pointlist,elemlist,tecplot_filename,no_of_points,no_of_elements)