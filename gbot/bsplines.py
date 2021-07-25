"""
Course: ME/MF F342 Computer Aided Design
Author: Bhavya Bhatia

Topic: Bsplines

Instructions:
-------------

"""


import numpy as np
import scipy.interpolate as si

cv = np.array([[ 50.,  25.],
   [ 59.,  12.],
   [ 50.,  10.],
   [ 57.,   2.],
   [ 40.,   4.],
   [ 40.,   14.]])

def bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = np.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = np.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = np.clip(degree,1,degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = np.clip(degree,1,count-1)


    # Calculate knot vector
    kv = None
    if periodic:
        kv = np.arange(0-degree,count+degree+degree-1,dtype='int')
    else:
        kv = np.concatenate(([0]*degree, np.arange(count-degree+1), [count-degree]*degree))


    # Calculate query range
    u = np.linspace(periodic,(count-degree),n)

    print(u)

    # Calculate result
    return np.array(si.splev(u, (kv,cv.T,degree))).T


import matplotlib.pyplot as plt
colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')

cv = np.array([[ 50.,  25.],
   [ 59.,  12.],
   [ 50.,  10.],
   [ 57.,   2.],
   [ 40.,   4.],
   [ 40.,   14.]])

plt.plot(cv[:,0],cv[:,1], 'o-', label='Control Points')

d = 4
p = bspline(cv,n=1000,degree=d,periodic=False)
x,y = p.T
plt.plot(x,y,'k-',label='Degree %s'%d,color=colors[d%len(colors)])

plt.minorticks_on()
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(35, 70)
plt.ylim(0, 30)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

########################################################################
########################################################################
# End of File