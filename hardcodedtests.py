import numpy as np
import scipy as sp

x0 = np.array([1,1]).reshape((2,1))
x1 = np.array([1,-1]).reshape((2,1))
x2 = np.array([-1,1]).reshape((2,1))
x3 = np.array([-1,-1]).reshape((2,1))

x = x1

H = np.array([[3.0, 1.0],
              [1.0, 0]])
y = H@x
y_normed = y/np.linalg.norm(y)
print(y_normed)


def MLcost(x,H,y):
    c = np.asmatrix(y-H@x)

    return c.H * c

print('ML Costs:')
print(MLcost(x0,H,y))
print(MLcost(x1,H,y))
print(MLcost(x2,H,y))
print(MLcost(x3,H,y))

def DOTcost(x,H,y_normed):
    x_normed = np.asmatrix(x)/np.linalg.norm(x)

    # Hx_normed = np.asmatrix(H@x_normed)
    # print(Hx_normed)
    H_normed = np.asmatrix(H)/abs(np.linalg.det(H))
    Hx_normed = np.asmatrix(H_normed@x_normed)

    # Hx_normed = Hx/np.linalg.norm(Hx)
    y_normed = np.asmatrix(y)/np.linalg.norm(y)

    c = y_normed.H * Hx_normed
    return c

print('Dot Prod Costs (Higher is better): ')
print(DOTcost(x0,H,y_normed))
print(DOTcost(x1,H,y_normed))
print(DOTcost(x2,H,y_normed))
print(DOTcost(x3,H,y_normed))

print('Checking matrix norm')
print(np.linalg.norm(H))

print('Checking matrix det')
print(np.linalg.det(H))

print('Checking np.dot')
print(np.dot(y_normed.transpose(), y_normed))