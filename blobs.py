import numpy as np

from util import iget, iset


def dist(a, b):
    s = 0
    for c in zip(a, b):
        d = int(c[0]) - c[1]
        s += d*d
    return s


def caluculate_colorspace_distances(image):
    width, height = image.shape[:2]
    xdist = np.zeros((width-1, height))
    ydist = np.zeros((width, height-1))

    for y in range(0, height):
        for x in range(0, width-1):
            xdist[x][y] = dist(image[x][y], image[x+1][y])

    for x in range(0, width):
        for y in range(0, height-1):
            ydist[x][y] = dist(image[x][y], image[x][y+1])

    return xdist, ydist


class Blobs:
    def __init__(self, width, height, xdists, ydists):
        self.width = width
        self.height = height
        self.indices = np.zeros((width, height))
        self.blobs = [None]
        self.index = 0
        self.xdists = xdists
        self.ydists = ydists
        self.thresh = 128

        self.queue = []

    def get_blobs(self):
        return self.blobs[1:]

    def tryGrow(self, pix, pixels, dist):
        if pix in pixels:
            if dist < self.thresh:
                pixels.remove(pix)
                self.queue.append((pix, pixels))

    def seed(self, pix, pixels):
        self.index += 1
        self.queue.append((pix, pixels))
        while self.queue:
            self.grow(*self.queue.pop(0))

    def grow(self, pix, pixels):
        iset(self.indices, pix, self.index)

        if len(self.blobs) < self.index + 1:
            self.blobs.append([])
        self.blobs[self.index].append(pix)

        xg = (pix[0] + 1, pix[1])
        xl = (pix[0] - 1, pix[1])
        yg = (pix[0], pix[1] + 1)
        yl = (pix[0], pix[1] - 1)

        if xg[0] < self.width:
            self.tryGrow(xg, pixels, iget(self.xdists, pix))

        if pix[0] > 0:
            self.tryGrow(xl, pixels, iget(self.xdists, xl))

        if yg[1] < self.height:
            self.tryGrow(yg, pixels, iget(self.ydists, pix))

        if pix[1] > 0:
            self.tryGrow(yl, pixels, iget(self.ydists, yl))


def grow_blobs(width, height, xdist, ydist):
    pixels = set()
    for x in range(0, width):
        for y in range(0, height):
            pixels.add((x, y))
    blobs = Blobs(width, height, xdist, ydist)
    while pixels:
        blobs.seed(pixels.pop(), pixels)
    return blobs
