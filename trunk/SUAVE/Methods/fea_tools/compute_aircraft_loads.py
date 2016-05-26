# geomach_geometry.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

import numpy as np

def compute_aerodynamic_loads(aircraft):

    #Unpack
    
    
    #loop over a wing and compute the direction and the span
    for wng in range(0,len(aircraft.main_wing)):
        
        #update the wing properties
        
        dir = np.array(aircraft.main_wing[wng].tip_origin) - np.array(aircraft.main_wing[wng].root_origin)
        aircraft.main_wing[wng].dir = dir /np.linalg.norm(dir)
        
        
        for sec in range(0,len(aircraft.main_wing[wng].main_wing_section)):
    
            #update the wing section properties
            dir = np.array(aircraft.main_wing[wng].main_wing_section[sec].tip_origin) - np.array(aircraft.main_wing[wng].main_wing_section[sec].root_origin)
            aircraft.main_wing[wng].main_wing_section[sec].dir = dir /np.linalg.norm(dir)
            
            
    
    
    

    #ge

    for wng in range(0,len(aircraft.main_wing)):
    
        aircraft.main_wing[wng].total_force = 0.0
        aircraft.main_wing[wng].total_area = 0.0
        MTOW = aircraft.MTOW
        span = aircraft.main_wing[wng].span
        no_of_gridelements_chordwise = aircraft.no_of_gridelements_chordwise
    #    no_of_grid_elements_spanwise = aircraft.no_of_grid_elements_spanwise

        half_lift =  aircraft.main_wing[wng].sizing_lift #MTOW/2.0*9.81*2.5  #2.5g
        print "half lift", half_lift
        half_span =  span

        max_lift = 0.5*(2.0*half_lift/half_span)*aircraft.main_wing[wng].load_scaling  #the multiplication by 0.5 is for the lift on both sides of the wing
        root_origin_y = aircraft.main_wing[wng].main_wing_section[0].root_origin[1]
        
        compute_total_force = 0.
        
        
        #assume each wing has a direction and a span associated with it
       
       #if(aircraft.main_wing[wng].vertical == 0):

        print "Loading Wing ",wng
        #loop over the points for the main wing
        
        
        
        #compute the wing span

        for i in range(0,len(aircraft.pointlist)):



            element_lift = 0.0
            

            
            if(aircraft.pointlist[i].part==("w_"+str(wng))):
                
                

                
                #point converted into an array
                local_point = np.array(aircraft.pointlist[i].x)
                
                #compute the point direction relative to the wing root
                
                point_dir = (local_point - np.array(aircraft.main_wing[wng].main_wing_section[0].root_origin))
                point_dir = point_dir/np.linalg.norm(point_dir)
                point_projection_angle = np.arccos(np.dot(point_dir,aircraft.main_wing[wng].dir)) #assumes both are unit vectors


                #this is spanwise
                #relative_z = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[0].root_origin[2]


                current_span = 0.0
                current_rchord = 0.0
                current_tchord = 0.0
                
                #again length
                #current_z_global = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[0].root_origin[2]
                current_z_global = np.linalg.norm(local_point - np.array(aircraft.main_wing[wng].main_wing_section[0].root_origin))*np.cos(point_projection_angle)
                
                
                for j  in range(0,aircraft.main_wing[wng].no_of_sections):
                    prev_span = current_span
                    current_span = current_span + aircraft.main_wing[wng].main_wing_section[j].span
                    current_rchord = aircraft.main_wing[wng].main_wing_section[j].root_chord
                    current_tchord = aircraft.main_wing[wng].main_wing_section[j].tip_chord


                    
                    #use local span here
                    #if aircraft.pointlist[i].x[2]-aircraft.main_wing[wng].main_wing_section[0].root_origin[2]>prev_span and aircraft.pointlist[i].x[2]-aircraft.main_wing[wng].main_wing_section[0].root_origin[2]<current_span:
                    
                    
                    local_wing_location = np.linalg.norm(local_point-np.array(aircraft.main_wing[wng].main_wing_section[0].root_origin))




                    if (local_wing_location > prev_span) and (local_wing_location <= current_span):
                        
                        
                        
                        current_taper = current_tchord/current_rchord
                        #current_z_local = aircraft.pointlist[i].x[2] - aircraft.main_wing[wng].main_wing_section[j].root_origin[2]


                        local_point_projection_angle = np.arccos(np.dot(point_dir,aircraft.main_wing[wng].main_wing_section[j].dir)) #assumes both are unit vectors

                        current_z_local = np.linalg.norm(local_point - np.array(aircraft.main_wing[wng].main_wing_section[j].root_origin))*np.cos(local_point_projection_angle)
                        
                        
                        si  = current_z_local/aircraft.main_wing[wng].main_wing_section[j].span
                        
                        current_chord = si*current_tchord + (1-si)*current_rchord 
                        
                        current_leading_edge = aircraft.main_wing[wng].main_wing_section[j].root_origin[0] + current_z_local*np.tan(aircraft.main_wing[wng].main_wing_section[j].sweep)
                        current_x_local = aircraft.pointlist[i].x[0] - current_leading_edge
                        
                        non_dimensional_x_local = current_x_local/current_chord
                        
                        spanwise_lift = (1-current_z_global/half_span)*max_lift #l(y)
                        
                        
                        
                        #for a triangular distribution
                        max_chordwise_lift = 2.0*spanwise_lift/current_chord
                        #chordwise_lift = compute_triangular_lift(non_dimensional_x_local, max_chordwise_lift)


                        # for a rectangular distribution
                        chordwise_lift = spanwise_lift/current_chord
                        
                        #print non_dimensional_x_local,max_chordwise_lift,chordwise_lift
                        
                        element_lift = chordwise_lift * aircraft.pointlist[i].Sarea
                        
                        aircraft.main_wing[wng].total_force += element_lift
                        aircraft.main_wing[wng].total_area += aircraft.pointlist[i].Sarea
                        
                        
                        if (wng == 1):
                        
                            print i,current_z_local,current_chord,spanwise_lift,aircraft.pointlist[i].Sarea
                        
                        #if(aircraft.pointlist[i].normal[1]>=0.0):
                        if(aircraft.main_wing[wng].vertical == 0):
                        
                            aircraft.pointlist[i].f[0] = 0.0
                            aircraft.pointlist[i].f[1] = element_lift
                            aircraft.pointlist[i].f[2] = 0.0
                            aircraft.pointlist[i].chord = current_chord
                        
                        
                        
                        else:
                        
                            aircraft.pointlist[i].f[0] = 0.0
                            aircraft.pointlist[i].f[1] = 0.0
                            aircraft.pointlist[i].f[2] = element_lift
                            aircraft.pointlist[i].chord = current_chord

                        current_section = j

                        #print aircraft.pointlist[i].Sarea

                        break
                            






    if (aircraft.fuselage):
        for fus in range(0,len(aircraft.fuselage)):
            for i in range(0,len(aircraft.pointlist)):
                if(aircraft.pointlist[i].part=="f_"+str(fus)):
                    

                    aircraft.pointlist[i].f[0] = aircraft.pointlist[i].normal[0]*aircraft.internal_pressure* aircraft.pointlist[i].Sarea
                    aircraft.pointlist[i].f[1] = aircraft.pointlist[i].normal[1]*aircraft.internal_pressure* aircraft.pointlist[i].Sarea
                    aircraft.pointlist[i].f[2] = aircraft.pointlist[i].normal[2]*aircraft.internal_pressure* aircraft.pointlist[i].Sarea





#compute the internal pressure loads



def compute_triangular_lift(relative_chord_location, max_chordwise_lift):
    return relative_chord_location*max_chordwise_lift


