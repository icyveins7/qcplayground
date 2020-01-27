import numpy as np
import scipy as sp
import scipy.signal as sps
import qMUDclasses as qm

#delta_list = np.arange(1,32)
#delta_list = np.array([3])
delta_list = np.array([5])

for i in range(len(delta_list)):
    delta = delta_list[i]
    oracle = qm.DHAOracle(delta, 3)
    print(oracle.delta_bin)
    oracle.makeGates()
    txt = oracle.showGates(adjustBarrier=True)
    