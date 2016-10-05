# structural_dvs.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

#---Class structure for this----------------------
from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
from SUAVE.Methods.fea_tools.pyFSI.input.read_geomach_surface_points import read_geomach_surface_points
from SUAVE.Methods.fea_tools.pyFSI.input.read_stl_meshfile import read_stl_meshfile
from SUAVE.Methods.fea_tools.pyFSI.functions.compute_aircraft_loads import compute_aerodynamic_loads
from SUAVE.Methods.fea_tools.pyFSI.class_str.material.class_structure import PSHELL
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt

class structural_dvs:
    
    def __init__(self,no_of_wings,no_of_fuselages,no_of_intersections,no_of_miscellaneous):
        self.wings = [ wing_structure() for i in range(no_of_wings)]
        self.fuselages = [ fuselage_structure() for i in range(no_of_fuselages)]
        self.intersections = [ intersection_structure() for i in range(no_of_intersections)]
        self.miscellaneous = [ miscellaneous_structure() for i in range(no_of_miscellaneous)]
    
    
 

    def compute_structural_dvs(self):
        
        
        #first compute the total elements
        
        no_of_dvs = 0
        #loop over the wings
        for wing in self.wings:
            no_of_dvs += wing.upper.required_no_of_elements
            wing.upper.tag[0] = wing.tag
            wing.upper.tag[1] = 'upp'
            
            no_of_dvs += wing.lower.required_no_of_elements
            wing.lower.tag[0] = wing.tag
            wing.lower.tag[1] = 'low'
            
            no_of_dvs += wing.tip.required_no_of_elements
            wing.tip.tag[0] = wing.tag + '_t'
            wing.tip.tag[1] = ''
            
            no_of_dvs += wing.spars.required_no_of_elements
            wing.spars.tag[0] = wing.tag + '_s'
            wing.spars.tag[1] = ''
            
            no_of_dvs += wing.ribs.required_no_of_elements
            wing.ribs.tag[0] = wing.tag + '_r'
            wing.ribs.tag[1] = ''
        
        
        
            print wing.upper.tag[0],wing.upper.tag[1],wing.upper.required_no_of_elements
        
#            no_of_dvs += wing.internal.required_no_of_elements
#            wing.internal.tag[0] = wing.tag + '_i'
#            wing.internal.tag[1] = ' '

    
        #loop over the fuselages
        for fuse in self.fuselages:
            no_of_dvs += fuse.top.required_no_of_elements
            fuse.top.tag[0] = fuse.tag
            fuse.top.tag[1] = 'top'
            
            no_of_dvs += fuse.bottom.required_no_of_elements
            fuse.bottom.tag[0] = fuse.tag
            fuse.bottom.tag[1] = 'bot'
            
            
            no_of_dvs += fuse.left.required_no_of_elements
            fuse.left.tag[0] = fuse.tag
            fuse.left.tag[1] = 'lft'
            
            no_of_dvs += fuse.right.required_no_of_elements
            fuse.right.tag[0] = fuse.tag
            fuse.right.tag[1] = 'rght'
            
            
            no_of_dvs += fuse.front.required_no_of_elements
            fuse.front.tag[0] = fuse.tag + '_f'
            fuse.front.tag[1] = ''
            
            no_of_dvs += fuse.rear.required_no_of_elements
            fuse.rear.tag[0] = fuse.tag + '_r'
            fuse.rear.tag[1] = ''
            
            no_of_dvs += fuse.r1.required_no_of_elements
            fuse.r1.tag[0] = fuse.tag + '_r1'
            fuse.r1.tag[1] = ''
            
            
            no_of_dvs += fuse.r2.required_no_of_elements
            fuse.r2.tag[0] = fuse.tag + '_r2'
            fuse.r2.tag[1] = ''
            
            
            no_of_dvs += fuse.r3.required_no_of_elements
            fuse.r3.tag[0] = fuse.tag + '_r3'
            fuse.r3.tag[1] = ''
            
            
            
            no_of_dvs += fuse.r4.required_no_of_elements
            fuse.r4.tag[0] = fuse.tag + '_r4'
            fuse.r4.tag[1] = ''
            
            
            
            no_of_dvs += fuse.l1.required_no_of_elements
            fuse.l1.tag[0] = fuse.tag + '_l1'
            fuse.l1.tag[1] = ''
            
            
            no_of_dvs += fuse.l2.required_no_of_elements
            fuse.l2.tag[0] = fuse.tag + '_l2'
            fuse.l2.tag[1] = ''
            
            
            no_of_dvs += fuse.l3.required_no_of_elements
            fuse.l3.tag[0] = fuse.tag + '_l3'
            fuse.l3.tag[1] = ''
            
            
            no_of_dvs += fuse.l4.required_no_of_elements
            fuse.l4.tag[0] = fuse.tag + '_l4'
            fuse.l4.tag[1] = ''
        


        #loop over the intersections
        for intersection in self.intersections:
            no_of_dvs += intersection.dv.required_no_of_elements
            #intersection.dv.tag[0] = intersection.component1 + '_' + intersection.component2
            intersection.dv.tag[0] = intersection.tag
            intersection.dv.tag[1] = ''


        #loop over the miscellaneous
        for misc in self.miscellaneous:
            no_of_dvs += misc.dv.required_no_of_elements
            #tag 0 user specified
            misc.dv.tag[0] = misc.tag
            misc.dv.tag[1] = ''


            
        self.total = no_of_dvs

        self.new_element_map = np.zeros(int(no_of_dvs))

        shell_element_list_new = [ PSHELL() for i in range(int(no_of_dvs))]
        self.shell_element_list_new = shell_element_list_new

        for i in range(0,int(no_of_dvs)):
            self.new_element_map[i] = i+1
            self.shell_element_list_new[i].pid = i+1
            self.shell_element_list_new[i].name = 'f_'+str(i)



class wing_structure:

    def __init__(self):

        self.upper = basic_structure()
        self.lower = basic_structure()
        self.tip = basic_structure()
        self.spars = basic_structure()
        self.ribs = basic_structure()
#self.internal = basic_structure()





class fuselage_structure:
    
    def __init__(self):
        self.top = basic_structure()
        self.bottom = basic_structure()
        self.left = basic_structure()
        self.right = basic_structure()
        self.front = basic_structure()
        self.rear = basic_structure()
        
        self.r1 = basic_structure()
        self.r2 = basic_structure()
        self.r3 = basic_structure()
        self.r4 = basic_structure()
        
        self.l1 = basic_structure()
        self.l2 = basic_structure()
        self.l3 = basic_structure()
        self.l4 = basic_structure()


class intersection_structure:

    def __init__(self):
        self.tag = ['intersection']
        self.dv = basic_structure()
        self.component1 = ''
        self.component2 = ''



class miscellaneous_structure:
    
    def __init__(self):
        self.tag = ['miscellaneous']
        self.dv = basic_structure()


class basic_structure:

    def __init__(self):
        self.tag = ['tag','']
        self.no_of_elements = 0
        self.required_no_of_elements = 0
        self.element_nos = []
        self.new_element_nos = []
        self.element_tags = []
        self.fea_element_nos = []



class aircraft_breakdown:
    def __init__(self):
        self.tag = ['breakdown']
        self.no_of_wings = 0
        self.no_of_fuselages = 0

