import numpy as np
from scipy.sparse.linalg import cgs
from scipy import sparse
import numpy.fft as fft

def tvBregman(f, ro1, ro2, gamma, beta, iter=1000):
    u = f
    dx = np.zeros_like(f)
    dy = np.zeros_like(f)
    bx = np.zeros_like(f)
    by = np.zeros_like(f)
    bz = np.zeros_like(f)

    z = f
    err = 1
    tol = 5 * 10**-6
    index = 0
    err_old = err

    while (err > tol) and err <= err_old:
        up = u
        err_old = err

        u = calculateUProblem(u, dx, dy, z, bx, by, bz, f, ro1, ro2)

        Ix = (np.roll(u, -1, axis=1) - u)
        Iy = (np.roll(u, -1, axis=0) - u)

        dx = shrink(Ix+bx, 1/ro1)
        dy = shrink(Iy+by, 1/ro1)

        s = beta*gamma / 2 - ro2*(u+bz)
        # s = lam*gamma*f - beta*gamma + 2*ro2*(u+bz)
        # s = np.divide(s, 2*(gamma*lam + 2*ro2))

        t = 2*ro2*gamma*beta*f

        z = (-s + np.sqrt(s**2 + t)) / (2*ro2)
        # z = s + np.sqrt(s**2 + t)

        bx = bx + Ix - dx
        by = by + Iy - dy
        bz = bz + u - z
        # bz = bz

        err = np.linalg.norm(u - up)/np.linalg.norm(u)
        index += 1

    # u = u*255
    # u[u<0] = 0
    # u[u>255] = 255

    return u


def shrink(x, lamda):
    b = np.abs(x)
    b = b - lamda
    b[b < 0] = 0
    return np.multiply(np.sign(x), b)


def calculateUProblem(u, dx, dy, z, bx, by, bz, f, ro1, ro2):
    norm = ro2 + 4*ro1

    unew = ro1*(np.roll(u, -1, axis=1) + np.roll(u, 1, axis=1)  # u(i+1,j) + u(i−1,j)
                + np.roll(u, -1, axis=0) + np.roll(u, 1,
                                                   axis=0)  # u(i,j+1) + u(i,j−1)
                + np.roll(dx, 1, axis=1) - dx
                + np.roll(dy, 1, axis=0) - dy
                - np.roll(bx, 1, axis=1) + bx
                - np.roll(by, 1, axis=0) + by
                ) + ro2 * (z - bz)

    unew = unew / norm
    return unew


def tvDenoise_Dong_Bregman(f, beta, ro1, ro2, iter=1000):
    print('ok');
    u = f
    dx = np.zeros_like(f)
    dy = np.zeros_like(f)
    bx = np.zeros_like(f)
    by = np.zeros_like(f)
    bz = np.zeros_like(f)

    z = f
    err = 1
    tol = 5 * 10**-6
    index = 0
    err_old = err

    while (err > tol) and err <= err_old:
        up = u
        err_old = err

        u = calculateUProblem(u, dx, dy, z, bx, by, bz, f, ro1, ro2)

        Ix = (np.roll(u, -1, axis=1) - u)
        Iy = (np.roll(u, -1, axis=0) - u)

        dx = shrink(Ix+bx, 1/ro1)
        dy = shrink(Iy+by, 1/ro1)

        z = calculateZ(f, u, beta, ro2, bz)

        bx = bx + Ix - dx
        by = by + Iy - dy
        bz = bz + u - z

        err = np.linalg.norm(u - up)/np.linalg.norm(u)
        index += 1

    return u

def calculateUProblem(u, dx, dy, z, bx, by, bz, f, ro1, ro2):
    norm = ro2 + 4*ro1

    unew = ro1*(np.roll(u, -1, axis=1) + np.roll(u, 1, axis=1)  # u(i+1,j) + u(i−1,j)
        + np.roll(u, -1, axis=0) + np.roll(u, 1, axis=0) #u(i,j+1) + u(i,j−1)
        + np.roll(dx, 1, axis=1) - dx
        + np.roll(dy, 1, axis=0) - dy
        - np.roll(bx, 1, axis=1) + bx
        - np.roll(by, 1, axis=0) + by
    ) + ro2 * (z - bz)

    unew = unew / norm
    return unew

def calculateZ(F, U, beta, ro, b):
    lamda = 1
    F[F==0] = 0.005
    Z = F
    gamma = 18
    for i in range(10):
        Gz = (Z**3)*ro + (Z**2)*(beta*gamma/F - ro*(U+b)) - (Z**1.5)*(beta*gamma*(F**-0.5)) + beta*lamda*(Z-F)
        DGz = (Z**2)*3*ro + Z*2*(beta*gamma/F - ro*(U+b)) - (Z**0.5)*1.5*(beta*gamma*(F**-0.5)) + beta*lamda
        Z = Z - Gz/DGz
        Z[Z<0] = 0.005
    return Z

def splitBregmanSecondOrderTV(f, beta, ro1, ro2, ro3, alfa1 = 0.1, alfa2 = 0.1):
    f = f.astype(complex)
    padnum = 10
    f = np.pad(f,(padnum, padnum), 'symmetric')
    m,n = np.shape(f)
    u = np.array(f)
    z = np.array(f)

    w1 = np.zeros_like(f)
    w2 = np.zeros_like(f)
    v1 = np.zeros_like(f)
    v2 = np.zeros_like(f)
    v3 = np.zeros_like(f)

    b11 = np.zeros_like(f)
    b12 = np.zeros_like(f)
    b21 = np.zeros_like(f)
    b22 = np.zeros_like(f)
    b23 = np.zeros_like(f)

    bz = np.zeros_like(f)

    eps = np.finfo(float).eps
    Y, X = np.meshgrid(np.arange(n), np.arange(m), sparse=False)
    G = np.cos(2*np.pi*X/m) + np.cos(2*np.pi*Y/n) - 2
    err = 1
    tol = 5 * 10**-6
    index = 0
    ite_number = 100
    eps = np.finfo(float).eps
    while err > tol and index <= ite_number:

        up = u
        ##################################################################
        # update u using FFT
        div_w_b = dxt(w1 - b11) + dyt(w2 - b12)
        div_v_b = dxt(dx(v1 - b21)) + dyt(dy(v2 - b22)) + 2*dyt(dxt(v3 - b23))

        gg = (ro3*(z - bz) - ro1*div_w_b + ro2*div_v_b)/ro3
        u = fft.ifftn(fft.fftn(gg) / (1 - 2*ro1*G/ro3 + 4*ro2*(G**2)/ro3))
        u = np.real(u)
        ##################################################################
        # update z

        z = calculateZSecondOrder(f, u, beta, ro3, bz)

         ##################################################################
        # update d using soft thresholding
        d1 = dx(u) + b11
        d2 = dy(u) + b12

        abs_d =  np.sqrt(d1**2 + d2**2 +  eps)
        if ro1 != 0:
            w1 = np.maximum(abs_d - (alfa1/(ro1/ro3)), 0) * d1 / abs_d
            w2 = np.maximum(abs_d - (alfa1/(ro1/ro3)), 0) * d2 / abs_d

        ##################################################################
        # update v using soft thresholding
        c1 = dxt(dx(u)) + b21
        c2 = dyt(dy(u)) + b22
        c3 = dy(dx(u)) + b23

        abs_c =  np.sqrt(c1**2 + c2**2 + c3**2 + eps)
        if ro2 != 0:
            v1 = np.maximum(abs_c - (alfa2/(ro2/ro3)), 0) * c1 / abs_c
            v2 = np.maximum(abs_c - (alfa2/(ro2/ro3)), 0) * c2 / abs_c
            v3 = np.maximum(abs_c - (alfa2/(ro2/ro3)), 0) * c3 / abs_c

        ##################################################################
        # update bregman iterative parameters
        b11 = d1 - w1
        b12 = d2 - w2
        b21 = c1 - v1
        b22 = c2 - v2
        b23 = c3 - v3

        bz = bz + u - z

        err = np.linalg.norm(u - up)/np.linalg.norm(u)
        index += 1
    u = u[padnum:m-padnum,padnum:n-padnum]
    return u

def calculateZSecondOrder(F, U, lamda, ro, b):
    s = U - (lamda/ro) + b
    z = s/2 + np.sqrt((s/2)**2 + lamda/ro*F)
    return z

def dx(u, isSym=False):
    ud = np.roll(u, 1, axis=1)
    dxu =  u - ud
    if isSym:
        n,m = np.shape(dxu)
        dxu[:, 0] = 0
    return dxu

def dxt(u, isSym=False):
    ud = np.roll(u, -1, axis=1)
    dxtu = ud - u
    if isSym:
        n,m = np.shape(dxtu)
        dxtu[:, m-1] = 0
    return dxtu

def dy(u, isSym=False):
    ud = np.roll(u, 1, axis=0)
    dyu =  u - ud
    if isSym:
        n,m = np.shape(dyu)
        dyu[0, :] = 0
    return dyu

def dyt(u, isSym=False):
    ud = np.roll(u, -1, axis=0)
    dytu = ud - u
    if isSym:
        n,m = np.shape(dytu)
        dytu[n-1, :] = 0
    return dytu
