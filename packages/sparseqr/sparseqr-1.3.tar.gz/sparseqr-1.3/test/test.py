#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import numpy
import scipy.sparse.linalg
import sparseqr

# QR decompose a sparse matrix M such that  Q R = M E
#
M = scipy.sparse.rand( 10, 10, density = 0.1 )
Q, R, E, rank = sparseqr.qr( M )
print( "Should be approximately zero:", abs( Q*R - M*sparseqr.permutation_vector_to_matrix(E) ).sum() ) 

# Solve many linear systems "M x = b for b in columns(B)"
#
B = scipy.sparse.rand( 10, 5, density = 0.1 )  # many RHS, sparse (could also have just one RHS with shape (10,))
x = sparseqr.solve( M, B, tolerance = 0 )

# Solve an overdetermined linear system  A x = b  in the least-squares sense
#
# The same routine also works for the usual non-overdetermined case.
#
A = scipy.sparse.rand( 20, 10, density = 0.1 )  # 20 equations, 10 unknowns
b = numpy.random.random(20)  # one RHS, dense, but could also have many (in shape (20,k))
x = sparseqr.solve( A, b, tolerance = 0 )
## Call `rz()`:
sparseqr.rz( A, b, tolerance = 0 )

# Solve a linear system  M x = B  via QR decomposition
#
# This approach is slow due to the explicit construction of Q, but may be
# useful if a large number of systems need to be solved with the same M.
#
M = scipy.sparse.rand( 10, 10, density = 0.1 )
Q, R, E, rank = sparseqr.qr( M )
r = rank  # r could be min(M.shape) if M is full-rank

# The system is only solvable if the lower part of Q.T @ B is all zero:
print( "System is solvable if this is zero (unlikely for a random matrix):", abs( (( Q.tocsc()[:,r:] ).T ).dot( B ) ).sum() )

# Systems with large non-square matrices can benefit from "economy" decomposition.
M = scipy.sparse.rand( 20, 5, density=0.1 )
B = scipy.sparse.rand( 20, 5, density = 0.1 )
Q, R, E, rank = sparseqr.qr( M )
print("Q shape (should be 20x20):", Q.shape)
print("R shape (should be 20x5):", R.shape)
Q, R, E, rank = sparseqr.qr( M, economy=True )
print("Q shape (should be 20x5):", Q.shape)
print("R shape (should be 5x5):", R.shape)

# Use CSC format for fast indexing of columns.
R = R.tocsc()[:r,:r]
Q = Q.tocsc()[:,:r]
QB = (Q.T).dot(B).tocsc()  # for best performance, spsolve() wants the RHS to be in CSC format.
result = scipy.sparse.linalg.spsolve(R, QB)

# Recover a solution (as a dense array):
x = numpy.zeros( ( M.shape[1], B.shape[1] ), dtype = result.dtype )
x[:r] = result.todense()
x[E] = x.copy()

# Recover a solution (as a sparse matrix):
x = scipy.sparse.vstack( ( result.tocoo(), scipy.sparse.coo_matrix( ( M.shape[1] - rank, B.shape[1] ), dtype = result.dtype ) ) )
x.row = E[ x.row ]

#initialize QR Factorization object
M = scipy.sparse.rand( 100, 100, density=0.05 )

#perform QR factorization, but store in Householder form
QR= sparseqr.qr_factorize( M )
X = numpy.zeros((M.shape[0],1))
#change last entry of the first column to a 1 
# this allows us to construct only the first column of Q
X[-1,0]=1 

Y = sparseqr.qmult(QR,X)
print("Y shape (should be 100x1):",Y.shape)