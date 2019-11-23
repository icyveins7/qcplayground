from projectq import MainEngine  # import the main compiler engine
from projectq.ops import C, X, H, Measure  # import the operations we want to perform (Hadamard and measurement)
from projectq.backends import CircuitDrawer

circuit_backend = CircuitDrawer()
eng = MainEngine(circuit_backend)  # create a default compiler (the back-end is a simulator)
qubit = eng.allocate_qubit()  # allocate a quantum register with 1 qubit
qureg = eng.allocate_qureg(5)


H | qubit  # apply a Hadamard gate
Measure | qubit  # measure the qubit
C(X,3) | (qureg[0],qureg[1],qureg[2],qureg[3])

eng.flush()  # flush all gates (and execute measurements)
print("Measured {}".format(int(qubit)))  # converting a qubit to int or bool gives access to the measurement result
print(circuit_backend.get_latex())