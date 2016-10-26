import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#currently look only at the main wing and the fuselage

#the function marks the lower surface of the fuselage (payload) and the wing lower surface (fuel loads)
#loop over the wings
#check if the contains_fuel tag is active
#pull out the starting and ending  x,y and z of the fule loads
#loop over the wing lower surface
#add the fuel load weight


def visualize_aircraft_loading(elemlist,pointlist):


    npoint = len(pointlist)
    nelem = len(elemlist)

    print "Writing tecplot deformation file"
    tecplot_file_orig = 'visualize_full_airc_loading.plt'
    
    #----orig file-----------------------------------------------
    #-------------------------------------------------------------------
    
    #-----writing the headers-----

    mesh_def = open(tecplot_file_orig,"wb")
    
    mesh_def.write("TITLE = \"Visualization of CSM meshes\"")
    mesh_def.write("\n")
    mesh_def.write("VARIABLES = \"x\", \"y\", \"z\", \"fx\", \"fy\", \"fz\", \"faero_x\", \"faero_y\", \"faero_z\", \"floads_x\", \"floads_y\", \"floads_z\", \"fpressure_x\", \"fpressure_y\", \"fpressure_z\", \"pressure\", \"n_x\", \"n_y\", \"n_z\", \"na_x\", \"na_y\", \"na_z\", ")
    mesh_def.write("\n")
    mesh_def.write("ZONE NODES=")
    mesh_def.write(format(npoint))
    mesh_def.write(", ELEMENTS=")
    mesh_def.write(format(nelem))
    #    mesh_def.write("\n")
    mesh_def.write(", DATAPACKING=POINT, ZONETYPE=FEQUADRILATERAL")
    mesh_def.write("\n")
        
        
    #---------writing the points----------------------
    # Write x coordinates.



    for i in range(0,len(pointlist)):
        mesh_def.write(format(pointlist[i].x[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[2]))
        mesh_def.write("\t")
        
        mesh_def.write(format(pointlist[i].f[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[2]))
        mesh_def.write("\t")
        
        mesh_def.write(format(pointlist[i].f_aero[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f_aero[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f_aero[2]))
        mesh_def.write("\t")


        mesh_def.write(format(pointlist[i].f_loads[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f_loads[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f_loads[2]))
        mesh_def.write("\t")


        mesh_def.write(format(pointlist[i].f_pressure[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f_pressure[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f_pressure[2]))
        mesh_def.write("\t")
        
        mesh_def.write(format(pointlist[i].nv[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].nv[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].nv[2]))
        mesh_def.write("\t")


        mesh_def.write(format(pointlist[i].nva[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].nva[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].nva[2]))
        mesh_def.write("\t")        
        
        
        pressure = np.sqrt(pointlist[i].f_pressure[0]**2.0 + pointlist[i].f_pressure[1]**2.0 + pointlist[i].f_pressure[2]**2.0)

        mesh_def.write(format(pressure))
        mesh_def.write("\n")


        #----------writing the elements----------------------

# Write the element connectivity (1-based).

    for i in range(0,len(elemlist)):
        mesh_def.write(format(elemlist[i].g[0]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[1]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[2]))
        mesh_def.write("  ")
        if(elemlist[i].type=='CTRIA3'):
            
            mesh_def.write(format(elemlist[i].g[2]))
            mesh_def.write("\n")
    
        if(elemlist[i].type=='CQUAD4'):
            
            mesh_def.write(format(elemlist[i].g[3]))
            mesh_def.write("\n")









    #x = np.zeros(len(pointlist))
    #y = np.zeros(len(pointlist))
    #z = np.zeros(len(pointlist))


    #Fpr_x = np.zeros(len(pointlist))
    #Fpr_y = np.zeros(len(pointlist))
    #Fpr_z = np.zeros(len(pointlist))
    
    
    #for i in range(0,len(pointlist)):
        #x[i] = pointlist[i].x[0]
        #y[i] = pointlist[i].x[1]
        #z[i] = pointlist[i].x[2]
        
        #Fpr_x[i] = pointlist[i].f_pressure[0]
        #Fpr_y[i] = pointlist[i].f_pressure[1]
        #Fpr_z[i] = pointlist[i].f_pressure[2]        
        
        
        
        

    ##plot the aerodynamic loading
    #fig = plt.figure()
    #ax = Axes3D(fig)
    #ax.quiver(x, y, z, Fpr_x, Fpr_y, Fpr_z)
    
    #plt.savefig("3d_pressure_loads_plot.png",format='png')







    ##Visualize the results
    #fig = plt.figure(1)
    #plt.xlabel('x axis')
    #plt.ylabel('y axis')

    #ax = Axes3D(fig)

    #for i in range (0,len(pointlist)):
        #if((pointlist[i].f[0]>0.000001) or (pointlist[i].f[1]>0.000001) or (pointlist[i].f[2]>0.000001)):
            
            #ax.scatter(pointlist[i].x[0], pointlist[i].x[1], pointlist[i].f[1],c="red")

    #plt.savefig("3d_loads_plot.png",format='png')

    ##plt.show()
    #plt.clf()



    #loads = np.zeros(len(pointlist))
    #y_position = np.zeros(len(pointlist))
    #for i in range(0,len(pointlist)):
        
        #if((pointlist[i].f[0]>0.000001) or (pointlist[i].f[1]>0.000001) or (pointlist[i].f[2]>0.000001)):
            #loads[i] = pointlist[i].f[1]
            #y_position[i] = pointlist[i].x[1]


    #fig2 = plt.figure(2)
    #plt.xlabel('y location')
    #plt.ylabel('loads')
    #plt.plot(y_position,loads,'*')
    #plt.savefig("2D_loads_distribution.png",format='png')
    #plt.clf()
    







