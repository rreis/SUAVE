##@package interpolation_xis
# For now: uses list.x1, list.x2 etc format. Another version will use list.x[:] format
##
import numpy as np
import scipy as sp
import scipy.sparse


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
##
def extrap_matrix(pointlist_a,pointlist_s, elemlist_s) : 
    #Allocate the arrays to hold the transfer functions.
    na = len(pointlist_a) # Number of points in fluid grid (fine)
    ns = len(pointlist_s) # Number of points in structure grid (coarse)
    es = len(elemlist_s) # Number of elements in structure grid (coarse)
    ind = 0
    ind2 = np.zeros(4)
    diff = np.zeros(es)
    # Construct empty sparse matrix
    #N = sp.sparse.coo_matrix( (na,ns) ) Alternative for storing _val and _i
    N_list_i = np.zeros((na,4))
    N_list_val = np.zeros((na,4))
    N_list_dx = np.zeros((na,3))

    #Calculate N1 components.

    # Create map from point id to point index
    max_id = max(pointlist_s[i].id for i in range(ns))
    map_s = np.int_(np.zeros(max_id+1))
    for i in range(ns):
        map_s[pointlist_s[i].id] =  int(i)
    # Calculate Element Centroids
    centroids = find_centroids(elemlist_s, pointlist_s,map_s)

    #Find the closest element.
    for i in range(na):
        print i, " out of " , na, " fluid points. "
        for j in range(es):
        #    for k in range(0,2):
        #        dx[k] = pointlist_a[i].x[k]-centroids[j,k]
            dx = np.zeros(3)
            dx[0] = pointlist_a[i].x1-centroids[j,0]
            dx[1] = pointlist_a[i].x2-centroids[j,1]
            dx[2] = pointlist_a[i].x3-centroids[j,2]
            diff[j] = np.dot(dx,dx)

        ind = np.argmin(diff)

        if elemlist_s[i].type == 'CTRIA3':
            nelempt = 3
        elif elemlist_s[i].type == 'CQUAD4':
            nelempt = 4

        x_temp=np.zeros((nelempt,4))
        x_temp[:,0] = 1
        #........Loop over nodes on the closest element.................
        #for j in range( nelempt ): # number of nodes on the element
        #    # copy the x location of the jth node of the closest element
        #    #for k in range(3):           
        #    #    # kth dimension of jth point on the element 
        #    #    x_temp[j,1+k] = pointlist_s[map_s[ elemlist_s[ind].g[j] ]].x[k] 
        x_temp[0,1] = pointlist_s[map_s[ elemlist_s[ind].g1 ]].x1
        x_temp[0,2] = pointlist_s[map_s[ elemlist_s[ind].g1 ]].x2
        x_temp[0,3] = pointlist_s[map_s[ elemlist_s[ind].g1 ]].x3

        x_temp[1,1] = pointlist_s[map_s[ elemlist_s[ind].g2 ]].x1
        x_temp[1,2] = pointlist_s[map_s[ elemlist_s[ind].g2 ]].x2
        x_temp[1,3] = pointlist_s[map_s[ elemlist_s[ind].g2 ]].x3

        x_temp[2,1] = pointlist_s[map_s[ elemlist_s[ind].g3 ]].x1
        x_temp[2,2] = pointlist_s[map_s[ elemlist_s[ind].g3 ]].x2
        x_temp[2,3] = pointlist_s[map_s[ elemlist_s[ind].g3 ]].x3
        if (nelempt >= 4):
            x_temp[3,1] = pointlist_s[map_s[ elemlist_s[ind].g4 ]].x1
            x_temp[3,2] = pointlist_s[map_s[ elemlist_s[ind].g4 ]].x2
            x_temp[3,3] = pointlist_s[map_s[ elemlist_s[ind].g4 ]].x3
        #.Define the closest point within the element............
        #.Define normal direction to plane defined by 2 vectors..
        v1 = np.zeros(3)
        v2 = np.zeros(3)
        j0 = map_s[ elemlist_s[ind].g1]#[0] ] 
        j1 = map_s[ elemlist_s[ind].g2]#[1] ]
        j2 = map_s[ elemlist_s[ind].g3]#[2] ]
        #for k in range(3):
        #    v1[k] = pointlist_s[ j0 ].x[k]-pointlist_s[ j1 ].x[k]
        #    v2[k] = pointlist_s[ j2 ].x[k]-pointlist_s[ j1 ].x[k]
        v1[0] = pointlist_s[ j0 ].x1-pointlist_s[ j1 ].x1
        v2[0] = pointlist_s[ j2 ].x1-pointlist_s[ j1 ].x1    
        v1[1] = pointlist_s[ j0 ].x2-pointlist_s[ j1 ].x2
        v2[1] = pointlist_s[ j2 ].x2-pointlist_s[ j1 ].x2
        v1[2] = pointlist_s[ j0 ].x3-pointlist_s[ j1 ].x3
        v2[2] = pointlist_s[ j2 ].x3-pointlist_s[ j1 ].x3

        #call unitnormvec(v1,v2,dx)        
        dx = np.cross(v1,v2)
        dx = dx/np.linalg.norm(dx)

        #for k in range(3):
        #    v1[k] = pointlist_a[i].x[k]-pointlist_s[ j1 ].x[k]
        v1[0] = pointlist_a[i].x1-pointlist_s[ j1 ].x1
        v1[1] = pointlist_a[i].x2-pointlist_s[ j1 ].x2
        v1[2] = pointlist_a[i].x3-pointlist_s[ j1 ].x3

        temp = np.dot(dx,v1)
        #call dot_prod(dx,v1,temp)
        #......................................................
        #..  v2 = X(i)-x(j), the vector from pt i to xj ......
        #..  xj is the closest point on the closest element....
        #......................................................
        v2 = dx*temp
        xj = [pointlist_a[i].x1 - v2[0],pointlist_a[i].x2 - v2[1],pointlist_a[i].x3 - v2[2]]  #pointlist_a[i].x[:] - v2 

        #......................................................
        #. Solve for the isoparametric representation of xj.......
        #......................................................
        #nelempt = len( elemlist_s[ind].g) # Number of points in the element

        e_temp = isoparam( nelempt, x_temp, xj)
        #......................................................
        #. Correct for points outside the element.................
        #. by finding the closest boundary........................    
        #......................................................    
        etol = 3. # Tolerance on the e values
        if ( any(abs( e_temp )>etol) ):
            diff = np.zeros( nelempt )
            #..Find the closest point.........................    
            for k in range(nelempt):
                dx = np.zeros(3)
                #j = map_s[ elemlist_s[ind].g[k] ] #int(se(k+4,ind(1)))
                if (k==0):
                    j = map_s[ elemlist_s[ind].g1 ]
                elif (k==1):
                    j = map_s[ elemlist_s[ind].g2 ]
                elif (k==2):
                    j = map_s[ elemlist_s[ind].g3 ]
                elif (k==3):
                    j = map_s[ elemlist_s[ind].g4 ]

                #dx[0] = pointlist_s[j].x[0] -pointlist_a[i].x[0]
                #dx[1] = pointlist_s[j].x[1] -pointlist_a[i].x[1]
                #dx[2] = pointlist_s[j].x[2] -pointlist_a[i].x[2]
                dx[0] = pointlist_s[j].x1 -pointlist_a[i].x1
                dx[1] = pointlist_s[j].x2 -pointlist_a[i].x2
                dx[2] = pointlist_s[j].x3 -pointlist_a[i].x3
                diff[k] = np.linalg.norm(dx) #np.sqrt(np.dot(dx,dx))
            ind2 = np.argmin( diff )
            if (ind2==0):
                k = map_s[ elemlist_s[ind].g1 ]
            elif (ind2==1):
                k = map_s[ elemlist_s[ind].g2 ]
            elif (ind2==2):
                k = map_s[ elemlist_s[ind].g3 ]
            elif (ind2==3):
                k = map_s[ elemlist_s[ind].g4 ]
            #k = map_s( elemlist_s[ind].g[ind2] ) #int( se[3+ind2,ind ] )
            xj = [pointlist_s[k].x1,pointlist_s[k].x2 ,pointlist_s[k].x3 - v2[2]]  
            #xj = pointlist_s[k].x[:] #sx[0:2,k] #! closest pt loc.
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
        N_list_i[i,:] = -1
        if nelempt <4:
            elmlst = [ elemlist_s[ind].g1, elemlist_s[ind].g2,elemlist_s[ind].g3]
        else:
            elmlst = [ elemlist_s[ind].g1, elemlist_s[ind].g2,elemlist_s[ind].g3,elemlist_s[ind].g4]
        for k in range( nelempt ):
            N_list_i[i,k] = map_s[ elmlst[k] ] #map_s[ elemlist_s[ind].g[k] ] #int( se(k+3,ind(1)) )
            N_list_val[i,k] = e_temp[k]
        N_list_dx[i,:] = [pointlist_a[i].x1- xj[0], pointlist_a[i].x2- xj[1], pointlist_a[i].x3- xj[2] ] #pointlist_a[i].x[:]- xj
    return N_list_i, N_list_val, N_list_dx




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
##
def extrap_a2s(pointlist_a,pointlist_s,elemlist_s,N_list_i,N_list_val,N_list_dx):
    na = len(pointlist_a)    # number of nodes (aero)
    #..........................................................
    #.Loop over points to solve for forces and moments.........
    #..........................................................
    # Zero out the forces stored in the structure pointlist
    for i in range(len(pointlist_s)):
        #pointlist_s[i].f[:] = 0
        pointlist_s[i].f1 = 0
        pointlist_s[i].f2 = 0
        pointlist_s[i].f3 = 0
        #pointlist_s[i].moment[:] = 0

    for i in range(na):
        dx = N_list_dx[i,0]
        dy = N_list_dx[i,1]
        dz = N_list_dx[i,2]
        # Loop over points of the nearest element
        for k in range(3):
            j = np.int_( N_list_i[i,k])
            if (j>=0):
                w = N_list_val[i,k]
                #pointlist_s[j].f[0:2] = pointlist_s[j].f[0:2] + pointlist_a[i].f[0:2]*w
                pointlist_s[j].f1 += pointlist_a[i].f1*w
                pointlist_s[j].f2 += pointlist_a[i].f2*w
                pointlist_s[j].f3 += pointlist_a[i].f3*w
                # Moment support not yet added
                #pointlist_s[j].moment[0:2] = pointlist_s[j].moment[0:2] + pointlist_a[i].moment[0:2]*w
                #pointlist_s[j].moment1 += pointlist_a[i].moment1*w
                #pointlist_s[j].moment2 += pointlist_a[i].moment2*w
                #pointlist_s[j].moment3 += pointlist_a[i].moment3*w
                    #..........Add the cross product of force and distance...
                #pointlist_s[j].moment[0]=pointlist_s[j].moment[0]-w*(dz*pointlist_a[i].f[1]-dy*pointlist_a[i].f[2])
                #pointlist_s[j].moment[1]=pointlist_s[j].moment[1]-w*(dx*pointlist_a[i].f[2]-dz*pointlist_a[i].f[0])
                #pointlist_s[j].moment[2]=pointlist_s[j].moment[2]-w*(dy*pointlist_a[i].f[0]-dx*pointlist_a[i].f[1])

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
def extrap_s2a(pointlist_a,pointlist_s,elemlist_s,N_list_i,N_list_val,N_list_dx): #(ax,sx,se,s_dx,a_dx):
    #...........................................................
    #Calculate deformations.....................................
    #...........................................................
    na = len(pointlist_a)
    for i in range(na):
        dx = N_list_dx[i,0]
        dy = N_list_dx[i,1]
        dz = N_list_dx[i,2]
        for k in range(4):
            j = np.int_(N_list_i[i,k])
            if (j!=-1): # "-1" is a filler value indicating no node (aka, there are only three nodes attached)
                w = N_list_val[i,k]
                #..........Add the cross product of rotation and distance
                pointlist_a[i].t1 += w*(dz*pointlist_s[j].r2 -dy*pointlist_s[j].r3)
                pointlist_a[i].t2 += w*(-dz*pointlist_s[j].r1 +dx*pointlist_s[j].r3)
                pointlist_a[i].t3 += w*(dy*pointlist_s[j].r1 -dx*pointlist_s[j].r2)
                #a_dx(1,i)=a_dx(1,i)+(dz*s_dx(5,j)-dy*s_dx(6,j))*w
                #a_dx(2,i)=a_dx(2,i)+(-dz*s_dx(4,j)+dx*s_dx(6,j))*w
                #a_dx(3,i)=a_dx(3,i)+(dy*s_dx(4,j)-dx*s_dx(5,j))*w

                #..........Add the displacement of xj
                #a_dx(1:3,i) = a_dx(1:3,i) + s_dx(1:3,j)*w
                pointlist_a[i].t1+= pointlist_s[j].t1*w
                pointlist_a[i].t2+= pointlist_s[j].t2*w
                pointlist_a[i].t3+= pointlist_s[j].t3*w
        
                #..........Add the rotation of xj
                pointlist_a[i].r1 += pointlist_s[j].r1*w
                pointlist_a[i].r2 += pointlist_s[j].r2*w
                pointlist_a[i].r3 += pointlist_s[j].r3*w
                #if (size(a_dx,1).eq.6) then
                #    a_dx(4:6,i) = a_dx(4:6,i) + s_dx(4:6,j)*w

    return 0

## A helper function
def  find_centroids(elemlist_s, pointlist_s,map_s):
    # map_s[j] = i, where pointlist_s[i].id = j
    #..........................................................
    #.........Now need to fill in the centroid locations.......
    #..........Note: node list may skip #s, so must use........
    #..........stored node index ids...........................
    #..........................................................

    dims = 3 #len(pointlist_s[0].x[:]) # Number of dimensions
    centroids = np.zeros((len(elemlist_s),dims)) # Initialize centroids
    # Loop over Elements
    for i in range(len(elemlist_s)-1):
        # Loop over points in element i
        #npts = len(elemlist_s[i].g)
        if elemlist_s[i].type == 'CTRIA3':
            npts = 3
        elif elemlist_s[i].type == 'CQUAD4':
            npts = 4
        for k in range(npts):
            #j = map_s[elemlist_s[i].g[k]] # j = kth point on element i 
            if (k==0):
                j = map_s[ elemlist_s[i].g1 ]
            elif (k==1):
                j = map_s[ elemlist_s[i].g2 ]
            elif (k==2):
                j = map_s[ elemlist_s[i].g3 ]
            elif (k==3):
                j = map_s[ elemlist_s[i].g4 ]

            centroids[i,0]+=pointlist_s[j].x1/npts            
            centroids[i,1]+=pointlist_s[j].x2/npts            
            centroids[i,2]+=pointlist_s[j].x3/npts            
            #for m in range(dims):
            #    centroids[i,m]+=pointlist_s[j].x[m]/npts

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
    s = 4
    b = [False]*3
    #...........................................................
    #.Loop over dimensions 1-3 to check if any are lost........
    #.  (aka, if all z coordinates are identical, reduce dim)..
    #...........................................................
    for k in range(1,4):
        b[k-1] = (x[0,k] == x[1,k])
        if (n>=3): b[k-1]=(b[k-1] and (x[0,k]==x[2,k]) )
        if (n>=4): b[k-1]=(b[k-1] and (x[0,k]==x[3,k]) )
        if (b[k-1]): s = s-1
    #...........................................................
    #.Copy non-degenerate rows.................
    #...........................................................
    if (n > s):
        n = s
    M = np.zeros((n,s))
    xj2 = np.zeros(s)
    M[:,0] = np.ones(n)
    xj2[0] = 1
    i=1
    for k in range(3):
        if (not b[k]):
            M[:,i] = x[0:n,k+1]
            xj2[i] = xj[k]
            i+=1

    #...........................................................
    #Use QR decomposition to solve for e.......................
    #..........................................................    
    Q,R = np.linalg.qr(M.T) 
    t2 = np.dot(Q.T,xj2)
    try:
        e2 = np.linalg.solve(R,t2) # solve_triangular
        e = e2[0:n]
        for i in range(n):
            dx = M[i,1:]-xj2[1:]
            t1 = np.dot(dx,dx)
            if (t1 < (1e-8)):
                e[:]=0
                e[i]=1        
    except np.linalg.linalg.LinAlgError as err:
        print "singular matrix error; taking nearest point"         
        e = np.zeros(n)
        t1 = np.zeros(n)
        for i in range(n):
            dx = M[i,1:] - xj2[1:]
            t1[i] = np.dot(dx,dx)
        min_id = np.argmin(t1)
        e[min_id] = 1.0
        
    return e

