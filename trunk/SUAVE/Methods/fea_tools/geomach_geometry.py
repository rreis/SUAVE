# geomach_geometry.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

import numpy as np

#import GeoMACH models
from conventional5 import Conventional5
from HWB import HWB
from supersonic import Supersonic
from visualize_geomach_bdf import visualize_geomach_geometry

#def geometry_generation(aircraft,stl_mesh_filename):
def geometry_generation(aircraft,geomach_structural_mesh,structural_surface_grid_points_file,stl_mesh_filename):

    print "Generating geometry"
    if(aircraft.type=='Conventional'):
        pgm = Conventional5()
        bse = pgm.initialize()
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
        pgm.comps['ltail'].set_airfoil()
        pgm.dvs['lwing_section_1_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.
        pgm.dvs['lwing_section_1_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[1] #-1.
        pgm.dvs['lwing_section_1_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[2] #2.6
        
        #relative to the root
        pgm.dvs['lwing_section_2_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[0]#-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_section_2_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[1]#-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_section_2_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[2]#-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
                                                                                     #
        pgm.dvs['lwing_section_3_x'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_origin[0]#-aircraft.main_wing[0].main_wing_section[1].root_origin[0] #16.5
        pgm.dvs['lwing_section_3_y'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_origin[1]#-aircraft.main_wing[0].main_wing_section[1].root_origin[1] #4.4
        pgm.dvs['lwing_section_3_z'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_origin[2]#-aircraft.main_wing[0].main_wing_section[1].root_origin[2]  #23.3
                                                                                                       #
        #print aircraft.main_wing[0].main_wing_section[2].tip_origin[0]                                #
        #print aircraft.main_wing[2].main_wing_section[2]                                              #
        pgm.dvs['lwing_section_4_x'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_origin[0]#-aircraft.main_wing[0].main_wing_section[2].root_origin[0] #16.5
        pgm.dvs['lwing_section_4_y'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_origin[1]#-aircraft.main_wing[0].main_wing_section[2].root_origin[1] #4.4
        pgm.dvs['lwing_section_4_z'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_origin[2]#-aircraft.main_wing[0].main_wing_section[2].root_origin[2]  #23.3
        
        
        
        pgm.dvs['lwing_section_1_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_chord # 10.0
        pgm.dvs['lwing_section_2_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].root_chord # 4.5
        pgm.dvs['lwing_section_3_chord'].data[0] = aircraft.main_wing[0].main_wing_section[2].root_chord # 1.2
        pgm.dvs['lwing_section_4_chord'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_chord # 1.2
        
        
        #horz tail
        
        pgm.dvs['ltail_section_1_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[0] #44.0
        pgm.dvs['ltail_section_1_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[1] #0.
        pgm.dvs['ltail_section_1_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[2] #1.3
        
        pgm.dvs['ltail_section_2_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[0]  #-aircraft.main_wing[1].main_wing_section[0].root_origin[0] #6.0
        pgm.dvs['ltail_section_2_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[1]  #-aircraft.main_wing[1].main_wing_section[0].root_origin[1] #1.4
        pgm.dvs['ltail_section_2_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[2]  #-aircraft.main_wing[1].main_wing_section[0].root_origin[2] #8.0
                                                                                                         #
        pgm.dvs['ltail_section_3_x'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_origin[0]  #-aircraft.main_wing[1].main_wing_section[1].root_origin[0] #6.0
        pgm.dvs['ltail_section_3_y'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_origin[1]  #-aircraft.main_wing[1].main_wing_section[1].root_origin[1] #1.4
        pgm.dvs['ltail_section_3_z'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_origin[2]  #-aircraft.main_wing[1].main_wing_section[1].root_origin[2] #8.0
        
        
    
        
        
        pgm.dvs['ltail_section_1_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_chord #4.
        pgm.dvs['ltail_section_2_chord'].data[0] = aircraft.main_wing[1].main_wing_section[1].root_chord
        pgm.dvs['ltail_section_3_chord'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_chord #1.
        
        
        #vertical tail
        
        
        pgm.dvs['vtail_section_1_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[0] #42.
        pgm.dvs['vtail_section_1_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[1] #1.7
        pgm.dvs['vtail_section_1_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.0
        
        pgm.dvs['vtail_section_2_x'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[0]#-aircraft.main_wing[2].main_wing_section[0].root_origin[0] #6.
        pgm.dvs['vtail_section_2_y'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[1]#-aircraft.main_wing[2].main_wing_section[0].root_origin[1] #8.
        pgm.dvs['vtail_section_2_z'].data[0] = aircraft.main_wing[2].main_wing_section[0].tip_origin[2]#-aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.
                                                                                                       #
                                                                                                       #
        pgm.dvs['vtail_section_3_x'].data[0] = aircraft.main_wing[2].main_wing_section[1].tip_origin[0]#-aircraft.main_wing[2].main_wing_section[1].root_origin[0] #6.
        pgm.dvs['vtail_section_3_y'].data[0] = aircraft.main_wing[2].main_wing_section[1].tip_origin[1]#-aircraft.main_wing[2].main_wing_section[1].root_origin[1] #8.
        pgm.dvs['vtail_section_3_z'].data[0] = aircraft.main_wing[2].main_wing_section[1].tip_origin[2]#-aircraft.main_wing[2].main_wing_section[1].root_origin[2] #0.
        
        pgm.dvs['vtail_section_1_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_chord # 10.0
        pgm.dvs['vtail_section_2_chord'].data[0] = aircraft.main_wing[2].main_wing_section[1].root_chord # 4.5
        pgm.dvs['vtail_section_3_chord'].data[0] = aircraft.main_wing[2].main_wing_section[1].tip_chord # 1.2
        
        
        '''
        pgm.dvs['vtail_root_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_chord #5.8
        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
        pgm.dvs['vtail_tip_chord'].data[0] = aircraft.main_wing[2].main_wing_section[1].tip_chord #2.0
        '''
        
        #fuselage
        
        pgm.dvs['fus_section_1_x'].data[0] = aircraft.fuselage[0].root_origin[0]  #0.
        pgm.dvs['fus_section_1_y'].data[0] = aircraft.fuselage[0].root_origin[1]  #0.
        pgm.dvs['fus_section_1_z'].data[0] = aircraft.fuselage[0].root_origin[2]  #0.
        
        pgm.dvs['fus_section_2_x'].data[0] = aircraft.fuselage[0].tip_origin[0]  #50.
        pgm.dvs['fus_section_2_y'].data[0] = aircraft.fuselage[0].tip_origin[1]  #0.
        pgm.dvs['fus_section_2_z'].data[0] = aircraft.fuselage[0].tip_origin[2]  #0.
        
        pgm.dvs['diameter'].data[0] = aircraft.fuselage[0].diameter/2.  #looks this is to fix a geomach bug
        
        pgm.compute_all()
        
        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()
        visualize_geomach_geometry('conventional_str.bdf','conventional_str.plt')
        
    elif (aircraft.type=='Supersonic'):
        pgm = Supersonic()
        bse = pgm.initialize()
        pgm.comps['lwing'].set_airfoil()
        #pgm.comps['lwing'].set_airfoil('n65203.dat')
        #pgm.comps['ltail'].set_airfoil()
        pgm.comps['vtail'].set_airfoil()
        #pgm.comps['vtail'].set_airfoil('supertail04.dat')
        pgm.dvs['lwing_section_1_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.
        pgm.dvs['lwing_section_1_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[1] #-1.
        pgm.dvs['lwing_section_1_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_origin[2] #2.6
        
        #relative to the root
        pgm.dvs['lwing_section_2_x'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[0]#-aircraft.main_wing[0].main_wing_section[0].root_origin[0] #16.5
        pgm.dvs['lwing_section_2_y'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[1]#-aircraft.main_wing[0].main_wing_section[0].root_origin[1] #4.4
        pgm.dvs['lwing_section_2_z'].data[0] = aircraft.main_wing[0].main_wing_section[0].tip_origin[2]#-aircraft.main_wing[0].main_wing_section[0].root_origin[2]  #23.3
                                                                                     #
        pgm.dvs['lwing_section_3_x'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_origin[0]#-aircraft.main_wing[0].main_wing_section[1].root_origin[0] #16.5
        pgm.dvs['lwing_section_3_y'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_origin[1]#-aircraft.main_wing[0].main_wing_section[1].root_origin[1] #4.4
        pgm.dvs['lwing_section_3_z'].data[0] = aircraft.main_wing[0].main_wing_section[1].tip_origin[2]#-aircraft.main_wing[0].main_wing_section[1].root_origin[2]  #23.3
                
        pgm.dvs['lwing_section_4_x'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_origin[0]#-aircraft.main_wing[0].main_wing_section[2].root_origin[0] #16.5
        pgm.dvs['lwing_section_4_y'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_origin[1]#-aircraft.main_wing[0].main_wing_section[2].root_origin[1] #4.4
        pgm.dvs['lwing_section_4_z'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_origin[2]#-aircraft.main_wing[0].main_wing_section[2].root_origin[2]  #23.3
                
        #relative to the root
        pgm.dvs['lwing_section_1_chord'].data[0] = aircraft.main_wing[0].main_wing_section[0].root_chord # 10.0
        pgm.dvs['lwing_section_2_chord'].data[0] = aircraft.main_wing[0].main_wing_section[1].root_chord # 4.5
        pgm.dvs['lwing_section_3_chord'].data[0] = aircraft.main_wing[0].main_wing_section[2].root_chord # 1.2
        pgm.dvs['lwing_section_4_chord'].data[0] = aircraft.main_wing[0].main_wing_section[2].tip_chord # 1.2
        
        #horz tail
        
        #pgm.dvs['ltail_root_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[0] #44.0
        #pgm.dvs['ltail_root_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[1] #0.
        #pgm.dvs['ltail_root_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[2] #1.3
        
        #pgm.dvs['ltail_tip_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[0]-aircraft.main_wing[1].main_wing_section[0].root_origin[0] #6.0
        #pgm.dvs['ltail_tip_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[1]-aircraft.main_wing[1].main_wing_section[0].root_origin[1] #1.4
        #pgm.dvs['ltail_tip_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[2]-aircraft.main_wing[1].main_wing_section[0].root_origin[2] #8.0
        
        #pgm.dvs['ltail_root_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_chord #4.
        ##pgm.dvs['ltail_mid_chord'].data[0] = 4.5
        #pgm.dvs['ltail_tip_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_chord #1.
        
        
        #vertical tail
        
        
        pgm.dvs['vtail_section_1_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[0] #42.
        pgm.dvs['vtail_section_1_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[1] #1.7
        pgm.dvs['vtail_section_1_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_origin[2] #0.0
        
        pgm.dvs['vtail_section_2_x'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[0]#-aircraft.main_wing[2].main_wing_section[0].root_origin[0] #6.
        pgm.dvs['vtail_section_2_y'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[1]#-aircraft.main_wing[2].main_wing_section[0].root_origin[1] #8.
        pgm.dvs['vtail_section_2_z'].data[0] = aircraft.main_wing[1].main_wing_section[0].tip_origin[2]#-aircraft.main_wing[2].main_wing_section[0].root_origin[2] #0.
                                                                                                       #
                                                                                                       #
        pgm.dvs['vtail_section_3_x'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_origin[0]#-aircraft.main_wing[2].main_wing_section[1].root_origin[0] #6.
        pgm.dvs['vtail_section_3_y'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_origin[1]#-aircraft.main_wing[2].main_wing_section[1].root_origin[1] #8.
        pgm.dvs['vtail_section_3_z'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_origin[2]#-aircraft.main_wing[2].main_wing_section[1].root_origin[2] #0.
        
        pgm.dvs['vtail_section_1_chord'].data[0] = aircraft.main_wing[1].main_wing_section[0].root_chord # 10.0
        pgm.dvs['vtail_section_2_chord'].data[0] = aircraft.main_wing[1].main_wing_section[1].root_chord # 4.5
        pgm.dvs['vtail_section_3_chord'].data[0] = aircraft.main_wing[1].main_wing_section[1].tip_chord # 1.2
        
        '''
        pgm.dvs['vtail_root_chord'].data[0] = aircraft.main_wing[2].main_wing_section[0].root_chord #5.8
        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
        pgm.dvs['vtail_tip_chord'].data[0] = aircraft.main_wing[2].main_wing_section[1].tip_chord #2.0
        '''
        
        #fuselage
        
        pgm.dvs['fus_root_x'].data[0] = aircraft.fuselage[0].root_origin[0]  #0.
        pgm.dvs['fus_root_y'].data[0] = aircraft.fuselage[0].root_origin[1]  #0.
        pgm.dvs['fus_root_z'].data[0] = aircraft.fuselage[0].root_origin[2]  #0.
        
        pgm.dvs['fus_tip_x'].data[0] = aircraft.fuselage[0].tip_origin[0]  #50.
        pgm.dvs['fus_tip_y'].data[0] = aircraft.fuselage[0].tip_origin[1]  #0.
        pgm.dvs['fus_tip_z'].data[0] = aircraft.fuselage[0].tip_origin[2]  #0.
        
        pgm.dvs['diameter'].data[0] = aircraft.fuselage[0].diameter/2.  #looks this is to fix a geomach bug
        
        pgm.compute_all()
        
        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()
        visualize_geomach_geometry('supersonic_str.bdf','supersonic_str.plt')     
        
    elif(aircraft.type=='BWB'):
        pgm = HWB()
        bse = pgm.initialize()
        num_sections =  pgm.num_sections 
        dim_tags = ['_x','_y','_z']
   
        for i in range(0,num_sections):
            if i<num_sections-1:
                pgm.dvs['lwing_section_'+str(i+1)+'_chord'].data[0] = aircraft.main_wing[0].main_wing_section[i].root_chord
                print 'lwing_section_'+str(i+1)+'_chord',aircraft.main_wing[0].main_wing_section[i].root_chord
            
            else:
                print 'lwing_section_'+str(i+1)+'_chord',aircraft.main_wing[0].main_wing_section[i].tip_chord
                pgm.dvs['lwing_section_'+str(i+1)+'_chord'].data[0] = aircraft.main_wing[0].main_wing_section[i].tip_chord
            for j in range(0,3):
                if i<num_sections-1:
                    pgm.dvs['lwing_section_'+str(i+1)+dim_tags[j]].data[0] = aircraft.main_wing[0].main_wing_section[i].root_origin[j]
                    print 'lwing_section_'+str(i+1)+dim_tags[j],aircraft.main_wing[0].main_wing_section[i].root_origin[j]
                else:
                    pgm.dvs['lwing_section_'+str(i+1)+dim_tags[j]].data[0] = aircraft.main_wing[0].main_wing_section[i].tip_origin[j]
                    print 'lwing_section_'+str(i+1)+dim_tags[j],aircraft.main_wing[0].main_wing_section[i].tip_origin[j]

        pgm.compute_all()
        
        #bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        bse.vec['df'].export_tec_scatter()
        bse.vec['cp'].export_tec_scatter()
        bse.vec['pt'].export_tec_scatter()
        bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()
        visualize_geomach_geometry('bwb_str.bdf','bwb_str.plt')
        print 'done'