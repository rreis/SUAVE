#---Class structure for this----------------------

#-------------grid class-------------------------
class grid:

    self.type
    self.id
    self.cp
    self.x1
    self.x2
    self.x3
    self.cd   #display coordinate system
    self.ps
    self.seid
    self.contbeg
    self.contend

class scalar_point:
    
    self.type
    self.id1
    self.id2
    self.id3
    self.id4
    self.id5
    self.id6
    self.id7
    self.id8



#---------------coordinate system class---------------

class CORD1:
    
    self.type
    self.cida
    self.g1a
    self.g2a
    self.g3a
    self.cidb
    self.g1b
    self.g2b
    self.g3b

class CORD2:
    
    self.type
    self.cid
    self.rid
    self.a1
    self.a2
    self.a3
    self.b1
    self.b2
    self.b3
    self.c1
    self.c2
    self.c3


#--------element classes--------------------------

#scalar elements---------
class CELAS:
    
    self.type
    self.eid
    self.pid
    self.k
    self.g1
    self.g2
    self.c1
    self.c2
    self.s1
    self.s2
    self.ge
    self.s


class PELAS:
    
    self.type
    self.pid1
    self.k1
    self.ge1
    self.s1
    self.pid2
    self.k2
    self.ge2
    self.s2


#1D elements-------------

class CROD:
    
    self.type
    self.eid   #element id
    self.pid    # property identification umber of PROD
    self.g1     #grid point id numbers of connection points
    self.g2

class PROD:
    
    self.type
    self.pid
    self.mid
    self.a   #area
    self.j    #torsional constant
    self.c    #torsional stress coeff
    self.nsm  #non structural mass per unit length

class CBAR:  #incomplete
    
    self.type
    self.eid   #element id
    self.pid    # property identification umber of PROD
    self.ga     #grid point id numbers of connection points
    self.gb




#2D elements------------

class CQUAD4:

    self.type
    self.eid
    self.pid
    self.g1   #point identification
    self.g2
    self.g3
    self.g4
    self.theta   #mat prop orientation
    self.zoffs      #offset from surface
    self.t1         #membrane thickness at g1 to g4
    self.t2
    self.t3
    self.t4

class CTRIA3:
    
    self.type
    self.eid
    self.pid
    self.g1   #point identification
    self.g2
    self.g3
    self.g4
    self.theta   #mat prop orientation
    self.zoffs      #offset from surface
    self.tflag      #integer flag signifying meaning of Ti
    self.t1         #membrane thickness at g1 to g3
    self.t2
    self.t3




class PSHELL:
    
    def __defaults__(self):

        self.type = 'PSHELL'
        self.pid
        self.mid1       #material identification number
        self.mid2       #mat identification for bending
        self.mid3       #mat ident for transf shear
        self.t          #def mem thickness for ti
        self.bmi        #bending moment inertia ratio
        self.ts_t       #transverse shear thickness ratio
        self.nsm        #non structural mass per unit area
        self.z1         #fiber distances for stress calc
        self.z2
        self.mid4       #mat identification number for mem-bend coupling


#3D elements------------



#--------material classes--------------------------

class MAT1:
    
    def __defaults__(self):

        self.type = 'MAT1'
        self.mid =                  #material identification  number
        self.e =0.0                 #youngs modulus
        self.g =0.0                 #shear modulus
        self.nu =0.0                #poisson's ratio
        self.rho = 0.0              #masss density
        self.a =0.0                 #thermal expansion coeff
        self.tref=0.0               #reference temperature
        self.st =0.0                #stress lim for tension
        self.sc = 0.0               #stress for comp
        self.ss = 0.0               #stress for shear
        self.mcsid =                #material coord sys identif number




#----------class constraint------------------------

class SPC:

    def __defaults__(self):

        self.type='SPC'
        self.sid =0           #identification number of single point constr set
        self.g1=0.0           #grid or scalar point id
        self.c1=0               #component no
        self.d1=0.0             #value of enforced disp
        self.g2=0.0
        self.c2=0
        self.d2=0.0





#----------class load----------------------------


class FORCE:
    
    def __defaults__(self):

    self.type='FORCE'
    self.sid=0      #local set identification number
    self.g=0        #grid point identificatyion number
    self.cid=0      #coordinate system identification number
    self.f=1.0          #scale factor
    self.n1=0.0         #components of force  vector measured in coordinate system defined by cid
    self.n2=0.0
    self.n3=0.0

class FORCE1:
    
    def __defaults__(self):
    
    self.type='FORCE'
    self.sid=0      #local set identification number
    self.g=0        #grid point identificatyion number
    self.f=0      #magnitude of force
    self.g1=1.0          #grid point identification numbers
    self.g2=0.0



class FORCE2:
    
    def __defaults__(self):
    
    self.type='FORCE'
    self.sid=0      #local set identification number
    self.g=0        #grid point identificatyion number
    self.f=0      #magnitude of force
    self.g1=1.0          #grid point identification numbers
    self.g2=0.0
    self.g3=0.0
    self.g4=0.0



#----------class su2 import--------------
class SU2_import:
    
    def __defaults__(self):
    
        self.type='SU2_surf'
        self.x=0.0
        self.y=0.0
        self.z=0.0
        self.cp=0.0
        self.mno=0.0
        self.gi= 0       #global index





