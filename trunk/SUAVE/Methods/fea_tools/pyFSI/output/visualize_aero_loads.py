##@write_tecplot_file
#@brief Writing a tecplot file for visualization
#@details
#@author Paul Urbanczyk,Anil Variyar
#@version 1.0
#
# FSI developers: Heather Kline, Anil Variyar, Paul Urbanczyk
#
#
##

#-----------
#---function to convert integers to required nastran format

def visualize_aero_loads(aircraft):


    #loop all the elements and points into a total array

    print "Writing tecplot deformation file"
    tecplot_stress_file = 'stress_file.plt'
    
    #----orig file-----------------------------------------------
    #-------------------------------------------------------------------
    
    #-----writing the headers-----

    mesh_def2 = open("Visualize_aero_mesh.plt","wb")
    mesh_def2.write("TITLE = \"Visualization of CSM meshes\"")
    mesh_def2.write("\n")
    mesh_def2.write("VARIABLES = \"x\", \"y\", \"z\",")
    mesh_def2.write("\n")
    mesh_def2.write("ZONE NODES=")
    mesh_def2.write(format(length(pointlist)))
    mesh_def2.write(", ELEMENTS=")
    mesh_def2.write(format(length(elemlist)))
    #    mesh_def.write("\n")
    mesh_def2.write(", DATAPACKING=POINT, ZONETYPE=FEQUADRILATERAL")
    mesh_def2.write("\n")
    
    for i in range(0,len(pointlist)):
        
        mesh_def2.write(format(self.pointlist[i].x[0]))
        mesh_def2.write("\t")
        mesh_def2.write(format(self.pointlist[i].x[1]))
        mesh_def2.write("\t")
        mesh_def2.write(format(self.pointlist[i].x[2]))
        mesh_def2.write("\n")
    
    for i in range(0,len(elemlist)):
        mesh_def2.write(format(elemlist_upper[i].g[0]))
        mesh_def2.write("  ")
        mesh_def2.write(format(elemlist_upper[i].g[1]))
        mesh_def2.write("  ")
        mesh_def2.write(format(elemlist_upper[i].g[2]))
        mesh_def2.write("  ")
        mesh_def2.write(format(elemlist_upper[i].g[3]))
        mesh_def2.write("\n")
    
    mesh_def2.close()




