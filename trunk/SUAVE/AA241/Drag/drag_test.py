# total_drag.py
#
# Created:  Tim MacDonald, Sep 14
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

def total_drag(vehicle,conditions):
    a=0