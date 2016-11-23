class Edge(object):

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest

    def get_id(self):
        """ The id of an edge, to avoid collisions, is simply
        the tuple of the edge's source and destination typecasted
        to a string. Such an id ensures no duplicate edges are
        added. """
        return str((self.source, self.dest))

    def get_direction(self):
        return self.source, self.dest
