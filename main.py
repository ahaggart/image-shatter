import argparse

import cv2 as cv

from blobs import caluculate_colorspace_distances, grow_blobs
from polygons import find_edges, order_edges
from colorize import color_blobs, color_edges, color_ordered


def main(config):
    image = cv.imread('img/' + config.file)
    width, height = image.shape[:2]

    print("Calculating colorspace distances...")
    xdist, ydist = caluculate_colorspace_distances(image)

    print("Growing blobs...")
    blobs = grow_blobs(width, height, xdist, ydist)
    print("> Num blobs: {}".format(blobs.index))

    edges = find_edges(blobs)

    ordered = order_edges(edges)

    print("Coloring blobs...")
    # colors = color_blobs(image, blobs)
    # colors = color_edges(edges, width, height)
    colors = color_ordered(ordered, width, height)

    print("Writing image...")
    cv.imwrite('out/' + config.file, colors)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        help="the path to the file within the img/ directory",
    )
    main(parser.parse_args())
