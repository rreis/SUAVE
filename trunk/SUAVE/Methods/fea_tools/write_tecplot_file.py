# gwrite_tecplot_file.py
#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format

def write_tecplot_file(pointlist,elemlist,tecplot_file_orig,npoint,nelem):

    print "Writing tecplot deformation file"
    tecplot_stress_file = 'stress_file.plt'
    
    #----orig file-----------------------------------------------
    #-------------------------------------------------------------------
    
    #-----writing the headers-----

    mesh_def = open(tecplot_file_orig,"wb")
    
    mesh_def.write("TITLE = \"Visualization of CSM meshes\"")
    mesh_def.write("\n")
    #mesh_def.write("VARIABLES = \"x\", \"y\", \"z\", \"thickness\", \"in_stress_von_mises\", \"fin_stress_von_mises\", \"force x\",\"force y\",\"force z\",\"pressure\",")
    
    mesh_def.write("VARIABLES = \"x\"  \"y\"  \"z\" ")
    mesh_def.write("\n")
    mesh_def.write("\n")
    mesh_def.write("ZONE")
    mesh_def.write("\n")
    mesh_def.write("T=\"Zone Title\"")
    mesh_def.write("\n")
    mesh_def.write("DATAPACKING=Block")
    mesh_def.write("\n")
    mesh_def.write("ZONETYPE=FEQUADRILATERAL")
    mesh_def.write("\n")
    mesh_def.write("N=")
    mesh_def.write(format(npoint))
    mesh_def.write(" E=")
    mesh_def.write(format(nelem))
    mesh_def.write("\n")
        
        
    #---------writing the points----------------------
    # Write x coordinates.



    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[0]))
        if((i%4 == 0) and (i != 0)):
            mesh_def.write("\n")
        else:
            mesh_def.write("\t")

    mesh_def.write("\n")
        
        
    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[1]))
        if((i%4 == 0) and (i != 0)):
            mesh_def.write("\n")
        else:
            mesh_def.write("\t")
    mesh_def.write("\n")

        
    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[2]))
        if((i%4 == 0) and (i != 0)):
            mesh_def.write("\n")
        else:
            mesh_def.write("\t")

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
        if(elemlist[i].type=='CTRIA3'):
            
            mesh_def.write(format(elemlist[i].g[2]))
            mesh_def.write("\n")
    
        if(elemlist[i].type=='CQUAD4'):
            
            mesh_def.write(format(elemlist[i].g[3]))
            mesh_def.write("\n")





