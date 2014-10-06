# compute_conditions.py
#
# Created:  Tim MacDonald, Sep 2014
# Modified: 

import SUAVE

from SUAVE.Attributes.Results import Result

# python imports
import os, sys, shutil
from copy import deepcopy
from warnings import warn

# package imports
import numpy as np
import scipy as sp

from SUAVE.Structure import (
Data, Container, Data_Exception, Data_Warning,
)

def compute_conditions(altitude,velocity):
    
    # ----- Add equations here ---------------------############
    
    T = 0
    
    p = 0
    
    mew = 0
    
    Re = 0
    
    rho = 0
    
    c = 0
    
    Ma = 0
    
    # ----------------------------------------------############
    
    conditions = Data()
    conditions.freestream = Data()
    conditions.freestream.temperature         = T
    conditions.freestream.pressure            = p
    conditions.freestream.viscosity           = mew # kinematic viscosity
    conditions.freestream.velocity            = velocity
    conditions.freestream.mach_number         = Ma
    conditions.freestream.reynolds_number     = Re
    conditions.freestream.density             = rho
    conditions.freestream.altitude            = altitude
    conditions.freestream.speed_of_sound      = c
    
    return conditions