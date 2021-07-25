"""
Course: ME/MF F342 Computer Aided Design
Proffessor: Dr. Amit R. Singh

Submitted by: Bhavya Bhatia
Date: March 15, 2021

Topic: 3D Projective Transformations

Instructions:
-------------

"""
from numpy import *

def rotation(theta, axis):
    """
    Rotation matrix for 3D rotation about a given axis.
    
    Parameters:
    -----------
    theta: angle of rotation in radians.
    axis: a vector (not necessarily a unit vector) in the direction
          of the desired axis of rotation.
    
    Output:
    -------
    R: a 3D rotation matrix
    """
    # To covert input to array
    axis = asarray(axis)

    #condition to prevent 0 error
    if(axis[0] ==0 and axis[1] == 0 and axis[2] ==0):
        return zeros([3,3])
    else:
        #converting axis into unit vector
        Px = axis[0]/(linalg.norm(axis))
        Py = axis[1]/(linalg.norm(axis))
        Pz = axis[2]/(linalg.norm(axis))

   
    # writing P array using px,Py,Pz
    P = array([[0,-Pz,Py],[Pz,0,-Px],[-Py,Px,0]])

    #Identity Matrix
    I = identity(3)

    #Formula for rotation matrix
    R = I + sin(theta)*P + (1-cos(theta))*(P@P)

    return R


def affinesubmatrix(theta, thetaaxis, phi, phiaxis, lambda1, lambda2, lambda3):
    """
    Create a 3x3 matrix (to be used as the upper left submatrix of a 4x4
    transformation matrix) from scalings and rotations. Symbols theta and phi
    have meanings as discussed in the lectures.

    Parameters:
    -----------
    theta: final rotation about `thetaaxis`.
    thetaaxis: a vector (not necessarily a unit vector) along the axis of rotation.
    phi: orientation for scaling
    phiaxis: a vector (not necessarily a unit vector) along the axis of rotation.
    lambda1: scaling in the rotated x direction.
    lambda2: scaling in the rotated y direction.
    lambda3: scaling in the rotated z direction.

    Output:
    -------
    A: a 3x3 matrix
    """
    # D : Scaling matrix
    D = array([ [lambda1,0,0 ],
                [0,lambda2,0 ],
                [0,0, lambda3]])

    #using rotation function to calculation RTheta, RPhi and RMinusPhi 
    RTheta = rotation(theta,thetaaxis)
    RPhi = rotation(phi,phiaxis)
    RMinusPhi = rotation(-phi,phiaxis)

    # Affine submatrix
    A = RTheta@RMinusPhi@D@RPhi

    return A


def affinity(A, tx, ty, tz):
    """
    Create a 4x4 affine transformation matrix.
    
    Parameters:
    -----------
    A: a 3x3 non-singular (sub)matrix. For example, the output of `affinesubmatrix` function.
    tx: translation in the x-direction.
    ty: translation in the y-direction.
    tz: translation in the z-direction.
    
    Output:
    -------
    H: a 4x4 affine transformation matrix 
    """
    # To covert input to array
    A = asarray(A)

    # Appending tx,ty,tz and the last row to make affine transformation matrix
    H = array([ [A[0][0], A[0][1] , A[0][2] , tx],
                [A[1][0], A[1][1] , A[1][2] , ty],
                [A[2][0], A[2][1] , A[2][2] , tz],
                [0      , 0       , 0       , 1 ],])

    return H


def similarity(s, theta, axis, tx, ty, tz):
    """
    Create a 4x4 similarity transformation matrix.
    
    Parameters:
    -----------
    s: isotropic scaling ratio.
    theta: angle of rotation about `thetaaxis`.
    axis: a vector (not necessarily a unit vector along the axis of rotation.
    tx: translation in the x-direction.
    ty: translation in the y-direction
    tz: translation in the z-direction
    
    Output:
    -------
    H: a 4x4 similarity transformation matrix 
    """
    # calling rotation function to find the rotation matrix
    rotationMatrix = rotation(theta,axis)

    #multiplying it with s to get the similarity matrix
    similarityMatrix = s*rotationMatrix

    # Since H is just similarity matrix with added tx,ty,tz we can use affine function to do make H
    H = affinity(similarityMatrix,tx,ty,tz)

    return H


def findprojectivity(X, x):
    """
    Calculate a 3x3 projectivity matrix from coordinates of 4 points before and after transformation.
    
    Parameters:
    -----------
    X: a 2x4 matrix whose columns denote 4 points BEFORE transformation.
    x: a 2x4 matrix whose columns denote 4 points AFTER transformation.
    
    Output:
    -------
    H: a 3x3 projectivity matrix.
    
    Note:
    -----
    We will always return H such that h33 = 1.
    """
    # creating before and after points : xi,yi are before and pi,qi are after coordinates
    x1 = X[0][0]
    y1 = X[1][0] 

    x2 = X[0][1]
    y2 = X[1][1]  

    x3 = X[0][2]
    y3 = X[1][2]    

    x4 = X[0][3]
    y4 = X[1][3]  

    p1 = x[0][0]
    q1 = x[1][0] 

    p2 = x[0][1]
    q2 = x[1][1]  

    p3 = x[0][2]
    q3 = x[1][2]    

    p4 = x[0][3]
    q4 = x[1][3]

    # using the matrix we will get 3 equations for each corresponding before and after coordinate
    # thus we get 4X3 = 12 equations in Total to solve for 12 unkowns
    # 8 variables of the matrix and the rest k1,k2,k3,k4 
    # solving linear equation of type AX =b

    A = array([
        [x1, y1, 1, 0, 0, 0, 0, 0, -p1, 0, 0, 0], 
        [x2, y2, 1, 0, 0, 0, 0, 0, 0, -p2, 0, 0], 
        [x3, y3, 1, 0, 0, 0, 0, 0, 0, 0, -p3, 0], 
        [x4, y4, 1, 0, 0, 0, 0, 0, 0, 0, 0, -p4], 
        [0, 0, 0, x1, y1, 1, 0, 0, -q1, 0, 0, 0], 
        [0, 0, 0, x2, y2, 1, 0, 0, 0, -q2, 0, 0], 
        [0, 0, 0, x3, y3, 1, 0, 0, 0, 0, -q3, 0], 
        [0, 0, 0, x4, y4, 1, 0, 0, 0, 0, 0, -q4], 
        [0, 0, 0, 0, 0, 0, x1, y1, -1, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, x2, y2, 0, -1, 0, 0], 
        [0, 0, 0, 0, 0, 0, x3, y3, 0, 0, -1, 0], 
        [0, 0, 0, 0, 0, 0, x4, y4, 0, 0, 0, -1]
        ])
    b = array([0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1])
    res = linalg.solve(A, b)

    # After solving the linear quation we will get all the matrix points
    a11	= res[0]
    a12	= res[1]
    tx = res[2]
    a21	= res[3]
    a22	= res[4]
    ty = res[5]
    v1	= res[6]
    v2	= res[7]

    #the resultant projectivity matrix would look like this
    H = array([
                [a11, a12, tx], 
                [a21, a22, ty], 
                [v1,   v2,  1],    
                ])

    return H


def cameramatrix(zc, yc, C, f, px, py):
    """
    Create a 3x4 camera matrix.
    
    Parameters:
    -----------
    zc: a 3x1 vector along the principal axis of the camera.
    yc: a 3x1 vector along the up-direction of the camera.
    C: a 3x1 position vector of the camera center in the world axes.
    f: focal length of the camera.
    px, py: distance of the principal point from the image axes origin.
    
    Note:
    -----
    Read the PDF notes provided on Camera Matrix.
    
    Output:
    -------
    P: the 3x4 Camera Matrix.
     """
    # converting all values into numpy arrays
    yc = asarray(yc)
    zc = asarray(zc)
    C = asarray(C)

    # taking xc by cross product of yc and zc
    xc = cross(yc.T , zc.T)

    #taking transpose to convert into 3x1
    xc = xc.T

    #converting all to unit vectors
    xc = xc/(linalg.norm(xc))
    yc = yc/(linalg.norm(yc))
    zc = zc/(linalg.norm(zc))

    
    
    R = array([[xc[0][0],yc[0][0],zc[0][0]],
                [xc[1][0],yc[1][0],zc[1][0]],
                [xc[2][0],yc[2][0],zc[2][0]]])

    #camera calibration matrix
    K = array([ [f, 0, px, 0] ,
                [0, f, py, 0],
                [0, 0, 1 , 0]])

    #translation matrix
    t = -R@C       
    
    
    H = array([ [R[0][0], R[0][1] , R[0][2] , t[0][0]],
                [R[1][0], R[1][1] , R[1][2] , t[1][0]],
                [R[2][0], R[2][1] , R[2][2] , t[2][0]],
                [0      , 0       , 0       , 1      ]])

    #P is the camera matrix
    P = K@H

    return asarray(P)
   

def cameraimage(P, X):
    """
    Returns the images of points in X when seen from a camera whose matrix is P. 
    
    Parameters:
    -----------
    P: a 3x4 camera matrix
    X: a 3xN matrix whose columns represent N points in the world axes.
    
    Note:
    -----
    Read the PDF notes provided on Camera Matrix.
    
    Output:
    -------
    x: a 2xN matrix whose columns represent N points in the image axes.
    """
    # converting all values into numpy arrays
    P = asarray(P)
    X = asarray(X)

    # getting the value of N 
    N = X[0].size

    # aappending 1s row at then end to convert it into homogenious coordinates
    X = append(X, array([ones(N)]),axis=0)

    #x will be PxX
    x = P@X

   
    #iteration over x to divide the elements by the last row 
    for i in range(2):
        for j in range(N): 
            x[i][j] = (x[i][j]/x[2][j])
    
    # deleting the last row of x because a 2XN array is to be returned
    x = delete(x,2,0)

    return x

'''
Example: 
-----------

axis = [0,1,1]
theta = 60

print(rotation(theta,axis))

'''