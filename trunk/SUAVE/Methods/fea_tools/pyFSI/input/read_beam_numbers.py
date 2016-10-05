#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
from SUAVE.Methods.fea_tools.pyFSI.class_str.elements.class_structure import CBAR
import numpy


def read_beam_numbers(conn_filename):
    
    
    max_glob_point=0;
    
    element_count=0
    element_pres =0
    count=0
    pcount=0
    no_of_beam_elements = 0
    no_of_points=0
    elemlist =[]
    
    
    
    #----------each zone has a separate material-----
    
    # no_of_materials = 0
    no_of_points = 0
    #no_of_elements = 0
    no_of_beams = 0
    no_of_beam_materials = 0
    
    
    
    file = open(conn_filename, 'r')
    
    for line in file:
        
        no_of_beam_materials = no_of_beam_materials + 1
        loc_no_points =int(line)
        no_of_beams = no_of_beams + loc_no_points-1
        no_of_points = loc_no_points + no_of_points
        for i in range(0,loc_no_points):
            
            for line in file:
                break
        
    file.close()
    

    return no_of_beams









