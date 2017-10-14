"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
import heapq

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

positive_infinity = float('inf')

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

def bfs(initial_node, dest_node):
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
        for to_node_state in get_state(from_node)["neighbors"]:
            to_node = to_node_state["id"]
            # If the node was already in parent dictionary, it means that the 
            # node was already visited from a different parent.
            # We will retain the same order in which nodes are visited in BFS
            if to_node not in node_to_parent_dict:
                node_to_parent_dict[to_node] = from_node
            # Keep track of visited nodes to avoid cycles in a cyclic graph
            if to_node not in visited_node_set:                
                queue_list.append(to_node)
                visited_node_set.add(to_node)

    return get_path_to_destination_node(node_to_parent_dict, dest_node)

def dijkstra_search(initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    priority_queue = []
    node_to_parent_dict = {}
    node_cost = {}
    visited_node_set = set()

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
        
        visited_node_set.add(from_node)

        for to_node_state in get_state(from_node)["neighbors"]:
            to_node = to_node_state["id"]
            # to_node cost = from_node cost + edge distance between
            # from_node -> to_node
            dist = node_cost[from_node] + distance(from_node, to_node)
            # Update to_node only if it was not visited before or if it has
            # new lower cost compared to previous cost
            if to_node not in visited_node_set:
                visited_node_set.add(to_node)
                if to_node not in node_cost or dist > node_cost[to_node]:
                    node_cost[to_node] = dist
                    priority = -dist
                    heapq.heappush(priority_queue, HeapNode(priority, to_node))
                    # Update new parent that gives new lower cost
                    node_to_parent_dict[to_node] = from_node

    return get_path_to_destination_node(node_to_parent_dict, dest_node)

def distance(from_node, to_node):
    return transition_state(from_node, to_node)["event"]["effect"]

def get_path_to_destination_node(node_to_parent_dict, dest_node):
    """
    Returns the path to the from the root node to the dest_node using 
    the node->parent dictionary provided. The dictionary is created 
    as a by-product of any graph search algorithm
    """
    visited_node_set = set()
    path = []

    visited_node_set.add(dest_node)

    if dest_node in node_to_parent_dict:
        # Start with the destination node to compute the path upward
        parent_node = node_to_parent_dict[dest_node]
        while parent_node is not None and parent_node not in visited_node_set:
            # Add the edge to the top of list since we move bottom up
            visited_node_set.add(parent_node)
            path.insert(0, parent_node + ":" + dest_node + ":" + str(distance(parent_node, dest_node)))
            #path.insert(0, parent_node + ":" + dest_node)
            dest_node = parent_node
            if dest_node in node_to_parent_dict:
                parent_node = node_to_parent_dict[dest_node]
            else:
                parent_node = None

    for p in path:
        print(p)

    return path

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

if __name__ == "__main__":
    # Your code starts here
    start_id = '7f3dc077574c013d98b2de8f735058b4'
    end_id = 'f1f131f647621a4be7c71292e79613f9'

    print("bfs")
    bfs(start_id, end_id)
    print("dijkstra")
    dijkstra_search(start_id, end_id)
