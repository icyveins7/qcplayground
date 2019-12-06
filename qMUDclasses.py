import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.signal as sps
from projectq import MainEngine  # import the main compiler engine
from projectq.ops import C, X, H, Measure  # import the operations we want to perform (Hadamard and measurement)
from projectq.backends import CircuitDrawer

class DHAOracle:
    def __init__(self, delta, numBits):
        self.delta = delta
        self.numBits = numBits
        self.delta_bin = np.binary_repr(delta, numBits)
        self.delta_bin = [int(i) for i in self.delta_bin]
        self.gatesList = []
        
        self.circuit_drawer = CircuitDrawer()
        self.diag_eng = MainEngine(self.circuit_drawer)
        
        self.valreg = self.diag_eng.allocate_qureg(self.numBits)
        self.refreg = self.diag_eng.allocate_qureg(self.numBits)
        
        # old qiskit ver
#        self.valreg = QuantumRegister(self.numBits, 'val')
#        self.refreg = QuantumRegister(self.numBits, 'reg')
#        self.qc = QuantumCircuit(self.valreg, self.refreg)
#        self.circdrawer = circuit_drawer(self.qc)

    def makeGates(self, delta_bin=None):
        if delta_bin is None:
            delta_bin = self.delta_bin
        
        idx = 0 # current bit
        cidx = 0 # current control bit
        prefix = [] # initialize with no prefixes
        
        while (idx<len(delta_bin)):
            # Condition 1. All bits are 1
            if np.all(delta_bin[idx:]):
                gate = tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[i] for i in len(delta_bin[idx:])]) + tuple(self.refreg[cidx])
                return gate
            else:
                # Condition 2. All remaining bits are 0.
                if np.all(np.logical_not(delta_bin[idx:])):
                    f

        print(self.qc)

    def showGates(self):
        self.qc.h(0)
        self.qc.mct(self.valreg[0:3], self.refreg[0], None, 'noancilla')

        print(self.qc)