# -*- coding: utf-8 -*-
"""
Course: ME/MF F342 Computer Aided Design
Proffessor: Dr. Murali Palla

Submitted by: Bhavya Bhatia
Date: April 28, 2021

Topic: Computational Geometry Boolean Operations

Instructions:
-------------

"""

STUDENT_NAME='BHAVYA BHATIA'
STUDENT_ID='2018A4PS0846P'

import numpy as np
import sympy as simp


VL=np.array([[0,0],[4,0],[4,4],[0,4]])
VL2=np.array([[8,2],[5,1],[5,3]])



# section 1: it contains all the helper functions
############################################################################
############################################################################

def intersect(a,b,c,d):

    try:
        A = np.array([  [ (b[0]-a[0]) , (c[0]-d[0]) ],
                        [ (b[1]-a[1]) , (c[1]-d[1]) ]])

        B = np.array([(c[0]-a[0]) , (c[1]-a[1])])

        C = np.linalg.solve(A, B)
    except Exception as e:
        #print(e)

        return ([float("NaN"),float("NaN")])


    
    u = (C[0])
    v = (C[1])

    x = a[0]*(1-u) + b[0]*u
    y = a[1]*(1-u) + b[1]*u

    #print(u,v)

    if(0<=u<=1 and  0<=v<=1):
        p = ([x,y])
    else:
        p  = ([float("NaN"),float("NaN")])

    #print(p)

    return p


# helper function to check if two segments intersect
def isIntersect(segment1,segment2):
    # points of segment 1
     
    a = np.asarray(segment1[0])
    b = np.asarray(segment1[1])
    #points of segment 2
    c = np.asarray(segment2[0])
    d = np.asarray(segment2[1])


    p = intersect(a,b,c,d)

    
    if(np.all(np.isnan(p))):
        return False

    
    return True

'''
    Alternate Implementationn : 

    # updating points to make p2,p3,p4 vectors
    p2 = p2-p1
    p3 = p3-p1
    p4 = p4-p1

    # if cross product of p2,p3 and p2,p4 have same sign then the segments dont intersect else they do
    if((np.cross(p2,p3) > 0 and np.cross(p2,p4) >0) or (np.cross(p2,p3) < 0 and np.cross(p2,p4) <0) ):
        return False

    elif((np.cross(p2,p3) < 0 and np.cross(p2,p4) >0) or (np.cross(p2,p3) > 0 and np.cross(p2,p4) <0) ):
        return True
    else:
        if(np.cross(p2,p3) == 0):
            if(p2[0]<p3[0] and p2[1]<p3[1]):
                return False
            else:
                return True
            
        if(np.cross(p2,p4) == 0):
            if(p2[0]<p4[0] and p2[1]<p4[1]):
                return False
            else:
                return True
    '''          

# helper function to check if two consecutive line segments are left rotated or right
def leftOrRight(p0,p1,p2):
    p1 = p1-p0
    p2 = p2-p0

    if(np.cross(p1,p2) > 0 ):
        return 1
    else:
        return -1

#helper to get intersecting points 
def intersectingPoints(VL1, VL2):

    arr = []
    i=0
    while i<len(VL1):
        j=0
        while j< len(VL2):
            p = intersect(VL1[i], VL1[(i+1)%len(VL1)] , VL2[j], VL2[(j+1)%len(VL2)])
           
            if (not(np.all( np.isnan(p) )) ):
                arr.append(p)
            
            j+=1
        i+=1

  
    return arr

#helper to order points so that it can be plotted as a polygon
def orderPoints(VL):

    if(len(VL) ==0 ):
        return []
    # calculate the center points 
    centerX =0
    centerY = 0
    for point in VL:
        centerX += point[0]
        centerY += point[1]
    
    centerX /= len(VL)
    centerY /= len(VL)

    

    def mykey(p):
        a = np.arctan2(p[0] - centerX ,p[1] - centerY)
        
        return -a
    
 
    VL = sorted(VL, key= mykey )

    return np.asarray(VL)


# section 2: it contains all the Final functions
########################################################################
########################################################################

def check_simplepolygon(VL):
    '''
    Parameters
    ----------
    VL : An sequence of vertices in the form of a 2D array

    Returns
    -------
    True/False depending on whether VL is a simple polygon or not.

    '''
    VL = np.asarray(VL)
    # create pairs of points to form line segments 
    lineSegments = np.array([[VL[len(VL)-1],VL[0]]])

    i=0
    while i < len(VL)-1:
        lineSegments = np.append(lineSegments,[[VL[i],VL[i+1]]] ,axis =0)
        i += 1


    # loop through all the line segments and check if any 2  itersect
    i =0
    while i < len(lineSegments):
        j=0
        while j < i-1:
            #if 2 segments intersect then the poly is complex, return false
       
            if( not(np.array_equal(lineSegments[j] , lineSegments[(i+1)%len(lineSegments)])) and isIntersect(lineSegments[i],lineSegments[j])):
                return False
            
            j += 1    
        i += 1
    # if code reaches here that means no line segment is intersecting, return true
    return True
        

def check_convexity(VL):
    '''
    Parameters
    ----------
    VL : An sequence of vertices in the form of a 2D array

    Returns
    -------
    True/False depending on whether VL forms a boundary of a convexy polygon.

    '''
    VL = np.asarray(VL)
    # stores the first rotation of the polygon, 1 or -1
    rotation = leftOrRight(VL[0],VL[1],VL[2])

    # loop through all the consecutive points to get rotation
    i=0
    while i < len(VL):
        # if rotation is not equal at any point the polygon is not convex 
        if( rotation != leftOrRight(VL[i],VL[(i+1)%len(VL)], VL[(i+2)%len(VL)])):
            return False
        i += 1    

    # if code reaches here that means all the points have same rotation.
    return True        



def point_membership(P,VL):
    '''
    Parameters
    ----------
    P : a 2D point example, P = np.array([1,2])
    VL : An sequence of vertices in the form of a 2D array

    Returns
    -------
    Should an integer type 
    1 if the P is inside the boundaries defined by VL
    0 if the P is outside the boundaries defined by VL
    -1 if the P is on the boundary defined by VL

    '''

    P = np.asarray(P)
    VL = np.asarray(VL)

    '''
    Aletrnate Implementation using only numpy:

    i=0
    # create pairs of points to form line segments 
    lineSegments = np.array([[VL[len(VL)-1],VL[0]]])

    while i < len(VL)-1:
        lineSegments = np.append(lineSegments,[[VL[i],VL[i+1]]] ,axis =0)
        i += 1

    ray = np.array([P, [10000000 ,P[1]]])

    #loop through all the line segments and check if the ray intersects them
    
    
    i=0
    while i < len(lineSegments):
        #if it intersects then increase counter except when the point lies on the boundary
        if(isIntersect(ray, lineSegments[i])):
            intersectPoint = intersect(ray[0],ray[1],lineSegments[i][0],lineSegments[i][1])
            if(np.allclose(intersectPoint , ray[0])):
                #print("boundary point")
                return -1
            
            
        i += 1
    
    # find all the unique intersection points the ray has
    points = np.unique(points,axis =0)
    print(points)
    #calculate the count
    count = len(points)

    if(count%2 == 1):
        #print("inside point",count)
        return 1
    else:
        #print("outside point",count)   
        return 0
    '''
  
    poly=  simp.Polygon(*(tuple(map(tuple, VL))))
    
    if(poly.intersection(simp.Point(P))):
        return -1

    #print(poly.intersection(simp.Point(P)))

    elif(poly.encloses_point(simp.Point(P))):
        return 1
    else:
        return 0



def find_intersection(VL1,VL2):
    '''
    Parameters
    ----------
    VL1 : a 2D array, shape=(N rows, 2 columns)
        A sequence of vertices, which form the boundary of a solid 1
    VL2 : a 2D array, shape=(N rows, 2 columns)
        A sequence of vertices, which form the boundary of a solid 2

    Returns
    -------
    VL_int : A sequence of vertices of the boundary of the intersection 
     of the two solids 1 and 2.

    '''
    VL1 = np.asarray(VL1)
    VL2 = np.asarray(VL2)
    # get all the intersecting points
    VL_int = intersectingPoints(VL1,VL2)

    
    # append all the point of VL1 that are inside VL2
    i =0
    while i < len(VL1):
        if(point_membership(VL1[i],VL2) != 0):
            VL_int.append(VL1[i])
        
        i += 1    
    
    
    # append all the point of VL2 that are inside VL1
    i =0
    while i < len(VL2):
        if(point_membership(VL2[i],VL1) != 0):
            VL_int.append(VL2[i])
        i += 1    
    
    VL_int = np.unique(VL_int,axis =0)


    #order all the points
    VL_int = orderPoints(VL_int)

    return VL_int



def find_union(VL1,VL2):
    '''
    Parameters
    ----------
    VL1 : a 2D array, shape=(N rows, 2 columns)
        A sequence of vertices, which form the boundary of a solid 1
    VL2 : a 2D array, shape=(N rows, 2 columns)
        A sequence of vertices, which form the boundary of a solid 2

    Returns
    -------
    VL_int : A sequence of vertices of the boundary of the union 
     of the two solids 1 and 2.

    '''
    VL1 = np.asarray(VL1)
    VL2 = np.asarray(VL2)

    VL_int = intersectingPoints(VL1,VL2)

    # append all the point of VL1 that are outside VL2
    i =0
    while i < len(VL1):
        if(point_membership(VL1[i],VL2) != 1):
            VL_int.append(VL1[i])
        
        i += 1    
    
    
    # append all the point of VL2 that are outside VL1
    i =0
    while i < len(VL2):
        if(point_membership(VL2[i],VL1) != 1):
            VL_int.append(VL2[i])
        i += 1    
    
    VL_int = np.unique(VL_int,axis =0)
  

    #order all the points
    VL_int = orderPoints(VL_int)

    return VL_int

  

def find_difference(VL1, VL2):
    '''
    Parameters
    ----------
    VL1 : a 2D array, shape=(N rows, 2 columns)
        A sequence of vertices, which form the boundary of a solid 1
    VL2 : a 2D array, shape=(N rows, 2 columns)
        A sequence of vertices, which form the boundary of a solid 2

    Returns
    -------
    VL_int : A sequence of vertices of the boundary of the difference  
     of the two solids 1 and 2.
     S1-S2.
    '''
    VL1 = np.asarray(VL1)
    VL2 = np.asarray(VL2)

    if(np.array_equal(VL1, VL2) ):
        return []
    
    VL_int = intersectingPoints(VL1,VL2)

 

    print(setA)

    # append all the point of VL1 that are outside VL2
    i =0
    while i < len(VL1):
        if(point_membership(VL1[i],VL2) != 1):
            VL_int.append(VL1[i])
        
        i += 1    
    
    
    # append all the point of VL2 that are inside VL1
    i =0
    while i < len(VL2):
        if(point_membership(VL2[i],VL1) != 0):
            VL_int.append(VL2[i])
        i += 1    
    
    VL_int = np.unique(VL_int,axis =0)
  

    #order all the points
    VL_int = orderPoints(VL_int)

    return VL_int


########################################################################
########################################################################
# End of File