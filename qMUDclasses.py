import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.signal as sps
from projectq import MainEngine  # import the main compiler engine
from projectq.ops import C, X, H, Measure, Barrier  # import the operations we want to perform (Hadamard and measurement)
from projectq.backends import CircuitDrawer

class DHAOracle:
    def __init__(self, delta, numBits, ancillaBit=None):
        self.C = C
        self.X = X
        self.H = H
        self.Barrier = Barrier
        
        self.delta = delta
        self.numBits = numBits
        self.delta_bin = np.binary_repr(delta, numBits)
        self.delta_bin = [int(i) for i in self.delta_bin]
        self.gatesList = []
        self.reverseGatesList = []
        
        self.circuit_drawer = CircuitDrawer()
        self.diag_eng = MainEngine(self.circuit_drawer)
        
        self.valreg = self.diag_eng.allocate_qureg(self.numBits)
        self.refreg = self.diag_eng.allocate_qureg(self.numBits)

        if (ancillaBit is None):
            self.ancilla = self.diag_eng.allocate_qureg(1)
        else:
            self.ancilla = ancillaBit

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
            # debug
            print (idx)
            
            # Condition 0. For each 0 at the start, place a simple CNOT.
            if delta_bin[idx] == 0:
                print('Condition 0')
                self.gatesList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[idx]]) + tuple([self.refreg[cidx]]))
                idx = idx+1 # move to next bit/next iteration
                cidx = cidx+1
                
            # Condition 1. All remaining bits are 1. E.g. 11111, 01111 etc.
            elif np.all(delta_bin[idx:]):
                print('Condition 1')
                self.gatesList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[i] for i in range(idx, len(delta_bin))]) + tuple([self.refreg[cidx]]))
                
                print('Exited at idx ' + str(idx)) # DEBUG
                
                idx = len(delta_bin) # end the loop, early stopping
            
            # Condition 2a. Current bit is 1, rest are 0. E.g. 01000 etc.
            elif np.all(np.logical_not(delta_bin[idx+1:])) and delta_bin[idx] == 1:
                print('Condition 2a')
                self.gatesList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[idx]]) + tuple([self.refreg[cidx]]))
                
                print('Exited at idx ' + str(idx)) # DEBUG
                
                idx = len(delta_bin) # early stopping
            
            # Condition 2b. Current bit is 1. End of sequence.
            elif (idx == len(delta_bin)-1) and delta_bin[idx] == 1:
                print('Condition 2b')
                self.gatesList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[idx]]) + tuple([self.refreg[cidx]]))
                
                print('Exited at idx ' + str(idx)) # DEBUG
                
                idx = len(delta_bin) # early stopping
                
            # Condition 3. Current bit is 1. All special cases failed.
            elif (delta_bin[idx] == 1):
                print('Condition 3')
                prefix.append(idx)
                idx = idx + 1
                # but we don't need to move cidx
                
            # Condition 4. Current bit is 0. All special cases failed.
            elif (delta_bin[idx] == 0):
                print('Condition 4')
                # attach all existing prefixes, and write a toffoli with a node at the 0
                self.gatesList.append(tuple([self.valreg[prefix[i]] for i in range(len(prefix))]) + tuple([self.valreg[idx]]) + tuple([self.refreg[cidx]]))
                idx = idx + 1
                
            else:
                print('Unknown conditions')

        # implement the gates
        for i in range(len(self.gatesList)):
            print(self.gatesList[i])
            
            # implement the gate
            self.C(X,len(self.gatesList[i])-1) | self.gatesList[i]
            
        # Barrier for neatness?
        self.Barrier | (self.valreg, self.refreg, self.ancilla)   
            
        # implement X gates on 0 bits
        for i in range(len(delta_bin)):
            if (delta_bin[i] == 0):
                self.X | self.refreg[i]
                
        
                
        # implement Hadamard on ancilla
        self.H | self.ancilla
            
        # implement centre Toffoli
        self.C(X,len(delta_bin)) | (self.refreg, self.ancilla)
        
        # == and then implement all the reverses ==
        # implement Hadamard on ancilla
        self.H | self.ancilla
        
        
        
        # implement X gates on 0 bits
        for i in range(len(delta_bin)):
            if (delta_bin[i] == 0):
                self.X | self.refreg[i]
                
        # Barrier for neatness?
        self.Barrier | (self.valreg, self.refreg, self.ancilla)
        
        # implement the gates
        for i in range(len(self.gatesList)-1, -1, -1):
            print(self.gatesList[i])
            
            # implement the gate
            self.C(X,len(self.gatesList[i])-1) | self.gatesList[i]
        
        
            
        # flush gates
        self.diag_eng.flush()
        
    def showGates(self, adjustBarrier=False):
        text2print = self.circuit_drawer.get_latex()
        
        if adjustBarrier:
            # fix the barrier text to be vertical
            text2print = text2print.replace("Barrier", "\\rotatebox{90}{Barrier}")
            
        print('\n')
        print(text2print)
        
        return text2print