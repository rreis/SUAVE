# compute_TAS_from_CAS.py
#
# Created:  May 2014, SUAVE Team
# Modified: Aug 2016, T. MacDonald
#
# Moved to Aerodynamics

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
import SUAVE

# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------
def compute_TAS_from_CAS(CAS,conditions,atmosphere):

    # unpack
    air_speed = CAS

    # get atmospheric conditions in SL, ISA (standard conditions)
    atmo_std = atmosphere.compute_values(0.)
    p0       = atmo_std.pressure
    rho0     = atmo_std.density
    vsound   = atmo_std.speed_of_sound
    theta    = conditions.freestream.temperature / atmo_std.temperature
    delta    = conditions.freestream.pressure / atmo_std.pressure

    # get air properties
    gamma = atmosphere.fluid_properties.compute_gamma()

    # compute true airspeed based in input Calibrated Airspeed
    true_airspeed = np.sqrt( 2*gamma*p0/((gamma-1)*rho0)) * np.sqrt(theta*((1/delta*((1+(gamma-1)/2*(air_speed/vsound)**2)**(gamma/(gamma-1))-1)+1)**((gamma-1)/gamma)-1))

    return true_airspeed.reshape(np.shape(conditions.freestream.temperature))
