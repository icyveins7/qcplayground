import numpy as np
import scipy as sp
import cMUDclasses as cm
import matplotlib.pyplot as plt

qpsk_bits = np.random.randint(0,4,100)
qpsk_sig = cm.PSKSignal(qpsk_bits, 4)
print(qpsk_sig)
print(qpsk_sig.getBits())
print(qpsk_sig.getM())

fig = plt.figure()
ax = plt.plot(np.real(qpsk_sig.getSymbols()), np.imag(qpsk_sig.getSymbols()), 'r.')
plt.show()