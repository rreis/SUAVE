#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
from SUAVE.Methods.fea_tools.pyFSI.class_str.elements.class_structure import CTRIA3

def read_opt_f06_file(opt_filename,no_of_design_variables,elemlist,no_of_elements):

    max_glob_point=0;
    file = open(opt_filename, "r")
    element_count=0
    element_pres =0
    count=0
    pcount=0
    #no_of_elements = 0
    no_of_points=0
    #elemlist =[]
    design_var_value1=[]
    design_var_value2=[]

    #[39:87]
    for line in file:
        #print line
        count =0

        if (line[35:48]== 'S U M M A R Y'):
#if (line[39:88]== 'NUMBER OF OPTIMIZATIONS W.R.T. APPROXIMATE MODELS'):


            #leave 8 lines
            
            #for li in range(0,8):
            for line in file:

                count = count +1
                if(line[39:82] == 'NUMBER OF FINITE ELEMENT ANALYSES COMPLETED'):

                    break



        

            for line in file:
                #print line

                line_val = [int(s) for s in line.split() if s.isdigit()]
                no_of_design_runs = int(line_val[0])
                #print no_of_design_runs
                objective_list = [int() for i in range(no_of_design_runs+1)]
                constraint_list = [int() for i in range(no_of_design_runs+1)]


#                design_var_value1 = [int() for i in range(no_of_design_runs+1)]
#                design_var_value2 = [design_var_value1() for i in range(no_of_design_variables)]

                design_var_value = [[0 for x in xrange(no_of_design_runs+1)] for x in xrange(no_of_design_variables)]
                




                break
                    
                    
        if (line[46:86]=='OBJECTIVE AND MAXIMUM CONSTRAINT HISTORY'):
            #print line
            for i in range(0,6):
                for line in file:
                    #print line
                    elem_count=0
                    break
        
            for line in file:
                #print line
                objective_list[0] = float(line[58:70])
                if (line[110:113] == 'N/A'):
                    constraint_list[0] = 0.0
                else:
                    constraint_list[0] = float(line[107:120])
                #if
                #print constraint_list[0]
                break
            
            for i in range(0,no_of_design_runs):
                if(i==15)or((i-15)%22==0):
                #if(i==14)or((i-14)%22==0):
                
                    for ijk in range(0,8):
                        for line in file:
                            #print line
                            elem_count=0
                            break
            
                for line in file:
                    #print line
                    elem_count=0
                    break
                for line in file:
                    #print line
                    objective_list[1+i] = float(line[58:70])
                    if (line[110:113] == 'N/A'):
                        constraint_list[0] = 0.0
                    else:
                        constraint_list[1+i] = float(line[107:120])
                    #print i , objective_list[1+i]
                    break

##break
#
#        if (line[55:78]=='DESIGN VARIABLE HISTORY'):
#            #print line
#            no_of_dv_sections = (no_of_design_runs+1)/6 +1
#            
#            for j in range(0,no_of_dv_sections):
#                
#
#                for line in file:
#                
#                    if(line[0]=='1'):
#                    
#                        for ijk in range(0,6):
#                            for line in file:
#                                elem_count=0
#                                break
#
#                    else:
#
#                        for ijk in range(0,3):
#                            for line in file:
#                                elem_count=0
#                                break
#                                    
#                                    
#                    break
#            
##                if (j>0):
##                    for line in file:
##                        elem_count=0
##                        break
#
#
#
#                for i in range(0,no_of_design_variables):
#                    for line in file:
#                        if(line[0]=='1'):
#                            
#                            for ijk in range(0,7):
#                                for line in file:
#                                    elem_count=0
#                                    break
##                        if (i == 0):
##
##                            for line in file:
##                                elem_count=0
##                                break
#
#                        for k in range(0,min(no_of_design_runs-6*j+1,6)):
#                            starting_value = 41 + k*15
#                            #print line[starting_value:starting_value+14],i,6*j+k
#                            design_var_value[i][6*j+k] = float(line[starting_value:starting_value+14])
#                        #print i,6*j+k,design_var_value[i][6*j+k]
#                        break
#
#
#
#            break
#            
#
#
#
#
#
#    
#    for i in range(0,no_of_elements):
#
#        elemlist[i].thickness = design_var_value[elemlist[i].pid-1][no_of_design_runs]
#    #print elemlist[i].pid-1
#    #print elemlist[i].thickness


    file.close()

    return objective_list,no_of_design_runs,design_var_value,constraint_list
