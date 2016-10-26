import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#ensure that element centroid computed

def compute_element_based_aircraft_loads(elemlist,pointlist,aircraft):



    #loop over the wings
    
    max_distance = 0.0
    
    
    for ipoint in range(0,len(pointlist)):
        pointlist[ipoint].aeroloaded = 0

    for i in range(0,len(aircraft.main_wing)):
        
        print "main wing loading : ",aircraft.main_wing[i].sizing_lift
        temp_sizing_lift = aircraft.main_wing[i].sizing_lift
        aircraft.main_wing[i].sizing_lift = aircraft.main_wing[i].sizing_lift*aircraft.main_wing[i].load_scaling
        

        wing_i_surface_element_numbers_l = set(aircraft.dv_breakdown.wings[i].lower.new_element_nos)
        wing_i_surface_element_numbers_u = set(aircraft.dv_breakdown.wings[i].upper.new_element_nos)
        aircraft.main_wing[i].total_force = 0.0


        print "Print wing u surface numbers :",wing_i_surface_element_numbers_u
        print "Print wing l surface numbers :",wing_i_surface_element_numbers_l


        for j in range(0,len(elemlist)):
            if (elemlist[j].pid in wing_i_surface_element_numbers_u):

            #compute the point direction relative to the wing root

                local_point = np.array(elemlist[j].centroid)
                

                point_dir = (local_point - np.array(aircraft.main_wing[i].root_origin))
                point_dir = point_dir/np.linalg.norm(point_dir)
                
                wing_axis = np.array([1.0,0.0,0.0])
                #point_projection_angle = np.arccos(np.dot(point_dir,aircraft.main_wing[i].spanwise_direction)) #assumes both are unit vectors
                point_projection_angle = np.arccos(np.dot(point_dir,wing_axis)) #assumes both are unit vectors

                elemlist[j].global_spanwise_coordinate = (np.linalg.norm(local_point - np.array(aircraft.main_wing[i].root_origin))*np.sin(point_projection_angle))/aircraft.main_wing[i].span  #np.cos(point_projection_angle)

                elemlist[j].local_chord = aircraft.main_wing[i].chord_surrogate(elemlist[j].global_spanwise_coordinate)

                max_distance = np.maximum(max_distance,elemlist[j].global_spanwise_coordinate)
                #breakup the load

                max_load   = 2.0*aircraft.main_wing[i].sizing_lift/aircraft.main_wing[i].span
                load_scale = max_load
                element_load = load_scale*compute_spanwise_load(elemlist[j])*compute_chordwise_load(elemlist[j])*elemlist[j].area
                
                
                
                aircraft.main_wing[i].total_force += element_load
                
                

                if(elemlist[j].type == "CTRIA3"):
                    for ijk in range(0,3):
                        pointlist[elemlist[j].g[ijk]].load+= 0.33*element_load
                        if(aircraft.main_wing[i].vertical == 0):
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 1.0/3.0*element_load
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 0.0
                        else:
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 1.0/3.0*element_load




                if(elemlist[j].type == "CQUAD4"):
                    for ijk in range(0,4):
                        pointlist[elemlist[j].g[ijk]].load+= 0.25*element_load
                        if(aircraft.main_wing[i].vertical == 0):
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 0.25*element_load
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 0.0
                        else:
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 0.25*element_load


            if (elemlist[j].pid in wing_i_surface_element_numbers_l):

            #compute the point direction relative to the wing root

                local_point = np.array(elemlist[j].centroid)

                point_dir = (local_point - np.array(aircraft.main_wing[i].root_origin))
                
                local_span = np.linalg.norm(point_dir)
                
                point_dir = point_dir/np.linalg.norm(point_dir)
                

                
                point_projection_angle = np.arccos(np.dot(point_dir,aircraft.main_wing[i].spanwise_direction)) #assumes both are unit vectors

                elemlist[j].global_spanwise_coordinate = local_span*np.cos(point_projection_angle)/aircraft.main_wing[i].summed_span

                elemlist[j].local_chord = aircraft.main_wing[i].chord_surrogate(elemlist[j].global_spanwise_coordinate)


                #breakup the load

                max_load   = 2.0*aircraft.main_wing[i].sizing_lift/aircraft.main_wing[i].span
                load_scale = max_load
                element_load = load_scale*compute_spanwise_load(elemlist[j])*compute_chordwise_load(elemlist[j])
                elemlist[j].pressure = element_load
                element_load = element_load*elemlist[j].area
                
                aircraft.main_wing[i].total_force += element_load

                if(elemlist[j].type == "CTRIA3"):
                    for ijk in range(0,3):
                        pointlist[elemlist[j].g[ijk]].load+= 0.33*element_load
                        if(aircraft.main_wing[i].vertical == 0):
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 1.0/3.0*element_load
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 0.0
                        else:
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 1.0/3.0*element_load




                if(elemlist[j].type == "CQUAD4"):
                    for ijk in range(0,4):
                        pointlist[elemlist[j].g[ijk]].load+= 0.25*element_load
                        if(aircraft.main_wing[i].vertical == 0):
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 0.25*element_load
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 0.0
                        else:
                            pointlist[elemlist[j].g[ijk]-1].f[0] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[1] += 0.0
                            pointlist[elemlist[j].g[ijk]-1].f[2] += 0.25*element_load



        print "unscaled load : ",aircraft.main_wing[i].total_force
        local_load_scaling = temp_sizing_lift/aircraft.main_wing[i].total_force
        
        if(np.abs(aircraft.main_wing[i].total_force) < 0.00000001):
            local_load_scaling = 0.0
        
        
        print "local_load_scaling : ",local_load_scaling
        
        aircraft.main_wing[i].total_force = 0.0
        
        for ielem in range(0,len(elemlist)):
        
            if ((elemlist[ielem].pid in wing_i_surface_element_numbers_u) or (elemlist[ielem].pid in wing_i_surface_element_numbers_l)):
        
                if(elemlist[ielem].type == "CTRIA3"):
                    for ijk in range(0,3):
                        
                        if(pointlist[elemlist[ielem].g[ijk]-1].aeroloaded == 0):
                            pointlist[elemlist[ielem].g[ijk]-1].f[0] = pointlist[elemlist[ielem].g[ijk]-1].f[0]*local_load_scaling
                            pointlist[elemlist[ielem].g[ijk]-1].f[1] = pointlist[elemlist[ielem].g[ijk]-1].f[1]*local_load_scaling
                            pointlist[elemlist[ielem].g[ijk]-1].f[2] = pointlist[elemlist[ielem].g[ijk]-1].f[2]*local_load_scaling
                
                            aircraft.main_wing[i].total_force += pointlist[elemlist[ielem].g[ijk]-1].f[1]
                            pointlist[elemlist[ielem].g[ijk]-1].aeroloaded = 1
            
            
            
            
                if(elemlist[ielem].type == "CQUAD4"):
                    for ijk in range(0,4):
                        if(pointlist[elemlist[ielem].g[ijk]-1].aeroloaded == 0):
                            pointlist[elemlist[ielem].g[ijk]-1].f[0] = pointlist[elemlist[ielem].g[ijk]-1].f[0]*local_load_scaling
                            pointlist[elemlist[ielem].g[ijk]-1].f[1] = pointlist[elemlist[ielem].g[ijk]-1].f[1]*local_load_scaling
                            pointlist[elemlist[ielem].g[ijk]-1].f[2] = pointlist[elemlist[ielem].g[ijk]-1].f[2]*local_load_scaling
                            pointlist[elemlist[ielem].g[ijk]-1].aeroloaded = 1
    
                            aircraft.main_wing[i].total_force += pointlist[elemlist[ielem].g[ijk]-1].f[1]
        
        
#        for iPoint in range(0,len(pointlist)):
#            pointlist[iPoint].f[0] = pointlist[iPoint].f[0]*local_load_scaling
#            pointlist[iPoint].f[1] = pointlist[iPoint].f[1]*local_load_scaling
#            pointlist[iPoint].f[2] = pointlist[iPoint].f[2]*local_load_scaling
#            
#            pointlist[iPoint].f_aero[0] = pointlist[iPoint].f[0]
#            pointlist[iPoint].f_aero[1] = pointlist[iPoint].f[1]
#            pointlist[iPoint].f_aero[2] = pointlist[iPoint].f[2]           
#            
#            
#            
#            aircraft.main_wing[i].total_force+=pointlist[iPoint].f[1]


    print "Maximum distance: ",max_distance



#    wing_i_surface_element_numbers_l = set(aircraft.dv_breakdown.wings[0].lower.new_element_nos)
#    wing_i_surface_element_numbers_u = set(aircraft.dv_breakdown.wings[0].upper.new_element_nos)
#
#
#    #Visualize the results
#
#    fig = plt.figure(1)
#    plt.xlabel('x axis')
#    plt.ylabel('y axis')
#
#    ax = Axes3D(fig)
#
#    for i in range (0,len(elemlist)):
#
#        if (elemlist[i].pid in wing_i_surface_element_numbers_u) or (elemlist[i].pid in wing_i_surface_element_numbers_l):
#
#            for j in range(0,4):
#
#                ax.scatter(pointlist[elemlist[i].g[j]-1].x[0], pointlist[elemlist[i].g[j]-1].x[2], pointlist[elemlist[i].g[j]-1].f[1],c="red")
#
#    plt.savefig("3d_loads_main_wing_plot.png",format='png')
#
#    #plt.show()
#    plt.clf()
#
#
#
#    loads = np.zeros(4*len(elemlist))
#    y_position = np.zeros(4*len(elemlist))
#    count = 0
#    for i in range(0,len(elemlist)):
#
#        if (elemlist[i].pid in wing_i_surface_element_numbers_u) or (elemlist[i].pid in wing_i_surface_element_numbers_l):
#
#            for j in range(0,4):
#
#                loads[count] = pointlist[elemlist[i].g[j]-1].f[1]
#                y_position[count] = pointlist[elemlist[i].g[j]-1].x[2]
#                count = count + 1
#
#
#    fig2 = plt.figure(2)
#    plt.xlabel('y location')
#    plt.ylabel('loads')
#    plt.plot(y_position,loads,'*')
#    plt.savefig("2D_loads_main_wing_distribution.png",format='png')
#    plt.clf()
#
#
#
#
#
#
#    wing_i_surface_element_numbers_l = set(aircraft.dv_breakdown.wings[1].lower.new_element_nos)
#    wing_i_surface_element_numbers_u = set(aircraft.dv_breakdown.wings[1].upper.new_element_nos)
#
#
#    #Visualize the results
#
#    fig3 = plt.figure(3)
#    plt.xlabel('x axis')
#    plt.ylabel('y axis')
#
#    ax = Axes3D(fig3)
#
#    for i in range (0,len(elemlist)):
#
#        if (elemlist[i].pid in wing_i_surface_element_numbers_u) or (elemlist[i].pid in wing_i_surface_element_numbers_l):
#
#            for j in range(0,4):
#
#                ax.scatter(pointlist[elemlist[i].g[j]-1].x[0], pointlist[elemlist[i].g[j]-1].x[2], pointlist[elemlist[i].g[j]-1].f[1],c="red")
#
#    plt.savefig("3d_loads_strut_wing_plot.png",format='png')
#
#    #plt.show()
#    plt.clf()
#
#
#
#    loads = np.zeros(4*len(elemlist))
#    y_position = np.zeros(4*len(elemlist))
#    count = 0
#    for i in range(0,len(elemlist)):
#
#        if (elemlist[i].pid in wing_i_surface_element_numbers_u) or (elemlist[i].pid in wing_i_surface_element_numbers_l):
#
#            for j in range(0,4):
#
#                loads[count] = pointlist[elemlist[i].g[j]-1].f[1]
#                y_position[count] = pointlist[elemlist[i].g[j]-1].x[2]
#                count = count + 1
#
#
#    fig4 = plt.figure(4)
#    plt.xlabel('y location')
#    plt.ylabel('loads')
#    plt.plot(y_position,loads,'*')
#    plt.savefig("2D_loads_strut_wing_distribution.png",format='png')
#    plt.clf()
#
#


    
    
    



def compute_spanwise_load(element):
    
    #triangular distribution
    spanwise_load = 1.0-element.global_spanwise_coordinate
    return spanwise_load



def compute_chordwise_load(element):
    
    #uniform
    chordwise_load = 1.0/element.local_chord
    
    
    #triangular distribution
    #chordwise_load = 2.0*(1.0-element.chordwise_coordinate)/element.local_chord
    
    return chordwise_load