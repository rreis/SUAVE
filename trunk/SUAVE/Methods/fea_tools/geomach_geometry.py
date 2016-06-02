# geomach_geometry.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#

import numpy as np

#import GeoMACH models
from conventional5 import Conventional5
from visualize_geomach_bdf import visualize_geomach_geometry

def geomach_geometry(aircraft,stl_mesh_filename):

    print "Generating geometry"
    if(aircraft.type=='Conventional'):
        pgm = Conventional5()
        bse = pgm.initialize()
        
        
        pgm.comps['lwing'].set_airfoil('rae2822.dat')
        pgm.comps['ltail'].set_airfoil()

        #pgm.dvs['lwing_root_x'].data[0] = 16.
        #pgm.dvs['lwing_root_y'].data[0] = -1.
        #pgm.dvs['lwing_root_z'].data[0] = 2.6
        
        ##relative to the root
        #pgm.dvs['lwing_tip_x'].data[0] = 16.5
        #pgm.dvs['lwing_tip_y'].data[0] = 4.4
        #pgm.dvs['lwing_tip_z'].data[0] = 23.3
        
        #pgm.dvs['lwing_root_chord'].data[0] = 10.
        #pgm.dvs['lwing_mid_chord'].data[0] = 10. # this seems like a questionable value for mid chord
        #pgm.dvs['lwing_tip_chord'].data[0] = 1.2      
        
        pgm.dvs['lwing_root_x'].data[0] = aircraft.wings.main_wing.origin[0]
        pgm.dvs['lwing_root_y'].data[0] = aircraft.wings.main_wing.origin[2]
        pgm.dvs['lwing_root_z'].data[0] = aircraft.fuselages.fuselage.effective_diameter/2.
        
        #relative to the root
        pgm.dvs['lwing_tip_x'].data[0] = aircraft.wings.main_wing.tip_location[0]
        pgm.dvs['lwing_tip_y'].data[0] = aircraft.wings.main_wing.tip_location[2]
        pgm.dvs['lwing_tip_z'].data[0] = aircraft.wings.main_wing.tip_location[1]
        
        pgm.dvs['lwing_root_chord'].data[0] = aircraft.wings.main_wing.chords.root
        pgm.dvs['lwing_mid_chord'].data[0] = .5*(aircraft.wings.main_wing.chords.root + aircraft.wings.main_wing.chords.tip) # this seems like a questionable value for mid chord
        pgm.dvs['lwing_tip_chord'].data[0] = aircraft.wings.main_wing.chords.tip
        
        
        ##horz tail
        
        pgm.dvs['ltail_root_x'].data[0] = aircraft.wings.horizontal_stabilizer.origin[0]
        pgm.dvs['ltail_root_y'].data[0] = aircraft.wings.horizontal_stabilizer.origin[2]
        #pgm.dvs['ltail_root_z'].data[0] = aircraft.wings.horizontal_stabilizer.origin[1]
        pgm.dvs['ltail_root_z'].data[0] = .5
        
        pgm.dvs['ltail_tip_x'].data[0] = aircraft.wings.horizontal_stabilizer.tip_location[0]
        pgm.dvs['ltail_tip_y'].data[0] = aircraft.wings.horizontal_stabilizer.tip_location[2]
        pgm.dvs['ltail_tip_z'].data[0] = aircraft.wings.horizontal_stabilizer.tip_location[1]
        
        pgm.dvs['ltail_root_chord'].data[0] = aircraft.wings.horizontal_stabilizer.chords.root
        #pgm.dvs['ltail_mid_chord'].data[0] = 4.5
        pgm.dvs['ltail_tip_chord'].data[0] = aircraft.wings.horizontal_stabilizer.chords.tip
        
        
        #vertical tail
        
        pgm.dvs['vtail_root_x'].data[0] = aircraft.wings.vertical_stabilizer.origin[0]
        pgm.dvs['vtail_root_y'].data[0] = aircraft.wings.vertical_stabilizer.origin[2]
        pgm.dvs['vtail_root_z'].data[0] = aircraft.wings.vertical_stabilizer.origin[1]
        
        pgm.dvs['vtail_tip_x'].data[0] = aircraft.wings.vertical_stabilizer.tip_location[0]
        pgm.dvs['vtail_tip_y'].data[0] = aircraft.wings.vertical_stabilizer.tip_location[2]
        pgm.dvs['vtail_tip_z'].data[0] = aircraft.wings.vertical_stabilizer.tip_location[1]
        
        pgm.dvs['vtail_root_chord'].data[0] = aircraft.wings.vertical_stabilizer.chords.root
        #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
        pgm.dvs['vtail_tip_chord'].data[0] = aircraft.wings.vertical_stabilizer.chords.tip
        
        
        #fuselage
        
        pgm.dvs['fus_root_x'].data[0] = aircraft.fuselages.fuselage.origin[0]
        pgm.dvs['fus_root_y'].data[0] = aircraft.fuselages.fuselage.origin[1]
        pgm.dvs['fus_root_z'].data[0] = aircraft.fuselages.fuselage.origin[2]
        
        pgm.dvs['fus_tip_x'].data[0] = aircraft.fuselages.fuselage.lengths.total
        pgm.dvs['fus_tip_y'].data[0] = 0.
        pgm.dvs['fus_tip_z'].data[0] = 0.
        
        pgm.dvs['diameter'].data[0] = aircraft.fuselages.fuselage.effective_diameter/2.

        pgm.compute_all()

        bse.vec['pt_str']._hidden[:] = False
        bse.vec['pt_str'].export_tec_str()
        #bse.vec['df'].export_tec_scatter()
        #bse.vec['cp'].export_tec_scatter()
        #bse.vec['pt'].export_tec_scatter()
        #bse.vec['cp_str'].export_IGES()
        bse.vec['cp_str'].export_STL(stl_mesh_filename)
        
        pgm.meshStructure()
        
        visualize_geomach_geometry('conventional_str.bdf','conventional_str.plt')
