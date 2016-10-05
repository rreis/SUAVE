#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#---Class structure for this----------------------
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.print_equation import print_equation
#-------------grid class-------------------------
class DCONSTR:
    def __defaults__(self):

        self.type = 'DCONSTR'
        self.dcid = 0   #design constrain set identification number
        self.rid        #DRESPi entry identification number
        self.lallow =10e-10    #lower bound on the response quantity
        self.lid                #set identi of a TABLEDi entry that suplies the lower bound as a fun of freq
        self.uallow = 10e10    #upper bound on the response quantity
        self.uid                #set identification of a Tabledi entry that supplies the upper bound as a fun of freq
        self.lowfq              #low end of the freq range in Hz
        self.highfq             #high end of freq range in hz


    def printt(fo):

        fo.write("$DCONSTR\n")

        fo.write(str_form(self.type));
        fo.write(int_form(self.dcid));
        
        fo.write(int_form(self.rid));
        fo.write(int_form(self.lallow));
        
        fo.write(int_form(self.uallow));
    
    
        fo.write("\n");


class DCONADD:
    def __defaults__(self):
        
        self.type = 'DCONADD'
        self.dcid = 0   #design constrain set identification number
        self.dc1        # dconstr id's
        self.dc2      #
        self.dc3                #


    def printt(fo):

        fo.write("$DCONADD\n")

        fo.write(str_form(self.type));
        fo.write(int_form(self.dcid));
        
        fo.write(int_form(self.dc1));
        #fo.write(int_form(self.dc2));
    
        fo.write("\n");




#---directly available responses--------------------
class DRESP:
    def __defaults__(self):
        
        self.type = 'DRESP'
        self.dcid = 0   #design constrain set identification number
        self.dc1        # dconstr id's
        self.dc2 =10e-10    #
        self.dc3

#---directly available responses--------------------

#response types ar listed in pg 279
class DRESP1:
    def __defaults__(self):
        
        self.type = 'DRESP1'
        self.id = 0   #unique identification number
        self.label        # user defined label
        self.rtype     # response type
        self.ptype     # used to identify the property type (ELEM, PBAR,PSHELL)
        self.region    #region identifier for constraint screening
        self.atta       #response attributes
        self.attb
        self.atti


    def printt(fo):


        fo.write(str_form(self.type));
        fo.write(int_form(self.id));
        
        fo.write(str_form(self.label));
        
        fo.write(str_form(self.rtype));
        
        if (self.ptype=='0'):
            fo.write(str_form('        '));
        else:
            fo.write(str_form(self.ptype));
        
        
        if (self.region==0):
            fo.write(int_form('        '));
        else:
            fo.write(int_form(self.region));
        
        if (self.atta==0):
            fo.write(int_form('        '));
        else:
            fo.write(int_form(self.atta));
        
        
        if (self.attb==0):
            fo.write(int_form('        '));
        else:
            fo.write(int_form(self.attb));
        
        if (self.att1==0):
            fo.write(int_form('        '));
        else:
            fo.write(int_form(self.att1));
        
        
        #att1 should be a user defined list
        #        fo.write("\n");
        #        fo.write(int_form(dresp1_list[i].att1));
        
        
        fo.write("\n");

#associated with DCONSTR


#response types ar listed in pg 279
class DRESP2:
    def __defaults__(self):
        
        self.type = 'DRESP1'
        self.id = 0   #unique identification number
        self.label        # user defined label
        self.eqid     # equation id
        self.region     #region identifier for constraint screening
        self.method     # method to be used on fun
        self.c1       #constants used
        self.c2
        self.c3
        self.associated # value associated with (like "DRESP1"
        self.nr1
        self.nr2
        self.nr3

    def printt(fo):


        fo.write(str_form(self.type));
        fo.write(int_form(self.id));

        fo.write(str_form(self.label));
        fo.write(int_form(self.eqid));


        if (self.region==0):
            fo.write(str_form('        '));
        else:
            fo.write(int_form(self.region));


        if (self.method=='0'):
            fo.write(str_form('        '));
        else:
            fo.write(str_form(self.method));

        if (self.c1==0):
            fo.write(str_form('        '));
        else:
            fo.write(float_form(self.c1));


        if (dresp2_list[i].c2==0):
            fo.write(str_form('        '));
        else:
            fo.write(float_form(self.c2));


        if (self.c3==0):
            fo.write(str_form('        '));
        else:
            fo.write(float_form(self.c3));

        fo.write("\n");
        fo.write(str_form('        '));
        fo.write(str_form(self.associated));

        fo.write(int_form(self.nr1));
        fo.write(int_form(self.nr2));
        fo.write(int_form(self.nr3));
        
        #att1 should be a user defined list
        #        fo.write("\n");
        #        fo.write(int_form(self.att1));
        
        
        fo.write("\n");







#associated with DCONSTR



#-----------discrete optimization-------------
class DDVAL:
    def __defaults__(self):
        
        self.type = 'DDVAL'
        self.id = 0   #unique discrete value identification number
        self.ddval1        # discrete values
        self.ddval2 =10e-10    #
        self.ddval3


class DEQUATN:
    def __defaults__(self):
        
        self.type = 'DEQUATN'
        self.id = eqid   #unique equation identification number
        self.equation        # equation



    def printt(fo):

        fo.write("$DEQUATN\n")
    
        print_equation(equation_list[i],fo)

#design varibales : iof case control commadn is absent, all desvar bulk data entries will be used
class DESVAR:
    def __defaults__(self):
        
        self.type = 'DESVAR'
        self.id   #unique design variable identification number
        self.label        # user supplied name for printing purposes
        self.xinit          #initial value (real within bounds)
        self.xlb =1e-10     #lower bound
        self.xub =1e20          #upper bound
        self.delxv =0.5         #move limit for the design var during approx
        self.ddval              #id of ddval entry taht provides a set of allowable discrete values


    def printt(fo):

        fo.write(str_form(self.type));
        fo.write(int_form(self.id));
        
        fo.write(str_form(self.label));
        fo.write(float_form(self.xinit));
        fo.write(float_form(self.xlb));
        fo.write(float_form(self.xub));
        fo.write(float_form(self.delxv));
        
        fo.write("\n");


#associalted entities  #pg 234
class DVPREL1:
    def __defaults__(self):
        
        self.type = 'DVPREL1'
        self.id   #unique design variable identification number
        self.type2        # name of property entry
        self.pid          #property entry id
        self.fid            #property name
        self.pmin =1e-10     #lower bound
        self.pmax =1e20          #upper bound
        self.c0 =0.0     #  constant term of relation
        self.dvid1          #   desvar entry identification number
        self.coef1          #coeff of linear relation
        self.dvid2
        self.coef2
        self.pval='pval'  #falg to indicate coef1 is to be set to current ppty value


    def printt(fo):

        fo.write(str_form(self.type));
        fo.write(int_form(self.id));
        
        fo.write(str_form(self.type2));
        fo.write(int_form(self.pid));
        
        if (self.fid=='0'):
            fo.write(str_form('        '));
        else:
            fo.write(str_form(self.fid));
        
        
        
        fo.write(float_form(self.pmin));
        fo.write(float_form(self.pmax));
        fo.write(float_form(self.c0));
        fo.write("\n");
        fo.write(str_form('        '));
        fo.write(int_form(self.dvid1));
        fo.write(float_form(self.coef1));
        #---dvidi and coefi should be user defined lists
        
        fo.write("\n");


class DVCREL1:
    def __defaults__(self):
        
        self.type = 'DVCREL1'
        self.id = id   #unique design variable identification number
        self.type2        # Name of th element connectivity entiity such as "CBAR","CQUAD", etc
        self.eid          #element identification number
        self.cpname      #name of connectivity property "X1","X2" etc
        self.cpmin =1e20          #minimum value allowed for this property
        self.cpmax =1e20         # max value allowed for this property
        self.c0          # constant term of relation
        self.dvid1          #desvar entry identification number
        self.coef1         #-coefficient of linear relation
        self.pval ='PVAL'  # flag to indicate coef2 is to be set to current connectivity property

#Associated with DESVAR



#---deisgn variable to grid coordinate relations for shape sensitivity
class DVGRID:
    def __defaults__(self):
        
        self.type = 'DVGRID'
        self.id = dvid   #unique  identification number
        self.gid        #  grid point identification number
        self.cid          #coordinate identification number
        self.coeff    # multiplier of vector measure by ni
        self.n1          # Componenets of vector measue in the coordinate system defined by cid
        self.n2          #
        self.n3          #
#--Associated desvar



class DLINK:
    def __defaults__(self):
        
        self.type = 'DLINK'
        self.id = 0   #unique  identification number
        self.ddvid        #dependent design variable identification number
        self.c0=0.0          #constant term
        self.cmult =1.0       # constant multiplier
        self.idv1         # independent design var identification number
        self.c1          #coefficienty corresp to i
        self.idv2          #
        self.c2         #
        self.idv3              #
        self.c3         #
#Associated desvar

#function to override the default values used in des opt
class DOPTPRM:
    def __defaults__(self):
        
        self.type = 'DOPTPRM'
        self.param1   #unique  identification number
        self.val1        #
        self.param2          #
        self.val2       #
        self.idv1         #
        self.c1          #
        self.idv2          #
        self.c2         #
        self.idv3              #
        self.c3         #
#used values

#DESMAX : MAx number of design variabales


    def printt(fo):

        fo.write("$Optimization params set\n")
    
    
        fo.write(str_form(self.type));
        fo.write(str_form(self.param1));
        
        fo.write(int_form(self.val1));
        
        
        fo.write("\n");

#Associated desvar



