#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format

def write_tecplot_file_str(pointlist,elemlist,tecplot_file_orig,npoint,nelem):
    
    print "Writing tecplot deformation file"
    
    
    #----orig file-----------------------------------------------
    #-------------------------------------------------------------------
    
    #-----writing the headers-----
    
    mesh_def = open(tecplot_file_orig,"wb")
    
    mesh_def.write("TITLE = \"Visualization of CSM meshes\"")
    mesh_def.write("\n")
    mesh_def.write("VARIABLES = \"x\", \"y\", \"z\",\"d\",")
    mesh_def.write("\n")
    mesh_def.write("ZONE NODES=")
    mesh_def.write(format(npoint))
    mesh_def.write(", ELEMENTS=")
    mesh_def.write(format(nelem))
    mesh_def.write("\n")
    mesh_def.write(", DATAPACKING=BLOCK, ZONETYPE=FEQUADRILATERAL")
    mesh_def.write("\n")
    
    
    #---------writing the points----------------------
    # Write x coordinates.
    
    
    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[0]))
        mesh_def.write("\n")
    
    
    for iNode in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[1]))
        mesh_def.write("\n")
    
    for iNode in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[2]))
        mesh_def.write("\n")
    
    for iNode in range(0,npoint):
        mesh_def.write(format(1))
        mesh_def.write("\n")
    
    
    
    
    #----------writing the elements----------------------
    
    # Write the element connectivity (1-based).
    
    for i in range(0,nelem):
        mesh_def.write(format(elemlist[i].g[0]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[1]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[2]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[3]))
        mesh_def.write("\n")
    
    
    
    
    
    
#mesh_def.close()


#----deformation file-----------------------------------------------
#-------------------------------------------------------------------


#    #-----writing the headers-----
#
#    mesh_def = open(tecplot_file_deformed,"wb")
#
#    mesh_def.write("TITLE = \"Visualization of CSM meshes\"")
#    mesh_def.write("\n")
#    mesh_def.write("VARIABLES = \"x\", \"y\", \"z\",\"d\",")
#    mesh_def.write("\n")
    mesh_def.write("ZONE NODES=")
    mesh_def.write(format(npoint))
    mesh_def.write(", ELEMENTS=")
    mesh_def.write(format(nelem))
    mesh_def.write("\n")
    mesh_def.write(", DATAPACKING=BLOCK, ZONETYPE=FEQUADRILATERAL")
    mesh_def.write("\n")


    #---------writing the points----------------------
    # Write x coordinates.


    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[0]+0.0))
        mesh_def.write("\n")


    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[1]+0.0))
        mesh_def.write("\n")

    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[2]+0.0))
        mesh_def.write("\n")

    for iNode in range(0,npoint):
        mesh_def.write(format(2))
        mesh_def.write("\n")




    #----------writing the elements----------------------

    # Write the element connectivity (1-based).

    for i in range(0,nelem):
        mesh_def.write(format(elemlist[i].g[0]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[1]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[2]))
        mesh_def.write("  ")
        mesh_def.write(format(elemlist[i].g[3]))
        mesh_def.write("\n")



    
    
    mesh_def.close()









