#---Class structure for this----------------------
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
        self.normal = None


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



