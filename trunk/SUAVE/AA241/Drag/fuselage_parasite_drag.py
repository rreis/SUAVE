# fuselage_parasite_drag.py
#
# Created:  Tim MacDonald, Sep 2014
# Modified: 

import SUAVE

# suave imports
from SUAVE.Attributes.Gases import Air # you should let the user pass this as input
air = Air()
compute_speed_of_sound = air.compute_speed_of_sound

from SUAVE.Attributes.Results import Result

# python imports
import os, sys, shutil
from copy import deepcopy
from warnings import warn

# package imports
import numpy as np
import scipy as sp

def fuselage_parasite_drag(vehicle,conditions):
    
    # Unpack values needed for computations
    T = conditions.freestream.temperature
    Re = conditions.freestream.reynolds_number
    Ma = conditions.freestream.mach_number
    reference_area = vehicle.reference_area
    
    cf = skin_friction_cofficient(Re,Ma,T)
    
    cd_upsweep = upsweep_drag_coefficient(reference_area)
    
    cd_misc = miscellaneous_drag(vehicle)
    
    # define total_cd
    total_cd = 0
    
    return total_cd
    
def skin_friction_cofficient(Re,Ma,T):
    
    # ----- Add equations here ---------------------############
    cf = 0
    
    return cf

def upsweep_drag_coefficient(reference_area):
    
    # ----- Add equations here ---------------------############
    cd_upsweep = 0
    
    return cd_upsweep

def miscellaneous_drag(vehicle):
    
    # ----- Add equations here ---------------------############
    cd_misc = 0
    
    return cd_misc