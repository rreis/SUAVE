
# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import numpy as np
import scipy as sp
from scipy import integrate
import pylab as plt

from SUAVE.Core import Units

def post_process(vehicle,mission_profile):
    
    plt.show(block=True) # here so as to not block the regression test
    results = mission_profile
    
    # ------------------------------------------------------------------    
    #   Throttle
    # ------------------------------------------------------------------
    fig = plt.figure("Throttle and Fuel Burn")
    tot_energy = 0.0
    #base_time = 0.0
    max_power = (vehicle.mass_properties.operating_empty - 1000 - 22500.0)*1500
    for segment in results.segments.values():
        time = segment.conditions.frames.inertial.time[:,0] / Units.min
        eta  = segment.conditions.propulsion.throttle[:,0]
        e = segment.analyses.propulsion.vehicle.propulsors.turbo_fan.fuel_cell.efficiency
        spec_energy = segment.analyses.propulsion.vehicle.propulsors.turbo_fan.fuel_cell.propellant.specific_energy
        mdot = segment.conditions.propulsion.fuel_mass_rate[:,0]
        power = spec_energy*mdot*e
        velocity   = segment.conditions.freestream.velocity[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]
        
        axes = fig.add_subplot(3,1,1)
        axes.plot( time , power/1000.0 , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Power Output (kW)')
        axes.grid(True)
        
        #axes = fig.add_subplot(3,1,2)
        #axes.plot( time , mdot , 'bo-' )
        #axes.set_xlabel('Time (mins)')
        #axes.set_ylabel('Fuel Burn Rate (kg/s)')
        #axes.grid(True)  
        
        power = velocity*Thrust/1000.0
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , power , 'bo-' )
        axes.plot( time , np.array([max_power/1000.0] * len(time)) , 'r--')
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Power Required (kW)')
        axes.grid(True)   
        
        power = velocity*Thrust
        mdot_power = mdot*spec_energy
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , power/mdot_power , 'bo-' )
        axes.set_xlabel('Time (mins)')
        axes.set_ylabel('Total Efficiency')
        axes.grid(True)          
        
        tot_energy = tot_energy + np.trapz(power/1000.0,time*60)
    print 'Integrated Power Required: %.0f kJ' % tot_energy
                  

    # ------------------------------------------------------------------    
    #   Angle of Attack
    # ------------------------------------------------------------------
    
    plt.figure("Angle of Attack History")
    axes = plt.gca()    
    for i in range(len(results.segments)):     
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        aoa = results.segments[i].conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        axes.plot(time, aoa, 'bo-')
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Angle of Attack (deg)')
    axes.grid(True)        

    # ------------------------------------------------------------------    
    #   Efficiency
    # ------------------------------------------------------------------

    #plt.figure("Efficiency")
    #axes = plt.gca()    
    #for i in range(len(results.segments)):     
        #time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        #e = results.segments[i].conditions.aerodynamics.angle_of_attack[:,0] / Units.deg
        #axes.plot(time, aoa, 'bo-')
    #axes.set_xlabel('Time (mins)')
    #axes.set_ylabel('Angle of Attack (deg)')
    #axes.grid(True)        
    
    
    # ------------------------------------------------------------------    
    #   Altitude
    # ------------------------------------------------------------------
    plt.figure("Altitude")
    axes = plt.gca()    
    for i in range(len(results.segments)):     
        time     = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        altitude = results.segments[i].conditions.freestream.altitude[:,0] / Units.km
        axes.plot(time, altitude, 'bo-')
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Altitude (km)')
    axes.grid(True)
    
    # ------------------------------------------------------------------    
    #   Fuel Burn and Required Air Intake
    # ------------------------------------------------------------------  
    fig = plt.figure("Fuel Burn")
    dist_base = 0.0
    for segment in results.segments.values():
                
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        velocity   = segment.conditions.freestream.velocity[:,0]
        density   = segment.conditions.freestream.density[:,0]
        mach_number   = segment.conditions.freestream.mach_number[:,0]
        mdot = segment.conditions.propulsion.fuel_mass_rate[:,0]
            
        axes = fig.add_subplot(3,1,1)
        axes.plot( time , mdot , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Fuel Burn (kg/s)')
        axes.grid(True)
        
        oxy_intake = mdot*8.0
        air_kg = oxy_intake/0.23
        air_vol = air_kg/density
        air_A = air_vol/velocity
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , air_A , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Required Intake Area')
        axes.grid(True)
            
        intake_drag = air_kg*velocity
            
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , intake_drag , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Drag Due to Intake')
    
    # ------------------------------------------------------------------    
    #   Vehicle Mass
    # ------------------------------------------------------------------    
    plt.figure("Vehicle Mass")
    axes = plt.gca()
    m_empty = vehicle.mass_properties.operating_empty
    mass_base = vehicle.mass_properties.takeoff
    for i in range(len(results.segments)):
        time = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        mass = results.segments[i].conditions.weights.total_mass[:,0]
        mdot = results.segments[i].conditions.propulsion.fuel_mass_rate[:,0]
        eta  = results.segments[i].conditions.propulsion.throttle[:,0]
        mass_from_mdot = np.array([mass_base] * len(time))
        mass_from_mdot[1:] = -integrate.cumtrapz(mdot,time*60.0)+mass_base
        axes.plot(time, mass_from_mdot, 'b--')
        axes.plot(time, mass, 'bo-')
        mass_base = mass_from_mdot[-1]
    axes.set_xlabel('Time (mins)')
    axes.set_ylabel('Vehicle Mass (kg)')
    axes.grid(True)
    
    mo = vehicle.mass_properties.takeoff
    mf = mass[-1]
    D_m = mo-mf
    spec_energy = vehicle.propulsors[0].propellant.specific_energy
    tot_energy = D_m*spec_energy
    print "Total Energy Used          %.0f kJ (does not account for efficiency loses)" % (tot_energy/1000.0)

    # ------------------------------------------------------------------    
    #   Concorde Debug
    # ------------------------------------------------------------------
     
    fig = plt.figure("Velocity and Density")
    dist_base = 0.0
    for segment in results.segments.values():
            
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        velocity   = segment.conditions.freestream.velocity[:,0]
        density   = segment.conditions.freestream.density[:,0]
        mach_number   = segment.conditions.freestream.mach_number[:,0]
        
        axes = fig.add_subplot(3,1,1)
        axes.plot( time , velocity , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Velocity (m/s)')
        axes.grid(True)
        
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , mach_number , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Mach')
        axes.grid(True)
        
        distance = np.array([dist_base] * len(time))
        distance[1:] = integrate.cumtrapz(velocity*1.94,time/60.0)+dist_base
        dist_base = distance[-1]
        
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , distance , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Distance (nmi)')
    
    
    
    # ------------------------------------------------------------------    
    #   Aerodynamics
    # ------------------------------------------------------------------
    
    fig = plt.figure("Aerodynamic Forces")
    for segment in results.segments.values():
        
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        Lift   = -segment.conditions.frames.wind.lift_force_vector[:,2]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , Lift , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Lift (N)')
        axes.grid(True)
        
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , Drag , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Drag (N)')
        axes.grid(True)
        
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , Lift/Drag , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('L/D')
        axes.grid(True)        
        
        #axes = fig.add_subplot(3,1,3)
        #axes.plot( time , Thrust , 'bo-' )
        #axes.set_xlabel('Time (min)')
        #axes.set_ylabel('Thrust (N)')
        #axes.grid(True)
        
    # ------------------------------------------------------------------    
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    
    fig = plt.figure("Aerodynamic Coefficients")
    for segment in results.segments.values():
        
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        CLift  = segment.conditions.aerodynamics.lift_coefficient[:,0]
        CDrag  = segment.conditions.aerodynamics.drag_coefficient[:,0]
        Drag   = -segment.conditions.frames.wind.drag_force_vector[:,0]
        Thrust = segment.conditions.frames.body.thrust_force_vector[:,0]
        CLV    = segment.conditions.aerodynamics.lift_breakdown.vortex[:,0]

        axes = fig.add_subplot(3,1,1)
        axes.plot( time , CLift , 'bo-' )
        axes.plot( time , CLV , 'yo-')  
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('CL')
        axes.grid(True)
        
        axes = fig.add_subplot(3,1,2)
        axes.plot( time , CDrag , 'bo-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('CD')
        axes.grid(True)
        
        axes = fig.add_subplot(3,1,3)
        axes.plot( time , Drag   , 'bo-' )
        axes.plot( time , Thrust , 'ro-' )
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Drag and Thrust (N)')
        axes.grid(True)
    
    
    # ------------------------------------------------------------------    
    #   Aerodynamics 2
    # ------------------------------------------------------------------
    
    fig = plt.figure("Drag Components")
    axes = plt.gca()    
    for i, segment in enumerate(results.segments.values()):
        
        time   = segment.conditions.frames.inertial.time[:,0] / Units.min
        drag_breakdown = segment.conditions.aerodynamics.drag_breakdown
        cdp = drag_breakdown.parasite.total[:,0]
        cdi = drag_breakdown.induced.total[:,0]
        cdc = drag_breakdown.compressible.total[:,0]
        cdm = drag_breakdown.miscellaneous.total[:,0]
        cd  = drag_breakdown.total[:,0]
        
        
        axes.plot( time , cdp , 'ko-', label='CD_P' )
        axes.plot( time , cdi , 'bo-', label='CD_I' )
        axes.plot( time , cdc , 'go-', label='CD_C' )
        axes.plot( time , cdm , 'yo-', label='CD_M' )
        axes.plot( time , cd  , 'ro-', label='CD'   )
        
        if i == 0:
            axes.legend(loc='upper center')
        
    axes.set_xlabel('Time (min)')
    axes.set_ylabel('CD')
    axes.grid(True)
    
    base_weight = 22500.0
    base_weight_str = 'Base Weight = ' + '%.0f' % base_weight + ' kg\n'
    
    m_takeoff = vehicle.mass_properties.takeoff
    m_takeoff_str = 'Takeoff Weight = ' + '%.0f' % m_takeoff + ' kg\n'
    
    m_empty   = vehicle.mass_properties.operating_empty
    m_empty_str = 'Empty Weight = ' + '%.0f' % m_empty + ' kg\n'
    
    m_fuel_cell = m_empty - base_weight
    m_fuel_cell_str = 'Fuel Cell Weight = ' + '%.0f' % m_fuel_cell + ' kg\n'
    
    m_fuel      = m_takeoff - m_empty
    m_fuel_str = 'Fuel Weight = ' + '%.0f' % m_fuel + ' kg\n'
    
    total_range = distance[-1]
    total_range_str = 'Range = ' + '%.0f' % total_range + ' nmi\n'
    
    prop_name = vehicle.propulsors.turbo_fan.propellant.tag
    prop_str = 'Propellant Type = ' + prop_name + '\n'
    
    cell_density = 1.9e6 # W/m^3
    cell_volume = max_power/cell_density
    
    cell_vol_str = 'Cell Volume = ' + '%.0f' % cell_volume + ' m^3\n'
    
    prop_density = vehicle.propulsors.turbo_fan.propellant.density
    fuel_volume = m_fuel/prop_density
    
    fuel_vol_str = 'Fuel Volume = ' + '%.0f' % fuel_volume + ' m^3\n'
    
    f = open(prop_name+'_%.0f'%total_range+'.txt','w')
    f.write(prop_str)
    f.write(total_range_str)
    f.write(m_fuel_str)
    f.write(m_takeoff_str)
    f.write(m_empty_str)
    f.write(m_fuel_cell_str)
    f.write(base_weight_str)
    f.write('Reserve Fuel = 1000 kg\n')
    f.write(cell_vol_str)
    f.write(fuel_vol_str)
    f.close
    
    plt.show()
    
    return     