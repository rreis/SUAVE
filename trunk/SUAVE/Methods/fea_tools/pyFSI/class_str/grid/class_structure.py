import numpy as np
#---Class structure for this----------------------
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-------------grid class-------------------------
## grid point class
# Includes location, forces, translations
##
class grid:
    def __init__(self):

        self.type = None
        self.id = None
        self.cp = None
        self.x = np.array([0.,0.,0.])
        self.cd = None  #display coordinate system
        self.ps = None
        self.seid = None
        self.contbeg = None
        self.contend = None
        self.global_to_loc = None
        self.t = np.array([0.,0.,0.])
        self.r = np.array([0.,0.,0.])
        self.pressure = 0
        self.f = np.array([0.,0.,0.])
        self.closest_vector = np.array([0.0, 0.0, 0.0])
        self.closest_elem_index = 0
        self.closest_dist = 0
        self.area = 0.0
        self.fuel_load_p = 0
        self.fuel_load = 0.0
        self.payload_p = 0
        self.payloadload = 0.0
        self.load = 0.0
        self.von_mises_computed = 0.0
        self.in_stress_x = 0.0
        self.in_stress_y = 0.0
        self.in_stress_xy = 0.0
        self.f_aero = np.array([0.,0.,0.])
        self.f_pressure = np.array([0.,0.,0.])
        self.f_loads = np.array([0.,0.,0.])
        self.nv = np.array([0.,0.,0.])
        self.nva = np.array([0.,0.,0.])

    def printt(self,fo):
    
        fo.write("$write grid data\n")

    #--write to the grid points-

        fo.write(str_form(self.type));
        fo.write(int_form(self.id));
        fo.write(int_form(self.cp));
        fo.write(float_form(self.x[0]));
        fo.write(float_form(self.x[1]));
        fo.write(float_form(self.x[2]));
        fo.write(int_form(self.cd));

        fo.write("\n");





#---------------coordinate system class---------------

class CORD1:
    
    def __init__(self):
    
        self.type = None
        self.cida = None
        self.g1a = None
        self.g2a = None
        self.g3a = None
        self.cidb = None
        self.g1b = None
        self.g2b = None
        self.g3b = None

class CORD2:

    def __init__(self):
    
        self.type = None
        self.cid = None
        self.rid = None
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.b1 = None
        self.b2 = None
        self.b3 = None
        self.c1 = None
        self.c2 = None
        self.c3 = None



