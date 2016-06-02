# John Hwang, 2014

from __future__ import division

from GeoMACH.PGM.core import PGMconfiguration, PGMparameter, PGMdv
from GeoMACH.PGM.components import PGMwing, PGMbody, PGMshell
from GeoMACH.PGM.components import PGMjunction, PGMtip, PGMcone
from GeoMACH.PSM import Airframe
import numpy


class Conventional5(PGMconfiguration):

    def _define_comps(self):
        self.comps['fuse'] = PGMbody(num_x=12, num_y=4, num_z=2)
        self.comps['lwing'] = PGMwing(num_x=4, num_z=4, left_closed=True)
        #self.comps['rwing'] = PGMwing(num_x=4, num_z=4, right_closed=True)
        #self.comps['lpylon'] = PGMwing()
        #self.comps['lnac'] = PGMshell(num_x=4, num_y=1, num_z=4)
        self.comps['ltail'] = PGMwing(left_closed=True)
        #self.comps['rtail'] = PGMwing(right_closed=True)
        self.comps['vtail'] = PGMwing(num_x=2, left_closed=True)

        self.comps['fuse_f'] = PGMcone(self, 'fuse', 'front', 2)
        self.comps['fuse_r'] = PGMcone(self, 'fuse', 'rear', 1)
        self.comps['lwing_t'] = PGMtip(self, 'lwing', 'left', 0.1)
        #self.comps['rwing_t'] = PGMtip(self, 'rwing', 'right', 0.1)
        self.comps['ltail_t'] = PGMtip(self, 'ltail', 'left', 0.1)
        #self.comps['rtail_t'] = PGMtip(self, 'rtail', 'right', 0.1)
        self.comps['vtail_t'] = PGMtip(self, 'vtail', 'left', 0.1)

        self.comps['lwing_fuse'] = PGMjunction(self, 'fuse', 'lft', 'E', [2,3], 'lwing', 'right')
        #self.comps['rwing_fuse'] = PGMjunction(self, 'fuse', 'rgt', 'W', [2,5], 'rwing', 'left')
#        self.comps['lpylon_lwing'] = PGMjunction(self, 'lwing', 'low', 'N', [1,0], 'lpylon', 'right')
#        self.comps['lpylon_lnac'] = PGMjunction(self, 'lnac', 'tp0', 'W', [1,0], 'lpylon', 'left')
        self.comps['ltail_fuse'] = PGMjunction(self, 'fuse', 'lft', 'E', [1,9], 'ltail', 'right')
        #self.comps['rtail_fuse'] = PGMjunction(self, 'fuse', 'rgt', 'W', [1,0], 'rtail', 'left')
        self.comps['vtail_fuse'] = PGMjunction(self, 'fuse', 'top', 'E', [0,8], 'vtail', 'right')

    def _define_params(self):
        fuse = self.comps['fuse'].props
        fuse['pos'].params[''] = PGMparameter(2, 3)
        fuse['nor'].params[''] = PGMparameter(1, 1)
        fuse['scl'].params[''] = PGMparameter(1, 1)
        fuse['flt'].params[''] = PGMparameter(2, 4, pos_u=[0.39,0.55])
        fuse['pos'].params['nose'] = PGMparameter(3, 3, pos_u=[0,0.065,0.13], order_u=3)
        fuse['scl'].params['nose'] = PGMparameter(3, 1, pos_u=[0,0.07,0.14], order_u=3)
        fuse['scl'].params['tail'] = PGMparameter(2, 1, pos_u=[0.7,1.0])

        lwing = self.comps['lwing'].props
        lwing['pos'].params[''] = PGMparameter(1, 3)
        lwing['scl'].params[''] = PGMparameter(3, 1, pos_u=[0,0.35,1.0])
        lwing['pos'].params['lin'] = PGMparameter(2, 3)
        lwing['shY','upp'].params[''] = PGMparameter(10, 6, order_u=4, order_v=4)
        lwing['shY','low'].params[''] = PGMparameter(10, 6, order_u=4, order_v=4)

#        rwing = self.comps['rwing'].props
#        rwing['pos'].params[''] = PGMparameter(1, 3)
#        rwing['scl'].params[''] = PGMparameter(3, 1, pos_u=[0,0.65,1.0])
#        rwing['pos'].params['lin'] = PGMparameter(2, 3)
#	rwing['shY','upp'].params[''] = PGMparameter(10, 6, order_u=4, order_v=4)
#	rwing['shY','low'].params[''] = PGMparameter(10, 6, order_u=4, order_v=4)

#        lpylon = self.comps['lpylon'].props
#        lpylon['pos'].params[''] = PGMparameter(1, 3)
#        lpylon['pos'].params['lin'] = PGMparameter(2, 3)
#        lpylon['scl'].params[''] = PGMparameter(2, 1)
#        lpylon['nor'].params[''] = PGMparameter(1, 3)
#
#        lnac = self.comps['lnac'].props
#        lnac['pos'].params[''] = PGMparameter(1, 3)
#        lnac['pos'].params['lin'] = PGMparameter(2, 3)
#        lnac['nor'].params[''] = PGMparameter(1, 1)
#        lnac['scl'].params[''] = PGMparameter(1, 1)
#        lnac['thk'].params[''] = PGMparameter(3, 1)

        ltail = self.comps['ltail'].props
        ltail['pos'].params[''] = PGMparameter(1, 3)
        ltail['pos'].params['lin'] = PGMparameter(2, 3)
        ltail['scl'].params[''] = PGMparameter(2, 1)
        ltail['rot'].params[''] = PGMparameter(2, 3)
        ltail['ogn'].params[''] = PGMparameter(1, 3)

#        rtail = self.comps['rtail'].props
#        rtail['pos'].params[''] = PGMparameter(1, 3)
#        rtail['pos'].params['lin'] = PGMparameter(2, 3)
#        rtail['scl'].params[''] = PGMparameter(2, 1)
#        rtail['rot'].params[''] = PGMparameter(2, 3)
#        rtail['ogn'].params[''] = PGMparameter(1, 3)

        vtail = self.comps['vtail'].props
        vtail['pos'].params[''] = PGMparameter(1, 3)
        vtail['pos'].params['lin'] = PGMparameter(2, 3)
        vtail['nor'].params[''] = PGMparameter(1, 3)
        vtail['scl'].params[''] = PGMparameter(2, 1)
        vtail['rot'].params[''] = PGMparameter(2, 3)
        vtail['ogn'].params[''] = PGMparameter(1, 3)

    def _define_dvs(self):
        dvs = self.dvs

        #main wing

        dvs['lwing_root_x'] = PGMdv((1), 16.).set_identity_param('lwing', 'pos', '', (0,0))
        dvs['lwing_root_y'] = PGMdv((1), -1.).set_identity_param('lwing', 'pos', '', (0,1))
        dvs['lwing_root_z'] = PGMdv((1), 2.6).set_identity_param('lwing', 'pos', '', (0,2))

        #relative to the root
        dvs['lwing_tip_x'] = PGMdv((1), 16.5).set_identity_param('lwing', 'pos', 'lin', (1,0))
        dvs['lwing_tip_y'] = PGMdv((1), 4.4).set_identity_param('lwing', 'pos', 'lin', (1,1))
        dvs['lwing_tip_z'] = PGMdv((1), 23.3).set_identity_param('lwing', 'pos', 'lin', (1,2))

        dvs['lwing_root_chord'] = PGMdv((1), 10).set_identity_param('lwing', 'scl', '', (0,0))
        dvs['lwing_mid_chord'] = PGMdv((1), 4.5).set_identity_param('lwing', 'scl', '', (1,0))
        dvs['lwing_tip_chord'] = PGMdv((1), 1.2).set_identity_param('lwing', 'scl', '', (2,0))


        #horz tail

        dvs['ltail_root_x'] = PGMdv((1), 44.0).set_identity_param('ltail', 'pos', '', (0,0))
        dvs['ltail_root_y'] = PGMdv((1), 0.).set_identity_param('ltail', 'pos', '', (0,1))
        dvs['ltail_root_z'] = PGMdv((1), 1.3).set_identity_param('ltail', 'pos', '', (0,2))

        dvs['ltail_tip_x'] = PGMdv((1), 6.0).set_identity_param('ltail', 'pos', 'lin', (1,0))
        dvs['ltail_tip_y'] = PGMdv((1), 1.4).set_identity_param('ltail', 'pos', 'lin', (1,1))
        dvs['ltail_tip_z'] = PGMdv((1), 8.0).set_identity_param('ltail', 'pos', 'lin', (1,2))

        dvs['ltail_root_chord'] = PGMdv((1), 4.).set_identity_param('ltail', 'scl', '', (0,0))
        #dvs['ltail_mid_chord'] = PGMdv((1), 4.5).set_identity_param('ltail', 'scl', '', (1,0))
        dvs['ltail_tip_chord'] = PGMdv((1), 1.).set_identity_param('ltail', 'scl', '', (1,0))


        #vertical tail


        dvs['vtail_root_x'] = PGMdv((1), 42.).set_identity_param('vtail', 'pos', '', (0,0))
        dvs['vtail_root_y'] = PGMdv((1), 1.7).set_identity_param('vtail', 'pos', '', (0,1))
        dvs['vtail_root_z'] = PGMdv((1), 0.0).set_identity_param('vtail', 'pos', '', (0,2))

        dvs['vtail_tip_x'] = PGMdv((1), 6.).set_identity_param('vtail', 'pos', 'lin', (1,0))
        dvs['vtail_tip_y'] = PGMdv((1), 8.).set_identity_param('vtail', 'pos', 'lin', (1,1))
        dvs['vtail_tip_z'] = PGMdv((1), 0.).set_identity_param('vtail', 'pos', 'lin', (1,2))

        dvs['vtail_root_chord'] = PGMdv((1), 5.8).set_identity_param('vtail', 'scl', '', (0,0))
        #dvs['vtail_mid_chord'] = PGMdv((1), 4.5).set_identity_param('vtail', 'scl', '', (1,0))
        dvs['vtail_tip_chord'] = PGMdv((1), 2.0).set_identity_param('vtail', 'scl', '', (1,0))


        #fuselage

        dvs['fus_root_x'] = PGMdv((1), 0.).set_identity_param('fuse', 'pos', '', (0,0))
        dvs['fus_root_y'] = PGMdv((1), 0.).set_identity_param('fuse', 'pos', '', (0,1))
        dvs['fus_root_z'] = PGMdv((1), 0.).set_identity_param('fuse', 'pos', '', (0,2))

        dvs['fus_tip_x'] = PGMdv((1), 36.).set_identity_param('fuse', 'pos', '', (1,0))
        dvs['fus_tip_y'] = PGMdv((1), 0.).set_identity_param('fuse', 'pos', '', (1,1))
        dvs['fus_tip_z'] = PGMdv((1), 0.).set_identity_param('fuse', 'pos', '', (1,2))

        dvs['diameter']  = PGMdv((1), 3.0).set_identity_param('fuse', 'scl', '', (0,0))



    def _compute_params(self):
        fuse = self.comps['fuse'].props
        fuse['pos'].params[''].val([[0,0,0],[36,0,0]])
        fuse['nor'].params[''].val([1.0])
        fuse['scl'].params[''].val([2.6])
        fuse['flt'].params[''].val([[0,0,0.5,0.5],[0,0,0.5,0.5]])
        fuse['pos'].params['nose'].val([[0,-1.1,0],[0,0,0],[0,0,0]])
        fuse['scl'].params['nose'].val([-1.5, 0, 0])
        fuse['scl'].params['tail'].val([0, -1.4])

        lwing = self.comps['lwing'].props
        lwing['pos'].params[''].val([16,-1,2.6])
        lwing['scl'].params[''].val([10,4.5,1.2])
        lwing['pos'].params['lin'].val([[0,0,0],[16.5,4.4,23.3]])

#        rwing = self.comps['rwing'].props
#        rwing['pos'].params[''].val([16,-1,-2.6])
#        rwing['scl'].params[''].val([1.2,4.5,10])
#        rwing['pos'].params['lin'].val([[16.5,4.4,-23.3],[0,0,0]])

#        lpylon = self.comps['lpylon'].props
#        lpylon['pos'].params[''].val([21.2,-0.5,9])
#        lpylon['pos'].params['lin'].val([[0,0,0],[-2,-0.5,0]])
#        lpylon['scl'].params[''].val([2.1,2.5])
#        lpylon['nor'].params[''].val([1,0,0])
#
#        lnac = self.comps['lnac'].props
#        lnac['pos'].params[''].val([16.4,-2.4,9])
#        lnac['pos'].params['lin'].val([[0,0,0],[4.5,0,0]])
#        lnac['nor'].params[''].val([1])
#        lnac['scl'].params[''].val([1.25])
#        lnac['thk'].params[''].val([0.08,0.2,0.08])

        ltail = self.comps['ltail'].props
        ltail['pos'].params[''].val([44,0,1.3])
        ltail['pos'].params['lin'].val([[0,0,0],[6,1.4,8]])
        ltail['scl'].params[''].val([4,1])
        ltail['rot'].params[''].val([[0,10,0],[0,0,0]])
        ltail['ogn'].params[''].val([0.25,0,0])

#        rtail = self.comps['rtail'].props
#        rtail['pos'].params[''].val([44,0,-1.3])
#        rtail['pos'].params['lin'].val([[6,1.4,-8],[0,0,0]])
#        rtail['scl'].params[''].val([1,4])
#        rtail['rot'].params[''].val([[0,0,0],[0,-10,0]])
#        rtail['ogn'].params[''].val([0.25,0,0])

        vtail = self.comps['vtail'].props
        vtail['pos'].params[''].val([42,1.7,0])
        vtail['pos'].params['lin'].val([[0,0,0],[6,8,0]])
        vtail['nor'].params[''].val([1,0,0])
        vtail['scl'].params[''].val([5.8,2])
        vtail['rot'].params[''].val([[0,10,0],[0,0,0]])
        vtail['ogn'].params[''].val([0.25,0,0])

        return [], [], []

    def _set_bspline_options(self):
        comps = self.comps

        comps['fuse'].faces['rgt'].set_option('num_cp', 'u', [12,12,12,12])#[4,4,4,4]
        comps['fuse'].faces['rgt'].set_option('num_cp', 'v', [54,12,12,12,12,24,12,45,12,12,30,12])#[18,4,4,4,4,8,4,15,4,4,10,4]
        comps['fuse'].faces['rgt'].set_option('num_pt', 'v', [120,48,48,48,48,180,48,120,48,48,210,48], both=False)#40,16,16,16,16,60,16,60,16,16,70,16
        comps['fuse'].faces['top'].set_option('num_cp', 'u', [24,24]) #8,8
        comps['lwing'].faces['upp'].set_option('num_cp', 'v', [36,24,24,120]) #[6,4,4,20]

    #def meshStructure(self):
        #afm = Airframe(self, 1) #0.2)


    ##main wing leading section ribs
        #idims = numpy.linspace(0.45,0.9,7)
        #jdims = numpy.linspace(0,1,16)
        #for i in range(idims.shape[0]-1):
            #for j in range(jdims.shape[0]):
                #afm.addVertFlip('lwing_r::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i+1],jdims[j]])
        ##afm.addVertFlip('rwing_i_r::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i+1],1-jdims[j]])




        ##main wing leading section spars

        #for i in range(idims.shape[0]):
            #for j in range(jdims.shape[0]-1):
                #if i is 0 or i is idims.shape[0]-1:
                    #afm.addVertFlip('lwing_s::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]])
                ##afm.addVertFlip('rwing_i_s::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i],1-jdims[j+1]])
                #else:
##                    afm.addVertFlip('lwing_i_sa::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[1,0.85])
##                    afm.addVertFlip('lwing_i_sb::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[0.15,0])
                    #afm.addVertFlip('lwing_s::'+str(i)+':'+str(j),'lwing',[idims[i],jdims[j]],[idims[i],jdims[j+1]])



##                    afm.addVertFlip('rwing_i_sa::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i],1-jdims[j+1]],w=[1,0.85])
##                    afm.addVertFlip('rwing_i_sb::'+str(i)+':'+str(j),'rwing',[idims[i],1-jdims[j]],[idims[i],1-jdims[j+1]],w=[0.15,0])






        ##wing box lower/back edge
        #idims = numpy.linspace(0.18,0.45,6)
        #for j in range(idims.shape[0]-1):
            #afm.addVertFlip('lwing_i_i1::'+str(j)+':0','lwing',[idims[j],jdims[j]],[idims[j+1],jdims[j+1]])
            ##afm.addVertFlip('rwing_i_i1::'+str(j)+':0','rwing',[idims[j],1-jdims[j]],[idims[j+1],1-jdims[j+1]])
            #afm.addVertFlip('lwing_i_i2::'+str(j)+':0','lwing',[idims[j],jdims[j]],[0.45,jdims[j]])
        ##afm.addVertFlip('rwing_i_i2::'+str(j)+':0','rwing',[idims[j],1-jdims[j]],[0.45,1-jdims[j]])


        ##wing box connection inside fuselage spars
##        idims = numpy.linspace(0.45,0.85,7)
##        jdims = numpy.linspace(0,1,16)
##        for i in range(idims.shape[0]):
##            if i is 0 or i is idims.shape[0]-1:
##                afm.addCtrVert('lwing_Misc_1::'+str(i)+':'+str(j),'lwing','rwing',idims[i])
##            else:
##                afm.addCtrVert('lwing_Misc_2::'+str(i)+':'+str(j),'lwing','rwing',idims[i],w=[1,0.85])
##                afm.addCtrVert('lwing_Misc_3::'+str(i)+':'+str(j),'lwing','rwing',idims[i],w=[0.15,0])
##        for i in range(idims.shape[0]-1):
##            afm.addCtr('lwing_Misc_4::','lwing','rwing',0,[idims[i],idims[i+1]])
##        for i in range(idims.shape[0]-1):
##            afm.addCtr('lwing_Misc_5::','lwing','rwing',1,[1-idims[i],1-idims[i+1]])
##        afm.addCtrVert('lwing_Misc_6::'+str(i)+':'+str(j),'lwing','rwing',0.18)



        ##ribs for horizontal and vertical tail
        #idims = numpy.linspace(0.25,0.65,2)
        #jdims = numpy.linspace(0,0.9,10)
        #for i in range(idims.shape[0]-1):
            #for j in range(jdims.shape[0]):
                #afm.addVertFlip('ltail_r::'+str(i)+':'+str(j),'ltail',[idims[i],jdims[j]],[idims[i+1],jdims[j]])
                ##afm.addVertFlip('rtail_i_r::'+str(i)+':'+str(j),'rtail',[idims[i],1-jdims[j]],[idims[i+1],1-jdims[j]])
                #afm.addVertFlip('vtail_r::'+str(i)+':'+str(j),'vtail',[idims[i],jdims[j]],[idims[i+1],jdims[j]])



        ##spars for horizontal and vertical tail
        #for i in range(idims.shape[0]):
            #for j in range(jdims.shape[0]-1):
                #afm.addVertFlip('ltail_s::'+str(i)+':'+str(j),'ltail',[idims[i],jdims[j]],[idims[i],jdims[j+1]])
                ##afm.addVertFlip('rtail_i_s::'+str(i)+':'+str(j),'rtail',[idims[i],1-jdims[j]],[idims[i],1-jdims[j+1]])
                #afm.addVertFlip('vtail_s::'+str(i)+':'+str(j),'vtail',[idims[i],jdims[j]],[idims[i],jdims[j+1]])



        ##i think internal components for tails
##        for i in range(idims.shape[0]):
##                afm.addCtrVert('ltail_Misc_1::'+str(i)+':'+str(j),'ltail','rtail',idims[i])
##        for i in range(idims.shape[0]-1):
##            afm.addCtr('ltail_Misc_2::'+str(i)+':0','ltail','rtail',0,[idims[i],idims[i+1]])
##        for i in range(idims.shape[0]-1):
##            afm.addCtr('ltail_Misc_3::+str(i)'+':0','ltail','rtail',1,[1-idims[i],1-idims[i+1]])




        ##fuselage rings
        #idims = numpy.linspace(0,1,4)
        #jdims = numpy.linspace(0,1,20)
        #for i in range(idims.shape[0]-1):
            #for j in range(jdims.shape[0]):
                #afm.addVert('fuse_r1::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i+1],jdims[j]],w=[1.0,0.94],i=[0,2])
                #afm.addVert('fuse_r2::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i+1],jdims[j]],w=[1.0,0.94],i=[1,3])
                #afm.addVert('fuse_r3::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i+1],jdims[j]],w=[1.0,0.94],i=[2,0])
                #afm.addVert('fuse_r4::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i+1],jdims[j]],w=[1.0,0.94],i=[3,1])



        ##fuselage longerons
        #for i in range(idims.shape[0]-1):
            #for j in range(jdims.shape[0]-1):
                #afm.addVert('fuse_l1::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[1.0,0.97],i=[0,2])
                #afm.addVert('fuse_l2::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[1.0,0.97],i=[1,3])
                #afm.addVert('fuse_l3::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[1.0,0.97],i=[2,0])
                #afm.addVert('fuse_l4::'+str(i)+':'+str(j),'fuse',[idims[i],jdims[j]],[idims[i],jdims[j+1]],w=[1.0,0.97],i=[3,1])



        ##probably intersection
        #for j in range(jdims.shape[0]-1):
            #afm.addVertFlip('fus_Misc_1::'+str(j)+':0','fuse',[0.4,jdims[j]],[0.4,jdims[j+1]],w=[1.0,0.5],i=[0,2])
            #afm.addVertFlip('fus_Misc_2::'+str(j)+':0','fuse',[0.4,jdims[j]],[0.4,jdims[j+1]],w=[0.5,0.0],i=[0,2])




        #afm.preview('conventional_pvw.dat')
        #afm.mesh()
        #afm.computeMesh('conventional_str')



    def aircraft_params(self,aircraft):
        print




if __name__ == '__main__':

    pgm = Conventional5()
    bse = pgm.initialize()

    pgm.comps['lwing'].set_airfoil('rae2822.dat')
    pgm.comps['ltail'].set_airfoil()
    #main wing

    pgm.dvs['lwing_root_x'].data[0] = 16.
    pgm.dvs['lwing_root_y'].data[0] = -1.
    pgm.dvs['lwing_root_z'].data[0] = 2.6

    #relative to the root
    pgm.dvs['lwing_tip_x'].data[0] = 16.5
    pgm.dvs['lwing_tip_y'].data[0] = 4.4
    pgm.dvs['lwing_tip_z'].data[0] = 23.3

    pgm.dvs['lwing_root_chord'].data[0] = 10.
    pgm.dvs['lwing_mid_chord'].data[0] = 4.5
    pgm.dvs['lwing_tip_chord'].data[0] = 1.2


    #horz tail

    pgm.dvs['ltail_root_x'].data[0] = 44.0
    pgm.dvs['ltail_root_y'].data[0] = 0.
    pgm.dvs['ltail_root_z'].data[0] = 1.3

    pgm.dvs['ltail_tip_x'].data[0] = 6.0
    pgm.dvs['ltail_tip_y'].data[0] = 1.4
    pgm.dvs['ltail_tip_z'].data[0] = 8.0

    pgm.dvs['ltail_root_chord'].data[0] = 4.
    #pgm.dvs['ltail_mid_chord'].data[0] = 4.5
    pgm.dvs['ltail_tip_chord'].data[0] = 1.


    #vertical tail


    pgm.dvs['vtail_root_x'].data[0] = 42.
    pgm.dvs['vtail_root_y'].data[0] = 1.7
    pgm.dvs['vtail_root_z'].data[0] = 0.0

    pgm.dvs['vtail_tip_x'].data[0] = 6.
    pgm.dvs['vtail_tip_y'].data[0] = 8.
    pgm.dvs['vtail_tip_z'].data[0] = 0.

    pgm.dvs['vtail_root_chord'].data[0] = 5.8
    #pgm.dvs['vtail_mid_chord'].data[0] = 4.5
    pgm.dvs['vtail_tip_chord'].data[0] = 2.0


    #fuselage

    pgm.dvs['fus_root_x'].data[0] = 0.
    pgm.dvs['fus_root_y'].data[0] = 0.
    pgm.dvs['fus_root_z'].data[0] = 0.

    pgm.dvs['fus_tip_x'].data[0] = 50.
    pgm.dvs['fus_tip_y'].data[0] = 0.
    pgm.dvs['fus_tip_z'].data[0] = 0.

    pgm.dvs['diameter'].data[0] = 2.6
    pgm.compute_all()

    #bse.vec['pt_str']._hidden[:] = False
    bse.vec['pt_str'].export_tec_str()
    #bse.vec['df'].export_tec_scatter()
    #bse.vec['cp'].export_tec_scatter()
    #bse.vec['pt'].export_tec_scatter()
    #bse.vec['cp_str'].export_IGES()
    bse.vec['cp_str'].export_STL('conventional_airc.stl')

    pgm.meshStructure()
