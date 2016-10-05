#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#--------reading in a grid file(stl,tec,su2)----------------------------------------------------------

from pyFSI.class_str.grid.class_structure import grid
from pyFSI.class_str.elements.class_structure import CTRIA3


def read_opt_f06_file_ol(opt_filename,no_of_design_variables):


    max_glob_point=0;
    file = open(opt_filename, "r")
    element_count=0
    element_pres =0
    count=0
    pcount=0
    no_of_elements = 0
    no_of_points=0
    elemlist =[]
    design_var_value1=[]
    design_var_value2=[]
    #no_of_design_runs = 0
    #----------each zone has a separate material-----



        
    for line in file:
        

        
        if (line[39:86]=='NUMBER OF OPTIMIZATIONS W.R.T. APPROXIMATE MODELS'):
            print line
            no_of_design_runs = [int(s) for s in line.split() if s.isdigit()]
            print no_of_design_runs
            objective_list = [int() for i in range(no_of_design_runs+1)]
        
        
            design_var_value1 = [int() for i in range(no_of_design_runs+1)]
            design_var_value2 = [design_var_value1() for i in range(no_of_design_variables)]
        
        if (line[46:85]=='OBJECTIVE AND MAXIMUM CONSTRAINT HISTORY'):
            print line

          for i in range(0,6):
            for line in file:
              elem_count=0
        
        
          for line in file:
            objective_list[0] = float(line[58:70])

          for i in range(0,no_of_design_runs):
              
            if(i==15):
                
                for i in range(0,7):
                    for line in file:
                        elem_count=0
                
                
              
            for line in file:
                
              elem_count=0
            for line in file:
              objective_list[1+i] = float(line[58:70])
                      
                      



        
        if (line[55:78]=='DESIGN VARIABLE HISTORY'):
            
            #skip 4 lines
            
            #-loop over first 5 design iterations
            
#            #page 1
#            for i in range(0,1):
#                for line in file:
#                    elem_count=0




            no_of_dv_sections = (no_of_design_runs+1)/6
            
            for j in range(0,no_of_dv_sections):
                

                    
                for ijk in range(0,4):
                    for line in file:
                        elem_count=0
                
                
                for i in range(0,no_of_design_variables):
                    for line in file:
                        if(line[0]=='1'):
 
                            for ijk in range(0,6):
                                for line in file:
                                    elem_count=0
            
                    if (i == 0):
                    
                        for line in file:
                            elem_count=0

                    for k in range(0,min(no_of_design_variables-6*j,6)):
                        starting_value = 40 + k*13
                        design_var_value[i][6*j+k] = line[starting_value:starting_value+13]






            #page 2:n-1

            #read the data


    print design_var_value
    file.close()


