#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
def write_aero_panel_mesh(elemlist,pointlist,wake_boundary,filename,wake_compute):
    
    mesh_def = open(filename,"wb")
    mesh_def.write(format(len(pointlist)))
    mesh_def.write("\n")
    mesh_def.write(format(len(elemlist)))
    mesh_def.write("\n")
    
    if (wake_compute==1):
        mesh_def.write(format(len(wake_boundary)))
        mesh_def.write("\n")

    for i in range(0,len(pointlist)):
        
        mesh_def.write(format(pointlist[i].x[0]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[1]))
        mesh_def.write("\t")
        mesh_def.write(format(pointlist[i].x[2]))
        mesh_def.write("\n")
    
    
    for i in range(0,len(elemlist)):
        for j in range(0,4):
            mesh_def.write(format(elemlist[i].g[j]-1))
            mesh_def.write("\t")
        mesh_def.write("\n")



    if (wake_compute==1):

        for i in range(0,len(wake_boundary)):
            for j in range(0,2):
                mesh_def.write(format(wake_boundary[i].g[j]-1))
                mesh_def.write("\t")
            
            mesh_def.write(format(wake_boundary[i].upper))
            mesh_def.write("\t")
            mesh_def.write(format(wake_boundary[i].lower))
            mesh_def.write("\n")

    
    
    mesh_def.close()
    
    print "Done writing the aero panel mesh"