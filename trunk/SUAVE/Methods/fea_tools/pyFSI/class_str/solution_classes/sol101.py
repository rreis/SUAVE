#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#---Class structure for this----------------------
#--imports---
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from pyFSI.class_str.io.nastran_datatype_write_formats import float_form
from pyFSI.class_str.io.nastran_datatype_write_formats import int_form
from pyFSI.class_str.io.nastran_datatype_write_formats import str_form
from pyFSI.class_str.io.nastran_datatype_write_formats import float_forms
from pyFSI.class_str.io.nastran_datatype_write_formats import int_forms
from pyFSI.input.read_su2_surface_file_euler import read_su2_surface_file_euler
from pyFSI.input.read_bdf_file import read_bdf_file
from pyFSI.class_str.load_disp_bc.class_structure import FORCE
from pyFSI.output.write_tacs_load_file import write_tacs_load_file
from pyFSI.input.read_su2_surface_file_euler_f import read_su2_surface_file_euler_f
from pyFSI.output.write_su2_deformation_file import write_su2_deformation_file
from pyFSI.input.read_tacs_displacement_file import read_tacs_displacement_file
from pyFSI.utility_functions.nearest_point import nearest_point

class sol101:
    
    def __init__(self):
        print "ha"
        self.pointlist=[]
        self.pointlist_fl=[]
        self.load_list=[]
        self.elemlist=[]
        self.case_control_def=0
        self.load_type=0
        self.material_list=[]
        self.shell_element_list=[]
        self.beam_element_list=[]
        self.spc_type=0
        self.constrained_grid_point_list=[]
        self.case_control_analysis_type=None
        self.times = 600
        self.sol =101
        
        
        self.no_of_points=0
        self.no_of_elements=0
        self.no_of_beams=0
        self.no_of_shell_elements=0
        self.no_of_beam_elements=0
        self.no_of_materials=0
        self.no_of_constrained_grid_points=0
        self.no_of_grid_points_w_load=0
        self.no_of_property_types=0




    def initialize():
        print "ha"
    
    def read_bdf(self,mesh_filename):

        [elemlist,pointlist,no_of_points,no_of_elements,material_list,no_of_materials,shell_element_list,no_of_shell_elements,constrained_grid_point_list,no_of_constrained_grid_points] = read_bdf_file(mesh_filename,1.0)


        self.elemlist = elemlist
        self.pointlist = pointlist
        self.material_list = material_list
        self.shell_element_list = shell_element_list
        self.constrained_grid_point_list = constrained_grid_point_list
        
        self.no_of_points = no_of_points
        self.no_of_elements = no_of_elements
        self.no_of_materials = no_of_materials
        self.no_of_shell_elements = no_of_shell_elements
        self.no_of_constrained_grid_points = no_of_constrained_grid_points
    


    def read_load_file(self,loads_filename,filetype):
    
        if (filetype == "su2_euler"):
            pointlist_fl,no_of_points_fl,local_to_global_points_fl,global_to_local_points_fl =  read_su2_surface_file_euler(loads_filename)

            self.pointlist_fl = pointlist_fl
            self.no_of_points_fl = no_of_points_fl
            self.local_to_global_points_fl = local_to_global_points_fl
            self.global_to_local_points_fl = global_to_local_points_fl


        if (filetype == "su2_euler_f"):
            pointlist_fl,no_of_points_fl,local_to_global_points_fl,global_to_local_points_fl =  read_su2_surface_file_euler_f(loads_filename)
        
            self.pointlist_fl = pointlist_fl
            self.no_of_points_fl = no_of_points_fl
            self.local_to_global_points_fl = local_to_global_points_fl
            self.global_to_local_points_fl = global_to_local_points_fl

            for i in range(0,self.no_of_points_fl):
                self.pointlist_fl[i].f[0] = self.pointlist_fl[i].f[0]*self.dynamic_pressure
                self.pointlist_fl[i].f[1] = self.pointlist_fl[i].f[1]*self.dynamic_pressure
                self.pointlist_fl[i].f[2] = self.pointlist_fl[i].f[2]*self.dynamic_pressure




    def read_su2_cfd_mesh(self,cfd_mesh_file_name):
        print
    #write_tacs_load_file(self.pointlist,self.elemlist,tacs_load_file_name)


    def compute_nastran_loads(self):
        #interpolate_loads(self.pointlist_fl,self.pointlist,self.elemlist)


        no_of_points_str = self.no_of_points
        pointlist_str = self.pointlist

        coord_system=0

        load_count = 0
    
        load_list = [ FORCE() for i in range(no_of_points_str)]
        for i in range(0,no_of_points_str):
        
            if(pointlist_str[i].f[0]!=0 or pointlist_str[i].f[1]!=0 or pointlist_str[i].f[2]!=0 ):
            
                load_list[load_count].type='FORCE'
                load_list[load_count].sid=1
                load_list[load_count].g=pointlist_str[i].id #pointlist_fl[pcount].id
                load_list[load_count].cid=coord_system
                load_list[load_count].f= 1.0
                load_list[load_count].n1=pointlist_str[i].f[0]
                load_list[load_count].n2=pointlist_str[i].f[1]
                load_list[load_count].n3=pointlist_str[i].f[2]
                load_list[load_count].area = pointlist_str[i].area
                load_count = load_count +1

        self.load_list = load_list
        self.no_of_grid_points_w_load = load_count



    def specify_loads(self,specified_loads):
        self.load_list = specified_loads
        self.no_of_grid_points_w_load = len(specified_loads)
    
    
    
    
    def specify_constraint(self,specified_constraint):
        print
    
    
    def write_tacs_load_file(self,tacs_load_filename):
        write_tacs_load_file(self.pointlist,self.elemlist,tacs_load_filename)
    
    
    def write_su2_def_file(self,su2_def_filename):
        
        #loop over the surface mesh
        pointlist_fl = self.pointlist_fl
        for i in range(0,len(pointlist_fl)):
            #find the nearest structural point
            nearest_point_value = nearest_point(self.pointlist,pointlist_fl[i],len(self.pointlist))
            pointlist_fl[i].t1 = self.pointlist[nearest_point_value].t1
            pointlist_fl[i].t2 = self.pointlist[nearest_point_value].t2
            pointlist_fl[i].t3 = self.pointlist[nearest_point_value].t3
                       
        write_su2_deformation_file( pointlist_fl,su2_def_filename)
    
    
    def read_tacs_displacement_file(self,tacs_displacement_filename):
        read_tacs_displacement_file(self.pointlist,tacs_displacement_filename)
    

    def write_sol(self,output_filename):
        print "ha"
    
        #----------------writing the output to the file----------------------------------------------
        #------open the file-------
        fo = open(output_filename,"wb")
        
        
        
        #---------Executive_control_section----------------------------------------
        
        fo.write("SOL ")
        fo.write(format(self.sol))
        fo.write("\n")
        
        fo.write("TIME ")
        fo.write(format(self.times))
        fo.write("\n")
        
        fo.write("CEND")
        fo.write("\n")
        
        
        
        #-----------Case_control_section------------------------------------------
        
        #--load case--
        
        
        if(self.case_control_def==1):
            fo.write("DISPLACEMENT = ALL")
            fo.write("\n")
            fo.write("ELFORCE = ALL")
            fo.write("\n")
            fo.write("ELSTRESS = ALL")
            
            fo.write("\n")
        
        fo.write("LOAD = ")
        fo.write(format(self.load_type))
        fo.write("\n")
        
        fo.write("SPC = ")
        fo.write(format(self.spc_type))
        fo.write("\n")
        
        
        #-------------------Bulk Data Section--------------------------------------
        
        fo.write("BEGIN BULK\n")
        
        #---------------writing grid data------
        fo.write("PARAM    POST    0\n")
        
        #-------loop over the points-----------
        fo.write("$write grid data\n")
        
        #--write to the grid points-
        
#        for i in range(0,self.no_of_points):
#            
#            fo.write(str_form(self.pointlist[i].type));
#            fo.write(int_form(self.pointlist[i].id));
#            fo.write(int_form(self.pointlist[i].cp));
#            fo.write(float_form(self.pointlist[i].x[0]));
#            fo.write(float_form(self.pointlist[i].x[1]));
#            fo.write(float_form(self.pointlist[i].x[2]));
#            fo.write(int_form(self.pointlist[i].cd));
#            
#            #    fo.write(int_form(self.pointlist[i].ps));
#            #    fo.write(int_form(self.pointlist[i].seid));
#            fo.write("\n");

        
        #------------16 point string----------------
        
        for i in range(0,self.no_of_points):
            
            fo.write(str_form('GRID*'));
            fo.write(int_forms(self.pointlist[i].id));
            fo.write(int_forms(self.pointlist[i].cp));
            fo.write(float_forms(self.pointlist[i].x[0]));
            fo.write(float_forms(self.pointlist[i].x[1]));
            fo.write(str_form('*G'+str(self.pointlist[i].id)))
            fo.write("\n");
            fo.write(str_form('*G'+str(self.pointlist[i].id)))
            fo.write(float_forms(self.pointlist[i].x[2]));
            fo.write(int_forms(self.pointlist[i].cd));
            
            #    fo.write(int_form(pointlist[i].ps));
            #    fo.write(int_form(pointlist[i].seid));
            fo.write("\n");
        
        
        
        #------------writing element data------
        fo.write("$write element data\n")
        
        #--write to the grid points-
        

        
        for i in range(0,self.no_of_elements):
            
            
            
            
            fo.write(str_form(self.elemlist[i].type));
            fo.write(int_form(self.elemlist[i].eid));
            fo.write(int_form(self.elemlist[i].pid));
            fo.write(int_form(self.elemlist[i].g[0]));
            fo.write(int_form(self.elemlist[i].g[1]));
            fo.write(int_form(self.elemlist[i].g[2]));
            
            if(self.elemlist[i].type=='CQUAD4'):
                fo.write(int_form(self.elemlist[i].g[3]));
            
            
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[0]]));
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[1]]));
            #        fo.write(int_form(global_to_loc_points[elemlist[i].g[2]]));
            
            #print elemlist[i].g[0],elemlist[i].g[1],elemlist[i].g[2]
            #print global_to_loc_points[elemlist[i].g[0]],elemlist[i].g[1],elemlist[i].g[2]
            
            
            fo.write("\n")
        
        
        
        
        
        
        
        
        
        #------------writing element property data------
        fo.write("$write element property\n")
        for i in range(0, self.no_of_shell_elements):
            
            fo.write(str_form(self.shell_element_list[i].type));
            fo.write(int_form(self.shell_element_list[i].pid));
            fo.write(int_form(self.shell_element_list[i].mid1));
            fo.write(float_form(self.shell_element_list[i].t));
            fo.write(int_form(self.shell_element_list[i].mid2));
            fo.write(str_form('        '));
            fo.write(int_form(self.shell_element_list[i].mid3));
            
            
            
            
            fo.write("\n");
        
        
        
        #------------writing material data------
        fo.write("$material property\n")
        
        for i in range(0, self.no_of_materials):
            fo.write(str_form(self.material_list[i].type));
            fo.write(int_form(self.material_list[i].mid));
            fo.write(float_form(self.material_list[i].e));
            fo.write("        ");
            fo.write(float_form(self.material_list[i].nu));
            fo.write(float_form(self.material_list[i].rho));
            
            fo.write("\n");
        
        #-----------------spc data------------
        fo.write("$spc data\n")
        for i in range(0,self.no_of_constrained_grid_points):
            #        fo.write(str_form(constrained_grid_point_list[i].type));
            #        fo.write(int_form(constrained_grid_point_list[i].sid));
            #        #fo.write(int_form(constrained_grid_point_list[i].g[0]));
            #
            #        fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
            #        fo.write(int_form(constrained_grid_point_list[i].c1));
            #        fo.write(float_form(constrained_grid_point_list[i].d1));
            
            fo.write(str_form(self.constrained_grid_point_list[i].type));
            fo.write(int_form(self.constrained_grid_point_list[i].sid));
            #fo.write(int_form(constrained_grid_point_list[i].g[0]));
            
            fo.write(int_form(self.constrained_grid_point_list[i].c1));
            #fo.write(int_form(global_to_loc_points[constrained_grid_point_list[i].g[0]]));
            
            fo.write(int_form(self.constrained_grid_point_list[i].g1))
            
            #fo.write(float_form(constrained_grid_point_list[i].d1));
            
            
            fo.write("\n");
        
        
        #-----------------load data------------
        fo.write("$load data\n")
        
        #   if(load_type =='FORCE'):
        
        for i in range(0, self.no_of_grid_points_w_load):
            fo.write(str_form(self.load_list[i].type));
            fo.write(int_form(self.load_list[i].sid));
            #fo.write(int_form(load_list[i].g));
            #fo.write(int_form(global_to_loc_points[load_list[i].g]));
            fo.write(int_form(self.load_list[i].g));
            
            
            fo.write(int_form(self.load_list[i].cid));
            fo.write(float_form(self.load_list[i].f));
            
            fo.write(float_form(self.load_list[i].n[0]));
            fo.write(float_form(self.load_list[i].n[1]));
            fo.write(float_form(self.load_list[i].n[2]));
            fo.write("\n");
        
        
        #if(load_type =='PRESSURE'):
        
        #    for i in range(0, no_of_elements):
        #        fo.write(str_form(self.pressure_load[i].type));
        #        fo.write(int_form(self.pressure_load[i].sid));
        #
        #        fo.write(float_form(self.pressure_load[i].p));
        #       
        #       
        #        fo.write(int_form(self.pressure_load[i].g[0]));
        #        fo.write(int_form(self.pressure_load[i].g[1]));
        #        fo.write(int_form(self.pressure_load[i].g[2]));
        #
        #        fo.write("\n");
        
        
        #------------------
        fo.write("ENDDATA");
        
        #--------close the file----------------
        
        fo.close();






    
    #------------------------read solution file----------------------

    def read_sol(self,readf06_filename):
        print "ha"

        fo_rd = open(readf06_filename,"r")
            
        displacement_count=0
        point_count=0
        for line in fo_rd:
            
            
            
            if (line[45:82]=='D I S P L A C E M E N T   V E C T O R'):
                displacement_count=displacement_count+1
                print line
                #        start = line.find(' ')
                #        end = line.find('\n')
                #        no_of_points= int(line[start:end])
                #        #print no_of_points
                #        element_pres = 1
                #        pointlist = [ grid() for i in range(no_of_points)]
                
                
                point_count=0
                for line in fo_rd:
                    displacement_count=displacement_count+1
                    
                    skip_count=0
                    if((point_count%50 ==0)and(point_count!=0)):
                        #skip 7 lines
                        for line in fo_rd:
                            skip_count=skip_count+1
                            if (skip_count==7):
                                break
                    
                    
                    
                    
                    if(displacement_count<self.no_of_points+4)and(displacement_count>3):
                        #print line
                        #point_no = line.split(' ')
                        #point_no= [float(s) for s in line.split() if s.isdigit()]
                        point_no = re.findall(r'[\d\.\d]+', line)
                        point_no2= [float(s) for s in line.split() if s.isdigit()]
                        disp1 = float(line[25:40])
                        disp2 = float(line[41:55])
                        disp3 = float(line[56:71])
                        
                        #                    print line[25:40]
                        #                    print line[41:55]
                        #                    print line[56:71]
                        
                        self.pointlist[int(point_no[0])-1].t[0]=disp1
                        self.pointlist[int(point_no[0])-1].t[1]=disp2
                        self.pointlist[int(point_no[0])-1].t[2]=disp3
                        
                        #                    pointlist[int(point_no[0])-1].t[0]=float(point_no[1])
                        #                    pointlist[int(point_no[0])-1].t[1]=float(point_no[2])
                        #                    pointlist[int(point_no[0])-1].t[2]=float(point_no[3])
                        self.pointlist[int(point_no[0])-1].r[0]=float(point_no[4])
                        self.pointlist[int(point_no[0])-1].r[1]=float(point_no[5])
                        self.pointlist[int(point_no[0])-1].r[2]=float(point_no[6])
                        point_count = int(point_no[0])
        
        
        fo_rd.close()
        
        fig = plt.figure()
        
        ax = Axes3D(fig)
        
        
        for i in range (0,self.no_of_points):
            
            
            ax.scatter(self.pointlist[i].x[0]+self.pointlist[i].t[0]*10000, self.pointlist[i].x[1]+self.pointlist[i].t[0], self.pointlist[i].x[2]+self.pointlist[i].t[0],c="red")
            

            
            ax.scatter(self.pointlist[i].x[0], self.pointlist[i].x[1], self.pointlist[i].x[2],c="blue")
        
        #plt.axis('equal')
        
        plt.savefig('su2_fsi.png',format='png')
        
        plt.show()
        plt.clf()



#---------------------write an su2 deformation file------------------------------

    def write_su2_deformation(self,su2_def_file):

        print "Writing su2 deformation file"
    
        mesh_def = open(su2_def_file,"wb")
        
        for i in range(0,self.no_of_points):
            
            #        mesh_def.write(format(pointlist[i].global_to_loc-1))
            #        mesh_def.write(" ")
            #        mesh_def.write(format((pointlist[i].t[0])+pointlist[i].x[0]))
            #
            #        mesh_def.write(" ")
            #        mesh_def.write(format(pointlist[i].t[1]+pointlist[i].x[1]))
            #
            #        mesh_def.write(" ")
            #        mesh_def.write(format(pointlist[i].t[2]+pointlist[i].x[2]))
            
            
            mesh_def.write(format(self.pointlist[i].global_to_loc-1))
            mesh_def.write(" ")
            
            #        if(pointlist[i].t[0]==0.0):
            #            mesh_def.write(format(pointlist[i].t[0]))
            #        else:
            mesh_def.write(format(self.pointlist[i].t[0]*100))
            
            mesh_def.write(" ")
            mesh_def.write(format(self.pointlist[i].t[1]))
            
            mesh_def.write(" ")
            mesh_def.write(format(self.pointlist[i].t[2]))
            
            mesh_def.write("\n")
        
        mesh_def.close()

    #format global id, x y z deformations

    
