# cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, cdivision=True
import numpy as np
cimport numpy as np
from cython.parallel import prange

# Expand data into full genotype matrix
cpdef void expandGeno(const unsigned char[:,::1] B, unsigned char[:,::1] G) \
		noexcept nogil:
	cdef:
		size_t M = G.shape[0]
		size_t N = G.shape[1]
		size_t N_b = B.shape[1]
		size_t i, j, b, bytepart
		unsigned char[4] recode = [2, 9, 1, 0]
		unsigned char mask = 3
		unsigned char byte
	for j in prange(M):
		i = 0
		for b in range(N_b):
			byte = B[j,b]
			for bytepart in range(4):
				G[j,i] = recode[byte & mask]
				byte = byte >> 2
				i = i + 1
				if i == N:
					break

# Standardize batched genotype matrix
cpdef void standardizeE(double[:,::1] E, const unsigned char[:,::1] G, \
		const double[::1] f, const double[::1] d, const size_t m) noexcept nogil:
	cdef:
		size_t M = E.shape[0]
		size_t N = E.shape[1]
		size_t i, j, k
		double a, b
	for j in prange(M):
		k = m + j
		a = 2.0*f[k]
		b = d[k]
		for i in range(N):
			if G[k,i] == 9:
				E[j,i] = 0.0
			else:
				E[j,i] = (<double>G[k,i] - a)*b
