#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
import numpy as np

from nearest_point_interpolation import *


def nearest_n_points(pointlist_fl,pointlist_str,nearest_n_points,n):

    nearest_n_points_array =  [[0 for x in range(n)] for x in range(len(pointlist_fl))]  #np.array([len(pointlist_fl),10])

    mesh_def = open("loads.txt","wb")
        
    #write load file
    for i in range(0,len(pointlist_fl)):
        mesh_def.write(format(pointlist_fl[i].x[0]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_fl[i].x[1]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_fl[i].x[2]))
        mesh_def.write("\n")


    for i in range(0,len(pointlist_str)):
        mesh_def.write(format(pointlist_str[i][0]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_str[i][1]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist_str[i][2]))
        mesh_def.write("\n")


    mesh_def.close()

    no_of_fluid_points = len(pointlist_fl)
    no_of_structure_points = len(pointlist_str)

    mampp = nearest_n_point_interpolation(no_of_fluid_points, no_of_structure_points, n)


    print "Done with interpolation"

    file = open("interpolation.txt", 'r')
    
    for i in range(0,len(pointlist_fl)):
        for line in file:
            
            line_split = line.split(",")
            for j in range(0,n):
                nearest_n_points_array[i][j] = int(line_split[j])
            break
    
    

    return nearest_n_points_array
    #read values from load file






    
    









    
    















    







