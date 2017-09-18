"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    f = open(file_path, "r", encoding="utf-8")
    # graphs are dynamically maintained not necessarily based on the nodeCount.
    # nodeCount = int(f.readline().strip())
    for line in f:
        if(line.strip() != '' and ':' in line):
            graph.add_edge(parse_line_to_edge(graph, line))
    f.close()
    return graph

def parse_line_to_edge(graph, line):
    tokens = line.split(':')
    from_node = Node(int(tokens[0]))
    to_node = Node(int(tokens[1]))
    edge = Edge(from_node, to_node, int(tokens[2]))
    return edge

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)

    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        if node_1 in self.adjacency_list:
            return node_2 in (edge.to_node for edge in self.adjacency_list[node_1])
        return False

    def neighbors(self, node):
        neighbors_ = []
        if node in self.adjacency_list:
            for to_node in (edge.to_node for edge in self.adjacency_list[node]):
                neighbors_.append(to_node)
        return neighbors_

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            return True
        return False

    def remove_node(self, node):
        is_node_removed = False
        # Remove the node itself if present
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            is_node_removed = True
        # Remove any edges that might be pointing to the removed node
        for any_node in self.adjacency_list:
            for edge in (edge for edge in self.adjacency_list[any_node] if edge.to_node.__eq__(node)):
                self.remove_edge(edge)
        return is_node_removed

    def add_edge(self, edge):
        # Add the from_node first if it is not in adjacency_list
        if edge.from_node not in self.adjacency_list:
            self.add_node(edge.from_node)
        # Add the edge if not present in the adjacency_list
        if edge not in self.adjacency_list[edge.from_node]:
            self.adjacency_list[edge.from_node].append(edge)
            return True
        return False

    def remove_edge(self, edge):
        if edge.from_node in self.adjacency_list:
            if edge in self.adjacency_list[edge.from_node]:
                self.adjacency_list[edge.from_node].remove(edge)
                return True
        return False

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if self.__contains_node(node_1) and self.__contains_node(node_2):
            node_1_index = self.__get_node_index(node_1)
            node_2_index = self.__get_node_index(node_2)
            return self.adjacency_matrix[node_1_index][node_2_index] > 0
        return False

    def neighbors(self, node):
        # Finds all matrix cells that contains "1" and returns the corresponding neighbor nodes
        neighbors_ = []
        if self.__contains_node(node):
            node_index = self.__get_node_index(node)
            for col in range(0, len(self.adjacency_matrix[node_index])):
                if self.adjacency_matrix[node_index][col] > 0:
                    neighbors_.append(self.nodes[col])
        return sorted(neighbors_, key=lambda n: n.data)

    def add_node(self, node):
        # This implementation does not use node.data as index but uses the index of self.nodes[node]
        # as the matrix index, to save space
        # The following is matrix for below node list
        # self.nodes = [5001, 1, 500, 10]
        #         0(5001)   1(1)   2(500)   3(10)
        # 0(5001)    0       0      1        1
        # 1(1)       0       0      0        0
        # 2(500)     1       1      0        0
        # 3(10)      0       1      1        0
        if not self.__contains_node(node):
            self.nodes.append(node)
            if not self.adjacency_matrix:
                # Initialize the empty matrix
                self.adjacency_matrix.append([])
            else:
                # Extend the existing matrix with new rows of "0"s
                self.adjacency_matrix.append([0 for i in range(0, len(self.adjacency_matrix[0]))])
            # Add new columns to match the new row size and initialize the new column values to "0"
            for row in range(0, len(self.adjacency_matrix)):
                self.adjacency_matrix[row].append(0)
            return True
        return False

    def remove_node(self, node):
        if self.__contains_node(node):
            node_index = self.__get_node_index(node)
            self.nodes.remove(node)
            for row in range(0, len(self.adjacency_matrix[node_index])):
                del self.adjacency_matrix[row][node_index]
            del self.adjacency_matrix[node_index]
            return True
        return False

    def add_edge(self, edge):
        if not self.__contains_node(edge.from_node):
            self.add_node(edge.from_node)
        if not self.__contains_node(edge.to_node):
            self.add_node(edge.to_node)
        from_node_index = self.__get_node_index(edge.from_node)
        to_node_index = self.__get_node_index(edge.to_node)
        if self.adjacency_matrix[from_node_index][to_node_index] == 0:
            self.adjacency_matrix[from_node_index][to_node_index] = edge.weight
            return True
        return False

    def remove_edge(self, edge):
        if not self.__contains_node(edge.from_node):
            self.add_node(edge.from_node)
        if not self.__contains_node(edge.to_node):
            self.add_node(edge.to_node)
        from_node_index = self.__get_node_index(edge.from_node)
        to_node_index = self.__get_node_index(edge.to_node)
        if self.adjacency_matrix[from_node_index][to_node_index] > 0:
            self.adjacency_matrix[from_node_index][to_node_index] = 0
            return True
        return False

    def __get_node_index(self, node):
        """helper method to find node index"""
        if node in self.nodes:
            return self.nodes.index(node)
        return None

    def __contains_node(self, node):
        return node in self.nodes

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if self.edges:
            for edge in self.edges:
                node_list = [edge.from_node, edge.to_node]
                if node_1 in node_list and node_2 in node_list:
                    return True
        return False

    def neighbors(self, node):
        neighbors_ = []
        if self.edges:
            for to_node in (e.to_node for e in self.edges if e.from_node.__eq__(node)):
                neighbors_.append(to_node)
        return neighbors_

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            return True
        return False

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            if self.edges:
                for edge in (e for e in self.edges if e.to_node.__eq__(node)):
                    self.edges.remove(edge)
            return True
        return False

    def add_edge(self, edge):
        if edge not in self.edges:
            if edge.from_node not in self.nodes:
                self.add_node(edge.from_node)
            if edge.to_node not in self.nodes:
                self.add_node(edge.to_node)
            self.edges.append(edge)
            return True
        return False

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        return False

