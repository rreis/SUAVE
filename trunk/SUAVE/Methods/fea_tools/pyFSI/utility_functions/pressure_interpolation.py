#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format
from pyFSI.class_str.load_disp_bc.class_structure import PLOAD


def pressure_interpolation(elements,points,no_of_elements,global_to_loc_points,load_id):

    no_of_element_nodes= 3
    avg_pr = 0.0
    pressure_load = [ PLOAD() for i in range(no_of_elements)]

    for i in range(0,no_of_elements):

        pressure_load[i].type='PLOAD'

        avg_pr = avg_pr + points[global_to_loc_points[elements[i].g1]-1].pressure
        avg_pr = avg_pr + points[global_to_loc_points[elements[i].g2]-1].pressure
        avg_pr = avg_pr + points[global_to_loc_points[elements[i].g3]-1].pressure
        avg_pr = avg_pr /3.0


# elements[i].pressure = avg_pr

        pressure_load[i].type = 'PLOAD'
        pressure_load[i].p = avg_pr
        pressure_load[i].sid = load_id
        pressure_load[i].g1 = global_to_loc_points[elements[i].g1]
        pressure_load[i].g2 = global_to_loc_points[elements[i].g2]
        pressure_load[i].g3 = global_to_loc_points[elements[i].g3]


    return pressure_load












    







