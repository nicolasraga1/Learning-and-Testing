#practice from http://iamtrask.github.io/2015/07/12/basic-python-network/ 
import numpy as np

#sigmoid function used to convert numbers to probabilities
def nonlin(x, deriv=False):
	if deriv == True:
		return x * (1 - x)
	return 1 / (1 + np.exp(-x))

#input dataset where each row is a training input
#3 input nodes and 4 training examples
X = np.array([  [0,0,1],
				[0,1,1],
				[1,0,1],
				[1,1,1] ])

#output dataset where each row is a training output
y = np.array([[0,0,1,1]]).T

#seed random numbers to make calculation
#deterministic --> just for good practice
np.random.seed(1)

#initialize weights randomly with mean 0 and normalize
#short for synapse 0 --> think of as guess we are taking
#connects l0 to l1 by taking dotproduct
#3 input columns and 1 output column
syn0 = 2*np.random.random((3,1)) - 1

for iter in xrange(10000):

	#forward propagation
	l0 = X #first layer defined by the input data
	l1 = nonlin(np.dot(l0,syn0)) #hidden layer

	#how much did we miss
	l1_error = y - l1

	#multiply how much we missed by the slope of the sigmoid at 
	#the values in l1
	l1_delta = l1_error * nonlin(l1, True)

	#upate weights
	syn0 += np.dot(l0.T, l1_delta)

print "Output After Training"
print l1
