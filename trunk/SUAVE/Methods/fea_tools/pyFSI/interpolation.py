##@package interpolation
# Consistent and Conservative Interpolation/Extrapolation
##
import re
import numpy as np
import heapq
from scipy.sparse import csr_matrix
from SUAVE.Methods.fea_tools.pyFSI.input.read_bdf_file import read_bdf_file
from SUAVE.Methods.fea_tools.pyFSI.input.read_su2_surface_file_euler import read_su2_surface_file_euler
from SUAVE.Methods.fea_tools.pyFSI.class_str.solution_classes.sol200 import sol200
from SUAVE.Methods.fea_tools.pyFSI.class_str.solution_classes.sol101 import sol101
from SUAVE.Methods.fea_tools.pyFSI.input.read_nas_file import read_nas_file
from SUAVE.Methods.fea_tools.pyFSI.utility_functions.nearest_n_points  import nearest_n_points

## Writes sparse matrix N and nearest-point dx data to ascii format
#
##
def write_N(N,N_list_dx,filename):
    #------open the file-------
    fo = open(filename,"wb")
    fo.write("Extrapolation Matrix\n")
    for i,j,v in zip(N.row, N.col, N.data):
        fo.write( "(%d, %d), %s \n" % (i,j,v))
    fo.write("\n")
    fo.write("Vectors from aero points to nearest point within structural element\n")
    for x in N_list_dx:
        fo.write("%s \n" % x)
    fo.close();

    return 0;

## Writes sparse matrix N and nearest-point dx data to ascii format
#
##
def read_N(filename):
    # N matrix and dx values
    N_list_dx = []
    indptr = [0]
    indices = []
    data = []
    #------open the file-------
    fo = open(filename,"r")
    for line in fo:
        if (line[0:20]=="Extrapolation Matrix"):
            break
    i_temp = 0
    
    for line in fo:
        if (line[0:7] == "Vectors" or line=="\n"):
            break;
        d = re.split('\(| |,|\)|\ |\n| ',line)
        d = filter(None,d)
        i = int(d[0])
        if (i>i_temp ):
            i_temp  = i
            indptr.append(len(indices))
        indices.append(int(d[1]))
        data.append(float(d[2]))
    indptr.append(len(indices))
        
    for line in fo:
        if (line[0:7]=="Vectors"):
            break;
        
    for line in fo:
        if (line =="\n" or line==""):
            break
        d = re.split('\[|\]|\|\n|\ | |\'',line)
        d = filter(None,d)       
        N_list_dx.append(np.array([float(d[0]),float(d[1]),float(d[2]) ]))
        
    fo.close();          

    N_list_dx = np.array(N_list_dx)
    N = csr_matrix((data,indices,indptr),dtype = np.float64).tocoo()

    
    return N,N_list_dx;



## Runs interpolation from su2 to nastran
# file_in: su2 file
# file_out: nastran bdf file to write
# structure_file: nastran file  
##
def fsi_su2_to_nastran(file_in, file_out,structure_file,s101,filetype):

    s101.read_load_file(file_in,filetype)
    #s101.pointlist_fl=s101.pointlist_fl[7500:8000]
    N,N_list_dx = extrap_matrix(s101.pointlist_fl, s101.pointlist, s101.elemlist)
    #write_N(N,N_list_dx,"test.txt")
    #N,N_list_dx = read_N("test.txt")
    extrap_a2s(s101.pointlist_fl,s101.pointlist,s101.elemlist,N_list_dx, N)
    
    s101.compute_nastran_loads()

    s101.write_sol(file_out)
    return 0

## Runs interpolation from su2 to nastran
# file_in: f06 file
# file_out: mesh deformation file to write
# structure_file: previous fluid solution (has mesh info)  
##
def fsi_nastran_to_su2(file_in, file_out,fluid_file,s101):
    #filetype = "su2_euler"
    #s101 = sol101()
#    s101.times = 600
#    s101.sol =101
#    s101.case_control_def=1
#    s101.load_type=1
#    s101.spc_type=1
#    #s101.read_f06(file_in)
#    s101.read_load_file(fluid_file,filetype)

    s101.read_sol(file_in)

    N,N_list_dx = extrap_matrix(s101.pointlist_fl, s101.pointlist)
    extrap_s2a(s101.pointlist_fl,s101.pointlist,s101.elemlist,N_list_dx,N)

    # Write file needed
    s101.write_su2_def(file_out)
    
    return 0


## Calculates vector to closest point on an element
#    Inputs:
#    pt_a: node locations of aero grid point
#    pointlist_s: node locations of structure grid (coarse grid)
#    elemlist_s: element info for structure grid (coarse grid)
#    Output:
#    ind : index of nearest element
#    xj : location of nearest point on element
#    diff : distance to nearest point
##
def closest_point(pt_a,pointlist_s,elemlist_s,dim,map_s,centroids,nearest_n_points_array):
    diff = 0;
    ind =0
    # Closest 10 by centroid location
#    dc = np.array([np.linalg.norm(pt_a.x[:]-centroids[j][:]) for j in range(len(centroids))])
#    dc = np.array(dc)
#    j_list = dc.argsort()[:10]
    #j_list = heapq.nsmallest(10,range(len(dc)),dc.take)
    j_list = [ int() for i in range(10)]
    
    for i in range(0,10):
        j_list[i] = int(nearest_n_points_array[i])
    #j_list = heapq.nsmallest(10,dc)

    #print j_list
    for j in j_list:
        # Number of nodes assc with that element
        nelempt = len(elemlist_s[j].g)
        # Create the matrix [1, x1, y1, z1; 1, x2, y2, z2 ...] for isoparameter
        J = map_s[ elemlist_s[j].g[0:nelempt] ]
        # distance to closest node on element j
        temp2=diff
        for k in range(nelempt):
            temp = np.linalg.norm(pt_a.x[:] - pointlist_s[J[k]].x[:])
            if (k==0 or temp < temp2):
                temp2 = temp
                ind_temp = k


        #.Define the closest point within the element............
        #.Define normal direction to plane defined by 2 vectors..
        
        #v1 = pointlist_s[ J[0] ].x[:]-pointlist_s[ J[1] ].x[:]
        #v2 = pointlist_s[ J[2] ].x[:]-pointlist_s[ J[1] ].x[:]
        # Unit normal vector of element plane
        dx = np.cross(pointlist_s[ J[0] ].x[:]-pointlist_s[ J[1] ].x[:],pointlist_s[ J[2] ].x[:]-pointlist_s[ J[1] ].x[:]) #v1,v2)
        dx = dx/np.linalg.norm(dx) 
        # Vector from aero pt to node 1 on element
        v1 = pt_a.x[:]-pointlist_s[ J[1] ].x[:]
        #......................................................
        #..  v2 = X(i)-x(j), the vector from pt i to xj ......
        #..  xj is the closest point on the element....
        #......................................................
        xj = pt_a.x[:] - dx[:]*np.dot(dx,v1)
        temp = abs(np.dot(dx,v1))
        # Check if xj is outside the element:
        d1 = np.zeros(nelempt)
        d2 = np.zeros(nelempt)
        d3 = np.zeros(nelempt)
        for k in range(nelempt):
            d1[k] = xj[0]-pointlist_s[J[k]].x[0]
            d2[k] = xj[1]-pointlist_s[J[k]].x[1]
            d3[k] = xj[2]-pointlist_s[J[k]].x[2]
        
        # If xj is outside the element..
        if (all(d1<0) or all(d1>0) or all(d2<0) or all(d2>0) or all(d3<0) or all(d3>0)):
            # if distance to nearest node point is an improvement
            if (j==j_list[0] or temp2<diff):
                ind = j
                diff = temp2
                XXj = pointlist_s[J[ind_temp]].x[:]
            # otherwise: reject point
            else:
                temp = diff+1
        
        if (j==j_list[0] or temp <diff):
            diff = temp
            ind = j
            XXj = xj
    return ind, XXj, diff

## Forms matrix (sparse format) for extrapolation.
#
#    Inputs:
#    pointlist_a: node locations of aero grid (fine grid)
#    pointlist_s: node locations of structure grid (coarse grid)
#    elemlist_s: element info for structure grid (coarse grid)
#    Outputs:
#    N:
#    N_list_i: indices of nodes on closest elem. {n1, n2,n3,n4} 
#    N_list_val: values of isoparam. on closest elm. {e1,e2...}
#    N_list_dx: distance from pt i to closet pt on closest elm.
#    N: Sparse compressed row matrix
##
def extrap_matrix(pointlist_a,pointlist_s, elemlist_s) : 
    na = len(pointlist_a) # Number of points in fluid grid (fine)
    ns = len(pointlist_s) # Number of points in structure grid (coarse)
    es = len(elemlist_s) # Number of elements in structure grid (coarse)
    diff = 0.0
    dim = len(pointlist_a[0].x[:])
    dx = np.zeros(dim)

    # N matrix and dx values
    N_list_dx = np.zeros((na,3))
    indptr = [0]
    indices = []
    data = []
    
    print "pointlist_s[0].id = ", pointlist_s[0].id
    
    # Create map from point id to point index
    max_id = max(pointlist_s[i].id for i in range(ns))
    print "max_id = ", max_id
    map_s = np.int_(np.zeros(max_id+1))
    for i in range(ns):
        map_s[pointlist_s[i].id] =  int(i)
    # Calculate Element Centroids
    centroids = find_centroids(elemlist_s, pointlist_s,map_s)

    #call the nearest n point computation - added by anil
    nearest_n_points_arrays =  3
    nearest_n_points_array = nearest_n_points(pointlist_a,centroids,nearest_n_points_arrays,10)


    #Find the closest element.
    for i in range(na):
        if ( i % 100 == 0 ):
            print i, " out of " , na, " fluid points. "

        # Find closest element
        ind, xj, diff = closest_point(pointlist_a[i],pointlist_s,elemlist_s,dim,map_s,centroids,nearest_n_points_array[i])

        #*****MODIFIED BY PAUL U*****
        pointlist_a[i].closest_elem_index = ind
        pointlist_a[i].closest_vector[0] = xj[0]
        pointlist_a[i].closest_vector[1] = xj[1]
        pointlist_a[i].closest_vector[2] = xj[2]
        pointlist_a[i].closest_dist = diff
        #*****END PAUL U MOD*****

        # Number of nodes assc with that element
        nelempt = len(elemlist_s[ind].g)
        # Create the matrix [1, x1, y1, z1; 1, x2, y2, z2 ...] for isoparameter
        x_temp=np.zeros((nelempt,dim))
        #........Loop over nodes on the closest element.................
        j=0
        for gi in  elemlist_s[ind].g:
            x_temp[j,:] = pointlist_s[ map_s[ gi ] ].x[:]
            j+=1
        #......................................................
        #. Solve for the isoparametric representation of xj.......
        #......................................................
        e_temp = isoparam( nelempt, x_temp, xj)
        #......................................................
        #. Correct for points outside the element.................
        #. by finding the closest boundary........................    
        #......................................................    
        etol = 3. # Tolerance on the e values (far from the element the interpolation equations are not valid)
        if ( any(abs( e_temp )>etol) ):
            diff = np.zeros( nelempt )
            #..Find the closest point.........................    
            for k in range(nelempt):
                dx = np.zeros(3)
                j = map_s[ elemlist_s[ind].g[k] ] 
                dx = pointlist_s[j].x[:]- pointlist_a[i].x[:]
                diff[k] = np.dot(dx,dx) # No need for square root here.
            ind2 = np.argmin( diff )
            k = map_s[ elemlist_s[ind].g[ind2] ] 

            xj = pointlist_s[k].x[:] # closest pt loc.
            e_temp = np.zeros(4)
            e_temp[ind2] = 1.
            diff = np.zeros(es)
        #......................................................
        #.. Fill in the N matrix entries..........................
        #..   N_list: {indices of up to 4 closest nodes}(-1 =skip)..
        #..   N_list_val: {isoparametric values for those nodes}..
        #..   N_list_dx: vector from point i to xj ...............
        #..    xj is defined by the isoparametric representation..
        #......................................................
        for k in range( nelempt ):
            indices.append(np.int_(map_s[ elemlist_s[ind].g[k] ]))
            data.append( e_temp[k] )
        indptr.append(len(indices))            
        
        N_list_dx[i,:] =pointlist_a[i].x[:]- xj

    N = csr_matrix((data,indices,indptr),dtype = np.float64).tocoo()
    return N, N_list_dx




## aero to structural consistent extrapolation
#
#    Inputs:
#    pointlist_a: aero node locations are in pointlist_a[i].x[0:2]
#    pointlist_s: struct node locations
#    elemlist_s: elemnt info 
#    N: extrapolation matrix:
#        N_list_i,N_list_val, N_list_dx
#    Outputs:
#    pointlist_s updated with forces
# NOTE: future version should include moment calculation as well
##
def extrap_a2s(pointlist_a,pointlist_s,elemlist_s,N_list_dx,N):
    #..........................................................
    #.Loop over points to solve for forces and moments.........
    #..........................................................
    # Zero out the forces stored in the structure pointlist
    for i in range(len(pointlist_s)):
        pointlist_s[i].f = [0.0,0.0,0.0]
        #pointlist_s[i].moment[:] = 0
    
    # Loops over sparse matrix info 
    for (i,j,w) in zip(N.row, N.col, N.data):
        # Used for moment calc (not included yet)
        #dx = N_list_dx[i,0]
        #dy = N_list_dx[i,1]
        #dz = N_list_dx[i,2]
        pointlist_s[j].f = pointlist_s[j].f + pointlist_a[i].f*w


    return 0


## This function extrapolates structural deformations to the points of a finer grid. 
#
#    Inputs:
#    pointlist_a: aero node locations are in pointlist_a[i].x[0:2]
#    pointlist_s: struct node locations
#    elemlist_s: elemnt info 
#    N: extrapolation matrix:
#        N_list_i,N_list_val, N_list_dx
#    Outputs:
#    pointlist_a updated with deformations
##
def extrap_s2a(pointlist_a,pointlist_s,elemlist_s,N_list_dx,N): #(ax,sx,se,s_dx,a_dx):
    #...........................................................
    #Calculate deformations.....................................
    #...........................................................

    for (i,j,w) in zip(N.row, N.col, N.data):
        dx = N_list_dx[i,0]
        dy = N_list_dx[i,1]
        dz = N_list_dx[i,2]
        #..........Add the cross product of rotation and distance
        pointlist_a[i].t[0] += w*(dz*pointlist_s[j].r[1] -dy*pointlist_s[j].r[2])
        pointlist_a[i].t[1] += w*(-dz*pointlist_s[j].r[0] +dx*pointlist_s[j].r[2])
        pointlist_a[i].t[2] += w*(dy*pointlist_s[j].r[0] -dx*pointlist_s[j].r[1])
        #..........Add the displacement of xj
        pointlist_a[i].t+=pointlist_s[j].t*w

        #..........Add the rotation of xj
        pointlist_a[i].r+=pointlist_s[j].r*w  
              
    return 0

## A helper function
def  find_centroids(elemlist_s, pointlist_s,map_s):
    # map_s[j] = i, where pointlist_s[i].id = j
    #..........................................................
    #.........Now need to fill in the centroid locations.......
    #..........Note: node list may skip #s, so must use........
    #..........stored node index ids...........................
    #..........................................................

    dims = len(pointlist_s[0].x[:]) # Number of dimensions
    ns = len(elemlist_s)
    centroids = np.zeros((ns,dims)) # Initialize centroids
    # Loop over Elements
    for i in range(ns):
        npts = len(elemlist_s[i].g)
        div = 1./npts
        for k in range(npts):
            j = map_s[ elemlist_s[i].g[k] ] # j = kth point on element i
            #centroids[i,:]+=pointlist_s[j].x[:]*div      
            for m in range(dims):
                centroids[i,m]+=pointlist_s[j].x[m]*div        

    return centroids

## Finds isoparametric coordinates for 3 or 4 node elm.
#
#    Inputs:
#    n: number of boundary nodes (3 or 4)
#    x: an nx4 matrix filled with 1s and node coordinates
#    xj: the point to parameterize
#    Outputs:
#    e: the output parameterized coordinates
#    
#===============================================================
#    Solves:
#        xj = x * e
#    for e
##
def isoparam(n,x,xj):
    tol = 1e-16
    s = 4
    b = [False]*3
    #...........................................................
    #.Loop over dimensions 1-3 to check if any are lost........
    #.  (aka, if all z coordinates are identical, reduce dim)..
    #...........................................................
    for k in range(3):
        b[k] = (x[0,k] == x[1,k])
        if (n>=3): b[k]=(b[k] and (x[0,k]==x[2,k]) )
        if (n>=4): b[k]=(b[k] and (x[0,k]==x[3,k]) )
        if (b[k]): s = s-1
    #...........................................................
    #.Copy non-degenerate rows.................
    #...........................................................

    e = np.zeros(n)
    M = np.zeros((n,s))
    xj2 = np.zeros(s)
    M[:,0] = 1
    xj2[0]=1
    i=1
    for k in range(3):
        if (not b[k]):
            M[:,i] = x[0:n,k]
            xj2[i] = xj[k]
            i+=1
    #..................
    # Check for coincident point
    #....................
    b[0]=False
    for i in range(n):
        dx = M[i,1:]-xj2[1:]
        t1 = np.dot(dx,dx)
        # WARNING: Hard-coded tolerance
        if (t1 < (tol)):
            print "Point less than ", tol, " from element node"
            e[:]=0
            e[i]=1
            b[0]=True
    
    if not b[0]:  
        #...........................................................
        #Use QR decomposition to solve for e.......................
        #..........................................................    
        Q,R = np.linalg.qr(M.T) 
        t2 = np.dot(Q.T,xj2)
        try:
            e2 = np.linalg.lstsq(R,t2)[0] # solve_triangular
            e = e2[0:n]
          
        except np.linalg.linalg.LinAlgError:
            print "singular matrix error; taking nearest point"        
            e = np.zeros(n)
            t1 = np.zeros(n)
            for i in range(n):
                dx = M[i,1:] - xj2[1:]
                t1[i] = np.dot(dx,dx)
            min_id = np.argmin(t1)
            e[min_id] = 1.0
        
    return e


#def smallest(nos,val):
#    smallest_n = np.zeros(nos)
#    smallest_n = val(
#    for i in range(0,len(val)):
		





