import numpy as np
import scipy as sp
import scipy.signal as sps
import qMUDclasses as qm

delta = 15

oracle = qm.DHAOracle(delta, 5)
print(oracle.delta_bin)
oracle.makeGates()
oracle.showGates()