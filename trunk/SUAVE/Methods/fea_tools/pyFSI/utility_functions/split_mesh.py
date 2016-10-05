#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
import numpy as np


#--imports---
import re
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import math


from SUAVE.Methods.fea_tools.pyFSI.class_str.grid.class_structure import grid
from SUAVE.Methods.fea_tools.pyFSI.class_str.elements.class_structure import CTRIA3

def split_mesh(elemlist):

    no_of_triangle_elements = 2*len(elemlist)
    elemlist_tria = [ CTRIA3() for i in range(no_of_triangle_elements)]


    tria_count = 0

    for i in range(0,len(elemlist)):
        elemlist_tria[tria_count].type = "CTRIA3"
        elemlist_tria[tria_count].eid = tria_count + 1
        elemlist_tria[tria_count].g[0] = elemlist[i].g[0]
        elemlist_tria[tria_count].g[1] = elemlist[i].g[1]
        elemlist_tria[tria_count].g[2] = elemlist[i].g[3]
        elemlist_tria[tria_count].theta = 0.0
        elemlist_tria[tria_count].pid = elemlist[i].pid
        elemlist_tria[tria_count].thickness = 0.0
        
        tria_count = tria_count + 1
        
        elemlist_tria[tria_count].type = "CTRIA3"
        elemlist_tria[tria_count].eid = tria_count + 1
        elemlist_tria[tria_count].g[0] = elemlist[i].g[1]
        elemlist_tria[tria_count].g[1] = elemlist[i].g[2]
        elemlist_tria[tria_count].g[2] = elemlist[i].g[3]
        elemlist_tria[tria_count].theta = 0.0
        elemlist_tria[tria_count].pid = elemlist[i].pid
        elemlist_tria[tria_count].thickness = 0.0

        tria_count = tria_count + 1


    return  elemlist_tria


