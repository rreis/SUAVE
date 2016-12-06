import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#currently look only at the main wing and the fuselage

#the function marks the lower surface of the fuselage (payload) and the wing lower surface (fuel loads)
#loop over the wings
#check if the contains_fuel tag is active
#pull out the starting and ending  x,y and z of the fule loads
#loop over the wing lower surface
#add the fuel load weight
from SUAVE.Methods.fea_tools.get_element_ownership import get_element_ownership
from SUAVE.Methods.fea_tools.compute_element_based_aircraft_loads import compute_element_based_aircraft_loads
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.compute_normal import compute_normal
from SUAVE.Methods.fea_tools.visualize_aircraft_loading import visualize_aircraft_loading


def mark_loading_points(aircraft,elemlist,pointlist,bdf_structural_meshfile):

    #mark the necessary elements
    if(aircraft.loads_marked == 0):
        get_element_ownership(bdf_structural_meshfile,aircraft)
    
    
    compute_normal(elemlist,pointlist)
        
    
    compute_element_based_aircraft_loads(elemlist,pointlist,aircraft)
    #need to loop over the structural mesh and look at the wing lower surface elements
    wing_lower_surface_element_numbers = set(aircraft.dv_breakdown.wings[0].lower.new_element_nos)


    fuse_lower_surface_element_numbers = set([])
    if(aircraft.fuselage):
        fuse_lower_surface_element_numbers = set(aircraft.dv_breakdown.fuselages[0].bottom.new_element_nos)
       
    wing_loading_points = []
    fuse_loading_points = []

    for i in range(0,len(elemlist)):
        if elemlist[i].type == "CQUAD4" :
            for edg in range(0,3):
                elemlist[i].centroid[edg] = (pointlist[elemlist[i].g[0]-1].x[edg] + pointlist[elemlist[i].g[1]-1].x[edg]  + pointlist[elemlist[i].g[2]-1].x[edg]  + pointlist[elemlist[i].g[3]-1].x[edg] )/4.0
        

        elif elemlist[i].type == "CTRIA3" :
            for edg in range(0,3):
                elemlist[i].centroid[edg] = (pointlist[elemlist[i].g[0]-1].x[edg]  + pointlist[elemlist[i].g[1]-1].x[edg]  + pointlist[elemlist[i].g[2]-1].x[edg] )/3.0


    # for the wing loop over the elements (check if the numbers match those in the list and if so store the poin,id in a list


    for i in range(0,len(elemlist)):
        
        if (elemlist[i].pid in wing_lower_surface_element_numbers):
            
            if(elemlist[i].centroid[0] <= aircraft.main_wing[0].max_x) and (elemlist[i].centroid[1] <= aircraft.main_wing[0].max_y) and (elemlist[i].centroid[2] < aircraft.main_wing[0].max_z):
            
                for j in range(0,3):
                    wing_loading_points.append(elemlist[i].g[j])

                if (elemlist[i].type == "CQUAD4") :
                    wing_loading_points.append(elemlist[i].g[3])


        if (elemlist[i].pid in fuse_lower_surface_element_numbers):
            for j in range(0,3):
                fuse_loading_points.append(elemlist[i].g[j])
            
            if (elemlist[i].type == "CQUAD4") :
                fuse_loading_points.append(elemlist[i].g[3])






    #get the pointid for the wing and fuselage loads
    wing_loading_points_listset = list(set(wing_loading_points))


    fuse_loading_points_listset = list(set(fuse_loading_points))

    if(len(wing_loading_points_listset) == 0):
        distributed_fuel_load = 0.0
    else:
        distributed_fuel_load = aircraft.main_wing[0].fuel_load*9.81 / float(len(wing_loading_points_listset))
        #now add the point loads at the points
        for i in range(0,len(wing_loading_points_listset)):
            pointlist[wing_loading_points_listset[i]-1].f[1] += -1.0*float(distributed_fuel_load)
            pointlist[wing_loading_points_listset[i]-1].f_loads[1] += -1.0*float(distributed_fuel_load)
            #print "wing : ",i," : ",-1.0*float(distributed_fuel_load)
            pointlist[wing_loading_points_listset[i]-1].fuel_load_p = 1
            pointlist[wing_loading_points_listset[i]-1].fuel_load = -1.0*float(distributed_fuel_load)

    if(aircraft.fuselage):
        distributed_payload = aircraft.payload*9.81 / float(len(fuse_loading_points_listset))



    if(aircraft.fuselage):
        for i in range(0,len(fuse_loading_points_listset)):
            pointlist[fuse_loading_points_listset[i]-1].f[1] += -1.0*float(distributed_payload)
            pointlist[fuse_loading_points_listset[i]-1].f_loads[1] += -1.0*float(distributed_payload)
            pointlist[fuse_loading_points_listset[i]-1].payload_p = 1
            pointlist[fuse_loading_points_listset[i]-1].payload = -1.0*float(distributed_payload)


    aircraft.no_of_points_w_fuel_load = len(wing_loading_points_listset)
    aircraft.no_of_points_w_payload = len(fuse_loading_points_listset)



    #add fuselage pressure loads ------------------------------------------------------------------------------------
    
    if(aircraft.fuselage):    
    
        #compute the fuselage elements--------------
        fuselage_elements_b = set(aircraft.dv_breakdown.fuselages[0].bottom.new_element_nos)
        fuselage_elements_t = set(aircraft.dv_breakdown.fuselages[0].top.new_element_nos)
        fuselage_elements_l = set(aircraft.dv_breakdown.fuselages[0].left.new_element_nos)
        fuselage_elements_r = set(aircraft.dv_breakdown.fuselages[0].right.new_element_nos)
        
        pressure = aircraft.internal_pressure
        
        for ielem in range(0,len(elemlist)):
            
            if((elemlist[ielem].pid in fuselage_elements_b) or (elemlist[ielem].pid in fuselage_elements_t) or (elemlist[ielem].pid in fuselage_elements_l)  or (elemlist[ielem].pid in fuselage_elements_r)):
                
                if(elemlist[ielem].type == "CTRIA3"):
                    for ijk in range(0,3):
                
                        pointlist[elemlist[ielem].g[ijk]-1].f_pressure[0] += 1.0/3.0*pressure*elemlist[ielem].normal[0]*elemlist[ielem].area
                        pointlist[elemlist[ielem].g[ijk]-1].f_pressure[1] += 1.0/3.0*pressure*elemlist[ielem].normal[1]*elemlist[ielem].area
                        pointlist[elemlist[ielem].g[ijk]-1].f_pressure[2] += 1.0/3.0*pressure*elemlist[ielem].normal[2]*elemlist[ielem].area
                
                
    #                    pointlist[elemlist[ielem].g[ijk]-1].f[0] += 1.0/3.0*pressure*elemlist[ielem].normal[0]*elemlist[ielem].area
    #                    pointlist[elemlist[ielem].g[ijk]-1].f[1] += 1.0/3.0*pressure*elemlist[ielem].normal[1]*elemlist[ielem].area
    #                    pointlist[elemlist[ielem].g[ijk]-1].f[2] += 1.0/3.0*pressure*elemlist[ielem].normal[2]*elemlist[ielem].area
    
    
    
    
    
                if(elemlist[ielem].type == "CQUAD4"):
                    for ijk in range(0,4):
    
                        pointlist[elemlist[ielem].g[ijk]-1].f_pressure[0] = 0.25*pressure*elemlist[ielem].normal[0]*elemlist[ielem].area
                        pointlist[elemlist[ielem].g[ijk]-1].f_pressure[1] = 0.25*pressure*elemlist[ielem].normal[1]*elemlist[ielem].area
                        pointlist[elemlist[ielem].g[ijk]-1].f_pressure[2] = 0.25*pressure*elemlist[ielem].normal[2]*elemlist[ielem].area
    
                        pointlist[elemlist[ielem].g[ijk]-1].nv[0] = elemlist[ielem].normal[0]
                        pointlist[elemlist[ielem].g[ijk]-1].nv[1] = elemlist[ielem].normal[1]
                        pointlist[elemlist[ielem].g[ijk]-1].nv[2] = elemlist[ielem].normal[2]
                        
                        pointlist[elemlist[ielem].g[ijk]-1].nva[0] = elemlist[ielem].normal[0]*elemlist[ielem].area
                        pointlist[elemlist[ielem].g[ijk]-1].nva[1] = elemlist[ielem].normal[1]*elemlist[ielem].area
                        pointlist[elemlist[ielem].g[ijk]-1].nva[2] = elemlist[ielem].normal[2]*elemlist[ielem].area                    
    
    
    #                    pointlist[elemlist[ielem].g[ijk]-1].f[0] += 0.25*pressure*elemlist[ielem].normal[0]*elemlist[ielem].area
    #                    pointlist[elemlist[ielem].g[ijk]-1].f[1] += 0.25*pressure*elemlist[ielem].normal[1]*elemlist[ielem].area
    #                    pointlist[elemlist[ielem].g[ijk]-1].f[2] += 0.25*pressure*elemlist[ielem].normal[2]*elemlist[ielem].area  
    
                        
    
                
        
        
        #get all the points in the fuselage and the corresponding normal based on the element direction--------------
    
        for iPoint in range(0,len(pointlist)):
            pointlist[iPoint].f[0] += pointlist[iPoint].f_pressure[0]
            pointlist[iPoint].f[1] += pointlist[iPoint].f_pressure[1]
            pointlist[iPoint].f[2] += pointlist[iPoint].f_pressure[2]
    
     
    #------add the fuselage pressure loads-----------
    

    visualize_aircraft_loading(elemlist,pointlist)





    #loop over the elements in the wing lower surface (get the point id's)
    #split the loads uniformly among the lower surface points



#visualization of the loading points
#
#    fig = plt.figure(1)
#        
#    ax = Axes3D(fig)
#        
#        
#    for i in range(0,len(wing_loading_points_listset)):
#        ax.scatter(pointlist[wing_loading_points_listset[i]-1].x[0],pointlist[wing_loading_points_listset[i]-1].x[1],pointlist[wing_loading_points_listset[i]-1].x[2],c="blue")
#
#    
#    for i in range(0,len(fuse_loading_points_listset)):
#        ax.scatter(pointlist[fuse_loading_points_listset[i]-1].x[0],pointlist[fuse_loading_points_listset[i]-1].x[1],pointlist[fuse_loading_points_listset[i]-1].x[2],c="red")
#
#
#
#    plt.savefig('struct_braced_fuel_loads_vis.png',format='png')
#    
#    plt.show()
#    plt.clf()







