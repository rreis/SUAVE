# class_structure.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

#---Class structure for this----------------------
from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
from SUAVE.Methods.fea_tools.pyFSI.input.read_geomach_surface_points import read_geomach_surface_points
from SUAVE.Methods.fea_tools.pyFSI.input.read_stl_meshfile import read_stl_meshfile
from SUAVE.Methods.fea_tools.compute_aircraft_loads import compute_aerodynamic_loads
from structural_dvs import structural_dvs
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt

class aircraft:
    
    def __init__(self):
    
        self.type =  'aircraft'
        self.no_of_fuselages = 1
        self.no_of_wings = 2
        self.span = 0.0
        self.wing_box_start_x = 0.0
        self.wing_box_end_x = 0.0
        self.wing_box_start_z = 0.0
        self.wing_box_end_z = 0.0
        self.MTOW = 1.0
        self.loads_marked = 0
        self.payload = 0.0
        #dv_breakdown = structural_dvs()
        #self.dv_breakdown = dv_breakdown
        self.main_wing_section = []
        self.pointlist = []
        self.structural_mesh_points = None
        self.structural_mesh_elements = None
        self.structural_mesh_material_list = None
        self.structural_mesh_shell_element_list = None
        self.structural_mesh_constrained_grid_point_list = None
        self.structural_mesh_added = 0
        self.structural_mesh_shell_map = None
	self.strut_wing = -1
	self.shell_element_lists_redone_int = 0
    



    def import_from_suave(self,vehicle):
        
        
        #full aircraft parameters
        self.type = vehicle.fea_type
        self.MTOW = vehicle.mass_properties.max_takeoff
        self.payload = vehicle.mass_properties.payload
        self.internal_pressure = 69.7*10**3 - 26.4*10**3 #69.7*10**3 - 30.1*10**3
        self.no_of_gridelements_chordwise = 50
        no_of_wings = 0
        no_of_fuselages = 0
	
	self.stype = vehicle.fea_type
        

	
	if((vehicle.fea_type == "Strut_Braced") or (vehicle.fea_type == "Strut_Braced2")):
	    for iwing in range(0,len(vehicle.wing_fea)):
		if(vehicle.wing[vehicle.wing_fea[iwing]].tag == "strut"):
		    self.strut_wing = iwing
		    break
		
        
        wing_fea = vehicle.wing_fea
        fuselage_fea = vehicle.fuselage_fea
        
        #print wing_fea
        
        
        if wing_fea:
            no_of_wings = len(wing_fea)
        
        if fuselage_fea:
            no_of_fuselages = len(fuselage_fea)
        
        no_of_intersections = vehicle.no_of_intersections
        no_of_miscellaneous = vehicle.no_of_miscellaneous
        
        self.number_of_intersections = no_of_intersections
        self.no_of_miscellaneous = no_of_miscellaneous
        
        self.intersection_tag = vehicle.intersection_tag

        
        
        
        no_of_wing_sections = [int() for i in range(no_of_wings)]
        for i in range(0,no_of_wings):
            no_of_wing_sections[i] = 0
        
        
        for i in range(0,no_of_wings):
            no_of_wing_sections[i] += vehicle.wings[wing_fea[i]].no_of_sections
        
        
        main_wing  = [ wing() for i in range(no_of_wings)]
        
        fuselages  = [ fuselage() for i in range(no_of_fuselages)]
        
        
        #----loop over the wings-----------
        
        for i in range(0,no_of_wings):
            
            main_wing_section  = [wing_section() for mnw in range(vehicle.wings[wing_fea[i]].no_of_sections)]
            
            #print i,int(wing_fea[i]),vehicle.wings[wing_fea[i]].no_of_sections
            
            for j in range(0,vehicle.wings[wing_fea[i]].no_of_sections):
                main_wing_section[j].type = vehicle.wings[wing_fea[i]].wing_sections[j].type
                main_wing_section[j].root_chord = vehicle.wings[wing_fea[i]].wing_sections[j].root_chord
                main_wing_section[j].tip_chord = vehicle.wings[wing_fea[i]].wing_sections[j].tip_chord
                main_wing_section[j].root_origin = vehicle.wings[wing_fea[i]].wing_sections[j].root_origin
                main_wing_section[j].tip_origin = vehicle.wings[wing_fea[i]].wing_sections[j].tip_origin
                main_wing_section[j].mid_origin = vehicle.wings[wing_fea[i]].wing_sections[j].mid_origin
                main_wing_section[j].span = vehicle.wings[wing_fea[i]].wing_sections[j].span
                main_wing_section[j].sweep = vehicle.wings[wing_fea[i]].wing_sections[j].sweep
        
            
            main_wing[i].tag = vehicle.wings[wing_fea[i]].geometry_tag
            main_wing[i].main_wing_section = main_wing_section
            main_wing[i].no_of_sections = vehicle.wings[wing_fea[i]].no_of_sections
            main_wing[i].type =  'wing_section'
            main_wing[i].root_chord = vehicle.wings[wing_fea[i]].chords.root
            main_wing[i].tip_chord = vehicle.wings[wing_fea[i]].chords.tip
            main_wing[i].span = vehicle.wings[wing_fea[i]].spans.projected
            #main_wing[i].origin = vehicle.wings[wing_fea[i]].no_of_sections
            main_wing[i].root_origin = vehicle.wings[wing_fea[i]].root_origin
            main_wing[i].tip_origin = vehicle.wings[wing_fea[i]].tip_origin
            main_wing[i].sweep = vehicle.wings[wing_fea[i]].sweep
            main_wing[i].airfoil = vehicle.wings[wing_fea[i]].airfoil
            main_wing[i].element_area = vehicle.wings[wing_fea[i]].element_area
            main_wing[i].vertical = vehicle.wings[wing_fea[i]].vertical
            main_wing[i].structural_dv = vehicle.wings[wing_fea[i]].structural_dv
            main_wing[i].sizing_lift = vehicle.wings[wing_fea[i]].sizing_lift
            main_wing[i].max_x = vehicle.wings[wing_fea[i]].max_x
            main_wing[i].max_y = vehicle.wings[wing_fea[i]].max_y
            main_wing[i].max_z = vehicle.wings[wing_fea[i]].max_z
            main_wing[i].fuel_load = vehicle.wings[wing_fea[i]].fuel_load
            main_wing[i].load_scaling = vehicle.wings[wing_fea[i]].load_scaling
            
            print main_wing[i].tag,main_wing[i].structural_dv
            
            
            if(vehicle.wings[wing_fea[i]].strut_presence == 1):
            
            #if(i==0):
                main_wing[i].strut_location = vehicle.wings[wing_fea[i]].strut_location
                main_wing[i].strut_section = vehicle.wings[wing_fea[i]].strut_section
                main_wing[i].lv_location = vehicle.wings[wing_fea[i]].lv_location
                main_wing[i].fuel_load = vehicle.wings[wing_fea[i]].fuel_load





        #----loop over the fuselages-----------

        for i in range(0,no_of_fuselages):
            fuselages[i].tag = vehicle.fuselages[fuselage_fea[i]].geometry_tag
            fuselages[i].type = 'fuselage'
            fuselages[i].root_origin = vehicle.fuselages[fuselage_fea[i]].root_origin
            fuselages[i].tip_origin = vehicle.fuselages[fuselage_fea[i]].tip_origin
            fuselages[i].diameter = vehicle.fuselages[fuselage_fea[i]].effective_diameter
            fuselages[i].length = vehicle.fuselages[fuselage_fea[i]].lengths.total
            fuselages[i].structural_dv = vehicle.fuselages[fuselage_fea[i]].structural_dv




        self.main_wing = main_wing
        self.fuselage = fuselages
        


        dv_breakdown = structural_dvs(no_of_wings,no_of_fuselages,no_of_intersections,no_of_miscellaneous)


        for i in range(0,no_of_fuselages):
            dv_breakdown.fuselages[i].tag = "fuse"
            dv_breakdown.fuselages[i].top.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].bottom.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].left.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].right.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].front.required_no_of_elements = 1 #fuselages[i].structural_dv
            dv_breakdown.fuselages[i].rear.required_no_of_elements = 1 #fuselages[i].structural_dv

            dv_breakdown.fuselages[i].r1.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].r2.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].r3.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].r4.required_no_of_elements = fuselages[i].structural_dv

            dv_breakdown.fuselages[i].l1.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].l2.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].l3.required_no_of_elements = fuselages[i].structural_dv
            dv_breakdown.fuselages[i].l4.required_no_of_elements = fuselages[i].structural_dv



        for i in range(0,no_of_wings):

            dv_breakdown.wings[i].tag = main_wing[i].tag
            dv_breakdown.wings[i].upper.required_no_of_elements = main_wing[i].structural_dv
            dv_breakdown.wings[i].lower.required_no_of_elements = main_wing[i].structural_dv
            dv_breakdown.wings[i].tip.required_no_of_elements = 1 #main_wing[i].structural_dv
            dv_breakdown.wings[i].spars.required_no_of_elements = main_wing[i].structural_dv
            dv_breakdown.wings[i].ribs.required_no_of_elements = main_wing[i].structural_dv

            print dv_breakdown.wings[i].tag,dv_breakdown.wings[i].upper.required_no_of_elements,dv_breakdown.wings[i].lower.required_no_of_elements,dv_breakdown.wings[i].tip.required_no_of_elements,dv_breakdown.wings[i].spars.required_no_of_elements,dv_breakdown.wings[i].ribs.required_no_of_elements

        #intersections are currently done manually

        dv_value = 1


        for  i in range(0,no_of_intersections):
            
            dv_breakdown.intersections[i].tag = vehicle.intersection_tag[i] #"int_"+str(i)
            dv_breakdown.intersections[i].dv.required_no_of_elements = dv_value

#            dv_breakdown.intersections[i].tag = "lwing_fuse"
#            dv_breakdown.intersections[i].dv.required_no_of_elements = dv_value

#            dv_breakdown.intersections[1].tag = "ltail_vtail"
#            dv_breakdown.intersections[1].dv.required_no_of_elements = dv_value
#
#            dv_breakdown.intersections[2].tag = "vtail_fuse"
#            dv_breakdown.intersections[2].dv.required_no_of_elements = dv_value
#
#            dv_breakdown.intersections[3].tag = "lstrut_lwing"
#            dv_breakdown.intersections[3].dv.required_no_of_elements = dv_value
#
#            dv_breakdown.intersections[4].tag = "lstrut_fuse"
#            dv_breakdown.intersections[4].dv.required_no_of_elements = dv_value



        for  i in range(0,no_of_miscellaneous):
            
            dv_breakdown.miscellaneous[i].tag = vehicle.miscellaneous_tag[i] #"misc_"+str(i)
            dv_breakdown.miscellaneous[i].dv.required_no_of_elements = dv_value

#            dv_breakdown.miscellaneous[0].tag = "lwing_i_i1"
#            dv_breakdown.miscellaneous[0].dv.required_no_of_elements = dv_value
#
#            dv_breakdown.miscellaneous[1].tag = "lwing_i_i2"
#            dv_breakdown.miscellaneous[1].dv.required_no_of_elements = dv_value
#
#            dv_breakdown.miscellaneous[2].tag = "fus_Misc_1"
#            dv_breakdown.miscellaneous[2].dv.required_no_of_elements = dv_value
#
#            dv_breakdown.miscellaneous[3].tag = "fus_Misc_2"
#            dv_breakdown.miscellaneous[3].dv.required_no_of_elements = dv_value




        self.dv_breakdown = dv_breakdown
        self.dv_breakdown.compute_structural_dvs()




    def read_surface_discretization(self,mesh_filename):
        self.pointlist =read_geomach_surface_points(mesh_filename)



        #mark the points as wing or fuselage
        for i in range(0,len(self.pointlist)):
    
            if(self.pointlist[i].x[0]>self.wing_box_start_x) and (self.pointlist[i].x[0]<self.wing_box_end_x) and (self.pointlist[i].x[2]>self.wing_box_start_z) and (self.pointlist[i].x[2]<self.wing_box_end_z):
    
                self.pointlist[i].part = "w"
            


            elif(self.pointlist[i].x[0]>self.fuselage_start_x) and (self.pointlist[i].x[0]<self.fuselage_end_x) and (self.pointlist[i].x[2]>self.fuselage_start_z) and (self.pointlist[i].x[2]<self.fuselage_end_z):
    
                self.pointlist[i].part = "f"



	    else:
		self.pointlist[i].part = "i"






    def read_stl_file(self,mesh_filename):
        [element_list,element_count] = read_stl_meshfile(mesh_filename)
        self.elemlist = element_list
        self.no_of_elements = element_count
    
    
        pointlist = [ grid() for i in range(self.no_of_elements)]
        

        
        for i in range(0,len(pointlist)):
            pointlist[i].x[0] = self.elemlist[i].centroid[0]
            pointlist[i].x[1] = self.elemlist[i].centroid[1]
            pointlist[i].x[2] = self.elemlist[i].centroid[2]
            pointlist[i].normal = self.elemlist[i].normal_g
            pointlist[i].Sarea = self.elemlist[i].Sarea
            pointlist[i].part = "i"
            pointlist[i].chord = 0.0
    
    
        self.pointlist = pointlist
        

    
        #mark the points as wing or fuselage
        for i in range(0,len(self.pointlist)):
            
            for wng in range(0,len(self.main_wing)):
            #for wng in range(0,2):
            
                if(self.pointlist[i].x[0]>self.main_wing[wng].wing_box_start_x) and (self.pointlist[i].x[0]<self.main_wing[wng].wing_box_end_x) and (self.pointlist[i].x[2]>self.main_wing[wng].wing_box_start_z) and (self.pointlist[i].x[2]<self.main_wing[wng].wing_box_end_z)and (self.pointlist[i].x[1]>self.main_wing[wng].wing_box_start_y) and (self.pointlist[i].x[1]<self.main_wing[wng].wing_box_end_y):
                    
                    self.pointlist[i].part = "w_"+str(wng)
                    self.pointlist[i].chord = 0.0



            if(self.fuselage):
                for fus in range(0,len(self.fuselage)):
                    if(self.pointlist[i].x[0]>self.fuselage[fus].fuselage_start_x) and (self.pointlist[i].x[0]<self.fuselage[fus].fuselage_end_x) and (self.pointlist[i].x[2]>self.fuselage[fus].fuselage_start_z) and (self.pointlist[i].x[2]<self.fuselage[fus].fuselage_end_z):
                        
                        self.pointlist[i].part = "f_"+str(fus)
                        self.pointlist[i].chord = 0.0
            
            



    def visualize_loads(self,tec_file,matlab_file,pyplot_file):
        print "Writing tecplot loads file"
        
#        mesh_def2 = open(matlab_file,"wb")
#            
#        for i in range(0,len(self.pointlist)):
#            
#            if (np.abs(self.pointlist[i].f[1])>0.000001):
#                mesh_def2.write(format(self.pointlist[i].x[0]))
#                mesh_def2.write("\t")
#                mesh_def2.write(format(self.pointlist[i].x[1]))
#                mesh_def2.write("\t")
#                mesh_def2.write(format(self.pointlist[i].x[2]))
#                mesh_def2.write("\t")
#                mesh_def2.write(format(self.pointlist[i].f[0]))
#                mesh_def2.write("\t")
#                mesh_def2.write(format(self.pointlist[i].f[1]))
#                mesh_def2.write("\t")
#                mesh_def2.write(format(self.pointlist[i].f[2]))
#                mesh_def2.write("\t")
#                mesh_def2.write(format(self.pointlist[i].chord))
#                mesh_def2.write("\n")
#
#        mesh_def2.close()
#


        #visualize using matplotlib
        fig = plt.figure(1)
#        plt.plot(design_runs,constraint_list,'-*')
        plt.xlabel('x axis')
        plt.ylabel('y axis')
#        plt.savefig('constraint_nasa_orieo.png')

        ax = Axes3D(fig)


        for i in range (0,len(self.pointlist)):
            #if(np.abs(self.pointlist[i].f[1])>0.000001):
            if(self.pointlist[i].part == "w_0"):
                
                ax.scatter(self.pointlist[i].x[0], self.pointlist[i].x[1], self.pointlist[i].f[2],c="red")
        
        #else:
        #ax.scatter(self.pointlist[i].x[0], self.pointlist[i].x[1], self.pointlist[i].x[2],c="white")


        plt.savefig(pyplot_file,format='png')
    
        plt.show()
        plt.clf()



        loads = np.zeros(len(self.pointlist))
        y_position = np.zeros(len(self.pointlist))
        loads_chord = np.zeros(len(self.pointlist))
        chord = np.zeros(len(self.pointlist))
        for i in range(0,len(self.pointlist)):
            
            if(self.pointlist[i].part == "w_0"):
                loads[i] = self.pointlist[i].f[2]
                y_position[i] = self.pointlist[i].x[1]
                loads_chord[i] = self.pointlist[i].f[2]*self.pointlist[i].chord
                chord[i] = self.pointlist[i].chord


        fig2 = plt.figure(2)
        plt.xlabel('y location')
        plt.ylabel('loads')
        plt.plot(y_position,loads,'*')
        plt.savefig("loads_distribution.png",format='png')
        plt.clf()


        fig3 = plt.figure(3)
        plt.xlabel('y location')
        plt.ylabel('loads * chord')
        plt.plot(y_position,loads_chord,'*')
        plt.savefig("loads_chord_distribution.png",format='png')
        plt.clf()


        fig4 = plt.figure(4)
        plt.xlabel('y location')
        plt.ylabel('chord')
        plt.plot(y_position,chord,'*')
        plt.savefig("chord_distribution.png",format='png')
        plt.clf()


    def compute(self):
        
        for i in range(0,len(self.main_wing)):
        
        #add coordinates
        
            self.main_wing[i].span = np.linalg.norm(np.array(self.main_wing[0].tip_origin) - np.array(self.main_wing[0].root_origin))
            self.main_wing[i].wing_spans = np.zeros(len(self.main_wing[i].main_wing_section))
            self.main_wing[i].wing_spans_cumulative = np.zeros(len(self.main_wing[i].main_wing_section)+1)
            
            self.main_wing[i].summed_span = 0.0
            self.main_wing[i].wing_spans_cumulative[0] = 0.0
            self.main_wing[i].spanwise_direction = np.array(self.main_wing[i].tip_origin) - np.array(self.main_wing[i].root_origin)
            self.main_wing[i].spanwise_direction = self.main_wing[i].spanwise_direction/np.linalg.norm(self.main_wing[i].spanwise_direction)
            
            
            # learn the model
            spanwise_coord_wing = np.array([0,self.main_wing[i].span])
            spanwise_chord_wing = np.array([self.main_wing[i].root_chord,self.main_wing[i].tip_chord])
            
            chord_surrogate_wing = np.poly1d(np.polyfit(spanwise_coord_wing, spanwise_chord_wing ,1))
            self.main_wing[i].chord_surrogate = chord_surrogate_wing
        
            for j in range(len(self.main_wing[i].main_wing_section)):
                self.main_wing[i].wing_spans[j] = self.main_wing[i].main_wing_section[j].span
                
                self.main_wing[i].wing_spans_cumulative[j+1] = self.main_wing[i].wing_spans_cumulative[j] + self.main_wing[i].main_wing_section[j].span
    
                self.main_wing[i].summed_span+= self.main_wing[i].main_wing_section[j].span
                self.main_wing[i].main_wing_section[j].spanwise_direction = np.array(self.main_wing[i].main_wing_section[j].tip_origin) - np.array(self.main_wing[i].main_wing_section[j].root_origin)
    
                #setup interpolation
                # learn the model
                spanwise_coord = np.array([0,self.main_wing[i].main_wing_section[j].span])
                spanwise_chord = np.array([self.main_wing[i].main_wing_section[j].root_chord,self.main_wing[i].main_wing_section[j].tip_chord])
                
                #what happens for multisection main wings
                chord_surrogate = np.poly1d(np.polyfit(spanwise_coord, spanwise_chord ,1))
                self.main_wing[i].main_wing_section[j].chord_surrogate = chord_surrogate
    
    
    
    
        
        #get the limit
        
        
        #get the bounding boxes from the structural meshes generated by geomach
        
        #loop over the corresponding elements and find the max coordinates
        
        #generate the bounding boxes over the wings and fuselage
        for wng in range(0,len(self.main_wing)):
            
            #get the limit and compute the interpolations
            
        
        
        #loop over the wings
        
            #loop over the wings to get the wing box
            min_x = self.main_wing[wng].main_wing_section[0].root_origin[0]
            min_z = self.main_wing[wng].main_wing_section[0].root_origin[2]
            min_y = self.main_wing[wng].main_wing_section[0].root_origin[1]
            
            max_x = self.main_wing[wng].main_wing_section[0].root_origin[0]
            max_z = self.main_wing[wng].main_wing_section[0].root_origin[2]
            max_y = self.main_wing[wng].main_wing_section[0].root_origin[1]
        
            for i in range(0,self.main_wing[wng].no_of_sections):


                if self.main_wing[wng].vertical == 0:
        
                    if (self.main_wing[wng].main_wing_section[i].root_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].root_chord>max_x) :
                        max_x = self.main_wing[wng].main_wing_section[i].root_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].root_chord

                    if (self.main_wing[wng].main_wing_section[i].tip_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].tip_chord>max_x) :
                        max_x = self.main_wing[wng].main_wing_section[i].tip_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].tip_chord

                    if (self.main_wing[wng].main_wing_section[i].root_origin[0] -0.25*self.main_wing[wng].main_wing_section[i].root_chord<min_x) :
                        min_x = self.main_wing[wng].main_wing_section[i].root_origin[0] -0.25*self.main_wing[wng].main_wing_section[i].root_chord

                    if (self.main_wing[wng].main_wing_section[i].tip_origin[0]-0.25*self.main_wing[wng].main_wing_section[i].tip_chord<min_x) :
                        min_x = self.main_wing[wng].main_wing_section[i].tip_origin[0]-0.25*self.main_wing[wng].main_wing_section[i].tip_chord



                    if (self.main_wing[wng].main_wing_section[i].root_origin[2]>max_z) :
                        max_z = self.main_wing[wng].main_wing_section[i].root_origin[2]

                    if (self.main_wing[wng].main_wing_section[i].tip_origin[2]>max_z) :
                        max_z = self.main_wing[wng].main_wing_section[i].tip_origin[2]
                
                    if (self.main_wing[wng].main_wing_section[i].root_origin[2]<min_z) :
                        min_z = self.main_wing[wng].main_wing_section[i].root_origin[2]
                    
                    if (self.main_wing[wng].main_wing_section[i].root_origin[2]<min_z) :
                        min_z = self.main_wing[wng].main_wing_section[i].tip_origin[2]
            
            
            
            
                    #y value
                    if (self.main_wing[wng].main_wing_section[i].root_origin[1]>max_y) :
                        max_y = self.main_wing[wng].main_wing_section[i].root_origin[1]

                    if (self.main_wing[wng].main_wing_section[i].tip_origin[1]>max_y) :
                        max_y = self.main_wing[wng].main_wing_section[i].tip_origin[1]
                    
                    if (self.main_wing[wng].main_wing_section[i].root_origin[1]<min_y) :
                        min_y = self.main_wing[wng].main_wing_section[i].root_origin[1]
                    
                    if (self.main_wing[wng].main_wing_section[i].tip_origin[1]<min_y) :
                        min_y = self.main_wing[wng].main_wing_section[i].tip_origin[1]
                            
                            
                            
                    self.main_wing[wng].wing_box_start_x = min_x
                    self.main_wing[wng].wing_box_end_x = max_x*1.3
                    self.main_wing[wng].wing_box_start_z = min_z
                    self.main_wing[wng].wing_box_end_z = self.main_wing[wng].main_wing_section[0].root_origin[2] + self.main_wing[wng].span    #max_z
                                    
                    self.main_wing[wng].wing_box_start_y = min_y - 0.2*self.main_wing[wng].root_chord
                    self.main_wing[wng].wing_box_end_y = max_y + 0.2*self.main_wing[wng].root_chord
    
    
                elif self.main_wing[wng].vertical == 1:
                
                
                    if (self.main_wing[wng].main_wing_section[i].root_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].root_chord>max_x) :
                        max_x = self.main_wing[wng].main_wing_section[i].root_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].root_chord
                    
                    if (self.main_wing[wng].main_wing_section[i].tip_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].tip_chord>max_x) :
                        max_x = self.main_wing[wng].main_wing_section[i].tip_origin[0]+0.75*self.main_wing[wng].main_wing_section[i].tip_chord
                    
                    if (self.main_wing[wng].main_wing_section[i].root_origin[0] -0.25*self.main_wing[wng].main_wing_section[i].root_chord<min_x) :
                        min_x = self.main_wing[wng].main_wing_section[i].root_origin[0] -0.25*self.main_wing[wng].main_wing_section[i].root_chord
                    
                    if (self.main_wing[wng].main_wing_section[i].tip_origin[0]-0.25*self.main_wing[wng].main_wing_section[i].tip_chord<min_x) :
                        min_x = self.main_wing[wng].main_wing_section[i].tip_origin[0]-0.25*self.main_wing[wng].main_wing_section[i].tip_chord
                    
                    
                    
                    if (self.main_wing[wng].main_wing_section[i].root_origin[2]>max_z) :
                        max_z = self.main_wing[wng].main_wing_section[i].root_origin[2]
                    
                    if (self.main_wing[wng].main_wing_section[i].tip_origin[2]>max_z) :
                        max_z = self.main_wing[wng].main_wing_section[i].tip_origin[2]
                    
                    if (self.main_wing[wng].main_wing_section[i].root_origin[2]<min_z) :
                        min_z = self.main_wing[wng].main_wing_section[i].root_origin[2]
                    
                    if (self.main_wing[wng].main_wing_section[i].tip_origin[2]<min_z) :
                        min_z = self.main_wing[wng].main_wing_section[i].tip_origin[2]
                    
                    
                    
                    
                    #y value
                    if (self.main_wing[wng].main_wing_section[i].root_origin[1]>max_y) :
                        max_y = self.main_wing[wng].main_wing_section[i].root_origin[1]
                    
                    if (self.main_wing[wng].main_wing_section[i].tip_origin[1]>max_y) :
                        max_y = self.main_wing[wng].main_wing_section[i].tip_origin[1]
                    
                    if (self.main_wing[wng].main_wing_section[i].root_origin[1]<min_y) :
                        min_y = self.main_wing[wng].main_wing_section[i].root_origin[1]
                    
                    if (self.main_wing[wng].main_wing_section[i].tip_origin[1]<min_y) :
                        min_y = self.main_wing[wng].main_wing_section[i].tip_origin[1]
        
        
        
        



                    self.main_wing[wng].wing_box_start_x = min_x
                    self.main_wing[wng].wing_box_end_x = max_x*1.3
                    self.main_wing[wng].wing_box_start_z = min_z - 0.2*self.main_wing[wng].root_chord
                    self.main_wing[wng].wing_box_end_z = max_z + 0.2*self.main_wing[wng].root_chord   #max_z
                    
                    self.main_wing[wng].wing_box_start_y = min_y
                    self.main_wing[wng].wing_box_end_y = self.main_wing[wng].main_wing_section[0].root_origin[1] + self.main_wing[wng].span




            for isurr in range(0,5):
                print self.main_wing[1].chord_surrogate(float(isurr))
    
            
            print "Wing : ",wng,"\n"
            print "wing_box_start_x : ",self.main_wing[wng].wing_box_start_x,"\n"
            print "wing_box_end_x : ",self.main_wing[wng].wing_box_end_x,"\n"
            print "wing_box_start_y : ",self.main_wing[wng].wing_box_start_y,"\n"
            print "wing_box_end_y : ",self.main_wing[wng].wing_box_end_y,"\n"
            print "wing_box_start_z : ",self.main_wing[wng].wing_box_start_z,"\n"
            print "wing_box_end_z : ",self.main_wing[wng].wing_box_end_z,"\n"
            print "\n"


        #loop over the fuselages
        if(self.fuselage):
            for fus in range(0,len(self.fuselage)):

                self.fuselage[fus].fuselage_start_x = 0.0
                self.fuselage[fus].fuselage_end_x = self.fuselage[fus].fuselage_start_x + 0.9*self.fuselage[fus].length
                self.fuselage[fus].fuselage_start_z = 0.0
                self.fuselage[fus].fuselage_end_z = self.fuselage[fus].diameter
		
		
	
	if((self.stype == "Strut_Braced") or (self.stype == "Strut_Braced2") or (self.stype == "Strut_braced") or (self.stype == "Strut_braced2")):
	    self.compute_strut_location()


    def compute_strut_location(self):
	
	strut_wing_index = self.strut_wing
	
        strut_location_wing = self.main_wing[0].strut_location
        #lv_location_wing = self.main_wing[0].lv_location
        #lv_location_strut = self.main_wing[3].lv_location
        main_wing_span =  np.linalg.norm(np.array(self.main_wing[0].tip_origin) - np.array(self.main_wing[0].root_origin))
        main_wing_rc = self.main_wing[0].root_chord
        main_wing_tc = self.main_wing[0].tip_chord
        max_strut_chord = self.main_wing[0].root_chord + (main_wing_tc - main_wing_rc)*strut_location_wing
        
        
        main_wing_direction = (np.array(self.main_wing[0].tip_origin) -np.array(self.main_wing[0].root_origin))/main_wing_span
        
        strut_span = np.linalg.norm(np.array(self.main_wing[strut_wing_index].tip_origin) - np.array(self.main_wing[strut_wing_index].root_origin))
        
        strut_direction = (np.array(self.main_wing[strut_wing_index].tip_origin) - np.array(self.main_wing[strut_wing_index].root_origin))/np.linalg.norm(np.array(self.main_wing[strut_wing_index].tip_origin) - np.array(self.main_wing[strut_wing_index].root_origin))
        
        #loop over the main wing and compute the strut location based on the wing location assume on the 1st section
        strut_position_wing = np.array(self.main_wing[0].root_origin) + main_wing_direction*strut_location_wing*main_wing_span
        strut_position_tip = np.array(self.main_wing[0].root_origin) + main_wing_direction*strut_location_wing*main_wing_span*1.0 - np.array([0.0,0.5,0.0])
        

	


        #add the mid section
        self.main_wing[0].main_wing_section[0].mid_origin = strut_position_wing
        

        #update the strut
        self.main_wing[strut_wing_index].tip_origin = strut_position_tip #strut_position_wing #[15.0,1.0,14.4]
        self.main_wing[strut_wing_index].span = self.main_wing[strut_wing_index].tip_origin[2] - self.main_wing[strut_wing_index].root_origin[2]
        self.main_wing[strut_wing_index].sweep = np.arctan((self.main_wing[strut_wing_index].tip_origin[2]- self.main_wing[strut_wing_index].root_origin[2])/(self.main_wing[strut_wing_index].tip_origin[0]- self.main_wing[strut_wing_index].root_origin[0]))
        self.main_wing[strut_wing_index].tip_chord = max_strut_chord * 0.8
        
        
        self.main_wing[strut_wing_index].main_wing_section[0].tip_origin = strut_position_tip #strut_position_wing
        self.main_wing[strut_wing_index].main_wing_section[0].sweep = self.main_wing[strut_wing_index].sweep
        self.main_wing[strut_wing_index].main_wing_section[0].span = self.main_wing[strut_wing_index].span
        
        print "strut location :",self.main_wing[strut_wing_index].tip_origin
        print "wing mid location :",strut_position_wing
        
        
#        #update the lv

#        lv_position_wing = np.array(self.main_wing[0].root_origin) + main_wing_direction*lv_location_strut*main_wing_span
#        
#        
#        lv_position_strut = np.array(self.main_wing[3].root_origin) + lv_location_strut*strut_direction*strut_span

#        self.main_wing[4].root_origin = lv_position_strut  #[15.0,1.0,14.4]
#        self.main_wing[4].tip_origin = lv_position_wing #[15.0,1.0,14.4]
#        self.main_wing[4].span = self.main_wing[4].tip_origin[2] - self.main_wing[4].root_origin[2]
#        self.main_wing[4].sweep = 0.0 #np.arctan((main_wing[4].tip_origin[2]- main_wing[4].root_origin[2])/(main_wing[4].tip_origin[0]- main_wing[4].root_origin[0]))
#        
#        
#        self.main_wing[4].main_wing_section[0].root_origin = lv_position_strut
#        self.main_wing[4].main_wing_section[0].tip_origin = lv_position_wing
#        self.main_wing[4].main_wing_section[0].sweep = self.main_wing[4].sweep
#        self.main_wing[4].main_wing_section[0].span = self.main_wing[4].span

#        print "strut_location computing"
#        print "main_wing_span",main_wing_span
#        print "main_wing_direction",main_wing_direction
#        print "strut_location_wing",strut_location_wing
#        print "strut_position_wing",strut_position_wing


    def set_structural_dvs(self,dv_value):
        print

    def compute_loading_model(self):
        print
        #loop over the wings and for each wing, set up the mesh and the elements
        #the mesh is fine with 100 rows spanwise and 20 elements chordwise

        #call the
        #aircraft_aero_mesh_generation(aircraft)








class wing:
    
    
    def __init__(self):
        
        self.type =  'wing_section'
        self.no_of_wing_sections = 0
        self.root_chord = 1.0
        self.tip_chord = 1.0
        self.span = 1.0
        self.sweep = 0.0
        self.origin = [0.0,0.0,0.0]
        self.root_origin = [0.0,0.0,0.0]
        self.tip_origin = [0.0,0.0,0.0]
        self.airfoil = "rae2012"
        self.element_area = 1.0
        self.fuel_load = 0.0

#     def compute_wing_box(self):
#        print




class wing_section:


    def __init__(self):
    
        self.type =  'wing_section'
        self.root_chord = 1.0
        self.tip_chord = 1.0
        self.span = 1.0
        self.sweep = 0.0
        self.root_origin = [0.0,0.0,0.0]
        self.tip_origin = [0.0,0.0,0.0]
        self.mid_origin = np.zeros(3)




class fuselage:
    
    
    def __init__(self):
        
        self.type =  'fuselage'
        self.diameter = 1.0
        self.length = 1.0
        self.origin = [0.0,0.0,0.0]



