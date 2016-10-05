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
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.pressure_interpolation import pressure_interpolation


from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DCONSTR
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DCONADD
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DRESP
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DRESP1
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DRESP2
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DDVAL
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DEQUATN
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DESVAR
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DVPREL1
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DVCREL1
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DVGRID
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DLINK
from SUAVE.Methods.fea_tools.pyFSI.class_str.optimization.constraints.class_structure import DOPTPRM

from SUAVE.Methods.fea_tools.pyFSI.utility_functions.print_equation import print_equation


from SUAVE.Methods.fea_tools.pyFSI.input.read_nas_file import read_nas_file
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.interpolate_grid import interpolate_grid
from SUAVE.Methods.fea_tools.pyFSI.output.write_tecplot_file import write_tecplot_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_beam_numbers import read_beam_numbers
from SUAVE.Methods.fea_tools.pyFSI.input.read_constraints import read_constraints

from SUAVE.Methods.fea_tools.pyFSI.input.read_beam import read_beam
from SUAVE.Methods.fea_tools.pyFSI.input.read_beam_numbers import read_beam_numbers
from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file import read_opt_f06_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_opt_f06_file_stress import read_opt_f06_file_stress
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.check_mesh_quality import check_mesh_quality


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


