#!/usr/bin/env sage

import numpy as np
from sage.all import *

class markov_chain:
    def __init__(self, matrix, vector=None):
        # TODO make this Exception more specific
        if not markov_chain.valid_markov_chain(matrix, vector):
            raise Exception

        self.matrix = matrix

        # if the state vector doesn't exist, create one with equal elements
        # summing to 1
        if vector:
            self.vector = vector
        else:
            height = self.matrix.shape[0]
            self.vector = np.full((height,), 1 / height)

        # initialize digraph to be None
        # will be created and cached later if needed
        self.make_digraph()

    def make_digraph(self):
        digraph = sage.graphs.digraph.DiGraph(self.matrix.shape[0])
        digraph.allow_loops(new=True)
        digraph.weighted(new=True)

        for r in range(self.matrix.shape[0]):
            for (c, probability) in enumerate(self.matrix[r, :]):
                if probability > 0:
                    digraph.add_edge(c, r, probability)

        self.digraph = digraph

    def show(self, **kwargs):
        self.digraph.plot(**kwargs).show()

    @staticmethod
    def valid_markov_chain(matrix, vector=None):
        # verify that the matrix is 2D and square
        (rows, columns) = matrix.shape

        if rows != columns: return False

        # verify that each column adds up to 1
        for i in range(columns):
            if not np.isclose(matrix[:, i].sum(), 1):
                return False

        # make sure every element is between 0 and 1
        for element in matrix.flat:
            if element < 0 or element > 1:
                return False

        # check the vector's validity, if it exists
        if vector:
            # the vector is the right shape
            if vector.shape != (rows,):
                return False

            # none of the vector's elements are negative
            for element in vector:
                if element < 0:
                    return False

        return True

def display_stuff(matrix, vector=None):
    # make this an exception instead
    if not markov_chain.valid_markov_chain(matrix): return None
    
    digraph = sage.graphs.digraph.DiGraph(matrix.shape[0])
    digraph.allow_loops(new=True)
    digraph.weighted(new=True)
    
    for r in range(matrix.shape[0]):
        for (c, probability) in enumerate(matrix[r, :]):
            if probability > 0:
                digraph.add_edge(c, r, probability)

    # relabel vertices if vector given
    if vector.shape == (matrix.shape[0],):
        #digraph.relabel(["%d: %.2f" % (i, v) for i, v in enumerate(vector)])
        digraph.relabel([(i, v) for i, v in enumerate(vector)])

    digraph.plot(edge_labels=True).show()

if __name__ == '__main__':
    pass
