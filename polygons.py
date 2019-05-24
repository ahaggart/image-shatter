from util import iget


def neighborFunc(width, height):
    """Return a generator for valid neighbors in a grid of given dimensions.
    """
    def getNeighbors(pix):
        x, y = pix
        if x > 0:
            yield x-1, y
        if x < width - 1:
            yield x+1, y
        if y > 0:
            yield x, y - 1
        if y < height - 1:
            yield x, y + 1
    return getNeighbors


def find_edges(blobs):
    """Find edge pixels for a list of blobs.
    """
    edges = []
    for blob in blobs.get_blobs():
        edges.append(collect_edges(blob, blobs.indices))
    return edges


def collect_edges(blob, indices):
    """Collect a dictionary of edge pixels for a given blob.
    """
    edges = {}
    neighbors = neighborFunc(*indices.shape[:2])
    for pix in blob:
        index = iget(indices, pix)
        others = set()  # collect neighboring pixels residing in other blobs
        for neighbor in neighbors(pix):
            if iget(indices, neighbor) != index:
                others.add(neighbor)
        if others:  # add pixel to dictionary only if it has outside neighbors
            edges[pix] = others
    return edges


def cornerNeighborsCW(coord):
    """Return a list of corner neighbors in clockwise order.
    """
    x, y = coord
    yield x, y+1
    yield x+1, y+1
    yield x+1, y
    yield x+1, y-1
    yield x, y-1
    yield x-1, y-1
    yield x-1, y
    yield x-1, y+1


def order_edges(edges):
    """Order the pixels in a set of edges.
    """
    ordered = []
    for edge in edges:
        ordered.append(order_edge(edge))
    return ordered


def order_edge(edge):
    """Order a set of edge pixels
    """
    # use a list comprehension so we can iterate over whatever collection type
    # is passed in. Could optimize for dictionary, set, etc
    pixels = set([pix for pix in edge])
    ordered = []
    pix = None
    while pixels:
        if pix is None:
            pix = pixels.pop()
        ordered.append(pix)
        neighbors = cornerNeighborsCW(pix)
        pix = None
        for neighbor in neighbors:
            if neighbor in pixels:
                pixels.remove(neighbor)
                pix = neighbor
                break  # break on first neighbor -> move clockwise around edge
    return ordered
