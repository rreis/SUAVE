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

def compute_normal(elemlist,pointlist):



    for i in range(0,len(elemlist)):
        normal = np.zeros(3)
        v1 = np.zeros(3)
        v2 = np.zeros(3)
        
        if (elemlist[i].type == "CTRIA3"):
            print



        if (elemlist[i].type == "CQUAD4"):
        
            
            for j in range(0,3):
                
                v1[j] = pointlist[elemlist[i].g[2]-1].x[j] - pointlist[elemlist[i].g[0]-1].x[j];
                v2[j] = pointlist[elemlist[i].g[3]-1].x[j] - pointlist[elemlist[i].g[1]-1].x[j];                
                
                
                
                #v1[j] = pointlist[elemlist[2]][i] - pointlist[elemlist[0]][i];
                #v2[j] = pointlist[elemlist[3]][i] - pointlist[elemlist[1]][i];
                          

            normal[0] = v1[1]*v2[2] - v1[2]*v2[1]
            normal[1] = -1*(v1[0]*v2[2] - v1[2]*v2[0])
            normal[2] = v1[0]*v2[1] - v1[1]*v2[0]
            
            
            normal_magnitude = np.sqrt(normal[0]**2.0 + normal[1]**2.0 + normal[2]**2.0)
            
            normal[0] = normal[0]/normal_magnitude
            normal[1] = normal[1]/normal_magnitude
            normal[2] = normal[2]/normal_magnitude    
            
            
            elemlist[i].normal = normal
            
            
            
            #area computation
            
            #triangle 1
            s0 = np.sqrt((pointlist[elemlist[i].g[0]-1].x[0] -  pointlist[elemlist[i].g[1]-1].x[0])**2.0 + (pointlist[elemlist[i].g[0]-1].x[1] -  pointlist[elemlist[i].g[1]-1].x[1])**2.0 + (pointlist[elemlist[i].g[0]-1].x[2] -  pointlist[elemlist[i].g[1]-1].x[2])**2.0)
            
            s1 = np.sqrt((pointlist[elemlist[i].g[1]-1].x[0] -  pointlist[elemlist[i].g[2]-1].x[0])**2.0 + (pointlist[elemlist[i].g[1]-1].x[1] -  pointlist[elemlist[i].g[2]-1].x[1])**2.0 + (pointlist[elemlist[i].g[1]-1].x[2] -  pointlist[elemlist[i].g[2]-1].x[2])**2.0)
             
            s2 = np.sqrt((pointlist[elemlist[i].g[2]-1].x[0] -  pointlist[elemlist[i].g[0]-1].x[0])**2.0 + (pointlist[elemlist[i].g[2]-1].x[1] -  pointlist[elemlist[i].g[0]-1].x[1])**2.0 + (pointlist[elemlist[i].g[2]-1].x[2] -  pointlist[elemlist[i].g[0]-1].x[2])**2.0)
            
            
            ss = 0.5*(s0 + s1 + s2)
            
            area0 = np.sqrt(ss*(ss-s0)*(ss-s1)*(ss-s2))
            
            #triangle 2
            
            #triangle 1
            s0 = np.sqrt((pointlist[elemlist[i].g[0]-1].x[0] -  pointlist[elemlist[i].g[2]-1].x[0])**2.0 + (pointlist[elemlist[i].g[0]-1].x[1] -  pointlist[elemlist[i].g[2]-1].x[1])**2.0 + (pointlist[elemlist[i].g[0]-1].x[2] -  pointlist[elemlist[i].g[2]-1].x[2])**2.0)
            
            s1 = np.sqrt((pointlist[elemlist[i].g[2]-1].x[0] -  pointlist[elemlist[i].g[3]-1].x[0])**2.0 + (pointlist[elemlist[i].g[2]-1].x[1] -  pointlist[elemlist[i].g[3]-1].x[1])**2.0 + (pointlist[elemlist[i].g[2]-1].x[2] -  pointlist[elemlist[i].g[3]-1].x[2])**2.0)
            
            
            s2 = np.sqrt((pointlist[elemlist[i].g[3]-1].x[0] -  pointlist[elemlist[i].g[0]-1].x[0])**2.0 + (pointlist[elemlist[i].g[3]-1].x[1] -  pointlist[elemlist[i].g[0]-1].x[1])**2.0 + (pointlist[elemlist[i].g[3]-1].x[2] -  pointlist[elemlist[i].g[0]-1].x[2])**2.0)
            
            
            ss = 0.5*(s0 + s1 + s2)
            
            area1 = np.sqrt(ss*(ss-s0)*(ss-s1)*(ss-s2))
            
            area = area0 +area1      
            
            elemlist[i].area = area