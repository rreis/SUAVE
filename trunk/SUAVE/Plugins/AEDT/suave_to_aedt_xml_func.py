# suave_to_aedt_xml_func.py
# 
# Created:  Sum 2015, T, MacDonald
# Modified: Aug 2016, T. MacDonald

import lxml.etree as ET # Use pip to download lxml if needed
import lxml.builder
from SUAVE.Core import Data, DataOrdered
import SUAVE
from os.path import isfile
import numpy as np

from BADA3_fitting import main as SUAVE_bada_fit
from ANP_fitting import main as SUAVE_anp_fit

# Select aircraft file and mission file names here
from bada3_737800_to_numpy import main as create_bada
from bada3_737800_to_numpy import vehicle_setup as bada_vehicle
from anp_737800_to_numpy import main as create_anp
from anp_737800_to_numpy import vehicle_setup as anp_vehicle
from point_profile_gen import main as profile_gen

def read_inputs():
    base_filename = '737_Val'
    general_ID = '737800_V'
    
    # Airframe Data
    af = Data()
    
    af.model = 'Boeing 737800V Series'
    af.engineCount = '2'
    af.engineLocation = 'W'
    af.designationCode = 'C'
    af.maxRange = '4000'
    af.euroGroupCode = 'JS'
    af.usageCode = 'P'
    af.sizeCode = 'L'
    af.engineType = 'J'
    af.auxiliaryPowerUnitId = 'APU 131-9'  
    
    return (base_filename, general_ID, af)
    
def build_data_files(base_filename, output=False):
    # Build mission data files if needed
    if isfile('bada3_' + base_filename + '_climbISA.npy'):
        while True:
            resp = raw_input('BADA mission files exist with base name ' + base_filename + ' already exist. Use or overwrite? [use/overwrite]:\n')
            if resp == 'use':
                break
            elif resp == 'overwrite':
                create_bada(base_filename)
                break
            else:
                print 'Type \'use\' or \'overwrite\''
    else:
        create_bada(base_filename)
        
    if isfile('anp_' + base_filename + '_takeoff_accel.npy'):
        while True:
            resp = raw_input('ANP mission files exist with base name ' + base_filename + ' already exist. Use or overwrite? [use/overwrite]:\n')
            if resp == 'use':
                break
            elif resp == 'overwrite':
                create_anp(base_filename)
                break
            else:
                print 'Type \'use\' or \'overwrite\''        
    else:
        create_anp(base_filename)    
        
    profile_flag = False
    
    # Build mission data files if needed
    if isfile('points_' + base_filename + '_SUAVE_climb.npy'):
        while True:
            resp = raw_input('Profile point files exist with base name ' + base_filename + ' already exist. Use, overwrite, or ignore? [use/overwrite/ignore]:\n')
            if resp == 'use':
                profile_flag = True
                break
            elif resp == 'overwrite':
                profile_gen(base_filename)
                profile_flag = True
                break
            elif resp == 'ignore':
                break
            else:
                print 'Type \'use\', \'overwrite\', or \'ignore\''
    else:
        resp = raw_input('Profile point files do not exist with base name ' + base_filename +'. Create? [y/n]:\n')
        if resp == 'y':
            profile_gen(base_filename)
            profile_flag = True
        elif resp == 'n':
            pass
        else:
            print 'Type \'y\' or \'n\''    
    

    return profile_flag    
    
def build_xml_tree(base_filename,general_ID,af,profile_flag):
    EM = lxml.builder.ElementMaker()
    
    airframe_tree = EM.airframe(
        EM.model(af.model),
        EM.engineCount(af.engineCount),
        EM.engineLocation(af.engineLocation),
        EM.designationCode(af.designationCode),
        EM.maxRange(af.maxRange),
        EM.euroGroupCode(af.euroGroupCode),
        EM.usageCode(af.usageCode),
        EM.sizeCode(af.sizeCode),
        EM.engineType(af.engineType),
        EM.auxiliaryPowerUnitId(af.auxiliaryPowerUnitId),
        )
    
    # Create a separate BADA data file for each aircraft in the future
    
    inputs = Data()
    inputs.tow=None
    bd_vehicle = bada_vehicle(inputs)
    bd = bd_vehicle.BADA
    (badaThrustArray,badaFuelArray,badaDragArray,coeff) = SUAVE_bada_fit(base_filename)
    
    bd.phase = [] 
    bd.configName = [] 
    bd.stallSpeed = [] 
    bd.parasiticDrag = [] 
    bd.inducedDrag = [] 
    
    bd.phase.append(badaDragArray[0])
    bd.configName.append(badaDragArray[1])
    bd.stallSpeed.append(badaDragArray[2])
    bd.parasiticDrag.append(badaDragArray[3])
    bd.inducedDrag.append(badaDragArray[4])
     
    bd.coeff_CF1 = badaFuelArray[0]
    bd.coeff_CF2 = badaFuelArray[1]
    bd.coeff_CF3 = badaFuelArray[2]
    bd.coeff_CF4 = badaFuelArray[3]
    bd.coeff_CR = badaFuelArray[4]
    
    bd.coeff_TC1 = badaThrustArray[0]
    bd.coeff_TC2 = badaThrustArray[1]
    bd.coeff_TC3 = badaThrustArray[2]
    bd.coeff_TC4 = badaThrustArray[3]
    bd.coeff_TC5 = badaThrustArray[4]
    bd.coeff_TDL = badaThrustArray[5]
    bd.coeff_TDH = badaThrustArray[6]
    bd.coeff_APP = badaThrustArray[7]
    bd.coeff_LD = badaThrustArray[8]
    
    # <badaAirplane> ######################################################################
    
    badaAirplane_tree = EM.badaAirplane(
        EM.badaAirplaneId(bd.badaAirplaneId),                  
        EM.mfgDescription(bd.mfgDescription),                       
        EM.numEngines(bd.numEngines),
        EM.engineTypeCode(bd.engineTypeCode),
        EM.wakeCategory(bd.wakeCategory),
        EM.referenceAircraftMass(bd.referenceAircraftMass),
        EM.minAircraftMass(bd.minAircraftMass),
        EM.maxAircraftMass(bd.maxAircraftMass),
        EM.maxPayloadMass(bd.maxPayloadMass),
        EM.weightGradient(bd.weightGradient),
        EM.maxOperatingSpeed(bd.maxOperatingSpeed),
        EM.maxOperatingMachNumber(bd.maxOperatingMachNumber),
        EM.maxOperatingAltitude(bd.maxOperatingAltitude),
        EM.maxAltitudeAtMaxTakeoffWeight(bd.maxAltitudeAtMaxTakeoffWeight),
        EM.temperatureGradientOnMaximumAltitude(bd.temperatureGradientOnMaximumAltitude),
        EM.wingSurfaceArea(bd.wingSurfaceArea),
        EM.buffetOnsetLiftCoeff(bd.buffetOnsetLiftCoeff),
        EM.buffetingGradient(bd.buffetingGradient),
        EM.machDragCoeff(bd.machDragCoeff),
        )
    
    new_bada_tree = EM.bada_temp()
    
    new_bada_tree.append(badaAirplane_tree)
    
    # <badaAltitudeDistributionSet> #######################################################     
    
    badaAltitudeDist_tree = EM.badaAltitudeDistributionSet(
        EM.badaAirplaneId(bd.badaAirplaneId),
        )
    
    for ii in range(len(bd.altitudeCount)):
        subtree = EM.altitudeDistribution(
            EM.altitudeCount(bd.altitudeCount[ii]),
            EM.distanceMean(bd.distanceMean[ii]),
            EM.distanceStddev(bd.distanceStddev[ii]),
            EM.distanceLow(bd.distanceLow[ii]),
            EM.distanceHigh(bd.distanceHigh[ii]),
            EM.altitude(bd.altitude[ii])
            )   
        badaAltitudeDist_tree.append(subtree)
    
    
    new_bada_tree.append(badaAltitudeDist_tree)
    
    # <badaProfileSet> ####################################################################                  
    
    badaProfileSet_tree = EM.badaProfileSet(
        EM.badaAirplaneId(bd.badaAirplaneId),
        )
    
    for ii in range(len(bd.massRangeValue)):
        subtree = EM.profile(
            EM.massRangeValue(bd.massRangeValue[ii]),
            EM.companyCode1(bd.companyCode1[ii]),
            EM.companyCode2(bd.companyCode2[ii]),
            EM.companyName(bd.companyName[ii]),
            EM.aircraftVersion(bd.aircraftVersion[ii]),
            EM.engine(bd.engine[ii]),
            EM.climbSpeedBelowTransitionAltitude(bd.climbSpeedBelowTransitionAltitude[ii]),
            EM.climbSpeedAboveTransitionAltitude(bd.climbSpeedAboveTransitionAltitude[ii]),
            EM.climbMachNumber(bd.climbMachNumber[ii]),
            EM.cruiseSpeedBelowTransitionAltitude(bd.cruiseSpeedBelowTransitionAltitude[ii]),
            EM.cruiseSpeedAboveTransitionAltitude(bd.cruiseSpeedAboveTransitionAltitude[ii]),
            EM.cruiseMachNumber(bd.cruiseMachNumber[ii]),
            EM.descentSpeedUnderTransitionAltitude(bd.descentSpeedUnderTransitionAltitude[ii]),
            EM.descentSpeedOverTransitionAltitude(bd.descentSpeedOverTransitionAltitude[ii]),
            EM.descentMachNumber(bd.descentMachNumber[ii]),
            )
        badaProfileSet_tree.append(subtree)
    
    new_bada_tree.append(badaProfileSet_tree)
    
    # <badaConfigSet> #####################################################################    
    
    badaConfigSet_tree = EM.badaConfigSet(
        EM.badaAirplaneId(bd.badaAirplaneId),
        )
    
    for ii in range(len(bd.phase)):
        subtree = EM.badaConfig(
            EM.phase(bd.phase[ii]),
            EM.configName(bd.configName[ii]),
            EM.stallSpeed(bd.stallSpeed[ii]),
            EM.parasiticDrag(bd.parasiticDrag[ii]),
            EM.inducedDrag(bd.inducedDrag[ii]),
            )    
        badaConfigSet_tree.append(subtree)
    
    new_bada_tree.append(badaConfigSet_tree)
    
    # <badaFuel> ##########################################################################   
    
    badaFuel_tree = EM.badaFuel(
        EM.badaAirplaneId(bd.badaAirplaneId),
        EM.coeff_CF1(bd.coeff_CF1),
        EM.coeff_CF2(bd.coeff_CF2),
        EM.coeff_CF3(bd.coeff_CF3),
        EM.coeff_CF4(bd.coeff_CF4),
        EM.coeff_CR(bd.coeff_CR),
        )
    
    new_bada_tree.append(badaFuel_tree)
    
    # <badaThrust> ########################################################################   
    
    badaThrust_tree = EM.badaThrust(
        EM.badaAirplaneId(bd.badaAirplaneId),
        EM.coeff_TC1(bd.coeff_TC1),
        EM.coeff_TC2(bd.coeff_TC2),
        EM.coeff_TC3(bd.coeff_TC3),
        EM.coeff_TC4(bd.coeff_TC4),
        EM.coeff_TC5(bd.coeff_TC5),
        EM.coeff_TDL(bd.coeff_TDL),
        EM.coeff_TDH(bd.coeff_TDH),
        EM.coeff_APP(bd.coeff_APP),
        EM.coeff_LD(bd.coeff_LD),
        EM.descentAlt(bd.descentAlt),
        EM.descentSpeed(bd.descentSpeed),
        EM.descentMach(bd.descentMach),
        )
    
    new_bada_tree.append(badaThrust_tree)
    
    
    # ##########################
    # ANP Data        ##########
    # ##########################
    
    inputs = Data()
    inputs.tow=None
    an_vehicle = anp_vehicle(inputs)
    an = an_vehicle.ANP
    an.anpAirplaneId = general_ID # this overrides ANP vehicle data
    (anpThrustSet,anpFlapsSet) = SUAVE_anp_fit(base_filename)
    
    #anpFlapsSet
    an.flapId = []
    an.operationType = []
    an.coeff_R = []
    an.coeff_CD = []
    an.coeff_B = []
    
    
    for ii in range(len(anpFlapsSet.tag)):
        an.flapId.append(anpFlapsSet.tag[ii])
        an.operationType.append(anpFlapsSet.op[ii])
        an.coeff_R.append(anpFlapsSet.R[ii])
        an.coeff_CD.append(anpFlapsSet.CD[ii])
        an.coeff_B.append(anpFlapsSet.B[ii])
    
    #anpThrustSet
    an.thrustType = []
    an.coeff_E = []
    an.coeff_F = []
    an.coeff_GA = []
    an.coeff_GB = []
    an.coeff_H = []
    
    an.mode1 = []
    an.beta1 = []
    an.beta2 = []
    an.beta3 = []
    an.alpha = []
    
    an.mode2 = []
    an.K1 = []
    an.K2 = []
    an.K3 = []
    an.K4 = []
    
    for ii in range(len(anpThrustSet.tag)):
        an.thrustType.append(anpThrustSet.tag[ii])
        an.coeff_E.append(anpThrustSet.E[ii])
        an.coeff_F.append(anpThrustSet.F[ii])
        an.coeff_GA.append(anpThrustSet.GA[ii])
        an.coeff_GB.append(anpThrustSet.GB[ii])
        an.coeff_H.append(anpThrustSet.H[ii])
    
    an.mode1.append('A')
    an.beta1.append(anpThrustSet.beta1)
    an.beta2.append(anpThrustSet.beta2)
    an.beta3.append(anpThrustSet.beta3)
    an.alpha.append(anpThrustSet.alpha)
    
    an.mode2.append('D')
    an.K1.append(anpThrustSet.K1)
    an.K2.append(anpThrustSet.K2)
    an.K3.append(anpThrustSet.K3)
    an.K4.append(anpThrustSet.K4)
    
    # <anpAirplane> #######################################################################  
    
    anpAirplane_tree = EM.anpAirplane(
        EM.anpAirplaneId(an.anpAirplaneId),
        EM.description(an.description),
        EM.sizeCode(an.sizeCode),
        EM.owner(an.owner),
        EM.engineTypeCode(an.engineTypeCode),
        EM.numberEngines(an.numberEngines),
        EM.maxGrossWeightTakeoff(an.maxGrossWeightTakeoff),
        EM.maxGrossWeightLand(an.maxGrossWeightLand),
        EM.maxDsStop(an.maxDsStop),
        EM.depThrustCoeffType(an.depThrustCoeffType),
        EM.thrustStatic(an.thrustStatic),
        EM.thrustRestore(an.thrustRestore),
        EM.noiseId(an.noiseId),
        EM.noiseCategory(an.noiseCategory),
        EM.minBurn(an.minBurn),
        )
    
    
    # <anpFlapsSet> #######################################################################  
    
    anpFlapsSet_tree = EM.anpFlapsSet(
        EM.anpAirplaneId(an.anpAirplaneId),
        )
    
    for ii in range(len(an.flapId)):
        subtree = EM.flaps(
            EM.flapId(an.flapId[ii]),
            EM.operationType(an.operationType[ii]),
            EM.coeff_R(an.coeff_R[ii]),
            EM.coeff_CD(an.coeff_CD[ii]),
            EM.coeff_B(an.coeff_B[ii]),
            )    
        anpFlapsSet_tree.append(subtree)
        
    # <anpThrustSet> ###################################################################### 
    
    anpThrustSet_tree = EM.anpThrustSet(
        EM.anpAirplaneId(an.anpAirplaneId),
        )
    
    for ii in range(len(an.thrustType)):
        subtree = EM.thrustJet(
            EM.thrustType(an.thrustType[ii]),
            EM.coeff_E(an.coeff_E[ii]),
            EM.coeff_F(an.coeff_F[ii]),
            EM.coeff_GA(an.coeff_GA[ii]),
            EM.coeff_GB(an.coeff_GB[ii]),
            EM.coeff_H(an.coeff_H[ii]),
            )
        anpThrustSet_tree.append(subtree)
        
    for ii in range(1):
        subtree = EM.tsfcCoefficients(
            EM.mode(an.mode1[ii]),
            EM.beta1(an.beta1[ii]),
            EM.beta2(an.beta2[ii]),
            EM.beta3(an.beta3[ii]),
            EM.alpha(an.alpha[ii]),
            )
        anpThrustSet_tree.append(subtree)
        
    for ii in range(1):
        subtree = EM.tsfcCoefficients(
            EM.mode(an.mode2[ii]),
            EM.k1(an.K1[ii]),
            EM.k2(an.K2[ii]),
            EM.k3(an.K3[ii]),
            EM.k4(an.K4[ii]),
            )
        anpThrustSet_tree.append(subtree)
        
    # <anpProfileSet> ##################################################################### 
    
    anpProfileSet_tree = EM.anpProfileSet(
        EM.anpAirplaneId(an.anpAirplaneId),
        )
    if profile_flag == True:
        base_anp_len = len(an.profile)
        segs = DataOrdered()
        segs.SUAVE_climb   = np.load('points_' + base_filename + '_SUAVE_climb.npy')
        segs.SUAVE_descent = np.load('points_' + base_filename + '_SUAVE_descent.npy')
        for ii,seg_key in enumerate(segs.keys()):
            an.profile.append(Data())
            if segs[seg_key][0,1] == 0.0:
                an.profile[ii+base_anp_len].operationType = 'A'
            elif segs[seg_key][0,1] == 1.0:
                an.profile[ii+base_anp_len].operationType = 'D'
            elif segs[seg_key][0,1] == 2.0:
                an.profile[ii+base_anp_len].operationType = 'L'       
            else:
                raise ValueError
            an.profile[ii+base_anp_len].profileGroupId = 'STANDARD'
            an.profile[ii+base_anp_len].profileStageLength = str(ii+base_anp_len)
            an.profile[ii+base_anp_len].weight = str(int(segs[seg_key][0,6]))
            an.profile[ii+base_anp_len].profilePoints = Data()
            an.profile[ii+base_anp_len].profilePoints.point = []
            for jj in range(len(segs[seg_key][:,0])):
                an.profile[ii+base_anp_len].profilePoints.point.append(Data())
                an.profile[ii+base_anp_len].profilePoints.point[jj].pointNum = str(jj+1)
                an.profile[ii+base_anp_len].profilePoints.point[jj].altitude = str(segs[seg_key][jj,2])
                an.profile[ii+base_anp_len].profilePoints.point[jj].distance = str(segs[seg_key][jj,3])
                an.profile[ii+base_anp_len].profilePoints.point[jj].speed = str(segs[seg_key][jj,4])
                an.profile[ii+base_anp_len].profilePoints.point[jj].thrustSet = str(segs[seg_key][jj,5])
                an.profile[ii+base_anp_len].profilePoints.point[jj].opMode = an.profile[ii+base_anp_len].operationType 
            an.profile[ii+base_anp_len].seg_type = 'points'
    
    for ii in range(len(an.profile)):
        if (an.profile[ii].seg_type == 'points'):
            point_data = []
            for jj in range(len(an.profile[ii].profilePoints.point)):
                point_tree = EM.point(
                    EM.pointNum(an.profile[ii].profilePoints.point[jj].pointNum),
                    EM.distance(an.profile[ii].profilePoints.point[jj].distance),
                    EM.altitude(an.profile[ii].profilePoints.point[jj].altitude),
                    EM.speed(an.profile[ii].profilePoints.point[jj].speed),
                    EM.thrustSet(an.profile[ii].profilePoints.point[jj].thrustSet),
                    EM.opMode(an.profile[ii].profilePoints.point[jj].opMode),
                    )
                point_data.append(point_tree)
            point_tree = EM.profilePoints(point_data[0])
            for jj in range(len(an.profile[ii].profilePoints.point))[1:]:
                point_tree.append(point_data[jj])
            subtree = EM.profile(
                EM.operationType(an.profile[ii].operationType),
                EM.profileGroupId(an.profile[ii].profileGroupId),
                EM.profileStageLength(an.profile[ii].profileStageLength),
                EM.weight(an.profile[ii].weight),
                point_tree,
                )
        elif (an.profile[ii].seg_type == 'steps'):
            step_data = []
            for jj in range(len(an.profile[ii].procedureSteps.step)):
                step_tree = EM.step(
                    EM.stepNum(an.profile[ii].procedureSteps.step[jj].stepNum),
                    EM.flapId(an.profile[ii].procedureSteps.step[jj].flapId),
                    EM.stepType(an.profile[ii].procedureSteps.step[jj].stepType),
                    EM.thrustType(an.profile[ii].procedureSteps.step[jj].thrustType),
                    EM.param1(an.profile[ii].procedureSteps.step[jj].param1),
                    EM.param2(an.profile[ii].procedureSteps.step[jj].param2),
                    EM.param3(an.profile[ii].procedureSteps.step[jj].param3),
                    )
                step_data.append(step_tree)
            step_tree = EM.procedureSteps(step_data[0])
            for jj in range(len(an.profile[ii].procedureSteps.step))[1:]:
                step_tree.append(step_data[jj])
            subtree = EM.profile(
                EM.operationType(an.profile[ii].operationType),
                EM.profileGroupId(an.profile[ii].profileGroupId),
                EM.profileStageLength(an.profile[ii].profileStageLength),
                EM.weight(an.profile[ii].weight),
                step_tree,
                )
        else:
            raise(ValueError,'Profile Operation Type Not Supported')
        anpProfileSet_tree.append(subtree)
    
    
    # <aircraft> ##########################################################################   
    
    aircraft_tree = EM.aircraft(
        EM.description(bd.description),
        EM.airframeModel(af.model),
        EM.engineCode(bd.engineCode),
        EM.engineModCode(bd.engineModCode),
        EM.anpAirplaneId(an.anpAirplaneId),
        EM.badaAirplaneId(bd.badaAirplaneId),
        )
    
    new_bada_tree.append(aircraft_tree)
    
    # <energyShare> #######################################################################   
    
    energyShare_tree = EM.energyShare(
        EM.anpAirplaneId(an.anpAirplaneId),
        EM.badaAirplaneId(bd.badaAirplaneId),
        EM.transEnergyShare(bd.transEnergyShare),
        )
    
    new_bada_tree.append(energyShare_tree)
    
    # ##########################
    # File Operations ##########
    # ##########################
    
    new_full_tree = EM.AsifXml(
        EM.fleet(airframe_tree,
                 anpAirplane_tree,
                 anpFlapsSet_tree,
                 anpThrustSet_tree,
                 anpProfileSet_tree,
                 badaAirplane_tree,
                 badaAltitudeDist_tree,
                 badaProfileSet_tree,
                 badaConfigSet_tree,
                 badaFuel_tree,
                 badaThrust_tree,
                 aircraft_tree,
                 energyShare_tree,
                 ),
        )
    
    lxml.etree.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    lxml.etree.register_namespace('xsd', 'http://www.w3.org/2001/XMLSchema')
    new_full_tree.set('{http://www.w3.org/2001/XMLSchema-instance}xsi', '')
    new_full_tree.set('{http://www.w3.org/2001/XMLSchema}xsd', '')
    for xx in new_full_tree.attrib: del new_full_tree.attrib[xx]
    new_full_tree.set('version', '1.2.11')
    new_full_tree.set('content', 'fleet')
            
    new_anp_bada = 'AEDT_import_' + base_filename +'.xml'
    f1 = open(new_anp_bada,'w')
    f1.write(lxml.etree.tostring(new_full_tree, pretty_print=True))
    f1.close()    

def main():
    (base_filename, general_ID, af) = read_inputs()
    profile_flag = build_data_files(base_filename)
    build_xml_tree(base_filename,general_ID,af,profile_flag)
    print 'AEDT_import_' + base_filename +'.xml' + ' created!'

main()
    