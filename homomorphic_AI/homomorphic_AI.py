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
		b = np.array(list(np.binary_repr(np.abs(c[i]))), dytpe='int')
		if c[i] < 0 :
			b *= -1
		c_star[(i * l) + (l - len(b)): (i + 1) * l] += b
	return c_star

def get_S_star(S, m, n, l):
	S_star = list()
	for i in range(l):
		S_star.append(S*2**(l - i - 1))
	S_star = np.array(S_star).transpose(1,2,0).reshape(m, n * l)
	return S_star

x = np.array([0,1,2,5])
m = len(x)
n = m
w = 16
S = generate_key(w,m,n)
c = encrypt(x, S, m, n, w)
print decrypt(c, S, w)
print decrypt(c + c, S, w)
print decrypt(c * 10, S, w)