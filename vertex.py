class Vertex(object):

    def __init__(self, vertex_id):
        self.vertex_id = vertex_id
        self.nbors = []

    def get_id(self):
        return self.vertex_id

    def add_nbor(self, nbor_id):
        assert nbor_id not in self.nbors
        self.nbors.append(nbor_id)

    def remove_nbor(self, nbor_id):
        assert nbor_id in self.nbors
        self.nbors.remove(nbor_id)

    def get_nbors(self):
        return self.nbors
