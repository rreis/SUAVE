# John Hwang, 2014

from __future__ import division

from GeoMACH.PGM.core import PGMconfiguration, PGMparameter, PGMdv
from GeoMACH.PGM.components import PGMwing, PGMbody, PGMshell
from GeoMACH.PGM.components import PGMjunction, PGMtip, PGMcone
from GeoMACH.PSM import Airframe
import numpy


class Conventional5(PGMconfiguration):


    def _define_comps(self):
        self.comps['lwing'] = PGMwing(num_x=4, num_z=4, left_closed=True)

        self.comps['lwing_t'] = PGMtip(self, 'lwing', 'left', 0.1)


    def _define_params(self):
        lwing = self.comps['lwing'].props
        lwing['pos'].params[''] = PGMparameter(1, 3)
        #lwing['scl'].params[''] = PGMparameter(3, 1, pos_u=[0,0.35,1.0])
        lwing['scl'].params[''] = PGMparameter(5, 1)
        lwing['pos'].params['B-spline'] = PGMparameter(5, 3)
        lwing['shY','upp'].params[''] = PGMparameter(10, 6, order_u=6, order_v=6)
        lwing['shY','low'].params[''] = PGMparameter(10, 6, order_u=6, order_v=6)


    def _define_dvs(self):
        dvs = self.dvs

        #main wing

        dvs['lwing_section_1_x'] = PGMdv((1), 16.).set_identity_param('lwing', 'pos', '', (0,0))
        dvs['lwing_section_1_y'] = PGMdv((1), -1.).set_identity_param('lwing', 'pos', '', (0,1))
        dvs['lwing_section_1_z'] = PGMdv((1), 2.6).set_identity_param('lwing', 'pos', '', (0,2))
        
        
        dvs['lwing_section_2_x'] = PGMdv((1), 16.2).set_identity_param('lwing', 'pos', 'B-spline', (1,0))
        dvs['lwing_section_2_y'] = PGMdv((1), 2.4).set_identity_param('lwing', 'pos', 'B-spline', (1,1))
        dvs['lwing_section_2_z'] = PGMdv((1), 12.3).set_identity_param('lwing', 'pos', 'B-spline', (1,2))

  
        
        #relative to the root
        dvs['lwing_section_3_x'] = PGMdv((1), 16.5).set_identity_param('lwing', 'pos', 'B-spline', (2,0))
        dvs['lwing_section_3_y'] = PGMdv((1), 4.4).set_identity_param('lwing', 'pos', 'B-spline',  (2,1))
        dvs['lwing_section_3_z'] = PGMdv((1), 23.3).set_identity_param('lwing', 'pos', 'B-spline', (2,2))

        dvs['lwing_section_4_x'] = PGMdv((1), 16.2).set_identity_param('lwing', 'pos', 'B-spline', (3,0))
        dvs['lwing_section_4_y'] = PGMdv((1), 2.4).set_identity_param('lwing', 'pos', 'B-spline',  (3,1))
        dvs['lwing_section_4_z'] = PGMdv((1), 12.3).set_identity_param('lwing', 'pos', 'B-spline', (3,2))
        
        dvs['lwing_section_5_x'] = PGMdv((1), 16.2).set_identity_param('lwing', 'pos', 'B-spline', (4,0))
        dvs['lwing_section_5_y'] = PGMdv((1), 2.4).set_identity_param('lwing', 'pos', 'B-spline',  (4,1))
        dvs['lwing_section_5_z'] = PGMdv((1), 12.3).set_identity_param('lwing', 'pos', 'B-spline', (4,2))


        dvs['lwing_section_1_chord'] = PGMdv((1), 10).set_identity_param('lwing', 'scl', '',  (0,0))
        dvs['lwing_section_2_chord'] = PGMdv((1), 4.5).set_identity_param('lwing', 'scl', '', (1,0))
        dvs['lwing_section_3_chord'] = PGMdv((1), 1.2).set_identity_param('lwing', 'scl', '', (2,0))
        dvs['lwing_section_4_chord'] = PGMdv((1), 1.2).set_identity_param('lwing', 'scl', '', (3,0))
        dvs['lwing_section_5_chord'] = PGMdv((1), 1.2).set_identity_param('lwing', 'scl', '', (4,0))



    def _compute_params(self):

        lwing = self.comps['lwing'].props
        lwing['pos'].params[''].val([16,-1,2.6])
        lwing['scl'].params[''].val([10,4.5,1.2,0.8,0.6])
        lwing['pos'].params['B-spline'].val([[0,0,0],[16.5,2.4,12.3],[16.5,4.4,23.3],[16.5,4.4,23.3],[16.5,4.4,23.3]])

        return [], [], []

    def _set_bspline_options(self):
        comps = self.comps

        comps['lwing'].faces['upp'].set_option('num_cp', 'v', [36,24,24,120,40,40]) #[6,4,4,20]

    def meshStructure(self):
        afm = Airframe(self, 1) #0.2)


    #main wing leading section ribs
        idims = numpy.linspace(0.45,0.9,7)
        jdims = numpy.linspace(0.5,1,6)
        for i in range(idims.shape[0]-1):
            for j in range(jdims.shape[0]):
                afm.addVertFlip('lwing_r::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i+1],jdims[j]])
        #afm.addVertFlip('rwing_i_r::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i+1],1-jdims[j]])




        #main wing leading section spars

        for i in range(idims.shape[0]):
            for j in range(jdims.shape[0]-1):
                if i is 0 or i is idims.shape[0]-1:
                    afm.addVertFlip('lwing_s::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]])
                #afm.addVertFlip('rwing_i_s::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i],1-jdims[j+1]])
                else:
#                    afm.addVertFlip('lwing_i_sa::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[1,0.85])
#                    afm.addVertFlip('lwing_i_sb::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[0.15,0])
                    afm.addVertFlip('lwing_s::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]])



#                    afm.addVertFlip('rwing_i_sa::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i],1-jdims[j+1]],w=[1,0.85])
#                    afm.addVertFlip('rwing_i_sb::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i],1-jdims[j+1]],w=[0.15,0])





#
#        #wing box lower/back edge
#        idims = numpy.linspace(0.18,0.45,6)
#        for j in range(idims.shape[0]-1):
#            afm.addVertFlip('lwing_i_i1::'+str(j)+':0','lwing',[idims[j],jdims[j]],[idims[j+1],jdims[j+1]])
#            #afm.addVertFlip('rwing_i_i1::'+str(j)+':0','rwing',[idims[j],1-jdims[j]],[idims[j+1],1-jdims[j+1]])
#            afm.addVertFlip('lwing_i_i2::'+str(j)+':0','lwing',[idims[j],jdims[j]],[0.45,jdims[j]])
#        #afm.addVertFlip('rwing_i_i2::'+str(j)+':0','rwing',[idims[j],1-jdims[j]],[0.45,1-jdims[j]])




        afm.preview('conventional_pvw.dat')
        afm.mesh()
        afm.computeMesh('conventional_str')



    def aircraft_params(self,aircraft):
        print




if __name__ == '__main__':

    pgm = Conventional5()
    bse = pgm.initialize()

    pgm.comps['lwing'].set_airfoil('rae2822.dat')
    #main wing

    pgm.dvs['lwing_section_1_x'].data[0] = 3.0 #16.
    pgm.dvs['lwing_section_1_y'].data[0] = 0.0 #-1.
    pgm.dvs['lwing_section_1_z'].data[0] = 0.0 #2.6
    
    pgm.dvs['lwing_section_2_x'].data[0] = -0.0598932 #16.1
    pgm.dvs['lwing_section_2_y'].data[0] = 0. #1.2
    pgm.dvs['lwing_section_2_z'].data[0] = 0.0128016 #12.3


    pgm.dvs['lwing_section_3_x'].data[0] = 0.762654111638 #16.2
    pgm.dvs['lwing_section_3_y'].data[0] = 0.0 #2.4
    pgm.dvs['lwing_section_3_z'].data[0] = 0.5248656 #24.1
    
    pgm.dvs['lwing_section_4_x'].data[0] = 1.41084469537 #16.5
    pgm.dvs['lwing_section_4_y'].data[0] = 0.0 #2.6
    pgm.dvs['lwing_section_4_z'].data[0] = 0.9089136 #27.1
    
    pgm.dvs['lwing_section_5_x'].data[0] = 1.78976941457 #16.5
    pgm.dvs['lwing_section_5_y'].data[0] = 0.0 #2.6
    pgm.dvs['lwing_section_5_z'].data[0] = 1.2097512 #27.1



#    #relative to the root
#    pgm.dvs['lwing_tip_x'].data[0] = 16.5
#    pgm.dvs['lwing_tip_y'].data[0] = 4.4
#    pgm.dvs['lwing_tip_z'].data[0] = 23.3

    pgm.dvs['lwing_section_1_chord'].data[0] = 3.048 #10.
    pgm.dvs['lwing_section_2_chord'].data[0] = 3.2875728 #4.5
    pgm.dvs['lwing_section_3_chord'].data[0] = 2.4384 #1.2
    pgm.dvs['lwing_section_4_chord'].data[0] = 1.6764 #0.8
    pgm.dvs['lwing_section_5_chord'].data[0] = 1.170432 #0.8


    pgm.compute_all()

    #bse.vec['pt_str']._hidden[:] = False
    bse.vec['pt_str'].export_tec_str()
    #bse.vec['df'].export_tec_scatter()
    #bse.vec['cp'].export_tec_scatter()
    #bse.vec['pt'].export_tec_scatter()
    #bse.vec['cp_str'].export_IGES()
    bse.vec['cp_str'].export_STL('conventional_airc.stl')

    pgm.meshStructure()
