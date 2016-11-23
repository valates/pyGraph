from vertex import Vertex
from edge import Edge
from wvertex import WeightedVertex
from wedge import WeightedEdge

class Graph(object): #WHY DOESNT LINTER LIKE STATIC METHODS

    DEFAULT_VERTEX_WEIGHT = 0
    DEFAULT_EDGE_WEIGHT = 1
    NUMBER_TYPES = [int, long, float, complex]
    #surely there's a defined constant for the last one...

    def __init__(self, vertex_weights=False, edge_weights=False):
        self.vertex_weights = vertex_weights
        self.vertices = []
        self.vertex_ids = []
        self.num_vertices = 0
        self.edge_weights = edge_weights
        self.edges = []
        self.edge_ids = []
        self.num_edges = 0

    def get_vertex_ids(self):
        return self.vertex_ids

    def get_vertex_count(self):
        return self.num_vertices

    def get_edge_ids(self):
        return self.edge_ids

    def get_edge_count(self):
        return self.num_edges

    def make_vertices_weighted(self):
        self.change_weight_vertices(True)

    def make_vertices_unweighted(self):
        self.change_weight_vertices(False)

    def change_weight_vertices(self, weighted):
        new_vertices = []
        for vertex in self.vertices:
            if (weighted):
                vertex_equivalent = WeightedVertex(vertex.get_id(), DEFAULT_VERTEX_WEIGHT)
            else:
                vertex_equivalent = Vertex(vertex.get_id())
            new_vertices.append(vertex_equivalent)
        self.vertices = new_vertices
        self.vertex_weights = weighted

    def make_edges_weighted(self):
        self.change_weight_edges(True)

    def make_edges_unweighted(self):
        self.change_weight_edges(False)

    def change_weight_edges(self, weighted):
        new_edges = []
        for edge in self.edges:
            source, dest = edge.get_direction()
            if (weighted):
                edge_equivalent = WeightedEdge(source, dest, DEFAULT_EDGE_WEIGHT)
            else:
                edge_equivalent = Edge(source, dest)
            new_edges.append(edge_equivalent)
        self.edges = new_edges
        self.edge_weights = weighted

    def add_vertex(self, vert_id, weight=None):
        assert type(vert_id) == str
        assert vert_id not in self.vertex_ids
        if (self.vertex_weights):
            vertex_to_add = WeightedVertex(vert_id, weight)
        else:
            vertex_to_add = Vertex(vert_id)
        self.vertices.append(vertex_to_add)
        self.vertex_ids(vert_id)
        self.num_vertices += 1

    def remove_vertex(self, vert_id):
        assert type(vert_id) == str
        assert vert_id in self.vertex_ids
        for vertex in self.vertices:
            if vertex.get_id() == vert_id:
                self.vertices.remove(vertex)
                break
        self.vertex_ids.remove(vert_id)
        self.num_vertices -= 1
        for vertex in self.vertices:
            source, dest = vert_id, vertex.get_id()
            if (str((source, dest)) in self.edge_ids):
                self.remove_edge(source, dest)
            source, dest = dest, source
            if (str((source, dest)) in self.edge_ids):
                self.remove_edge(source, dest)

    def add_edge(self, source, dest, weight=None):
        assert type(source) == str
        assert source in self.vertex_ids
        assert type(dest) == str
        assert dest in self.vertex_ids
        new_edge_id = str((source, dest))
        assert new_edge_id not in self.edge_ids
        if (self.edge_weights):
            assert weight is not None
            edge_to_add = WeightedEdge(source, dest, weight)
        else:
            edge_to_add = Edge(source, dest)
        self.edges.append(edge_to_add)
        self.edge_ids.append(new_edge_id)
        self.num_edges += 1

    def remove_edge(self, source, dest):
        assert type(source) == str
        assert source in self.vertex_ids
        assert type(dest) == str
        assert dest in self.vertex_ids
        edge_id = str((source, dest))
        assert edge_id in self.edge_ids
        for edge in self.edges:
            cur_source, cur_dest = edge.get_direction()
            if (cur_source == source) and (cur_dest == dest):
                self.edges.remove(edge)
                break
        self.edge_ids.remove(edge_id)
        self.num_edges -= 1

    def change_vertex_weight(self, vertex_id, weight):
        assert type(vertex_id) == str
        assert vertex_id in self.vertex_ids
        assert self.vertex_weights is True
        edit_index = find_index(vertex_id, self.vertex_ids)
        assert type(self.vertices[edit_index]) is WeightedVertex
        self.vertices[edit_index].set_vertex_weight(weight)

    def convert_path_to_str(path):
        assert type(path) == tuple
        assert len(path) == 2
        return str(path)

    def change_edge_weight(self, edge_id, weight):
        if type(edge_id) == tuple:
            edge_id = convert_path_to_str(edge_id)
        assert type(edge_id) == str
        assert edge_id in self.edge_ids
        assert self.edge_weights is True
        edit_index = find_index(edge_id, self.edge_ids)
        assert type(self.edges[edit_index]) is WeightedEdge
        self.edge[edit_index].set_edge_weight(weight)

    def find_index(id_to_find, id_list):
        assert type(id_to_find) == str
        assert type(id_list) == list
        for i in range(len(id_list)):
            cur_entry = id_list[i]
            assert type(cur_entry) == str
            if cur_entry == id_to_find:
                return i

    def get_vertex_weight(self, vertex_id):
        assert type(vertex_id) == str
        assert vertex_id in self.vertex_ids
        assert self.vertex_weights is True
        edit_index = find_index(vertex_id, self.vertex_ids)
        assert type(self.vertices[edit_index]) is WeightedVertex
        return self.vertices[edit_index].get_vertex_weight()

    def get_edge_weight(self, edge_id):
        assert type(edge_id) == str
        assert edge_id in self.edge_ids
        assert self.vertex_weights is True
        edit_index = find_index(edge_id, self.edge_ids)
        assert type(self.edges[edit_index]) is WeightedEdge
        return self.edges[edit_index].get_edge_weight()

    def set_vertices_weights(self, mul_vert_ids, weights):
        """ Wrap around is intentional. In the event a user
            wishes to set every vertex to one weight, only a single
            value is passed and it is converted to a list. """
        if type(weights) in NUMBER_TYPES:
            weights = [weights]
        assert type(weights) == list
        assert type(mul_vert_ids) == list
        assert len(mul_vert_ids) >= len(weights)
        for i in range(len(mul_vert_ids)):
            cur_vert_id = mul_vert_ids[i]
            assert type(cur_vert_id) == str
            self.change_vertex_weight(cur_vert_id, weights[(i % len(weights))])

    def set_edges_weights(self, mul_edge_ids, weights):
        """ Wrap around is intentional. In the event a user
            wishes to set every vertex to one weight, only a single
            value is passed and it is converted to a list. """
        if type(weights) in NUMBER_TYPES:
            weights = [weights]
        assert type(weights) == list
        assert type(mul_edge_ids) == list
        assert len(mul_edge_ids) >= len(weights)
        for i in range(len(mul_edge_ids)):
            cur_edge_id = mul_edge_ids[i]
            if type(cur_edge_id) == tuple:
                cur_edge_id = convert_path_to_str(cur_edge_id)
            assert (cur_edge_id == str)
            self.change_edge_weight(cur_edge_id, weights[(i % len(weights))])
