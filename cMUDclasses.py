import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

class PSKSignal:
    def __init__(self, bits, m=2):
        self.bits = bits
        self.m = m
        self.syms = self.createSymbols(bits, m)
        self.csi = np.nan

    def __repr__(self):
        return 'PSKSignal: M = ' + str(self.m) + ', length = ' + str(len(self.bits))

    def createSymbols(self, bits, m):
        symbols = np.exp(1j * 2 * np.pi * bits/m)
        return symbols

    def setCSI(self, offset_samples, filter_taps):
        self.csi = 0

    def getSymbols(self):
        return self.syms

    def getBits(self):
        return self.bits

    def getM(self):
        return self.m

    def getCSI(self):
        if(self.csi is np.nan):
            raise Exception('CSI not yet set!')
        else:
            return self.csi

    def getNumSyms(self):
        return len(self.syms)

    def getSignalCombinatorics(self):
        c = np.zeros(self.getNumSyms(), dtype=np.int32)
        c = c + self.m
        return c

class OptimalMUD:
    def __init__(self, signals):
        self.signals = signals

    def __repr__(self):
        return 'Total signals = ' + str(len(self.signals))

    def getSignalsCombinatorics(self):
        return np.hstack([i.getSignalCombinatorics() for i in self.signals])

    def addOneToBitSeq(self, bitSeq, combinatorics):
        bitSeq[0] = bitSeq[0] + 1
        for i in range(len(bitSeq) - 1):
            if bitSeq[i] / combinatorics[i] >= 1:
                bitSeq[i] = 0
                bitSeq[i+1] = bitSeq[i+1] + 1


    def ExhaustiveSearch(self, snr=2, iter=1):
        totalsigs = len(self.signals)

        sigcombis = np.prod(self.getSignalsCombinatorics())

        currBitSequence = self.getSignalsCombinatorics() * 0
        for i in range(sigcombis):
            if i != 0: # do not add on the first one


        noise = 1