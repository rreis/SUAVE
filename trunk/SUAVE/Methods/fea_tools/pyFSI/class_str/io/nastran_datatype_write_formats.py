#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format

def float_form(input):
    
    input_str=str(input)
    if(len(input_str)<=8):
        value=int_form(input)
    else:
        input_exp='{:4e}'.format(float(input))
        input_round=str(input_exp)[:4]
        exp=str(input_exp)[8:12]
        value=input_round+exp
    return value


def int_form(input):
    
    input_round=str(input)
    size=len(input_round)
    max_size=8
    #   value='00000000'
    value='        '
    zero_el=max_size-size
    size_zer=str(value)[:zero_el]
    value = input_round+size_zer
    
    return value


def str_form(input):
    size=len(input)
    max_size=8
    value='        '
    zero_el=max_size-size
    size_zer=str(value)[:zero_el]
    value = input+size_zer
    return value




def float_forms(input):
    

    input_str=str(input)

    max_size=16
    empty = '                '
    if(len(input_str)<=16):

        size_l = len(input_str)
        zero_el=max_size-size_l
        size_zer=str(empty)[:zero_el]
        value =  input_str+size_zer

    #value=int_forms(input)
    else:

        input_exp='{:16e}'.format(float(input))

        input_round=str(input_exp)  #[:12]
        #exp=str(input_exp)[12:16]
        
        size_l = len(input_round)
        zero_el=max_size-size_l
        size_zer=str(empty)[:zero_el]
        #value=input_round+exp
        value=input_round+size_zer


    return value


def int_forms(input):
    
    input_round=str(input)
    size=len(input_round)
    max_size=16
    #   value='00000000'
    value='                '
    zero_el=max_size-size
    size_zer=str(value)[:zero_el]
    value = input_round+size_zer
    
    return value






