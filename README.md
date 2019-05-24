# image-shatter

Apply a "shatter" or "crystallize" effect to an image.

## Processing

1. Blobbing

    Group similarly colored pixels into "blobs". The current implementation
    computes the color-space distance between adjacent pixels and compares it
    to a threshold value. Pixels closer than this threshold will be grouped
    into the same blob.
1. Edge Detection
1. Polygon Construction
1. Polygon Simplification
1. Triangulation
1. Antialiasing
1. Coloring

## References

[Calculating a convex hull](https://en.wikipedia.org/wiki/Graham_scan)