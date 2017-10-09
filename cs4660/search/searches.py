"""
Searches module defines all different search algorithms
"""
from graph import stack
from graph import graph as g
import heapq

'''
class HeaNode that represents a graph node with a priority
'''
class HeapNode(object):
    def __init__(self, priority, node):
        '''
        creates default HeapNode with a given graph node and INFINITE priority
        '''
        self.priority = priority
        self.node = node

    def __eq__(self, other):
        '''
        default implementation for object equals
        '''
        return self.node.__eq__(other.node)

    def __lt__(self, other):
        '''
        default implementation for less-than
        '''        
        return self.priority < other.priority

    def __gt__(self, other):
        '''
        default implementation for greater-than
        '''        
        return self.priority > other.priority

    def __cmp__(self, other):
        '''
        default implementation for object compare
        '''        
        if self.priority < other.priority:
            return -1
        elif self.priority == other.priority:
            return 0
        else:
            return 1            

    def __str__(self):
        '''
        default implementation for object to string
        '''          
        return "P-" + str(self.priority) + " " + self.node.__str__() 

    def __repr__(self):
        '''
        default implementation for object to string
        '''          
        return "P-" + str(self.priority) + " " + self.node.__str__()


def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    queue_list = []
    node_to_parent_dict = {}
    # Set to keep track of visited nodes 
    visited_node_set = set()

    # Intialize queue with initial_node to start the BFS
    queue_list.append(initial_node)

    while queue_list:
        from_node = queue_list.pop(0)

        if from_node == dest_node:
            break

        visited_node_set.add(from_node)
        for to_node in graph.neighbors(from_node):
            # If the node was already in parent dictionary, it means that the 
            # node was already visited from a different parent.
            # We will retain the same order in which nodes are visited in BFS
            if to_node not in node_to_parent_dict:
                node_to_parent_dict[to_node] = from_node
            # Keep track of visited nodes to avoid cycles in a cyclic graph
            if to_node not in visited_node_set:
                queue_list.append(to_node)

    return get_path_to_destination_node(graph, node_to_parent_dict, dest_node)
    
def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    node_to_parent_dict = {}
    # Set to keep track of visited nodes
    visited_node_set = set()

    # Intialize stack with initial_node to start the DFS
    node_stack = stack.Stack()
    node_stack.push(initial_node)

    while not node_stack.empty():
        from_node = node_stack.pop()

        if from_node == dest_node:
            break

        visited_node_set.add(from_node)
        # Traverse the neighbors list in reverse order
        # This is done so that the left most node (first node)
        # in the neighbors list is on top of the stack
        for to_node in reversed(graph.neighbors(from_node)):
            # Keep track of visited nodes to avoid cycles in a cyclic graph
            if to_node not in visited_node_set:
                # Update parent node dictionary for the current child node
                # if the child node is not already visited
                # Parent node might be ovewritten later when the same node is
                # encountered in greater depth.
                node_to_parent_dict[to_node] = from_node
                node_stack.push(to_node)

    return get_path_to_destination_node(graph, node_to_parent_dict, dest_node)

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    priority_queue = []
    node_to_parent_dict = {}
    node_cost = {}

    # Initialize the priority queue with initial code and initial cost, parent
    heapq.heappush(priority_queue, HeapNode(0, initial_node))
    node_to_parent_dict[initial_node] = None
    node_cost[initial_node] = 0

    while priority_queue:
        from_heap_node = heapq.heappop(priority_queue)
        from_node = from_heap_node.node

        # Exit if destination found
        if from_node == dest_node:
            break
        
        for to_node in graph.neighbors(from_node):
            # to_node cost = from_node cost + edge distance between
            # from_node -> to_node
            dist = node_cost[from_node] + graph.distance(from_node, to_node)
            # Update to_node only if it was not visited before or if it has
            # new lower cost compared to previous cost
            if to_node not in node_cost or dist < node_cost[to_node]:
                node_cost[to_node] = dist
                priority = dist
                heapq.heappush(priority_queue, HeapNode(priority, to_node))
                # Update new parent that gives new lower cost
                node_to_parent_dict[to_node] = from_node

    return get_path_to_destination_node(graph, node_to_parent_dict, dest_node)

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    priority_queue = []
    node_to_parent_dict = {}
    node_cost = {}

    # Initialize the priority queue with initial code and initial cost, parent
    heapq.heappush(priority_queue, HeapNode(0, initial_node))
    node_to_parent_dict[initial_node] = None
    node_cost[initial_node] = 0

    while priority_queue:
        from_heap_node = heapq.heappop(priority_queue)
        from_node = from_heap_node.node

        # Exit if destination found
        if from_node == dest_node:
            break
        
        for to_node in graph.neighbors(from_node):
            # to_node cost = from_node cost + edge distance between
            # from_node -> to_node            
            dist = node_cost[from_node] + graph.distance(from_node, to_node)
            # Update to_node only if it was not visited before or if it has
            # new lower cost compared to previous cost            
            if to_node not in node_cost or dist < node_cost[to_node]:
                node_cost[to_node] = dist
                # Adding heuristic cost is an additional step compared to
                # Dijkstra algorithm
                priority = dist + heuristic_dist(to_node.data, dest_node.data)
                heapq.heappush(priority_queue, HeapNode(priority, to_node))
                # Update new parent that gives new lower cost
                node_to_parent_dict[to_node] = from_node

    return get_path_to_destination_node(graph, node_to_parent_dict, dest_node)

def heuristic_dist(tile1, tile2):    
    scale = 1
    dx = abs(tile1.x - tile2.x)
    dy = abs(tile1.y - tile2.y)
    return scale * (dx + dy)

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
            path.insert(0, g.Edge(parent_node, dest_node, graph.distance(parent_node, dest_node)))
            dest_node = parent_node
            if dest_node in node_to_parent_dict:
                parent_node = node_to_parent_dict[dest_node]
            else:
                parent_node = None

    return path