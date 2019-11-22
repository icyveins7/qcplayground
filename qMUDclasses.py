import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.signal as sps
from qiskit import *
from qiskit.tools.visualization import circuit_drawer

class DHAOracle:
    def __init__(self, delta, numBits):
        self.delta = delta
        self.numBits = numBits
        self.delta_bin = np.binary_repr(delta, numBits)
        self.delta_bin = [int(i) for i in self.delta_bin]
        self.gatesList = []
        self.valreg = QuantumRegister(self.numBits, 'val')
        self.refreg = QuantumRegister(self.numBits, 'reg')
        self.qc = QuantumCircuit(self.valreg, self.refreg)
        self.circdrawer = circuit_drawer(self.qc)

    def makeGates(self):
        i = 0
        while (i<len(self.delta_bin)):
            if np.all(self.delta_bin[i:]):
                print(1)

        print(self.qc)

    def showGates(self):
        self.qc.h(0)
        self.qc.mct(self.valreg[0:3], self.refreg[0], None, 'noancilla')

        print(self.qc)