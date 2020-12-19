from denoise_type import DenoiseType
import numpy as np
from cv2 import cv2
import bregman
import os
from os.path import expanduser
home = expanduser("~")
path = os.path.dirname(os.path.realpath(__file__))


def openImage(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return image


def rescale1(image, l=0.1, u=1):
    image = image.astype(np.float64)
    inmin = image.min()
    inmax = image.max()
    return l + ((image-inmin)/(inmax-inmin))*(u-l)


def rescale255(image):
    image = rescale1(image, 0, 255)
    return image.astype(np.uint8)


def resizeImage(image, newWidth):
    height, width = image.shape[:2]
    newHeight = int((newWidth * height) / width)
    return cv2.resize(image, (newWidth, newHeight), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)


def saveImage(name, image):
    cv2.imwrite(home + "/" + name, image)
    return home + "/" + name


def customSaveImage(path, image):
    cv2.imwrite(path, image)


def addPossionNoise(image, peak=120.0):
    noisy = np.random.poisson(image / 255.0 * peak) / peak * 255
    noisy[noisy < 0] = 0
    noisy[noisy > 255] = 255
    noisy = rescale1(noisy)
    return noisy


def tvBregman(image, beta, ro1=1.2, ro2=1, gamma=0.8):
    return bregman.tvBregman(image, beta=beta, ro1=ro1, ro2=ro2, gamma=gamma)


def tvSecondOrder(image, beta, ro1, ro2, ro3, alfa1, alfa2):
    return bregman.splitBregmanSecondOrderTV(image, beta, ro1, ro2, ro3, alfa1, alfa2)


def tvDenoisePoisson(I0, iter=1000, dt=0.0004, beta=0.1):
    I = I0
    for i in range(iter):
        I_old = I

        div = calculateDiv(I)

        I[I == 0] = 0.9

        df = I0 / I

        It = div - beta*(1 - df)

        I = I + dt*It

        er = np.linalg.norm(I - I_old) / np.linalg.norm(I)
        if er < 5 * 10**-6:
            break
    return I


def tvDenoiseOnlyPoisson(I0, iter=1000, dt=0.0004, beta=0.1):
    I = I0
    for i in range(iter):
        I_old = I

        div = calculateDiv(I)

        I[I == 0] = 0.005

        df = I0 / I

        It = div - beta*(1 - df)

        I = I + dt*It

        er = np.linalg.norm(I - I_old) / np.linalg.norm(I)
        if er < 2 * 10**-6:
            break
    return I


def tvDenoiseOnlyPoissonModified(I0, iter=1000, dt=0.0004, beta=0.1):
    I = I0
    for i in range(iter):
        I_old = I

        div = calculateDiv(I)

        an = 1
        cn = -dt*I0

        bn = beta*dt - I - dt*div

        delta = bn ** 2 - np.multiply(4*an, cn)

        delta = np.sqrt(delta)

        uper = -bn + delta

        I = np.divide(uper, 2*an)

        er = np.linalg.norm(I - I_old) / np.linalg.norm(I)
        if er < 5 * 10**-6:
            break
    return I


def tvDenoisePoissonModified(I0, iter=1000, dt=0.1, beta=0.1):
    I = I0
    for i in range(iter):
        I_old = I

        div = calculateDiv(I)

        an = 1
        cn = -dt*I0

        bn = beta*dt - I - dt*div

        delta = bn ** 2 - np.multiply(4*an, cn)

        delta = np.sqrt(delta)

        uper = -bn + delta

        I = np.divide(uper, 2*an)

        er = np.linalg.norm(I - I_old) / np.linalg.norm(I)
        if er < 2 * 10**-6:
            break
    return I


def calculateDiv(I):
    ep2 = 1

    Ix = (np.roll(I, -1, axis=1) - np.roll(I, 1, axis=1)) / \
        2  # (I(j+1, k) - I(j-1, k))/2
    Iy = (np.roll(I, -1, axis=0) - np.roll(I, 1, axis=0)) / \
        2  # (I(j, k+1) - I(j, k-1))/2

    # I(j+1, k) + I(j-1, k) - 2*I
    Ixx = (np.roll(I, -1, axis=1) + np.roll(I, 1, axis=1) - 2*I)
    # I(j, k+1) + I(j, k-1) - 2*I
    Iyy = (np.roll(I, -1, axis=0) + np.roll(I, 1, axis=0) - 2*I)

    I1 = np.roll(I, -1, axis=(0, 1)) + np.roll(I, 1, axis=(0, 1))
    I2 = np.roll(I, [-1, 1], axis=(1, 0)) + np.roll(I, [1, -1], axis=(1, 0))
    Ixy = (I1 - I2)/4

    Num = np.multiply(Ixx, Iy ** 2 + ep2) - np.multiply(2 *
                                                        np.multiply(Ix, Iy), Ixy) + np.multiply(Iyy, Ix**2 + ep2)
    Den = (ep2 + Ix ** 2 + Iy ** 2) ** (3 / 2)
    div = np.divide(Num, Den)
    return div
