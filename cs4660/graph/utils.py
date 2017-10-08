"""
utils package is for some quick utility methods

such as parsing
"""

from graph.graph import Edge
from graph.graph import Node

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.y < other.y or self.x < other.x

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    f = open(file_path, "r", encoding="utf-8")
    line_list = []
    for line in f:
        if line.strip() != '':
            line_list.append(list(line.strip()))
    f.close()

    build_graph_from_grid_lines(graph, line_list)

    return graph

def build_graph_from_grid_lines(graph, line_list):
    node_grid = []
    row_count = len(line_list)
    if row_count > 0:
        for i in range(1, row_count-1):
            y = i - 1
            col_count = len(line_list[i])
            if col_count > 2:
                node_grid.append([])
                for j in range(1, col_count-1, 2):
                    x = int((j - 1)/2)
                    tile_symbol = line_list[i][j] + line_list[i][j+1];
                    if not tile_symbol.__eq__("##"):
                        node_grid[y].append(Node(Tile(x, y, str(tile_symbol))))
                    else:
                        node_grid[y].append(None)

        for x in range(0, len(node_grid)):
            for y in range(0, len(node_grid[x])):
                if node_grid[x][y] is not None:
                    graph.add_node(node_grid[x][y])
                    if x > 0 and node_grid[x-1][y] is not None:
                        graph.add_edge(Edge(node_grid[x-1][y], node_grid[x][y], 1))
                        graph.add_edge(Edge(node_grid[x][y], node_grid[x-1][y], 1))
                    if y > 0 and node_grid[x][y-1] is not None:
                        graph.add_edge(Edge(node_grid[x][y-1], node_grid[x][y], 1))
                        graph.add_edge(Edge(node_grid[x][y], node_grid[x][y-1], 1))

    return

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2)), Node(Tile(2, 2)), 1)) => "S"
    """
    direction_dict = {
        (0,0):"",
        (1,0):"W",
        (-1,0):"E",
        (0,1):"N",
        (0,-1):"S"
    }

    path_string = ""

    if edges:
        for edge in edges:
            tile1 = edge.from_node.data
            tile2 = edge.to_node.data
            path_string = path_string + direction_dict[(tile1.x-tile2.x,tile1.y-tile2.y)]

    return path_string

def get_path_to_destination_node(graph, node_to_parent_dict, dest_node):
    """
    Returns the path to the from the root node to the dest_node using 
    the node->parent dictionary provided. The dictionary is created 
    as a by-product of any graph search algorithm
    """
    path = []

    if dest_node in node_to_parent_dict:
        # Start with the destination node to compute the path upward
        parent_node = node_to_parent_dict[dest_node]
        while parent_node is not None:
            # Add the edge to the top of list since we move bottom up
            path.insert(0, Edge(parent_node, dest_node, graph.distance(parent_node, dest_node)))
            dest_node = parent_node
            if dest_node in node_to_parent_dict:
                parent_node = node_to_parent_dict[dest_node]
            else:
                parent_node = None

    return path