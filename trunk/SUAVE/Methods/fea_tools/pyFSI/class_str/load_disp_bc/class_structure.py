#---Class structure for this----------------------
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#


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


    def printt(fo):

    #        fo.write(str_form(self.type));
    #        fo.write(int_form(self.sid));
    #        #fo.write(int_form(self.g1));
    #
    #        fo.write(int_form(global_to_loc_points[self.g1]));
    #        fo.write(int_form(self.c1));
    #        fo.write(float_form(self.d1));

        fo.write(str_form(self.type));
        fo.write(int_form(self.sid));
        #fo.write(int_form(self.g1));

        fo.write(int_form(self.c1));
        fo.write(int_form(global_to_loc_points[self.g1]));

    #fo.write(float_form(self.d1));


        fo.write("\n");





#----------class load----------------------------


class FORCE:
    
    def __init__(self):

        self.type='FORCE'
        self.sid=0      #local set identification number
        self.g=0        #grid point identificatyion number
        self.cid=0      #coordinate system identification number
        self.f=1.0          #scale factor
        self.n1=0.0         #components of force  vector measured in coordinate system defined by cid
        self.n2=0.0
        self.n3=0.0
        self.n = [0.0,0.0,0.0]


    def printt(fo):

        fo.write(str_form(self.type));
        fo.write(int_form(self.sid));
        #fo.write(int_form(self.g));
        #fo.write(int_form(self.g]));
        fo.write(int_form(self.g));
        
        
        fo.write(int_form(self.cid));
        fo.write(float_form(self.f));
        
        fo.write(float_form(self.n1));
        fo.write(float_form(self.n2));
        fo.write(float_form(self.n3));
        fo.write("\n");



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


class PLOAD:
    
    def __defaults__(self):
        
        self.type='PLOAD'
        self.sid=0      #local set identification number
        self.p=0.0        #pressure value
        self.g1=0      #magnitude of force
        self.g2=0          #grid point identification numbers
        self.g3=0
        self.g4=0


    def printt(fo):

        fo.write(str_form(self.type));
        fo.write(int_form(self.sid));

        fo.write(float_form(self.p));


        fo.write(int_form(self.g1));
        fo.write(int_form(self.g2));
        fo.write(int_form(self.g3));

        fo.write("\n");




