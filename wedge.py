from edge import Edge


class WeightedEdge(Edge):

    def __init__(self, source, dest, weight):
        super().__init__(source, dest)
        assert weight is not None
        self.weight = weight

    def set__edge_weight(self, weight):
        assert weight is not None
        self.weight = weight

    def get_edge_weight(self):
        return self.weight
