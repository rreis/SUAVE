#---Class structure for this----------------------
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#


class scalar_point:
    
    def __defaults__(self):
    
        self.type =  'SP'
        self.id1 =  0
        self.id2 = 0
        self.id3 = 0
        self.id4 = 0
        self.id5 = 0
        self.id6 = 0
        self.id7 = 0
        self.id8 = 0






#--------element classes--------------------------

#scalar elements---------
class CELAS:

    def __defaults__(self):
    
        self.type = 'CELAS '
        self.eid = 0
        self.pid = 0
        self.k = 0
        self.g = [0,0]
        self.c1 = 0
        self.c2 = 0
        self.s1 = 0
        self.s2 = 0
        self.ge = 0
        self.s = 0





#1D elements-------------

class CROD:
    
    def __init__(self):
    
        self.type = 'CROD'
        self.eid  = 0  #element id
        self.pid  = 0   # property identification number of PROD
        self.g    = [0,0]



class CBAR:  #incomplete
    
    def __init__(self):
    
        self.type = 'CBAR'
        self.eid  = 0  #element id
        self.pid  = 0  # property identification number of PROD
        self.g   = [0,0]  #grid point id numbers of connection points
        #self.gb = 0
        #self.gb   = 0




#2D elements------------

class CQUAD4:
    
    def __init__(self):

        self.type = 'CQUAD4'
        self.eid  = 0
        self.pid  = 0
        self.g   = [0,0,0,0] #point identification
        self.theta = 0.0  #mat prop orientation
        self.zoffs  =0.0     #offset from surface
        self.t       = [0.0,0.0,0.0,0.0]   #membrane thickness at g1 to g4
        self.centroid = [0.0,0.0,0.0]
        self.pressure = 0.0

class CTRIA3:
    
    def __init__(self):
    
        self.type   = 'CTRIA3'
        self.eid    = 0
        self.pid    = 0
        self.g   = [0,0,0,0] #point identification
        self.theta   = 0.0 #mat prop orientation
        self.zoffs   = 0.0   #offset from surface
        self.tflag   = 0   #integer flag signifying meaning of Ti
        self.t       = [0.0,0.0,0.0,0.0]   #membrane thickness at g1 to g3
        self.pressure = 0.0
        self.thickness = 0.0
        self.centroid = [0.0,0.0,0.0]


    def printt(fo):

        fo.write(str_form(self.type));
        fo.write(int_form(self.eid));
        fo.write(int_form(self.pid));
        #        fo.write(int_form(self.g[0]));
        #        fo.write(int_form(self.g[1]));
        #        fo.write(int_form(self.g[2]));
        
        fo.write(int_form(global_to_loc_points[self.g[0]]));
        fo.write(int_form(global_to_loc_points[self.g[1]]));
        fo.write(int_form(global_to_loc_points[self.g[2]]));
        
        #print self.g[0],self.g[1],self.g[2]
        #print global_to_loc_points[self.g[0]],self.g[1],self.g[2]
        
        
        fo.write("\n");



#3D elements------------



