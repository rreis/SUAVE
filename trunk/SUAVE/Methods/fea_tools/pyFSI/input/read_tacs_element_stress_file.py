#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#Write a nastran file

#--imports---
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy


from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3
from pyFSI.class_str.material.class_structure import PSHELL
from pyFSI.class_str.material.class_structure import PBARL
from pyFSI.class_str.material.class_structure import MAT1
from pyFSI.class_str.load_disp_bc.class_structure import FORCE
from pyFSI.class_str.load_disp_bc.class_structure import PLOAD
from pyFSI.class_str.load_disp_bc.class_structure import SPC
from pyFSI.class_str.io.class_structure import SU2_import

from pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from pyFSI.class_str.io.nastran_datatype_write_formats import str_form

from pyFSI.class_str.io.nastran_datatype_write_formats import float_forms
from pyFSI.class_str.io.nastran_datatype_write_formats import int_forms
from pyFSI.utility_functions.pressure_interpolation import pressure_interpolation


from pyFSI.class_str.optimization.constraints.class_structure import DCONSTR
from pyFSI.class_str.optimization.constraints.class_structure import DCONADD
from pyFSI.class_str.optimization.constraints.class_structure import DRESP
from pyFSI.class_str.optimization.constraints.class_structure import DRESP1
from pyFSI.class_str.optimization.constraints.class_structure import DRESP2
from pyFSI.class_str.optimization.constraints.class_structure import DDVAL
from pyFSI.class_str.optimization.constraints.class_structure import DEQUATN
from pyFSI.class_str.optimization.constraints.class_structure import DESVAR
from pyFSI.class_str.optimization.constraints.class_structure import DVPREL1
from pyFSI.class_str.optimization.constraints.class_structure import DVCREL1
from pyFSI.class_str.optimization.constraints.class_structure import DVGRID
from pyFSI.class_str.optimization.constraints.class_structure import DLINK
from pyFSI.class_str.optimization.constraints.class_structure import DOPTPRM

from pyFSI.utility_functions.print_equation import print_equation


from pyFSI.input.read_nas_file import read_nas_file
from pyFSI.utility_functions.interpolate_grid import interpolate_grid
from pyFSI.output.write_tecplot_file import write_tecplot_file
from pyFSI.input.read_beam_numbers import read_beam_numbers
from pyFSI.input.read_constraints import read_constraints

from pyFSI.input.read_beam import read_beam
from pyFSI.input.read_beam_numbers import read_beam_numbers
from pyFSI.input.read_opt_f06_file import read_opt_f06_file
from pyFSI.input.read_opt_f06_file_stress import read_opt_f06_file_stress
from pyFSI.utility_functions.check_mesh_quality import check_mesh_quality


def read_tacs_element_stress_file(mesh_filename,s101):
    
    
    elemlist = s101.elemlist
    
    file = open(mesh_filename, 'r')

    count = 0
        
    for line in file:
        
        line_value = line.split()
        elemlist[count].in_stress_x = float(line_value[0])
        elemlist[count].in_stress_y = float(line_value[1])
        elemlist[count].in_stress_xy = float(line_value[2])
        count = count + 1





    file.close()


