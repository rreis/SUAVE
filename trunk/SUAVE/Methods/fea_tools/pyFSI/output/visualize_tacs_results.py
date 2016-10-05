#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format

def visualize_tacs_results(pointlist,elemlist,tecplot_file_orig):

    print "Writing tecplot deformation file"
    
    
    #----orig file-----------------------------------------------
    #-------------------------------------------------------------------
    
    #-----writing the headers-----

    mesh_def = open(tecplot_file_orig,"wb")
    
    #---------writing the points----------------------
    # Write x coordinates.
    
    mesh_def.write("TITLE = \"Visualization of CSM meshes\"")
    mesh_def.write("\n")
    mesh_def.write("VARIABLES = \"x\", \"y\", \"z\", \"thickness\", \"force x\",\"force y\",\"force z\",\"dx\", \"dy\", \"dz\", \"sx0\", \"sy0\",\"sxy0\",\"sx1\",\"sy1\",\"sxy1\",\"syz0\", \"sxz0\",")
    mesh_def.write("\n")
    mesh_def.write("ZONE NODES=")
    mesh_def.write(format(npoint))
    mesh_def.write(", ELEMENTS=")
    mesh_def.write(format(nelem))
    #    mesh_def.write("\n")
    mesh_def.write(", DATAPACKING=POINT, ZONETYPE=FEQUADRILATERAL")
    mesh_def.write("\n")
    
    
    
    for i in range(0,len(pointlist)):
        mesh_def.write(format(pointlist[i].x[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].thickness))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].t[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].t[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].t[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[3]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[4]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[5]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[6]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[7]))
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

#---------------Writing the displacements------------------------------
#----------------------------------------------------------------------

    mesh_def.write("ZONE NODES=")
    mesh_def.write(format(npoint))
    mesh_def.write(", ELEMENTS=")
    mesh_def.write(format(nelem))
    mesh_def.write(", DATAPACKING=POINT, ZONETYPE=FEQUADRILATERAL")
    mesh_def.write("\n")
    
    
    #---------writing the points----------------------
    # Write x coordinates.
    
    for i in range(0,len(pointlist)):
        mesh_def.write(format(pointlist[i].x[0]+pointlist[i].t[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[1]+pointlist[i].t[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[2]+pointlist[i].t[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].thickness))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].t[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].t[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].t[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[3]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[4]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[5]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[6]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].s[7]))
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


    mesh_def.close()









