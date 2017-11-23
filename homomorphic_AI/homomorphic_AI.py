import numpy as np

def generate_key(w, m, n):
	S = np.random.rand(m,n) * w / (2 ** 16)#proving max(S) < w
	return S

def encrypt(x, S, m, n, w):
	assert len(x) == len(S)

	e = (np.random.rand(m)) # proving max(e) < w/2
	c = np.linalg.inv(S).dot((w * x) + e)
	return c

def decrypt(c, S, w):
	return (S.dot(c) / w).astype('int')

def get_c_star(c, m, l):
	c_star = np.zeros(l * m, dtype='int')
	for i in range(m):
		b = np.array(list(np.binary_repr(np.abs(c[i]))), dtype='int')
		if c[i] < 0 :
			b *= -1
		c_star[(i * l) + (l - len(b)): (i + 1) * l] += b
	return c_star

def switch_key(c, S, m, n, T):
	l = int(np.ceil(np.log2(np.max(np.abs(c)))))
	c_star = get_c_star(c, m, l)
	S_star = get_S_star(S, m, n, l)
	n_prime = n + 1

	S_prime = np.concatenate((np.eye(m),T.T),0).T
	A = (np.random.rand(n_prime - m, n * l) * 10).astype('int')
	E = (1 * np.random.rand(S_star.shape[0], S_star.shape[1]).astype('int'))
	M = np.concatenate(((S_star - T.dot(A) + E), A), 0)
	c_prime = M.dot(c_star)
	return c_prime, S_prime

def get_S_star(S, m, n, l):
	S_star = list()
	for i in range(l):
		S_star.append(S*2**(l - i - 1))
	S_star = np.array(S_star).transpose(1,2,0).reshape(m, n * l)
	return S_star

def get_T(n):
	n_prime = n + 1
	T = (10 * np.random.rand(n, n_prime - n)).astype('int')
	return T

def encrypt_via_switch(x, w, m, n, T):
	c, S = switch_key(x * w , np.eye(m), m, n, T)
	return c,S
# first test
x = np.array([0,1,2,5])
m = len(x)
n = m
w = 16
S = generate_key(w,m,n)
# c = encrypt(x, S, m, n, w)

# #second test
T = get_T(n)
c,S = encrypt_via_switch(x, w, m, n, T)

print c
print decrypt(c, S, w)
print decrypt(c + c, S, w)
print decrypt(c * 10, S, w)






