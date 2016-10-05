#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format

def write_tacs_load_file(pointlist,elemlist,tacs_load_file,node_element_count):

    print "Writing tecplot deformation file"
    
    npoint = len(pointlist)
    nelem =  len(elemlist)
    
    #----orig file-----------------------------------------------
    #-------------------------------------------------------------------
    
    #-----writing the headers-----

    mesh_def = open(tacs_load_file,"wb")
    

    mesh_def.write(format(npoint))
    mesh_def.write(" ")
    mesh_def.write(format(nelem))
    mesh_def.write("\n")
    

        
        
    #---------writing the points----------------------
    # Write x coordinates.
    
    #---write the coordinates and the corresponding force----
    for i in range(0,npoint):
#        mesh_def.write(format(pointlist[i].id))
#        mesh_def.write(" ")
        mesh_def.write(format(pointlist[i].x[0]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist[i].x[1]))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist[i].x[2]))
        
        mesh_def.write(" ")
        mesh_def.write(format(-1.0*pointlist[i].f[0]/float(node_element_count[i])))
        mesh_def.write(" ")
        mesh_def.write(format(-1.0*pointlist[i].f[1]/float(node_element_count[i])))
        mesh_def.write(" ")
        mesh_def.write(format(-1.0*pointlist[i].f[2]/float(node_element_count[i])))
        
        mesh_def.write("\n")
    
    
    #---write the element connectivity of the mesh---------
    for i in range(0,nelem):
#        mesh_def.write(format(elemlist[i].eid))
#        mesh_def.write(" ")
        mesh_def.write(format(elemlist[i].g[0]-1))
        mesh_def.write(" ")
        mesh_def.write(format(elemlist[i].g[1]-1))
        mesh_def.write(" ")
        mesh_def.write(format(elemlist[i].g[2]-1))
        mesh_def.write(" ")
        mesh_def.write(format(elemlist[i].g[3]-1))
        mesh_def.write("\n")

        


    mesh_def.close()










