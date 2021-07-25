
"""
Course: ME/MF F342 Computer Aided Design
Author: Bhavya Bhatia

Topic: Divided Difference

Instructions:
-------------

"""


#Python3 program for implementing
# Newton divided difference formula

# Function to find the product term
def proterm(i, value, x):
	pro = 1
	for j in range(i):
		pro = pro * (value - x[j])
	return pro

# Function for calculating
# divided difference table
def dividedDiffTable(x, y, n):

	for i in range(1, n):
		for j in range(n - i):
			y[j][i] = ((y[j][i - 1] - y[j + 1][i - 1]) /
									(x[j] - x[i + j]))
	return y

# Function for applying Newton's
# divided difference formula
def applyFormula(value, x, y, n):

	sum = y[0][0]

	for i in range(1, n):
		sum = sum + (proterm(i, value, x) * y[0][i])
	
	return sum

# Function for displaying divided
# difference table
def printDiffTable(y, n):

	for i in range(n):
		for j in range(n - i):
			print(round(y[i][j], 4), "\t",
							end = " ")

		print("")

# Driver Code

# number of inputs given
n = 10
y = [[0 for i in range(10)]
		for j in range(10)]
x = [ 0,1,2,3,4,5,6,7,8,9 ]

# y[][] is used for divided difference
# table where y[][0] is used for input


for i in x:
    y[i][0] = i*i*i

# calculating divided difference table
y=dividedDiffTable(x, y, n)

# displaying divided difference table
printDiffTable(y, n)


########################################################################
########################################################################
# End of File
