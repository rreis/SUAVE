# Constant_Throttle_Constant_Mach.py
# 
# Created:  
# Modified: Aug 2016, T. MacDonald

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
import SUAVE
from SUAVE.Methods.Geometry.Three_Dimensional \
     import angles_to_dcms, orientation_product, orientation_transpose

# ----------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------

def unpack_body_angle(segment,state):

    # unpack unknowns
    theta      = state.unknowns.body_angle

    # apply unknowns
    state.conditions.frames.body.inertial_rotations[:,1] = theta[:,0]      


# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------


def initialize_conditions(segment,state):

    # unpack
    throttle   = segment.throttle
    mach       = segment.mach_number 
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    h_nondim   = state.numerics.dimensionless.control_points
    conditions = state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * state.initials.conditions.frames.inertial.position_vector[-1,2]
        segment.altitude_start = alt0

    # discretize on altitude
    alt = h_nondim * (altf-alt0) + alt0    

    # pack conditions  
    conditions.propulsion.throttle[:,0] = throttle
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context
    SUAVE.Methods.Missions.Segments.Common.Aerodynamics.update_atmosphere(segment,state) # get density for airspeed
    a         = conditions.freestream.speed_of_sound[:,0]   
    air_speed = mach*a
    segment.air_speed = air_speed
    #air_speed[:] = 123.
    conditions.frames.inertial.velocity_vector[:,0] = air_speed # start up value
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down

def update_differentials_time(segment,state):

    # unpack
    numerics = state.numerics
    xh = numerics.dimensionless.control_points
    Dh = numerics.dimensionless.differentiate
    Ih = numerics.dimensionless.integrate

    vz = state.conditions.frames.inertial.velocity_vector[:,2]
    h  = state.conditions.frames.inertial.position_vector[:,2]
    H  = h[-1] - h[0]

    # rescale altitude
    Dh = Dh / H
    Ih = Ih * H

    t = np.dot(Ih,1/vz)
    #print t
    if np.min(t) < 0:
        a = 0
    Tot_t = t[-1] - t[0]
    N = len(t)
    #t_norm = t/t[-1]

    # From chebyshev_data.py

    # coefficients
    c = np.array( [2.] + [1.]*(N-2) + [2.] )
    c = c * ( (-1.) ** np.arange(0,N) )
    A = np.tile( t, (N,1) ).T
    dA = A - A.T + np.eye( N )
    cinv = 1./c; 

    # build operator
    D = np.zeros( (N,N) );

    # math
    for i in range(N):
        for j in range(N):
            D[i][j] = c[i]*cinv[j]/dA[i][j]

    # more math
    D = D - np.diag( np.sum( D.T, axis=0 ) );

    # --- Integratin operator

    # invert D except first row and column
    I = np.linalg.inv(D[1:,1:]); 

    # repack missing columns with zeros
    I = np.append(np.zeros((1,N-1)),I,axis=0)
    I = np.append(np.zeros((N,1)),I,axis=1)

    # pack
    t_initial = state.conditions.frames.inertial.time[0,0]
    state.conditions.frames.inertial.time[:,0] = t_initial + t[:]    
    # pack
    numerics.time.control_points = t
    numerics.time.differentiate  = D
    numerics.time.integrate      = I

    return

# ----------------------------------------------------------------------
#  Update Velocity Vector from Wind Angle
# ----------------------------------------------------------------------

def update_velocity_vector_from_wind_angle(segment,state):

    # unpack
    conditions = state.conditions 

    mach = segment.mach_number

    a         = conditions.freestream.speed_of_sound[:,0]   
    air_speed = mach*a
    v_mag     = air_speed[:,None]

    #v_mag = 120.

    alpha      = state.unknowns.wind_angle[:,0][:,None]
    theta      = state.unknowns.body_angle[:,0][:,None]

    # Flight path angle
    gamma = theta-alpha

    # process
    v_x =  v_mag * np.cos(gamma)
    v_z = -v_mag * np.sin(gamma) # z points down

    # pack
    conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,2] = v_z[:,0]

    return conditions    

def update_forces(segment,state):

    # unpack
    conditions = state.conditions

    # unpack forces
    wind_lift_force_vector        = conditions.frames.wind.lift_force_vector
    wind_drag_force_vector        = conditions.frames.wind.drag_force_vector
    body_thrust_force_vector      = conditions.frames.body.thrust_force_vector
    inertial_gravity_force_vector = conditions.frames.inertial.gravity_force_vector

    # unpack transformation matrices
    T_body2inertial = conditions.frames.body.transform_to_inertial
    T_wind2inertial = conditions.frames.wind.transform_to_inertial

    # to inertial frame
    L = orientation_product(T_wind2inertial,wind_lift_force_vector)
    D = orientation_product(T_wind2inertial,wind_drag_force_vector)
    T = orientation_product(T_body2inertial,body_thrust_force_vector)
    W = inertial_gravity_force_vector

    # sum of the forces
    F = L + D + T + W
    # like a boss

    #numerics = state.numerics
    #xh = numerics.dimensionless.control_points
    #Dh = numerics.dimensionless.differentiate
    #Ih = numerics.dimensionless.integrate    

    #t = numerics.time.control_points
    #Dt = numerics.time.differentiate
    #It = numerics.time.integrate



    # pack
    conditions.frames.inertial.total_force_vector[:,:] = F[:,:]

    return

def residual_total_forces(segment,state):

    FT = state.conditions.frames.inertial.total_force_vector
    a  = state.conditions.frames.inertial.acceleration_vector
    m  = state.conditions.weights.total_mass    

    state.residuals.forces[:,0] = FT[:,0]/m[:,0] - a[:,0]
    state.residuals.forces[:,1] = FT[:,2]/m[:,0] - a[:,2]       

    return

def update_weights(segment,state):

    # unpack
    conditions = state.conditions
    m0        = conditions.weights.total_mass[0,0]
    m_empty   = segment.analyses.weights.mass_properties.operating_empty
    mdot_fuel = conditions.weights.vehicle_mass_rate
    I         = state.numerics.time.integrate
    numerics = state.numerics
    Ih        = numerics.dimensionless.integrate   
    xh        = numerics.dimensionless.control_points
    t         = numerics.time.control_points
    g         = conditions.freestream.gravity

    a,b,c = np.polyfit(t,mdot_fuel,2)
    t_cos = xh[:,0]*t
    mdot_cos = a*t_cos**2 + b*t_cos + c

    # calculate
    m = m0 + np.dot(I, -mdot_cos )

    a,b,c = np.polyfit(t_cos,m,2)
    m = a*t**2 + b*t + c
    m = m[:,None]

    # weight
    W = m*g

    # pack
    conditions.weights.total_mass[1:,0]                  = m[1:,0] # don't mess with m0
    conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]

    return


def update_acceleration(segment,state):

    # unpack conditions
    v = state.conditions.frames.inertial.velocity_vector
    D = state.numerics.time.differentiate
    numerics = state.numerics
    Dh        = numerics.dimensionless.integrate   
    xh        = numerics.dimensionless.control_points
    t         = numerics.time.control_points    

    a0,b0,c0 = np.polyfit(t,v[:,0],2)
    a1,b1,c1 = np.polyfit(t,v[:,1],2)
    a2,b2,c2 = np.polyfit(t,v[:,2],2)
    t_cos = xh[:,0]*t
    v_cos = v*1.
    v_cos[:,0] = a0*t_cos**2 + b0*t_cos + c0
    v_cos[:,1] = a1*t_cos**2 + b1*t_cos + c1
    v_cos[:,2] = a2*t_cos**2 + b2*t_cos + c2

    # accelerations
    acc = np.dot(D,v_cos)

    a0,b0,c0 = np.polyfit(t,acc[:,0],2)
    a1,b1,c1 = np.polyfit(t,acc[:,1],2)
    a2,b2,c2 = np.polyfit(t,acc[:,2],2)
    acc[:,0] = a0*t_cos**2 + b0*t_cos + c0
    acc[:,1] = a1*t_cos**2 + b1*t_cos + c1
    acc[:,2] = a2*t_cos**2 + b2*t_cos + c2  

    # pack conditions
    state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]  