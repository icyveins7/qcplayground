import numpy as np

idx = np.arange(16)
binary = [np.binary_repr(i,4) for i in idx]

def processQPSKString(qpskstring):
    b = 1
    if qpskstring[0] is '1':
        b = -1

    if qpskstring[1] is '1':
        b = b - 1j
    else:
        b = b + 1j

    return b

def processBinaryStrings(binary):
    vectors = np.asmatrix(np.zeros((2,len(binary)), dtype=np.complex64))

    for i in range(len(binary)):
        q1 = binary[i][0:2]
        q2 = binary[i][2:]

        vectors[0,i] = processQPSKString(q1)
        vectors[1,i] = processQPSKString(q2)

    return vectors

vectors = processBinaryStrings(binary)

H = np.matrix([[2,1],
               [1,0]])

def splitH_realimag(H):
    b = np.vstack((np.hstack((H, np.zeros((2, 2)))), np.hstack((np.zeros((2, 2)), H))))
    return b

splitH = splitH_realimag(H)
print(splitH)
splitH_sqr = splitH.H * splitH
print(splitH_sqr)



HH = np.matrix([[0,2],
                [2,0]], dtype=np.complex64)
cf = np.diag(vectors.H * HH * vectors)

print(vectors[:,2])
print(np.real(cf[2]))
print(np.real(cf))
print(binary)