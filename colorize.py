import numpy as np

from util import iget, iset


def get_avg_blob_color(image, blob):
    rgb = np.array([0.0, 0.0, 0.0])
    for pix in blob:
        rgb = rgb + iget(image, pix)

    return np.true_divide(rgb, len(blob))


def color_blobs(image, blobs):
    width, height = image.shape[:2]
    colors = np.zeros((width, height, 3))
    for blob in blobs.get_blobs():
        avg = get_avg_blob_color(image, blob)
        for pix in blob:
            iset(colors, pix, avg)
    return colors


def color_edges(edges, width, height, color=(255, 255, 255)):
    image = np.zeros((width, height, 3))
    for edge in edges:
        for pix in edge:
            iset(image, pix, color)
    return image


def color_ordered(edges, width, height, steps=64, color=(255, 255, 255)):
    step = 0
    color_step = np.true_divide(color, steps)
    image = np.zeros((width, height, 3))
    skip = 0
    for edge in edges:
        if skip == 5:
            skip = 0
            continue
        else:
            skip += 1
        for pix in edge:
            iset(image, pix, np.multiply(color_step, step))
            step = (step + 1) % steps
    return image
