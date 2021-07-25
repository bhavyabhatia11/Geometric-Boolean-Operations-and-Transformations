
"""
Course: ME/MF F342 Computer Aided Design
Author: Bhavya Bhatia

Topic: Divided Difference

Description:
-------------
Python3 program for implementing Newton's divided difference formula.

"""

#Global Variable
y = [[0 for i in range(10)]
		for j in range(10)]

# Helper Function to find the product term
def proterm(i, value, x):
	pro = 1
	for j in range(i):
		pro = pro * (value - x[j])
	return pro

# Function for calculating divided difference table
def dividedDiffTable(x, fx, n):
	'''
	Parameters:
	-----------
	x : The input values of the the function whose divided diffrence has to be calculated. 
	fx : The output values of y = f(x) corresponding to x
	n : Number of Values 

	Returns:
	-----------
	Returns a 2d array representing the divided difference
	'''
	
	for i in range(0,n):
	    y[i][0] = fx[i]

	for i in range(1, n):
		for j in range(n - i):
			y[j][i] = ((y[j][i - 1] - y[j + 1][i - 1]) /
									(x[j] - x[i + j]))
	return y

# Function for applying Newton's divided difference formula
def dividedDiffValue(value, x, fx, n):
	'''
	Parameters:
	-----------
	value : The value at which divided diffrence has to be calculated
	x : The input values of the the function whose divided diffrence has to be calculated. 
	fx : The output values of y = f(x) corresponding to x
	n : Number of Values 

	Returns:
	-----------
	returns an integer representing the divided diffrence at a particular value
	'''

	y = dividedDiffTable(x,fx,n)

	sum = y[0][0]

	for i in range(1, n):
		sum = sum + (proterm(i, value, x) * y[0][i])
	
	return round(sum, 2)

# Function for displaying divided difference table
def prettyPrintTable(x, fx, n):
	'''
	Parameters:
	-----------
	x : The input values of the the function whose divided diffrence has to be calculated. 
	fx : The output values of y = f(x) corresponding to x
	n : Number of Values 

	Returns:
	-----------
	returns a neatly printed representation of the divided diffrence.
	'''

	y = dividedDiffTable(x, fx, n)

	for i in range(n):
		for j in range(n - i):
			print(round(y[i][j], 4), "\t",
							end = " ")

		print("")

'''
Example:
---------------
from divided_difference import *

In : dividedDiffTable([5,6,9,11],[12,13,14,16],4)
Out : [[12, 1.0, -0.16666666666666669, 0.05000000000000001, 0, 0, 0, 0, 0, 0], [13, 0.3333333333333333, 0.13333333333333336, 0, 0, 0, 0, 0, 0, 0], [14, 1.0, 0, 0, 0, 0, 0, 0, 0, 0], [16, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

In : dividedDiffValue(7,[5,6,9,11],[12,13,14,16],4)
Out : 13.47

In : prettyPrintTable([5,6,9,11,13],[12,13,14,16,19],5)
Out :   12 	 1.0 	 -0.1667 	 0.05 	 -0.0064 	 
		13 	 0.3333 	 0.1333 	 -0.0012 	 
		14 	 1.0 	 0.125 	 
		16 	 1.5 	 
		19 

'''
########################################################################
########################################################################
# End of File
