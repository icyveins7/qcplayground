import numpy as np
import scipy as sp
import cMUDclasses as cm
import matplotlib.pyplot as plt

numBits = 1
m = 4 # m-ary signal
qpsk_bits = np.random.randint(0,m,numBits)
qpsk_sig = cm.PSKSignal(qpsk_bits, m)

# test some methods
print(qpsk_sig)
print(qpsk_sig.getBits())
print(qpsk_sig.getM())
print(qpsk_sig.getSignalCombinatorics())

qpsk_bits2 = np.random.randint(0,m,numBits)
qpsk_sig2 = cm.PSKSignal(qpsk_bits2, m)

cmud = cm.OptimalMUD([qpsk_sig, qpsk_sig2])
print(cmud.getSignalsCombinatorics())

# test more methods
testSeq = np.array([3,1], dtype=np.int32)
cmud.addOneToBitSeq(testSeq, cmud.getSignalsCombinatorics())
print(testSeq)

fig = plt.figure()
ax = plt.plot(np.real(qpsk_sig.getSymbols()), np.imag(qpsk_sig.getSymbols()), 'r.')
plt.show()