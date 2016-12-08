# John Hwang, 2014

from __future__ import division

from GeoMACH.PGM.core import PGMconfiguration, PGMparameter, PGMdv
from GeoMACH.PGM.components import PGMwing, PGMbody, PGMshell
from GeoMACH.PGM.components import PGMjunction, PGMtip, PGMcone
from GeoMACH.PSM import Airframe
import numpy


class HWB(PGMconfiguration):


    def _define_comps(self):
        self.comps['lwing'] = PGMwing(num_x=4, num_z=4, left_closed=False)
        self.comps['lwing_t'] = PGMtip(self, 'lwing', 'left', 0.1)


    def _define_params(self):
        num_sections = 7
        self.dvs.num_sections = num_sections
        lwing = self.comps['lwing'].props
        lwing['pos'].params[''] = PGMparameter(1, 3)
        #lwing['scl'].params[''] = PGMparameter(3, 1, pos_u=[0,0.35,1.0])
        lwing['scl'].params[''] = PGMparameter(num_sections, 1)
        lwing['pos'].params['lin'] = PGMparameter(num_sections, 3)
#        lwing['shY','upp'].params[''] = PGMparameter(10, 6, order_u=4, order_v=4)
#        lwing['shY','low'].params[''] = PGMparameter(10, 6, order_u=4, order_v=4)


    def _define_dvs(self):
        dvs = self.dvs
        num_sections = dvs.num_sections
        #main wing
        dim_tags = ['_x','_y','_z']
        
        dvs['lwing_section_1_x'] = PGMdv((1), 16.2).set_identity_param('lwing', 'pos', '', (0,0))
        dvs['lwing_section_1_y'] = PGMdv((1), -1.).set_identity_param('lwing', 'pos', '', (0,1))
        dvs['lwing_section_1_z'] = PGMdv((1), 2.6).set_identity_param('lwing', 'pos', '', (0,2))
        dvs['lwing_section_' + str(1) + '_chord'] = PGMdv((1), 10).set_identity_param('lwing', 'scl', '', (0,0))
        for i in range(1,num_sections):
            dvs['lwing_section_' + str(i+1) + '_chord'] = PGMdv((1), 10).set_identity_param('lwing', 'scl', '', (i,0))
            for j in range(0,3):
                dvs['lwing_section_'+str(i+1)+dim_tags[j]] = PGMdv((1), 16.).set_identity_param('lwing', 'pos', 'lin', (i,j))
                



    def _compute_params(self):
        num_sections = self.dvs.num_sections
        initial_scls = np.zeros(num_sections,1)
        initial_pos = np.zeros(num_sections,3)
        lwing = self.comps['lwing'].props
        lwing['pos'].params[''].val([16,-1,2.6])
        lwing['scl'].params[''].val(initial_vals)
        lwing['pos'].params['lin'].val(initial_pos)

        #lwing['scl'].params[''].val([10,4.5,4.2,4.0,3.9,3.5,1.2,.8])
        #lwing['pos'].params['lin'].val([[0,0,0],[16.5,2.4,12.3],[16.5,2.4,12.3],[16.5,2.4,12.3],[16.5,2.4,12.3],[16.5,2.4,12.3],[16.5,2.4,12.3],[16.5,4.4,23.3]])

        return [], [], []

    def _set_bspline_options(self):
        comps = self.comps
        comps['lwing'].faces['upp'].set_option('num_cp', 'v', [40,40,40,40]) #[6,4,4,20] #[36,24,24,120]
        comps['lwing'].faces['low'].set_option('num_cp', 'u', [40,40,40,40])

    def meshStructure(self):
        afm = Airframe(self, 1) #0.2)


    #main wing leading section ribs
        idims = numpy.linspace(0.45,0.9,7)
        jdims = numpy.linspace(0,1,16)
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






        #wing box lower/back edge
        idims = numpy.linspace(0.18,0.45,6)
        for j in range(idims.shape[0]-1):
            afm.addVertFlip('lwing_i_i1::'+str(j)+':0','lwing',[idims[j],jdims[j]],[idims[j+1],jdims[j+1]])
            #afm.addVertFlip('rwing_i_i1::'+str(j)+':0','rwing',[idims[j],1-jdims[j]],[idims[j+1],1-jdims[j+1]])
            afm.addVertFlip('lwing_i_i2::'+str(j)+':0','lwing',[idims[j],jdims[j]],[0.45,jdims[j]])
        #afm.addVertFlip('rwing_i_i2::'+str(j)+':0','rwing',[idims[j],1-jdims[j]],[0.45,1-jdims[j]])





        afm.preview('HWB_pvw.dat')
        afm.mesh()
        afm.computeMesh('HWB_str')



    def aircraft_params(self,aircraft):
        print




if __name__ == '__main__':

    pgm = HWB()
    bse = pgm.initialize()

    
    
    
    
    pgm.comps['lwing'].set_airfoil('rae2822.dat')
    #pgm.comps['ltail'].set_airfoil()
    #main wing

    pgm.dvs['lwing_section_1_x'].data[0] = 16.
    pgm.dvs['lwing_section_1_y'].data[0] = -1.
    pgm.dvs['lwing_section_1_z'].data[0] = 2.6
    
    pgm.dvs['lwing_section_2_x'].data[0] = 2.1
    pgm.dvs['lwing_section_2_y'].data[0] = 0
    pgm.dvs['lwing_section_2_z'].data[0] = 10.4


    pgm.dvs['lwing_section_3_x'].data[0] = 4.1
    pgm.dvs['lwing_section_3_y'].data[0] = 0.1
    pgm.dvs['lwing_section_3_z'].data[0] = 23.4
    
    pgm.dvs['lwing_section_4_x'].data[0] = 6.1
    pgm.dvs['lwing_section_4_y'].data[0] = 0.2
    pgm.dvs['lwing_section_4_z'].data[0] = 34.6


    pgm.dvs['lwing_section_5_x'].data[0] = 8.1
    pgm.dvs['lwing_section_5_y'].data[0] = 0.3
    pgm.dvs['lwing_section_5_z'].data[0] = 46.8
    
    pgm.dvs['lwing_section_6_x'].data[0] = 10.1
    pgm.dvs['lwing_section_6_y'].data[0] = 0.4
    pgm.dvs['lwing_section_6_z'].data[0] = 57.0


    pgm.dvs['lwing_section_7_x'].data[0] = 12.1
    pgm.dvs['lwing_section_7_y'].data[0] = 0.5
    pgm.dvs['lwing_section_7_z'].data[0] = 68.2

    pgm.dvs['lwing_section_8_x'].data[0] = 14
    pgm.dvs['lwing_section_8_y'].data[0] = 0.5
    pgm.dvs['lwing_section_8_z'].data[0] = 70
    
    
    pgm.dvs['lwing_section_1_chord'].data[0] = 24.
    pgm.dvs['lwing_section_2_chord'].data[0] = 24. #18.0
    pgm.dvs['lwing_section_3_chord'].data[0] = 24. #8.0
    pgm.dvs['lwing_section_4_chord'].data[0] = 24. #6.0
    pgm.dvs['lwing_section_5_chord'].data[0] = 24. #5.0
    pgm.dvs['lwing_section_6_chord'].data[0] = 24. #4.0
    pgm.dvs['lwing_section_7_chord'].data[0] = 24. #3.5  
    pgm.dvs['lwing_section_8_chord'].data[0] = 24. #3.5  

    pgm.compute_all()

    #bse.vec['pt_str']._hidden[:] = False
    bse.vec['pt_str'].export_tec_str()
    #bse.vec['df'].export_tec_scatter()
    #bse.vec['cp'].export_tec_scatter()
    #bse.vec['pt'].export_tec_scatter()
    #bse.vec['cp_str'].export_IGES()
    bse.vec['cp_str'].export_STL('HWB.stl')

    pgm.meshStructure()
