from vertex import Vertex

class WeightedVertex(Vertex):

    def __init__(self, vertex_id, weight):
        super().__init__(vertex_id)
        assert weight is not None
        self.weight = weight

    def set_vertex_weight(self, weight):
        assert weight is not None
        self.weight = weight

    def get_vertex_weight(self):
        return self.weight
