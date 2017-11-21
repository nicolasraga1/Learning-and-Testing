# practice from http://iamtrask.github.io/2015/07/12/basic-python-network/
import numpy as np 

def nonlin(x, deriv=False):
	if deriv:
		return x * (1 - x)
	return 1 / (1 + np.exp(-x))

#Input dataset matrix where each row is an input example
X = np.array([  [0,0,1],
				[0,1,1],
				[1,0,1],
				[1,1,1] ])

#Ouput dataset column vector where each row is an output example
y = np.array([[0,1,1,0]]).T

np.random.seed(1)

#connecting l0 to l1
syn0 = 2*np.random.random((3,4)) - 1
#connecting l1 to l2
syn1 = 2*np.random.random((4,1)) - 1

for j in xrange(60000):
	#feed forward through layers 0, 1, and 2
	l0 = X
	l1 = nonlin(np.dot(l0, syn0))
	l2 = nonlin(np.dot(l1, syn1))

	l2_error = y - l2

	if j % 10000 == 0:
		print "Error: " + str(np.mean(np.abs(l2_error)))

	#in what direction is the target value?
	# were we really sure? if so, don't change to much
	l2_delta = l2_error * nonlin(l2, True)

	#how much did each l1 value contribute to the l2 
	# error (according to the weights)?
	l1_error = l2_delta.dot(syn1.T)

	#in what direction if the target l1?
	# were we really sure? is so, don't change much
	l1_delta = l1_error * nonlin(l1, True)

	syn1 += l1.T.dot(l2_delta)
	syn0 += l0.T.dot(l1_delta)