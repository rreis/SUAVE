#
# Created:  Oct 2015, Anil Variyar
# Modified: May 2016, Anil Variyar
#
#-----------
#---function to convert integers to required nastran format

def write_su2_deformation_file(pointlist,su2_def_file):

    print "Writing su2 deformation file"

    mesh_def = open(su2_def_file,"wb")

    for i in range(0,len(pointlist)):
        
        mesh_def.write(format(pointlist[i].global_to_loc-1))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist[i].x[0]+pointlist[i].t1))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist[i].x[1]+pointlist[i].t2))
        mesh_def.write(" ")
        mesh_def.write(format(pointlist[i].x[2]+pointlist[i].t3))
        mesh_def.write("\n")

    mesh_def.close()








