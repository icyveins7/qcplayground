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

class OptimalMUD:
    def __init__(self, signals):
        self.signals = signals

    def __repr__(self):
        return 'Total signals = ' + str(len(self.signals))

    def ExhaustiveSearch(self, snr=2, iter=1):
        noise = 1