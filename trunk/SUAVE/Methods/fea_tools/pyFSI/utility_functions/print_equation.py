#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from SUAVE.Methods.fea_tools.pyFSI.class_str.io.nastran_datatype_write_formats import str_form


def print_equation(equat,fo):
    
    fo.write(str_form(equat.type))
    fo.write(int_form(equat.id))
 
    str_length=len(equat.equation)
    no_of_itr = (str_length - 56)/(80-16) +1
    
    line1=equat.equation[0:56]
    
    fo.write(format(line1))
    
    fo.write("\n")
    
    starting_pt = 56
    ending_pt = starting_pt+(80-16)
    
    for i in range(0,no_of_itr):
        
        fo.write("        ")
    
        fo.write(format(equat.equation[starting_pt:ending_pt]))
        
        starting_pt = ending_pt
        ending_pt = starting_pt+(80-16)
    
        fo.write("\n")
    














    







