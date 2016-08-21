# h_i = altitude [ft]
# TAS_i = true airspeed [kt]
# m_i = aircraft mass [kg]
# ROC_i = rate of climb [fpm]

# Debug:
# climb_ISA[:,ind_mass][climb_ISA[:,ind_seg]==7]

import csv
import SUAVE
import numpy as np
import scipy.optimize as spo
import pylab as plt
from SUAVE.Core import (
Data, Container, Data_Exception, Data_Warning, Units
)

def funcf(h,M,T,dT,segType):
    # Set standard values, based on bada user manual
    k = 1.4 # adiabatic index, same as gamma
    R = 287.05287 # real gas constant for air [m^2/(K*s^2)]
    g = 9.80665
    #b = -.0065 # ISA temperature gradient below the tropopause [K/m]
    s = segType # shortened for convenience
    
    ESF = np.zeros(len(h))
    b   = np.zeros(len(h))
    b[h<36089.0] = -.0065 # otherwise no temp gradient
    # Use segment type for calculations
    # 1.0 => constant CAS
    # 2.0 => constant mach
    # 3.0 => climb accel
    # 4.0 => climb decel
    # 5.0 => descent accel
    # 6.0 => descent decel
    ESF[s==1.0] = (1. + k*R*b[s==1.0]/2./g*M[s==1.0]**2*(T[s==1.0]-dT[s==1.0])/T[s==1.0] + (1.+(k-1.)/2.*M[s==1.0]**2)**(-1./(k-1.))*((1.+(k-1.)/2.*M[s==1.0]**2)**(k/(k-1.)) - 1.))**-1
    ESF[s==2.0] = (1. + k*R*b[s==2.0]/2./g*M[s==2.0]**2*(T[s==2.0]-dT[s==2.0])/T[s==2.0])**-1
    ESF[s==3.0] = 0.3
    ESF[s==4.0] = 1.7
    ESF[s==5.0] = 1.7
    ESF[s==6.0] = 0.3
        
    return ESF

def main(base_filename):
    climb_segs = 9
    nonISA_segs = 6
    descent_segs = 3
    cruise_segs = 1
    # Numpy array key
    ind_seg  = 0 # 0 - segment numbers
    ind_mis  = 1 # 1 - mission point
    ind_time = 2 # 2 - time [s]
    ind_alt  = 3 # 3 - altitude [ft]
    ind_ROC  = 4 # 4 - climb rate [m/s]
    ind_rho  = 5 # 5 - density [kg/m^3]
    ind_vel  = 6 # 6 - velocity [kts]
    ind_mach = 7 # 7 - mach number
    ind_temp = 8 # 8 - temperature [K]
    ind_dT   = 9 # 9 - temperature deivation from ISA [K]
    ind_mass = 10 # 10 - vehicle mass [kg]
    ind_dmdt = 11 # 11 - mass loss rate
    ind_type = 12 # 12 - segment type for ESF calcuation, see funcf for details
    climb_ISA_base    = np.load('bada3_' + base_filename + '_climbISA.npy')
    climb_nonISA_base = np.load('bada3_' + base_filename + '_climbNonISA.npy')
    descent_base      = np.load('bada3_' + base_filename + '_descent.npy')
    cruise_base       = np.load('bada3_' + base_filename + '_cruise.npy')
    all_segs_base = np.array([])
    all_segs_base = np.append(all_segs_base,climb_ISA_base)
    all_segs_base = np.append(all_segs_base,climb_nonISA_base)
    all_segs_base = np.append(all_segs_base,descent_base)
    all_segs_base = np.append(all_segs_base,cruise_base)    
    rows = len(climb_ISA_base[:,0])+len(climb_nonISA_base[:,0])+len(descent_base[:,0])+len(cruise_base[:,0])
    cols = len(climb_ISA_base[0,:])
    all_segs_base = all_segs_base.reshape(rows,cols)    
    engine_type  = 'jet'

    segments_base = [climb_ISA_base, climb_nonISA_base, descent_base, cruise_base, all_segs_base]
    climb_ISA    = Data()
    climb_nonISA = Data()
    descent      = Data()
    cruise       = Data()
    all_segs     = Data()
    segments = [climb_ISA, climb_nonISA, descent, cruise, all_segs]
    
    for ii, segb in enumerate(segments_base):
        segments[ii].seg  = segb[:,ind_seg ]
        segments[ii].mis  = segb[:,ind_mis ]
        segments[ii].time = segb[:,ind_time]
        segments[ii].alt  = segb[:,ind_alt ]
        segments[ii].ROC  = segb[:,ind_ROC ]
        segments[ii].rho  = segb[:,ind_rho ]
        segments[ii].vel  = segb[:,ind_vel ]
        segments[ii].mach = segb[:,ind_mach]
        segments[ii].temp = segb[:,ind_temp]
        segments[ii].dT   = segb[:,ind_dT  ]
        segments[ii].mass = segb[:,ind_mass]
        segments[ii].dmdt = segb[:,ind_dmdt]
        segments[ii].type = segb[:,ind_type]
    
    tol_flag = False
    flag1 = False
    count = 0 
    #tropo_alt = 36089 # 11000 m (BADA altitude is in feet) # this variable is not used
    
    k1 = (1852./3600.)**2 # [(m/s)^2/kt^2]
    k2 = 1./(60.*10.**3)  # [kN*min/(N*s)]
    k3 = 1./60.           # [min/s]    
    k4 = 1852./.3048/60.  # [fpm/kt]
    g = 9.80665    
    coeff = Data()
    
    while not(tol_flag):        
        
        if count == 4:
            plt.close('all')
        
        #if count != 0:
            #coeff_old = coeff*1.
            #m1_old    = m1*1.
            #m2_old    = m2*1.
            #m3_old    = m3*1.
            #m4_old    = m4*1.        

        # ISA Climb Trajectory Fitting ---------------------------------------------------------
                        
        (t0,t1,t2,t3,t4,d0,d2,d16,m1,coeff) = ISA_climb_fitting(climb_ISA, climb_segs, engine_type, coeff, count)
        
        # Descent trajectory fitting ---------------------------------------------------------                
        
        (t7,t7_hi,t7_lo,h_des,m3,coeff) = Descent_fitting(descent, descent_segs, engine_type, coeff, count)         
        
        # Non-ISA trajectory fitting ---------------------------------------------------------
        
        (t5,t6,m2,coeff) = Climb_nonISA_fitting(climb_nonISA, nonISA_segs, engine_type, coeff, count) # cruise?
        
        #plt.show()  
        
        ## Fuel Fitting, known dmdt
        
        # Climb fuel fitting
        
        (f2,f3,f4,coeff) = Climb_fuel_fitting(climb_ISA, climb_segs, engine_type, coeff, count, cruise)
            
        # Cruise fitting
        
        (f5,m4,coeff) = Cruise_fuel_fitting(cruise, cruise_segs, engine_type, coeff, count)
        
        # Descent fitting
        
        (f0,f1,coeff) = Descent_fuel_fitting(descent, descent_segs, engine_type, coeff, count)
        
        # for loop with all this code and including ISA climb fitting using known coefficients
        # determine mass change from equation on page 17 (3.1-44)
        
        coeff_ar = np.array([t0,t1,t2,t3,t4,t5,t6,t7_lo,t7_hi,d0,d2,d16,f0,f1,f2,f3,f4,f5,h_des])
        coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.t5,coeff.t6,coeff.t7_lo,coeff.t7_hi,coeff.d0,coeff.d2,coeff.d16,coeff.f0,coeff.f1,coeff.f2,coeff.f3,coeff.f4,coeff.f5,coeff.h_des = t0,t1,t2,t3,t4,t5,t6,t7_lo,t7_hi,d0,d2,d16,f0,f1,f2,f3,f4,f5,h_des
        ms = (m1,m2,m3,m4)
        #ms_old = (m1_old,m2_old,m3_old,m4_old)
        (RMS_dmdt,RMS_ROC) = RMS_calc(coeff_ar,all_segs,ms,ind_seg,ind_mis,ind_time,ind_alt,ind_ROC,ind_rho,ind_vel,ind_mach,ind_temp,ind_dT,ind_mass,ind_dmdt,ind_type,h_des)
        if count != 0:
            print RMS_dmdt-RMS_dmdt_old
            print RMS_ROC-RMS_ROC_old
            if (abs(RMS_dmdt-RMS_dmdt_old) < 1e-5) and (abs(RMS_ROC-RMS_ROC_old) < 1e-1):
                if flag1 == False:
                    flag1 = True
                else:
                    tol_flag = True
        (RMS_dmdt_old,RMS_ROC_old) = (RMS_dmdt*1.,RMS_ROC*1.) 
        count += 1
        print count
    # Now convert final values to parameters needed by AEDT
    # Assumes this is a jet aircraft
    
    #aircraft_type = 1 # 1 means jet
    

    
    if engine_type == 'jet':
        C_Tc1 = t0
        C_Tc2 = t0/t1
        C_Tc3 = t4/t0
        C_f1  = f2/k2
        C_f2  = f2/f3
        C_f3  = f0/k3
        C_f4  = f0/f1
        C_fcr = f5
    C_Tc4 = (t6-1.)/t5
    C_Tc5 = t5
    C_Tdl = t7_lo
    C_Tdh = t7_hi
    C_APP = t7_hi*2 # estimations based on other data, to be updated with SUAVE capability
    C_LD  = t7_hi*3
    #C_TCR = 1. # t7 = 1 at max thrust
    S = 125. # wing area of a 737
    C_D0 = d0*2./k1/S
    C_D2 = d2/2./(g**2)*k1*S
    
    print coeff
    print 'C_Tc1','C_Tc2','C_Tc3','C_Tc4','C_Tc5','C_Tdl','C_Tdh','C_APP','C_LD'
    print C_Tc1,C_Tc2,C_Tc3,C_Tc4,C_Tc5,C_Tdl,C_Tdh,C_APP,C_LD
    print 'C_f1','C_f2','C_f3','C_f4','C_fcr'
    print C_f1,C_f2,C_f3,C_f4,C_fcr
    print 'C_D0','C_D2'
    print C_D0,C_D2
    badaThrustArray = map(str,[C_Tc1,C_Tc2,C_Tc3,C_Tc4,C_Tc5,C_Tdl,C_Tdh,C_APP,C_LD])
    badaFuelArray   = map(str,[C_f1,C_f2,C_f3,C_f4,C_fcr])
    badaDragArray   = map(str,['CR','Clean',150.0,C_D0,C_D2])
    return (badaThrustArray,badaFuelArray,badaDragArray,coeff)

def RMS_calc(coeff,all_segs,ms,ind_seg,ind_mis,ind_time,ind_alt,ind_ROC,ind_rho,ind_vel,ind_mach,ind_temp,ind_dT,ind_mass,ind_dmdt,ind_type,h_des):
    ROC = all_segs.ROC


    k4 = 1852./.3048/60.
    g = 9.80665
    h = all_segs.alt
    TAS = all_segs.vel
    dmdt = all_segs.dmdt
    M = all_segs.mach
    T = all_segs.temp
    dT = all_segs.dT
    rho = all_segs.rho
    segType = all_segs.type
    ESF = funcf(h,M,T,dT,segType)
    gamma = np.arcsin(ROC/(k4*TAS))
    
    (t0,t1,t2,t3,t4,t5,t6,t7_lo,t7_hi,d0,d2,d16,f0,f1,f2,f3,f4,f5,h_des) = coeff
    (m1,m2,m3,m4) = ms
    m = np.array([])
    m = np.append(m,m1)
    m = np.append(m,m2)
    m = np.append(m,m3)
    m = np.append(m,m4)
    K = k4*TAS/m/g*ESF
    t7 = np.zeros(len(h))
    t7[h>=h_des] = t7_hi
    t7[h<h_des]  = t7_lo
    Thr = t7*(t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2)*(t6 - t5*dT)
    dmdt_apx = f5*(f0-f1*h+(f2+f3*TAS-f4*TAS**2)*Thr)
    D = (d0*rho*TAS**2 + d2*m**2/(rho*TAS**2*np.cos(gamma)**2))*(1+d16*M**16)
    RMS_ROC = np.sum((ROC - K*(Thr-D))**2)/np.sqrt(len(h))
    RMS_dmdt = np.sum((dmdt-dmdt_apx)**2)/np.sqrt(len(h))
    
    return (RMS_dmdt,RMS_ROC)

def RMS_thrust_jet(t,tc,ROC):
    scale = np.array([1e5,1e1,1e-5,1e-1,1e-1])
    (t0,t1,t4,d0,d2) = t*scale
    (t0c,t1c,t4c,d0c,d2c) = (tc[:,0],tc[:,1],tc[:,2],tc[:,3],tc[:,4])
    ROC_est = t0*t0c + t1*t1c + t4*t4c + d0*d0c + d2*d2c
    
    return np.sum((ROC-ROC_est)**2)*1e-6

def RMS_thrust_turbprop(t,tc,ROC):
    scale = np.array([1e5,1e1,1e-5,1e-1,1e-1]) # tbd
    (t0,t2,t3,d0,d2) = t*scale
    (t0c,t2c,t3c,d0c,d2c) = (tc[:,0],tc[:,1],tc[:,2],tc[:,3],tc[:,4])
    ROC_est = t0*t0c + t2*t2c + t3*t3c + d0*d0c + d2*d2c
    
    return np.sum((ROC-ROC_est)**2)*1e-6

def RMS_thrust_piston(t,tc,ROC):
    scale = np.array([1e5,1e1,1e-5,1e-1,1e-1]) # tbd
    (t0,t1,t2,d0,d2) = t*scale
    (t0c,t1c,t2c,d0c,d2c) = (tc[:,0],tc[:,1],tc[:,2],tc[:,3],tc[:,4])
    ROC_est = t0*t0c + t1*t1c + t2*t2c + d0*d0c + d2*d2c
    
    return np.sum((ROC-ROC_est)**2)*1e-6

def RMS_thrust_nonISA(t,tc,z):
    scale = np.array([1e-3,1e1])
    (t5,t6) = t*scale
    (t5c,t6c) = (tc[:,0],tc[:,1])
    z_est = t5*t5c + t6*t6c
    
    return np.sum((z-z_est)**2)*1e-4

def RMS_jet_climb_fuel(f,fc,z):
    scale = np.array([1e-6,1e-8])
    (f2,f3) = f*scale
    (f2c,f3c) = (fc[:,0],fc[:,1])
    z_est = f2*f2c + f3*f3c
    
    return np.sum((z-z_est)**2)*1e1

def RMS_turboprop_climb_fuel(f,fc,z):
    scale = np.array([1e-6,1e-8]) # tbd
    (f3,f4) = f*scale
    (f3c,f4c) = (fc[:,0],fc[:,1])
    z_est = f3*f3c + f4*f4c
    
    return np.sum((z-z_est)**2)*1e1

def RMS_cruise_fuel(f,fc,z):
    scale = np.array([1e0])
    f5 = f*scale
    f5c = fc[:,0]
    z_est = f5*f5c
    
    return np.sum((z-z_est)**2)*1e2

def RMS_jet_descent_fuel(f,fc,z):
    scale = np.array([1e-1,1e-6])
    (f0,f1) = f*scale
    (f0c,f1c) = (fc[:,0],fc[:,1])
    z_est = f0*f0c + f1*f1c
    
    return np.sum((z-z_est)**2)*1e4

def RMS_piston_descent_fuel(f,fc,z):
    scale = np.array([1e-1]) # tbd
    f0 = f*scale
    f0c = fc[:,0]
    z_est = f0*f0c
    
    return np.sum((z-z_est)**2)*1e4

def ISA_climb_fitting(climb_ISA, climb_segs, engine_type, coeff, count):
    
    h = climb_ISA.alt
    TAS = climb_ISA.vel
    
    if count == 0:
        m = climb_ISA.mass
    else:
        t0,t1,t2,t3,t4,f2,f3,f4 = coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.f2,coeff.f3,coeff.f4
        time = climb_ISA.time
        Thr = t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2
        dmdt = (f2+f3*TAS-f4*TAS**2)*Thr
        m = climb_ISA.mass*1.
        m_base = m*1.
        climb_length = len(climb_ISA.seg)/climb_segs
        for ii in range(climb_segs):
            for kk in range(climb_length):
                if kk != 0:
                    m[ii*climb_length+kk] = m[ii*climb_length-1+kk] - dmdt[ii*climb_length+kk]*(time[ii*climb_length+kk]-time[ii*climb_length-1+kk])
        print (f2,f3,f4)
        #print m_base-m
    m1 = m*1.
    ROC = climb_ISA.ROC*1.
    
    
    k4 = 1852./.3048/60. # [fpm/kt]
    g = 9.80665
    rho = climb_ISA.rho
    gamma = np.arcsin(ROC/(k4*TAS))
    M = climb_ISA.mach
    T = climb_ISA.temp
    dT = climb_ISA.dT
    segType = climb_ISA.type
    ESF = funcf(h,M,T,dT,segType)
    K = k4*TAS/m/g*ESF    
    
    t0c = np.ones(len(h))*K
    t1c = -h*K
    t2c = K*1./TAS
    t3c = -K*h/TAS
    t4c = K*h**2
    d0c = -K*rho*TAS**2
    d2c = -K*m**2/(rho*TAS**2*np.cos(gamma)**2)
    
    z = ROC
    cons = ({'type':'ineq','fun':lambda c: c[0]},
            {'type':'ineq','fun':lambda c: c[1]},
            {'type':'ineq','fun':lambda c: c[2]},
            {'type':'ineq','fun':lambda c: c[3]},
            {'type':'ineq','fun':lambda c: c[4]})     
    if engine_type == 'jet':
        H = np.vstack([t0c,t1c,t4c,d0c,d2c]).T
        (t0,t1,t4,d0,d2) = np.linalg.lstsq(H,z,rcond=-1)[0]
        t2 = 0
        t3 = 0
        if any(c < 0 for c in (t0,t1,t4,d0,d2)):
            inv_scale = np.array([1e-5,1e-1,1e5,1e1,1e1])
            res = spo.minimize(RMS_thrust_jet,[t0,t1,t4,d0,d2]*inv_scale,args=(H,ROC),constraints=cons,method='SLSQP',options={'disp':False})
            (t0,t1,t4,d0,d2) = res.x/inv_scale
    elif engine_type == 'turboprop':
        H = np.vstack([t0c,t2c,t3c,d0c,d2c]).T
        (t0,t2,t3,d0,d2) = np.linalg.lstsq(H,z)[0]
        t1 = 0
        t4 = 0
        if any(c < 0 for c in (t0,t2,t3,d0,d2)):
            inv_scale = np.array([1e-5,1e-1,1e5,1e1,1e1]) # to be determined
            res = spo.minimize(RMS_thrust_turboprop,[t0,t2,t3,d0,d2]*inv_scale,args=(H,ROC),constraints=cons,method='SLSQP',options={'disp':False})
            (t0,t2,t3,d0,d2) = res.x/inv_scale            
    elif engine_type == 'piston':
        H = np.vstack([t0c,t1c,t2c,d0c,d2c]).T
        (t0,t1,t2,d0,d2) = np.linalg.lstsq(H,z)[0]
        t3 = 0
        t4 = 0
        if any(c < 0 for c in (t0,t1,t2,d0,d2)):
            inv_scale = np.array([1e-5,1e-1,1e5,1e1,1e1]) # to be determined
            res = spo.minimize(RMS_thrust_piston,[t0,t1,t2,d0,d2]*inv_scale,args=(H,ROC),constraints=cons,method='SLSQP',options={'disp':False})
            (t0,t1,t2,d0,d2) = res.x/inv_scale            
    d16 = 0      
    
    fig = plt.figure("Regression Results")
    
    Thrust = t0 - t1*h + t4*h**2
    Drag   = d0*rho*TAS**2 + d2*m**2/(rho*TAS**2*np.cos(gamma)**2)      
    Drag   = (d0*rho*TAS**2 + d2*m**2/(rho*TAS**2*np.cos(gamma)**2))*(1+d16*M**16)
    
    k1 = (1852./3600.)**2 # [(m/s)^2/kt^2]
    k2 = 1./(60.*10.**3)  # [kN*min/(N*s)]
    k3 = 1./60.           # [min/s]         
    
    axes = fig.add_subplot(1,1,1)
    axes.plot( climb_ISA.time , ROC , 'bo' )
    axes.plot( climb_ISA.time , K*(Thrust-Drag) , 'ro' )
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Rate of Climb (fpm)')
    axes.grid(True)
    axes.legend(['SUAVE / Predicted Data Points','SUAVE Coefficient Fit'])
    
    coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.d0,coeff.d2,coeff.d16 = t0,t1,t2,t3,t4,d0,d2,d16  
    
    return (t0,t1,t2,t3,t4,d0,d2,d16,m1,coeff)

def Descent_fitting(descent, descent_segs, engine_type, coeff, count):
    
    t0,t1,t2,t3,t4,d0,d2,d16 = coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.d0,coeff.d2,coeff.d16
    k4 = 1852./.3048/60. # [fpm/kt]
    g = 9.80665    
    
    h = descent.alt
    TAS = descent.vel
    ROC = descent.ROC
    if count == 0:
        m = descent.mass
    else:
        t7_hi = coeff.t7_hi
        t7_lo = coeff.t7_lo
        f0    = coeff.f0
        f1    = coeff.f1
        h_des = coeff.h_des
        time = descent.time
        t7 = np.zeros(len(h))
        t7[h>=h_des] = t7_hi
        t7[h<h_des]  = t7_lo            
        T = t7*(t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2)
        dmdt = 1.*(f0-f1*h+(0.+0.*TAS-0.*TAS**2)*T) 
        m = descent.mass*1.
        descent_length = len(descent.seg)/descent_segs
        for ii in range(descent_segs):
            for kk in range(descent_length):
                if kk != 0:
                    m[ii*descent_length+kk] = m[ii*descent_length-1+kk] - dmdt[ii*descent_length+kk]*(time[ii*descent_length+kk]-time[ii*descent_length-1+kk])
    m3 = m*1.
    h = descent.alt
    TAS = descent.vel
    M = descent.mach
    T = descent.temp
    dT = descent.dT
    rho = descent.rho
    segType = descent.type
    ESF = funcf(h,M,T,dT,segType)
    K = k4*TAS/m/g*ESF 
    gamma = np.arcsin(ROC/(k4*TAS))
    Q = t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2
    
    t7c = K*Q
    d0c = -K*rho*TAS**2
    d2c = -K*m**2/(rho*TAS**2*np.cos(gamma)**2)
    H = np.vstack([t7c]).T
    z = ROC - (d0c*d0 + d2c*d2)*(1.+d16*M**16.)
    
    # Break descent block into segments
    # First determine the number of segments in descent
    segment_size = 16 # this is the number of segment in a single descent and the number of numerical points
    total_segs = len(z)/segment_size
    if len(z)%segment_size != 0:
        raise(ValueError) # segment size does not match length
    Hlist = [None]*total_segs
    zlist = [None]*total_segs
    for kk in range(total_segs):
        Hlist[kk] = H[kk*segment_size:kk*segment_size+segment_size-1,:]
        zlist[kk] = z[kk*segment_size:kk*segment_size+segment_size-1]
    # need to check if typical values are unimodal
    # consider fibonacci search pattern
    resid_list = np.ones(len(h)-3)*10000.
    residual_min   = 10000000000000000.
    iterlist = range(segment_size-3)
    iterlist = [x+2 for x in iterlist]
    for jj in iterlist:
        H1 = np.array([])
        H2 = np.array([])
        z1 = np.array([])
        z2 = np.array([])
        for kk in range(total_segs):
            H1 = np.append(H1,Hlist[kk][0:jj,:])
            H2 = np.append(H2,Hlist[kk][jj:segment_size,:])
            z1 = np.append(z1,zlist[kk][0:jj])
            z2 = np.append(z2,zlist[kk][jj:segment_size])
        H1 = H1.reshape(len(H1),1) # this is the number of variables in the H matrix
        H2 = H2.reshape(len(H2),1)
        res1 = np.linalg.lstsq(H1,z1)
        res2 = np.linalg.lstsq(H2,z2)
        t7_1 = res1[0][0]
        t7_2 = res2[0][0]      
        residual = res1[1][0] + res2[1][0]
        #print residual
        if (residual < residual_min) and ((t7_1 >= 0 and t7_2 >= 0) and (t7_1 <= 1 and t7_2 <= 1)):
            residual_min = residual*1.
            min_ind = jj
            t7_hi = t7_1*1.
            t7_lo = t7_2*1.
            h_des = (h[min_ind]+h[min_ind+1])/2.
    t7 = np.array([])
    for kk in range(total_segs):
        t7 = np.append(t7,t7_hi*np.ones(min_ind))
        t7 = np.append(t7,t7_lo*np.ones(segment_size-min_ind))
        
        
    fig = plt.figure("Descent Regression")
        
    Thrust = t7*(t0 - t1*h + t4*h**2) # Fix here
    Drag   = d0*rho*TAS**2 + d2*m**2/(rho*TAS**2*np.cos(gamma)**2)        
        
    axes = fig.add_subplot(1,1,1)
    axes.plot( descent.time , ROC , 'bo' )
    axes.plot( descent.time , K*(Thrust-Drag) , 'ro' )
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Rate of Climb (fpm)')
    axes.grid(True)
    axes.legend(['SUAVE / Predicted Data Points','SUAVE Coefficient Fit'])   
    
    coeff.t7,coeff.t7_hi,coeff.t7_lo,coeff.h_des = t7,t7_hi,t7_lo,h_des
    return (t7,t7_hi,t7_lo,h_des,m3,coeff)

def Climb_nonISA_fitting(climb_nonISA, nonISA_segs, engine_type, coeff, count):
    
    k4 = 1852./.3048/60. # [fpm/kt]
    g = 9.80665       
    
    t0,t1,t2,t3,t4,d0,d2,d16 = coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.d0,coeff.d2,coeff.d16   
    
    h = climb_nonISA.alt
    TAS = climb_nonISA.vel
    rho = climb_nonISA.rho
    ROC = climb_nonISA.ROC
    if count == 0:
        m = climb_nonISA.mass
    else:
        t5,t6,f2,f3,f4 = coeff.t5,coeff.t6,coeff.f2,coeff.f3,coeff.f4
        time = climb_nonISA.time
        dT = climb_nonISA.dT
        T = (t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2)*(t6-t5*dT)
        dmdt = (f2+f3*TAS-f4*TAS**2)*T
        m = climb_nonISA.mass*1.
        climb_length = len(climb_nonISA.seg)/nonISA_segs
        for ii in range(nonISA_segs):
            for kk in range(climb_length):
                if kk != 0:
                    m[ii*climb_length+kk] = m[ii*climb_length-1+kk] - dmdt[ii*climb_length+kk]*(time[ii*climb_length+kk]-time[ii*climb_length-1+kk])
    m2 = m*1.
    gamma = np.arcsin(ROC/(k4*TAS))
    
    k4 = 1852./.3048/60.
    g = 9.80665
    M = climb_nonISA.mach
    T = climb_nonISA.temp
    dT = climb_nonISA.dT
    segType = climb_nonISA.type
    ESF = funcf(h,M,T,dT,segType)
    K = k4*TAS/m/g*ESF         
    
    # t7 = 1 for max climb
    #t7 = np.zeros(len(h))
    #t7[h>=h_des] = t7_hi
    #t7[h<h_des]  = t7_lo
    Q = 1.*(t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2)
    t5c = -K*Q*dT
    t6c = K*Q
    d0c = -K*rho*TAS**2
    d2c = -K*m**2/(rho*TAS**2*np.cos(gamma))
    H = np.vstack([t5c,t6c]).T
    z = ROC - (d0c*d0 + d2c*d2)*(1.+d16*M**16.)
    (t5,t6) = np.linalg.lstsq(H,z)[0]
    dTs = np.array(list(set(dT)))
    if any(c < 0 for c in np.hstack([1-t6-t5*dTs,.4-1+t6+t5*dTs])) or (t5 < 0) or (np.abs((c[1]-1.)/c[0]) > 100.):
        inv_scale = np.array([1e3,1e-1])
        t5i = inv_scale[0]
        t6i = inv_scale[1]
        cons = ({'type':'ineq','fun':lambda c: c[0]},
                {'type':'ineq','fun':lambda c: np.array([-np.abs((c[1]/t6i-1.)/(c[0]/t5i)) + 100.])})
        for temp in dTs:
            cons = cons + ({'type':'ineq','fun':lambda c: 1 - c[1]/t6i - c[0]/t5i*temp},{'type':'ineq','fun':lambda c: .4 - 1 + c[1]/t6i + c[0]/t5i*temp})
        res = spo.minimize(RMS_thrust_nonISA,[t5,t6]*inv_scale,args=(H,z),constraints=cons,method='SLSQP',options={'disp':False})
        (t5,t6) = res.x/inv_scale 
        #pass
    
    fig = plt.figure("nonISA Climb Regression")        
    
    Thrust = 1.*(t0 - t1*h + t4*h**2)*(t6-t5*dT)
    Drag   = d0*rho*TAS**2 + d2*m**2/(rho*TAS**2*np.cos(gamma)**2)        
        
    axes = fig.add_subplot(1,1,1)
    axes.plot( climb_nonISA.time , ROC , 'bo' )
    axes.plot( climb_nonISA.time , K*(Thrust-Drag) , 'ro' )
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Rate of Climb (fpm)')
    axes.grid(True)
    axes.legend(['SUAVE / Predicted Data Points','SUAVE Coefficient Fit'])
    
    coeff.t5, coeff.t6 = t5,t6
    return (t5,t6,m2,coeff)

def Climb_fuel_fitting(climb_ISA, climb_segs, engine_type, coeff, count, cruise):
    
    t0,t1,t2,t3,t4,d0,d2,d16 = coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.d0,coeff.d2,coeff.d16     
    
    h = climb_ISA.alt
    TAS = climb_ISA.vel
    if count == 0:
        dmdt = climb_ISA.dmdt
        m = cruise.mass*1.
    
    #f0 = 0
    #f1 = 0
    #f5 = 1
    T = t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2
    if count != 0:
        f2 = coeff.f2
        f3 = coeff.f3
        f4 = coeff.f4
        dmdt = 1.*(0.-0.*h+(f2+f3*TAS-f4*TAS**2)*T)  
    f2c = T*1.
    f3c = TAS*T
    f4c = -TAS**2*T
    
    z = dmdt
    cons = ({'type':'ineq','fun':lambda c: c[0]},
            {'type':'ineq','fun':lambda c: c[1]})        
    if engine_type == 'jet':
        H = np.vstack([f2c,f3c]).T
        (f2,f3) = np.linalg.lstsq(H,z)[0]
        if any(c < 1 for c in (f2,f3)):
            inv_scale = np.array([1e6,1e8])
            res = spo.minimize(RMS_jet_climb_fuel,[f2,f3]*inv_scale,args=(H,z),constraints=cons,method='SLSQP',options={'disp':False})
            (f2,f3) = res.x/inv_scale                
        f4 = 0
    elif engine_type == 'turboprop':
        H = np.vstack([f3c,f4c]).T
        (f3,f4) = np.linalg.lstsq(H,z)[0]
        f2 = 0
        if any(c < 1 for c in (f3,f4)):
            inv_scale = np.array([1e6,1e8]) # tbd
            res = spo.minimize(RMS_turboprop_climb_fuel,[f3,f4]*inv_scale,args=(H,z),constraints=cons,method='SLSQP',options={'disp':False})
            (f3,f4) = res.x/inv_scale                           
    elif engine_type == 'piston':
        f2 = 0
        f3 = 0
        f4 = 0
        
    fig = plt.figure("Fuel Fitting Climb")
        
    dmdt_new = 1.*(0.-0.*h+(f2+f3*TAS-f4*TAS**2)*T)    
        
        
    axes = fig.add_subplot(1,1,1)
    axes.plot( climb_ISA.time , dmdt , 'bo' )
    axes.plot( climb_ISA.time , dmdt_new , 'ro' )
    #axes.plot( climb_ISA.time , dmdt_ex , 'go' )
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Fuel Consumption (kg/s)')
    axes.grid(True)
    axes.legend(['SUAVE / Predicted Data Points','SUAVE Coefficient Fit'])  
    
    coeff.f2,coeff.f3,coeff.f4 = f2,f3,f4
    return (f2,f3,f4,coeff)

def Cruise_fuel_fitting(cruise, climb_segs, engine_type, coeff, count): # climb segments?
    
    t0,t1,t2,t3,t4,d0,d2,d16 = coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.d0,coeff.d2,coeff.d16 
    f2 = coeff.f2
    f3 = coeff.f3
    f4 = coeff.f4    
    
    h = cruise.alt
    TAS = cruise.vel
    dmdt = cruise.dmdt          
    T = t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2 
    m = cruise.mass*1. # will be changed if count != 0
    if count != 0:
        f5 = coeff.f5
        dmdt = f5*(0.-0.*h+(f2+f3*TAS-f4*TAS**2)*T)  
         # this is used for RMS tolerance calculations
        cruise_length = len(cruise.seg)/climb_segs
        time = cruise.time
        for ii in range(climb_segs):
            for kk in range(cruise_length):
                if kk != 0:
                    m[ii*cruise_length+kk] = m[ii*cruise_length-1+kk] - dmdt[ii*cruise_length+kk]*(time[ii*cruise_length+kk]-time[ii*cruise_length-1+kk]) 
    m4 = m*1.
    f5c = (f2+f3*TAS-f4*TAS**2)*T
    H = f5c.reshape(len(f5c),1)
    z = dmdt
    f5 = np.linalg.lstsq(H,z)[0][0]
    if (f5 < 1):
        cons = ({'type':'ineq','fun':lambda c: c[0]})
        inv_scale = np.array([1e0])
        res = spo.minimize(RMS_cruise_fuel,[f5]*inv_scale,args=(H,z),constraints=cons,method='SLSQP',options={'disp':False})
        (f5) = res.x[0]/inv_scale[0]         
    
    fig = plt.figure("Fuel Fitting Cruise")
        
    dmdt_new = f5*(0.-0.*h+(f2+f3*TAS-f4*TAS**2)*T)     
        
    axes = fig.add_subplot(1,1,1)
    axes.plot( cruise.time , dmdt , 'bo' )
    axes.plot( cruise.time , dmdt_new , 'ro' )
    if np.round(dmdt[0]*1000.) != np.round(dmdt_new[0]*1000.):
        pass
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Fuel Consumption (kg/s)')
    axes.grid(True)
    axes.legend(['SUAVE / Predicted Data Points','SUAVE Coefficient Fit'])  
    
    coeff.f5 = f5
    return (f5,m4,coeff)

def Descent_fuel_fitting(descent, descent_segs, engine_type, coeff, count):
    
    t0,t1,t2,t3,t4,d0,d2,d16 = coeff.t0,coeff.t1,coeff.t2,coeff.t3,coeff.t4,coeff.d0,coeff.d2,coeff.d16 
    t7,t7_hi,t7_lo,h_des = coeff.t7,coeff.t7_hi,coeff.t7_lo,coeff.h_des
    
    h = descent.alt
    TAS = descent.vel
    dmdt = descent.dmdt
    t7 = np.zeros(len(h))
    t7[h>=h_des] = t7_hi
    t7[h<h_des]  = t7_lo        
    T = t7*(t0 - t1*h + t2*1./TAS - t3*h/TAS + t4*h**2) 
    if count != 0:
        f0 = coeff.f0
        f1 = coeff.f1
        dmdt = 1.*(f0-f1*h+(0.+0.*TAS-0.*TAS**2)*T)         
    f0c = np.ones(len(h))
    f1c = -h
    H = np.vstack([f0c,f1c]).T
    z = dmdt        
    if (engine_type == 'jet') or (engine_type == 'turboprop'):
        H = np.vstack([f0c,f1c]).T
        (f0,f1) = np.linalg.lstsq(H,z)[0] 
        if any(c < 1 for c in (f0,f1)):
            cons = ({'type':'ineq','fun':lambda c: c[0]},
                    {'type':'ineq','fun':lambda c: c[1]})                 
            inv_scale = np.array([1e1,1e6])
            res = spo.minimize(RMS_jet_descent_fuel,[f0,f1]*inv_scale,args=(H,z),constraints=cons,method='SLSQP',options={'disp':False})
            (f0,f1) = res.x/inv_scale              
    elif engine_type == 'piston':
        np.vstack([f0c]).T
        f0 = np.linalg.lstsq(H,z)[0]  
        f1 = 0
        if (f0 < 0):
            cons = ({'type':'ineq','fun':lambda c: c[0]})             
            inv_scale = np.array([1e1]) # tbd
            res = spo.minimize(RMS_piston_descent_fuel,[f0]*inv_scale,args=(H,z),constraints=cons,method='SLSQP',options={'disp':False})
            (f0) = res.x[0]/inv_scale[0]                  
          
    fig = plt.figure("Fuel Fitting Descent")
        
    dmdt_new = 1.*(f0-f1*h+(0.+0.*TAS-0.*TAS**2)*T)    
        
    axes = fig.add_subplot(1,1,1)
    axes.plot( descent.time , dmdt , 'bo' )
    axes.plot( descent.time , dmdt_new , 'ro' )
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Fuel Consumption (kg/s)')
    axes.grid(True)
    axes.legend(['SUAVE / Predicted Data Points','SUAVE Coefficient Fit'])    

    coeff.f0, coeff.f1 = f0,f1    
    return (f0,f1,coeff)

if __name__ == '__main__':

    base_filename = '737800_profile_test'

    main(base_filename)    
    
    plt.show()