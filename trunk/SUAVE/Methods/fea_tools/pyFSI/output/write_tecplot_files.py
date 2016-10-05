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
    mesh_def.write("VARIABLES = \"x\", \"y\", \"z\", \"thickness\", \"in_stress_von_mises\", \"fin_stress_von_mises\", \"force x\",\"force y\",\"force z\",\"pressure\",")
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



    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].thickness))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].in_stress_von_mises))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].fin_stress_von_mises))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].pressure))
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





#---------------Writing the displacements------------------------------
#----------------------------------------------------------------------

    mesh_def.write("ZONE NODES=")
    mesh_def.write(format(npoint))
    mesh_def.write(", ELEMENTS=")
    mesh_def.write(format(nelem))
#    mesh_def.write("\n")
#    mesh_def.write("VARIABLES = \"x\", \"y\", \"z\",\"d\",\"stress_v_in\",\"stress_v_fin\",")
#    mesh_def.write("\n")
    mesh_def.write(", DATAPACKING=POINT, ZONETYPE=FEQUADRILATERAL")
    mesh_def.write("\n")


#---------writing the points----------------------
# Write x coordinates.



    for i in range(0,npoint):
        mesh_def.write(format(pointlist[i].x[0]+pointlist[i].t[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[1]+pointlist[i].t[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[2]+pointlist[i].t[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].thickness))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].in_stress_von_mises))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].fin_stress_von_mises))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].f[2]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].pressure))
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


    mesh_def.close()


def write_fluid_file_csv(pointlist,file_name,num_points):

    print "Writing output fluid file csv"

    csv_file = open(file_name,"wb")    

    csv_file.write("index,x_coord,y_coord,z_coord,pressure,nearest_index,nearest_x,nearest_y,nearest_z,distance")
    csv_file.write("\n")
    
    for i in range(0,num_points):
        
        csv_file.write(format(pointlist[i].id))
        csv_file.write(", ")       
        csv_file.write(format(pointlist[i].x[0]))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].x[1]))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].x[2]))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].pressure))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].closest_elem_index))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].closest_vector[0]))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].closest_vector[1]))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].closest_vector[2]))
        csv_file.write(", ")
        csv_file.write(format(pointlist[i].closest_dist))
        csv_file.write("\n")

    csv_file.close()





