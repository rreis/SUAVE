#---Class structure for this----------------------
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#------scalar elements------

class PELAS:
    
    def __defaults__(self):
    
        self.type = 'PELAS'
        self.pid1 = 0
        self.k1    = 0.0
        self.ge1   = 0.0
        self.s1    = 0.0
        self.pid2  = 0
        self.k2    = 0.0
        self.ge2   = 0.0
        self.s2    = 0

    def printt(fo):

        print "hello"


#1D elements-------------


class PROD:
    
    def __defaults__(self):
    
        self.type = 'PROD'
        self.pid
        self.mid
        self.a   #area
        self.j    #torsional constant
        self.c    #torsional stress coeff
        self.nsm  #non structural mass per unit length

    def printt(fo):
        
        print "hello"

#--class PBAR

class PBAR:
    
    def __defaults__(self):
        
        self.type = 'PBAR'
        self.pid  = 0
        self.mid  = 0
        self.a    = 0.0 #area
        self.i1   = 0.0 #area moments of inertia
        self.i2   = 0.0  #area moments of inertia
        self.i3   = 0.0  #area moments of inertia
        self.j    = 0.0 #torsional constant
        self.nsm  = 0.0 #non structural mass per unit length
    
    def printt(fo):
        
        print "hello"

#--class PBAR

class PBARL:
    
    def __defaults__(self):
        
        self.type = 'PBARL'
        self.pid  = 0
        self.mid  = 0
        self.group = 0  #area
        self.dim1  = 0.0 #area moments of inertia
        self.dim2  = 0.0  #area moments of inertia
        self.dim3  = 0.0  #area moments of inertia
        self.dim4  = 0.0  #torsional constant
        self.dim5  = 0.0 #non structural mass per unit length
    
    def printt(fo):
        
        print "hello"





#2D elements------------


class PSHELL:
    
    def __defaults__(self):

        self.type = 'PSHELL'
        self.pid  = 0
        self.mid1 = 0      #material identification number
        self.mid2 = 0      #mat identification for bending
        self.mid3 = 0      #mat ident for transf shear
        self.t    = 0.0      #def mem thickness for ti
        self.bmi  = 0.0     #bending moment inertia ratio
        self.ts_t = 0.0     #transverse shear thickness ratio
        self.nsm   = 0.0      #non structural mass per unit area
        self.z1    = 0.0      #fiber distances for stress calc
        self.z2    = 0.0
        self.mid4  = 0     #mat identification number for mem-bend coupling
        self.t_min = 0.0
        self.t_max = 0.0

    def printt(fo):

        fo.write(str_form(self.type));
        fo.write(int_form(self.pid));
        fo.write(int_form(self.mid1));
        fo.write(float_form(self.t));
        fo.write(int_form(self.mid2));
        fo.write(str_form('        '));
        fo.write(int_form(self.mid3));
        fo.write("\n");


#3D elements------------



#--------material classes--------------------------

class MAT1:
    
    def __defaults__(self):

        self.type = 'MAT1'
        self.mid = 0                 #material identification  number
        self.e =0.0                 #youngs modulus
        self.g =0.0                 #shear modulus
        self.nu =0.0                #poisson's ratio
        self.rho = 0.0              #masss density
        self.a =0.0                 #thermal expansion coeff
        self.tref=0.0               #reference temperature
        self.st =0.0                #stress lim for tension
        self.sc = 0.0               #stress for comp
        self.ss = 0.0               #stress for shear
        self.mcsid = 0              #material coord sys identif number


    def printt(fo):
        
        fo.write(str_form(self.type));
        fo.write(int_form(self.mid));
        fo.write(float_form(self.e));
        fo.write("        ");
        fo.write(float_form(self.nu));
        fo.write(float_form(self.rho));
        
        fo.write("\n");







