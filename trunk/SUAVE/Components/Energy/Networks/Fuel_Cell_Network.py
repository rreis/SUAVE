# fuel_cell_network.py
# 
# Created:  Tim MacDonald, Feb 2015
# Modified:  
# Adapted from solar_enery_network_5.py

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE

# package imports
import numpy as np
import scipy as sp
import datetime
import time
from SUAVE.Core import Units

# python imports
import os, sys, shutil
from copy import deepcopy
from copy import copy
from warnings import warn


from SUAVE.Core import Data, Data_Exception, Data_Warning
from SUAVE.Components import Component, Physical_Component, Lofted_Body
from SUAVE.Components import Component_Exception
from SUAVE.Components.Propulsors.Propulsor import Propulsor

# ----------------------------------------------------------------------
#   Fuel Cell Network
# ----------------------------------------------------------------------


class Fuel_Cell_Network(Propulsor):
    def __defaults__(self):
        
        self.propellant  = None
        self.fuel_cell   = None
        self.motor       = None
        self.propulsor   = None
        self.payload     = None
        self.nacelle_dia = 0.0
        self.tag         = 'Network'        
        
    _component_root_map = None
    
    def evaluate(self,conditions,numerics):
    
        # unpack
        propellant  = self.propellant
        fuel_cell   = self.fuel_cell
        motor       = self.motor
        propulsor   = self.propulsor
        
        # step 1

        # step 2
        #if abs(fuel_cell.outputs.power[-1]) < 5*10**7:
            #a = 0  
        # ------- Defaults included here to get an initial run going #---- Fuel Cell Class
        fuel_cell.efficiency = 0.8
        fuel_cell.spec_energy = propellant.specific_energy
        fuel_cell.max_mdot = 2.0            
        eta = copy(conditions.propulsion.throttle)
        if np.any(abs(eta)>100):
            print 'Warning: Fuel Cell throttle values outside +-100 have not been tested'
        fuel_cell.power = fuel_cell.spec_energy*eta*fuel_cell.max_mdot*fuel_cell.efficiency
        if abs(eta[-1]-1.0) > 0.01:
            a = 0
        if abs(fuel_cell.power[-1]) < 5*10**7:
            a = 0                 
        fuel_cell.mdot = eta*fuel_cell.max_mdot
        #------- Fuel Cell Class
        
        
        if abs(fuel_cell.power[-1]) < 5*10**7:
            a = 0        
        fuel_cell.power_generated = copy(fuel_cell.power)
            
        # Motor Begin
        motor.efficiency = 0.95
        motor.power = fuel_cell.power*motor.efficiency
        # Motor End
        
        mdot = fuel_cell.mdot

        # link
        propulsor.power =  motor.power
        #print(motor.outputs.omega)
        # step 6
        F, mdotP, P, e = self.evaluate_prop(conditions)
        # Package for solver
        mdot = mdot[:,0]
        self.propulsive_efficiency = e
        
        length = len(F)
        F=F.reshape(length,1)
        mdot=mdot.reshape(length,1)
        P=P.reshape(length,1)
        
        # Determine drag required by the air intake
        f_density  = conditions.freestream.density
        f_velocity = conditions.freestream.velocity
        oxy_intake = mdot*8.0
        air_kg  = oxy_intake/0.23 # Percent oxygen in air by mass
        air_vol = air_kg/f_density
        air_A   = air_vol/f_velocity
        added_drag = air_kg*f_velocity
        #added_drag=added_drag[0]
        
        base_drag_force = conditions.frames.wind.drag_force_vector
        base_drag_force[:,0] = base_drag_force[:,0] - added_drag[:,0]
        
        
        ref_area = conditions.aerodynamics.drag_breakdown.parasite.main_wing.reference_area
        intake_cd = added_drag/(0.5*f_density*f_velocity**2*ref_area)
        
        cell_drag = conditions.aerodynamics.drag_breakdown.parasite.turbo_fan.parasite_drag_coefficient
        cell_drag = cell_drag + intake_cd
        conditions.aerodynamics.drag_breakdown.parasite.turbo_fan.intake_cd = intake_cd
        
        
        return F, mdot, P
            
    __call__ = evaluate        
                 
        
    def evaluate_prop(self,conditions):
        def fM(M):
            fm = ((gamma+1)/2)**((gamma+1)/2/(gamma-1))*(M/(1+(gamma-1)/2*M**2)**((gamma+1)/2/(gamma-1)))
            return fm
        
        def PtP(M):
            Pt = (1 + (gamma-1)/2*M**2)**(gamma/(gamma-1))
            return Pt
        
        def TtT(M):
            Tt = (1 + (gamma-1)/2*M**2)
            return Tt         
        M0 = conditions.freestream.mach_number
        U0 = conditions.freestream.velocity
        a0 = U0/M0
        P0 = conditions.freestream.pressure
        T0 = conditions.freestream.temperature
        rho0 = conditions.freestream.density
        mdot = U0*rho0*self.propulsor.A0
        power = self.propulsor.power
        # More code here
        gamma = 1.4
        R = 286.9
        Cp = 1005.0
        Pt0 = P0*PtP(M0)
        Tt0 = T0*TtT(M0)
        a0 = np.sqrt(gamma*R*T0)
        U0 = a0*M0
        mdot = gamma/((gamma+1)/2)**((gamma+1)/2/(gamma-1))*(Pt0*self.propulsor.A0/np.sqrt(gamma*R*Tt0))*fM(M0)
        
        M2 = 0.2                                # --------- These values don't matter for a simple model
        A2 = self.propulsor.A0*fM(M0)/fM(M2)
        Tt2 = Tt0
        Pt2 = Pt0
        
        P = power # this is power, not pressure
        p = P/mdot
        dTt = p/Cp
        neg_flag = np.zeros_like(dTt)
        neg_flag[dTt < 0] = 1
        dTt[dTt < 0.0] = -dTt[dTt < 0.0]
        Tt3 = Tt2 + dTt
        Pt3 = Pt2*(Tt3/Tt2)**(gamma/(gamma-1))
        M3 = 0.5                                # ---------
        A3 = A2*fM(M2)/fM(M3)*Pt2/Pt3*np.sqrt(Tt3/Tt2)
        
        Pe = P0
        Pte = Pt3
        Tte = Tt3
        
        #print Tt3/Tt2
    
        Me = np.sqrt(2.0*Pte*(Pte/Pe)**(-1/gamma)-2.0*Pe)/np.sqrt((gamma-1)*Pe)
        Ae = A3*fM(M3)/fM(Me)
        Te = Tte/TtT(Me)
        ae = np.sqrt(gamma*R*Te)
        Ue = Me*ae
        e = 2*U0/(U0+Ue)
        
        F = gamma*M0**2*(Me/M0*np.sqrt(Te/T0)-1)*P0*self.propulsor.A0
        F[neg_flag == 1] = -F[neg_flag == 1]
        F = F[:,0]
        mdot = mdot[:,0]
        P = np.zeros_like(F)        
        F[np.isnan(F)] = conditions.propulsion.throttle*-1.0*power/2e2
        
        return F, mdot, P, e
              
    
        

