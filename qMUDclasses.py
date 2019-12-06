import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.signal as sps
from projectq import MainEngine  # import the main compiler engine
from projectq.ops import C, X, H, Measure  # import the operations we want to perform (Hadamard and measurement)
from projectq.backends import CircuitDrawer

class DHAOracle:
    def __init__(self, delta, numBits):
        self.C = C
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
            # Condition 0. For each 0 at the start, place a simple CNOT.
            if delta_bin[idx] == 0:
                self.gatesList.append(tuple([self.valreg[idx]]) + tuple([self.refreg[cidx]]))
                idx = idx+1 # move to next bit/next iteration
                cidx = cidx+1
                
            # Condition 1. All remaining bits are 1. E.g. 11111, 01111 etc.
            elif np.all(delta_bin[idx:]):
                self.gatesList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[i] for i in range(idx, len(delta_bin))]) + tuple([self.refreg[cidx]]))
                
                print('Exited at idx ' + str(idx)) # DEBUG
                
                idx = len(delta_bin) # end the loop, early stopping
            
            # Condition 2. Current bit is 1, rest are 0. E.g. 01000 etc.
            elif np.all(np.logical_not(delta_bin[idx+1:])) and delta_bin[idx] == 1:
                self.gatesList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[idx]]) + tuple([self.refreg[cidx]]))
                
                print('Exited at idx ' + str(idx)) # DEBUG
                
                idx = len(delta_bin) # early stopping
            
            else:
                print('not yet implemented')
                idx = len(delta_bin)
            
#            # Condition 2. All remaining bits are 0. E.g. 10000, 01000 etc.
#            elif np.all(np.logical_not(delta_bin[idx:])):
#                gateList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[i] for i in range(len())]))

        for i in range(len(self.gatesList)):
            print(self.gatesList[i])
            
            # implement the gate
            self.C(X,len(self.gatesList[i])-1) | self.gatesList[i]
            
            
        # flush gates
        self.diag_eng.flush()
        
    def showGates(self):
        print(self.circuit_drawer.get_latex())