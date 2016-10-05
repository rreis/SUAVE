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

def compute_centroid(elemlist,pointlist):



    for i in range(0,len(elemlist)):
        temp_centroid = [0.0,0.0,0.0]
        
        if (elemlist[i].type == "CTRIA3"):
            for j in range(0,3):
                temp_centroid[0] += 1.0/3.0*(pointlist[elemlist[i].g[j]-1].x[0])
                temp_centroid[1] += 1.0/3.0*(pointlist[elemlist[i].g[j]-1].x[1])
                temp_centroid[2] += 1.0/3.0*(pointlist[elemlist[i].g[j]-1].x[2])


            #compute the area

            side1=  np.sqrt((pointlist[elemlist[i].g[1]-1].x[0]-pointlist[elemlist[i].g[0]-1].x[0])**2 + (pointlist[elemlist[i].g[1]-1].x[1]-pointlist[elemlist[i].g[0]-1].x[1])**2 + (pointlist[elemlist[i].g[1]-1].x[2]-pointlist[elemlist[i].g[0]-1].x[2])**2)
            side2=  np.sqrt((pointlist[elemlist[i].g[2]-1].x[0]-pointlist[elemlist[i].g[1]-1].x[0])**2 + (pointlist[elemlist[i].g[2]-1].x[1]-pointlist[elemlist[i].g[1]-1].x[1])**2 + (pointlist[elemlist[i].g[2]-1].x[2]-pointlist[elemlist[i].g[1]-1].x[2])**2)
            side3=  np.sqrt((pointlist[elemlist[i].g[0]-1].x[0]-pointlist[elemlist[i].g[2]-1].x[0])**2 + (pointlist[elemlist[i].g[0]-1].x[1]-pointlist[elemlist[i].g[2]-1].x[1])**2 + (pointlist[elemlist[i].g[0]-1].x[2]-pointlist[elemlist[i].g[2]-1].x[2])**2)
                              
            ss =  (side1 + side2 + side3)/2.0
            
            area = np.sqrt(ss*(ss-side1)*(ss-side2)*(ss-side3))






        if (elemlist[i].type == "CQUAD4"):
            for j in range(0,4):
                temp_centroid[0] += 1.0/4.0*(pointlist[elemlist[i].g[j]-1].x[0])
                temp_centroid[1] += 1.0/4.0*(pointlist[elemlist[i].g[j]-1].x[1])
                temp_centroid[2] += 1.0/4.0*(pointlist[elemlist[i].g[j]-1].x[2])
            


            #compute the area
                   
                #1st half
                              
            side1=  np.sqrt((pointlist[elemlist[i].g[1]-1].x[0]-pointlist[elemlist[i].g[0]-1].x[0])**2 + (pointlist[elemlist[i].g[1]-1].x[1]-pointlist[elemlist[i].g[0]-1].x[1])**2 + (pointlist[elemlist[i].g[1]-1].x[2]-pointlist[elemlist[i].g[0]-1].x[2])**2)
            side2=  np.sqrt((pointlist[elemlist[i].g[2]-1].x[0]-pointlist[elemlist[i].g[1]-1].x[0])**2 + (pointlist[elemlist[i].g[2]-1].x[1]-pointlist[elemlist[i].g[1]-1].x[1])**2 + (pointlist[elemlist[i].g[2]-1].x[2]-pointlist[elemlist[i].g[1]-1].x[2])**2)
            side3=  np.sqrt((pointlist[elemlist[i].g[0]-1].x[0]-pointlist[elemlist[i].g[2]-1].x[0])**2 + (pointlist[elemlist[i].g[0]-1].x[1]-pointlist[elemlist[i].g[2]-1].x[1])**2 + (pointlist[elemlist[i].g[0]-1].x[2]-pointlist[elemlist[i].g[2]-1].x[2])**2)
                                                                                
            ss =  (side1 + side2 + side3)/2.0
                                                                                
            area0 = np.sqrt(ss*(ss-side1)*(ss-side2)*(ss-side3))
                              
                       
                              
                #2nd half
                              
            side1=  np.sqrt((pointlist[elemlist[i].g[2]-1].x[0]-pointlist[elemlist[i].g[0]-1].x[0])**2 + (pointlist[elemlist[i].g[2]-1].x[1]-pointlist[elemlist[i].g[0]-1].x[1])**2 + (pointlist[elemlist[i].g[2]-1].x[2]-pointlist[elemlist[i].g[0]-1].x[2])**2)
            side2=  np.sqrt((pointlist[elemlist[i].g[3]-1].x[0]-pointlist[elemlist[i].g[2]-1].x[0])**2 + (pointlist[elemlist[i].g[3]-1].x[1]-pointlist[elemlist[i].g[2]-1].x[1])**2 + (pointlist[elemlist[i].g[3]-1].x[2]-pointlist[elemlist[i].g[2]-1].x[2])**2)
            side3=  np.sqrt((pointlist[elemlist[i].g[0]-1].x[0]-pointlist[elemlist[i].g[3]-1].x[0])**2 + (pointlist[elemlist[i].g[0]-1].x[1]-pointlist[elemlist[i].g[3]-1].x[1])**2 + (pointlist[elemlist[i].g[0]-1].x[2]-pointlist[elemlist[i].g[3]-1].x[2])**2)
                                                                                
            ss =  (side1 + side2 + side3)/2.0
                                                                                
            area1 = np.sqrt(ss*(ss-side1)*(ss-side2)*(ss-side3))
              
            area = area0 + area1



        elemlist[i].centroid = temp_centroid
        elemlist[i].area = area



