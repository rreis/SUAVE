# Constant_Throttle_Constant_Altitude.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from SUAVE.Methods.Geometry.Three_Dimensional \
     import angles_to_dcms, orientation_product, orientation_transpose

# ----------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------

def unpack_unknowns(segment,state):
    
    # unpack unknowns
    unknowns   = state.unknowns
    velocity_x = unknowns.velocity_x
    time       = unknowns.time
    theta      = unknowns.body_angle
    
    # unpack givens
    df         = segment.distance
    t_initial  = state.conditions.frames.inertial.time[0,0]
    t_nondim   = state.numerics.dimensionless.control_points
    
    # time
    t_final    = t_initial + time  
    time       = t_nondim * (t_final-t_initial) + t_initial     

    #apply unknowns
    conditions = state.conditions
    conditions.frames.inertial.velocity_vector[:,0]  = velocity_x[:,0]
    conditions.frames.body.inertial_rotations[:,1]   = theta[:,0]  
    conditions.frames.inertial.time[:,0]             = time[:,0]
    
# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------    

def initialize_conditions(segment,state):
    """ Segment.initialize_conditions(conditions,numerics,initials=None)
        update the segment conditions
        pin down as many condition variables as possible in this function
        Inputs:
            conditions - the conditions data dictionary, with initialized
            zero arrays, with number of rows = 
            segment.conditions.n_control_points
            initials - a data dictionary with 1-row column arrays pulled from
            the last row of the previous segment's conditions data, or none
            if no previous segment
        Outputs:
            conditions - the conditions data dictionary, updated with the 
                         values that can be precalculated
        Assumptions:
            --
        Usage Notes:
            may need to inspect segment (self) for user inputs
            will be called before solving the segments free unknowns
    """

    conditions = state.conditions

    # unpack inputs
    alt      = segment.altitude
    df       = segment.distance
    throttle = segment.throttle	
    N        = segment.state.numerics.number_control_points   
    
    # check for initial altitude
    if alt is None:
        if not state.initials: raise AttributeError('altitude not set')
        alt = -1.0 * state.initials.conditions.frames.inertial.position_vector[-1,2]
        segment.altitude = alt   
        
        ## estimate distances for faster convergence
        ##dists = t_nondim*df
    
        ##apply unknowns
        #conditions = state.conditions
        ##conditions.frames.inertial.position_vector[:,0]  = dists[:,0]        
    
    # pack conditions
    state.conditions.propulsion.throttle[:,0] = throttle  
    state.conditions.freestream.altitude[:,0] = alt
    state.conditions.frames.inertial.position_vector[:,2] = -alt # z points down   

# ----------------------------------------------------------------------
#  Solve Residuals
# ----------------------------------------------------------------------    

def solve_residuals(segment,state):
    """ Segment.solve_residuals(conditions,numerics,unknowns,residuals)
        the hard work, solves the residuals for the free unknowns
        called once per segment solver iteration
    """

    # unpack inputs
    conditions = state.conditions
    FT = conditions.frames.inertial.total_force_vector
    df = segment.distance
    v  = conditions.frames.inertial.velocity_vector
    p  = conditions.frames.inertial.position_vector
    D  = state.numerics.time.differentiate
    I  = state.numerics.time.integrate
    m  = conditions.weights.total_mass

    # process and pack
    acceleration = np.dot(D , v)
    conditions.frames.inertial.acceleration_vector = acceleration
    
    a  = state.conditions.frames.inertial.acceleration_vector

    state.residuals.forces[:,0] = FT[:,0]/m[:,0] - a[:,0]
    state.residuals.forces[:,1] = FT[:,2]/m[:,0] #- a[:,2]   
    state.residuals.final_distance_error = (p[-1,0] - df)/df

    return
    
# ------------------------------------------------------------------
#   Methods For Post-Solver
# ------------------------------------------------------------------    

def post_process(segment,state):
    """ Segment.post_process(conditions,numerics,unknowns)
        post processes the conditions after converging the segment solver.
        Packs up the final position vector to allow estimation of the ground
        roll distance (e.g., distance from brake release to rotation speed in
        takeoff, or distance from touchdown to full stop on landing).
        Inputs - 
            unknowns - data dictionary of converged segment free unknowns with
            fields:
                states, controls, finals
                    these are defined in segment.__defaults__
            conditions - data dictionary of segment conditions
                    these are defined in segment.__defaults__
            numerics - data dictionary of the converged differential operators
        Outputs - 
            conditions - data dictionary with remaining fields filled with post-
            processed conditions. Updated fields are:
            conditions.frames.inertial.position_vector  (x-position update)
        Usage Notes - 
            Use this to store the unknowns and any other interesting in 
            conditions for later plotting. For clarity and style, be sure to 
            define any new fields in segment.__defaults__
    """

    # unpack inputs
    conditions = state.conditions
    ground_velocity  = conditions.frames.inertial.velocity_vector
    I                = state.numerics.time.integrate
    initial_position = conditions.frames.inertial.position_vector[0,:]

    # process
    position_vector = initial_position + np.dot( I , ground_velocity)

    # pack outputs
    conditions.frames.inertial.position_vector = position_vector