from vertex import Vertex
from edge import Edge
from wvertex import WeightedVertex
from wedge import WeightedEdge

class Graph(object): #WHY DOESNT LINTER LIKE STATIC METHODS

    DEFAULT_VERTEX_WEIGHT = 0
    DEFAULT_EDGE_WEIGHT = 1
    NUMBER_TYPES = [int, long, float, complex]

    def __init__(self, undirected=False, vertex_weights=False, edge_weights=False):
        self.undirected = undirected
        self.vertex_weights = vertex_weights
        self.vertices = {}
        self.num_vertices = 0
        self.edge_weights = edge_weights
        self.edges = {}
        self.num_edges = 0

    def adjacent(self, vertex_x, vertex_y):
        assert vertex_x in self.vertices
        assert vertex_y in self.vertices
        if (self.num_edges < self.num_vertices):
            return (str((vertex_x, vertex_y)) in self.edges) or (str((vertex_y, vertex_x)) in self.edges)
        return (vertex_y in self.neighbors(vertex_x)) or (vertex_x in self.neighbors(vertex_y))

    def neighbors(self, vertex_id, disallow_self_neighbor=False, return_vertex_copies=False):
        """ A vertex is considered a neighbor of itself if a directed
             edge is from a vertex to itself. Setting
             disallow_self_neighbor to False prevent considering the
             vertex's self as a neighbor. """
        assert vertex_id in self.vertices
        adj_vertices = self.vertices[vertex_id].get_nbors()
        if (return_vertex_copies):
            adj_copies = []
            for cur_id in adj_vertices:
                if (disallow_self_neighbor is False) or ((disallow_self_neighbor) and (cur_id != vert_id)):
                    adj_copies.append(self.vertices[cur_id])
            return adj_copies
        if (disallow_self_neighbor):
            adj_vertices = [ver_id for ver_id in adj_vertices if ver_id != vertex_id]
        return adj_vertices

    def get_vertex_ids(self):
        return self.vertices.keys()

    def get_vertex_count(self):
        return self.num_vertices

    def get_edge_ids(self):
        return self.edges.keys()

    def get_edge_count(self):
        if (self.undirected):
            return (self.num_edges / 2)
        return self.num_edges

    def make_vertices_weighted(self):
        self.change_weight_vertices(True)

    def make_vertices_unweighted(self):
        self.change_weight_vertices(False)

    def change_weight_vertices(self, weighted):
        new_vertices = {}
        for vertex in self.vertices():
            cur_id = vertex.get_id()
            if (weighted):
                vertex_equivalent = WeightedVertex(cur_id, DEFAULT_VERTEX_WEIGHT)
            else:
                vertex_equivalent = Vertex(cur_id)
            new_vertices[cur_id] = vertex_equivalent
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
            new_edges[str((source, dest))] = edge_equivalent
        self.edges = new_edges
        self.edge_weights = weighted

    def add_vertex(self, vert_id, weight=None):
        assert type(vert_id) == str
        id_blacklist(vert_id)
        assert vert_id not in self.vertices
        if (self.vertex_weights):
            vertex_to_add = WeightedVertex(vert_id, weight)
        else:
            vertex_to_add = Vertex(vert_id)
        self.vertices[vertex_id] = vertex_to_add
        self.num_vertices += 1

    def remove_vertex(self, vert_id):
        assert type(vert_id) == str
        assert vert_id in self.vertices
        del self.vertices[vert_id]
        self.num_vertices -= 1
        for vertex in self.vertices:
            source, dest = vert_id, vertex.get_id()
            if (str((source, dest)) in self.edges):
                self.remove_edge(source, dest)
            source, dest = dest, source
            if (str((source, dest)) in self.edges):
                self.remove_edge(source, dest)

    def add_edge(self, source, dest, weight=None):
        assert type(source) == str
        id_blacklist(source)
        assert source in self.vertices
        assert type(dest) == str
        id_blacklist(dest)
        assert dest in self.vertices
        new_edge_id = str((source, dest))
        assert new_edge_id not in self.edges
        if (self.edge_weights):
            assert weight is not None
            edge_to_add = WeightedEdge(source, dest, weight)
        else:
            edge_to_add = Edge(source, dest)
        self.edges[new_edge_id] = edge_to_add
        self.num_edges += 1
        self.vertices[source].add_nbor(dest)
        if (self.undirected):
            self.add_edge(dest, source, weight)

    def remove_edge(self, source, dest):
        assert type(source) == str
        assert source in self.vertices
        assert type(dest) == str
        assert dest in self.vertices
        edge_id = str((source, dest))
        assert edge_id in self.edges
        del self.edges[edge_id]
        self.num_edges -= 1
        self.vertices[source].remove_nbor(dest)
        if (self.undirected):
            self.remove_edge(dest, source)

    def id_blacklist(cur_id):
        assert ',' not in cur_id
        assert '(' not in cur_id
        assert ')' not in cur_id

    def set_vertex_value(self, vertex_id, weight):
        assert type(vertex_id) == str
        assert vertex_id in self.vertices
        assert self.vertex_weights is True
        assert type(self.vertices[vertex_id]) is WeightedVertex
        self.vertices[vertex_id].set_vertex_weight(weight)

    def set_edge_value(self, edge_id, weight):
        if type(edge_id) == tuple:
            assert len(edge_id) == 2
            edge_id = str(edge_id)
        assert type(edge_id) == str
        assert edge_id in self.edges
        assert self.edge_weights is True
        assert type(self.edges[edge_id]) is WeightedEdge
        self.edges[edge_id].set_edge_weight(weight)
        if (self.undirected):
            self.set_edge_value(get_reverse_id(edge_id), weight)

    def get_reverse_id(input_id):
        id_holder = input_id.replace("(", "")
        id_holder = id_holder.replace(")", "")
        id_holder = id_holder.split(", ")
        return str((id_holder[1], id_holder[1]))

    def get_vertex_value(self, vertex_id):
        assert type(vertex_id) == str
        assert vertex_id in self.vertices
        assert self.vertex_weights is True
        assert type(self.vertices[vertex_id]) is WeightedVertex
        return self.vertices[vertex_id].get_vertex_weight()

    def get_edge_value(self, edge_id):
        assert type(edge_id) == str
        assert edge_id in self.edges
        assert self.edge_weights is True
        assert type(self.edges[edge_id]) is WeightedEdge
        return self.edges[edge_id].get_edge_weight()

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
            self.set_vertex_value(cur_vert_id, weights[(i % len(weights))])

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
                assert len(cur_edge_id) == 2
                cur_edge_id = str(cur_edge_id)
            assert (cur_edge_id == str)
            self.set_edge_value(cur_edge_id, weights[(i % len(weights))])

    def generate_adj_matrix(self):
        #add dictionaries?
        adj_matrix = {}
        for vertex_key in self.vertices:
            for vertex_key2 in self.vertices:
                entry_key = str((vertex_key, vertex_key2))
                if entry_key in self.edges:
                    adj_matrix[entry_key] = 1
                else:
                    adj_matrix[entry_key] = 0
        return adj_matrix
