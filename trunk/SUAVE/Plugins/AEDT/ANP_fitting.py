# h_i = altitude [ft]
# TAS_i = true airspeed [kt]
# m_i = aircraft mass [kg]
# ROC_i = rate of climb [fpm]

import csv
import SUAVE
import SUAVE.Analyses.Atmospheric.US_Standard_1976 as atmo
import numpy as np
import pylab as plt
from SUAVE.Core import (
Data, Container, Data_Exception, Data_Warning, Units
)

from scipy.optimize import curve_fit

def main(base_filename):
    sub_seg_len = 32
    climb_seg_len = 3
    climb_segs = 9
    nonISA_segs = 6
    descent_segs = 3
    cruise_segs = 1
    # Numpy array key
    ind_seg  = 0 # 0 - segment numbers
    ind_mis  = 1 # 1 - mission point
    ind_time = 2 # 2 - time [s]
    ind_alt  = 3 # 3 - altitude [m]
    ind_CAS  = 4 # 4 - calibrated/equivalent airspeed [m/s]
    ind_rho  = 5 # 5 - density [kg/m^3]
    ind_vel  = 6 # 6 - velocity [m/s]
    ind_mach = 7 # 7 - mach number
    ind_temp = 8 # 8 - temperature [K]
    ind_dT   = 9 # 9 - temperature deivation from ISA [K]
    ind_lift = 10 # 10 - lift force [N]
    ind_drag = 11 # 11 - drag force [N]
    ind_thr  = 12 # 12 - thrust force [N]
    ind_dmdt = 13 # 13 - mass change rate [kg/s]
    ind_pres = 14 # 14 - pressure [Pa]
    takeoff_accel = np.load('anp_' + base_filename + '_takeoff_accel.npy')
    takeoff_climb = np.load('anp_' + base_filename + '_takeoff_climb.npy')
    climb_accel = np.load('anp_' + base_filename + '_climb_accel.npy')
    climb_climb = np.load('anp_' + base_filename + '_climb_climb.npy')
    term_descent = np.load('anp_' + base_filename + '_term_descent.npy')
    static_thrust = np.load('anp_' + base_filename + '_static_thrust.npy')
    flap_descent = np.load('anp_' + base_filename + '_flap_descent.npy')
    engine_type  = 'jet'
    
    #tol_flag = False
    #flag1 = False
    #count = 0
    #tropo_alt = 36089 # 11000 m (BADA altitude is in feet) # this variable is not used
    
    anpFlapsSet = Data()
    anpFlapsSet.tag = []
    anpFlapsSet.op  = []
    anpFlapsSet.R   = []
    anpFlapsSet.CD  = []
    anpFlapsSet.B   = []  
    
    anpThrustSet = Data()
    anpThrustSet.tag = []
    anpThrustSet.E   = []
    anpThrustSet.F   = []
    anpThrustSet.GA  = []
    anpThrustSet.GB  = []
    anpThrustSet.H   = []
    
    # ###############################
    # Max Takeoff Net Thrust
    # ###############################     
    
    # Combined
    
    max_takeoff = np.vstack([takeoff_accel,takeoff_climb])
    max_takeoff_data = Data()
    max_takeoff_data.thr = (max_takeoff[:,ind_thr]) / Units.lbf / 2 # divide by two for number of engines
    max_takeoff_data.rho = max_takeoff[:,ind_rho] 
    max_takeoff_data.CAS = max_takeoff[:,ind_CAS] / Units.kts
    max_takeoff_data.temp = max_takeoff[:,ind_temp]
    max_takeoff_data.alt  = max_takeoff[:,ind_alt] / Units.ft
    max_takeoff_data.time = max_takeoff[:,ind_time]
    max_takeoff_data.pres = max_takeoff[:,ind_pres]

    E_T,F_T,GA_T = Thrust_fit(max_takeoff_data)        
    
    anpThrustSet.tag.append('T')
    anpThrustSet.E.append(str(E_T))
    anpThrustSet.F.append(str(F_T))
    anpThrustSet.GA.append(str(GA_T))
    anpThrustSet.GB.append('0')
    anpThrustSet.H.append('0')    
    
    # ###############################
    # Max Climb
    # ###############################     
    
    max_climb = np.vstack([climb_accel,climb_climb])
    max_climb_data = Data()
    max_climb_data.thr = (max_climb[:,ind_thr]) / Units.lbf / 2 # divide by two for number of engines
    max_climb_data.rho = max_climb[:,ind_rho] 
    max_climb_data.CAS = max_climb[:,ind_CAS] / Units.kts
    max_climb_data.temp = max_climb[:,ind_temp]
    max_climb_data.alt  = max_climb[:,ind_alt] / Units.ft
    max_climb_data.time = max_climb[:,ind_time]
    max_climb_data.pres = max_climb[:,ind_pres]
    
    E_C,F_C,GA_C = Thrust_fit(max_climb_data)
    
    anpThrustSet.tag.append('C')
    anpThrustSet.E.append(str(E_C))
    anpThrustSet.F.append(str(F_C))
    anpThrustSet.GA.append(str(GA_C))
    anpThrustSet.GB.append('0')
    anpThrustSet.H.append('0')
    
    # ###############################
    # Departure Fuel Flow Rate
    # ###############################    
    
    atmos = SUAVE.Analyses.Atmospheric.US_Standard_1976() 
    ref_data = atmos.compute_values(0)
    ref_temp = ref_data.temperature[:,0]
    ref_rho  = ref_data.density[:,0]
    ref_pres = ref_data.pressure[:,0]
    
    anp_climb = np.vstack([max_climb,max_takeoff])
    
    fuel_flow = anp_climb[:,ind_dmdt] * Units.min / 2.
    M         = anp_climb[:,ind_mach]
    h         = anp_climb[:,ind_alt] / Units.ft
    Fn        = (anp_climb[:,ind_thr]) / 2 / Units.kN
    Fn_lb     = Fn * Units.kN / Units.lbf 
    theta     = anp_climb[:,ind_temp] / ref_temp
    gamma     = anp_climb[:,ind_pres]  / ref_pres #anp_climb[0,ind_rho]
    
    xdata = np.vstack([M,h,Fn,gamma,theta,Fn_lb])
    ydata = fuel_flow
    guesses    = np.array([.58,.76,1e-6,3e-6])
    
    popt_dep, pcov = curve_fit(fn_dep,xdata,ydata,p0=guesses)    
    
    anpThrustSet.K1 = str(popt_dep[0])
    anpThrustSet.K2 = str(popt_dep[1])
    anpThrustSet.K3 = str(popt_dep[2])
    anpThrustSet.K4 = str(popt_dep[3])

    K1 = float(anpThrustSet.K1)
    K2 = float(anpThrustSet.K2)
    K3 = float(anpThrustSet.K3)
    K4 = float(anpThrustSet.K4)
    
    seg_len = len(anp_climb[:,ind_time])/2
    
    SUAVE_est_dmdt = (K1 + K2*M + K3*h + K4*Fn_lb/gamma)*np.sqrt(theta)*Fn / Units.min
    
    fig = plt.figure("Fuel Flow Regression Departure")
    axes = fig.add_subplot(1,1,1)
    axes.plot( anp_climb[0:seg_len,ind_time] , fuel_flow[0:seg_len] / Units.min, 'bo' )
    axes.plot( anp_climb[0:seg_len,ind_time] , SUAVE_est_dmdt[0:seg_len] , 'g-' )
    axes.plot( anp_climb[seg_len:,ind_time] , fuel_flow[seg_len:] / Units.min , 'bo' )
    axes.plot( anp_climb[seg_len:,ind_time] , SUAVE_est_dmdt[seg_len:], 'g-' )    
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Fuel Flow Rate (kg/s)')
    axes.legend(['SUAVE Data Points','SUAVE Coefficient Fit'])
    axes.grid(True)       
    
    # ###############################
    # Approach Fuel Flow Rate
    # ###############################
    
    anp_descent = np.vstack([term_descent,flap_descent])
    
    fuel_flow = anp_descent[:,ind_dmdt] * Units.min / 2.
    M         = anp_descent[:,ind_mach]
    Fn0       = static_thrust # in lbf
    Fn0       = np.ones(np.size(M)) * Fn0
    Fn        = (anp_descent[:,ind_thr]) / 2 / Units.kN
    theta     = anp_descent[:,ind_temp] / ref_temp
    gamma     = anp_descent[:,ind_pres]  / ref_pres
    Fn_lb     = Fn * Units.kN / Units.lbf
    
    xdata = np.vstack([M,Fn0,Fn,gamma,theta,Fn_lb])
    ydata = fuel_flow
    guesses    = np.array([1.35,2.02,18.74,.54])
    
    popt_arr, pcov = curve_fit(fn_arr,xdata,ydata,p0=guesses,maxfev=100000)
    
    anpThrustSet.alpha = str(popt_arr[0])
    anpThrustSet.beta1 = str(popt_arr[1])
    anpThrustSet.beta2 = str(popt_arr[2])
    anpThrustSet.beta3 = str(popt_arr[3])
    
    beta1 = float(anpThrustSet.beta1)
    beta2 = float(anpThrustSet.beta2)
    beta3 = float(anpThrustSet.beta3)
    alpha = float(anpThrustSet.alpha)
    
    beta1_ex = 1.353
    beta2_ex = 2.019
    beta3_ex = 18.74
    alpha_ex = 0.5356
    
    SUAVE_est_dmdt = (alpha + beta1*M + beta2*np.exp(-beta3*Fn_lb/gamma/Fn0))*np.sqrt(theta)*Fn / Units.min

    seg_len = len(term_descent[:,ind_time])
    
    fig = plt.figure("Fuel Flow Regression Approach")
    axes = fig.add_subplot(1,1,1)
    axes.plot( anp_descent[0:seg_len,ind_time] , fuel_flow[0:seg_len] / Units.min , 'bo' )
    axes.plot( anp_descent[0:seg_len,ind_time] , SUAVE_est_dmdt[0:seg_len], 'g-' )
    axes.plot( anp_descent[seg_len:,ind_time]  , fuel_flow[seg_len:] / Units.min , 'bo' )
    axes.plot( anp_descent[seg_len:,ind_time]  , SUAVE_est_dmdt[seg_len:], 'r-' )    
    #axes.plot( anp_descent[:,ind_time] , (alpha_ex + beta1_ex*M + beta2_ex*np.exp(-beta3_ex*Fn_lb/gamma/Fn0))*np.sqrt(theta)*Fn, 'ro' )
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Fuel Flow Rate (kg/s)')
    axes.legend(['SUAVE Data Points','SUAVE Coefficient Fit'])
    axes.grid(True)   
    
    plt.show()  
    
    # ###############################
    # Clean Lift to Drag
    # ############################### 
    
    lift_00 = np.mean(climb_climb[:,ind_lift])
    drag_00 = np.mean(climb_climb[:,ind_drag])
    R_T_00 = 1./(lift_00/drag_00)
    
    lift_05 = np.mean(takeoff_climb[:,ind_lift])
    drag_05 = np.mean(takeoff_climb[:,ind_drag])
    R_T_05 = 1./(lift_05/drag_05)    
    
    anpFlapsSet.tag.append('T_00')
    anpFlapsSet.op.append('D')
    anpFlapsSet.R.append(str(R_T_00))
    anpFlapsSet.CD.append('0')
    anpFlapsSet.B.append('0')
    
    # 01 for testing
    anpFlapsSet.tag.append('T_01')
    anpFlapsSet.op.append('D')
    anpFlapsSet.R.append(str(0.06253))
    anpFlapsSet.CD.append('0')
    anpFlapsSet.B.append('0')    
    
    anpFlapsSet.tag.append('T_05')
    anpFlapsSet.op.append('D')
    anpFlapsSet.R.append(str(R_T_05))
    anpFlapsSet.CD.append('0')
    anpFlapsSet.B.append('0')    
    
    print anpThrustSet
    print anpFlapsSet
    
    return (anpThrustSet,anpFlapsSet)

def Thrust_fit(segment):
    
    thrust  = segment.thr # divide by two for number of engines
    density = segment.rho
    CAS     = segment.CAS
    temp    = segment.temp
    h       = segment.alt
    time    = segment.time
    pressure = segment.pres
    
    z = thrust / (pressure/101325.)
    Ec = np.ones(np.size(thrust))
    Fc = CAS
    GAc = h    
    
    H = np.vstack([Ec,Fc,GAc]).T
    (E,F,GA) = np.linalg.lstsq(H,z)[0]  
    
    fig = plt.figure("Takeoff Thrust Regression")
    axes = fig.add_subplot(1,1,1)
    axes.plot( time , z , 'bo' )
    axes.plot( time , E + F*Fc + GA*GAc , 'g-' )
    axes.set_xlabel('Mission Time (s)')
    axes.set_ylabel('Net Corrected Thrust (lbf)')
    axes.grid(True)    
    
    return E,F,GA
    
def fn_dep(xdata,K1,K2,K3,K4):
    M     = xdata[0,:]
    h     = xdata[1,:]
    Fn    = xdata[2,:]
    gamma = xdata[3,:]
    theta = xdata[4,:]  
    Fn_lb = xdata[5,:]
    return (K1 + K2*M + K3*h + K4*Fn_lb/gamma)*np.sqrt(theta)*Fn
    
def fn_arr(xdata,alpha,beta1,beta2,beta3):
    M     = xdata[0,:]
    Fn0   = xdata[1,:]
    Fn    = xdata[2,:]
    gamma = xdata[3,:]
    theta = xdata[4,:]
    Fn_lb = xdata[5,:]
    return (alpha + beta1*M + beta2*np.exp(-beta3*Fn_lb/gamma/Fn0))*np.sqrt(theta)*Fn
    
    
    
if __name__ == '__main__':

    base_filename = '737800_profile_test'

    main(base_filename)    