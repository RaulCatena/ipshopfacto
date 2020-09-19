from collections import Counter
import os
import argparse
import pickle

class ProductNode(object):
    '''
    An abstraction around the product object
    '''

    def __init__(self, product_id):
        self.product_id = product_id
        self.edges = Counter()

    def addEdgeTo(self, other_product_id, weight_add = 1):
        self.edges[other_product_id] += weight_add

    def mostCommonConnections(self, n):
        return self.edges.most_common(n)


class KeyedGraph(object):
    '''
    A collection of nodes retrievable by product id
    '''

    def __init__(self):
        self.nodes = {}

    @staticmethod
    def fromProductNodeList(nodes):
        graph = KeyedGraph()
        for node in nodes:
            graph.addNode(node)
        return graph
    
    def addNode(self, node):
        if not node.product_id in self.nodes:
            self.nodes[node.product_id] = node
        else:
            print("Trying to add an already existing node")
            raise RuntimeError

    def nodeForId(self, id):
        if id in self.nodes:
            return self.nodes[id]
        return None

def connect_nodes_in_list(node_list):
    for i in range(len(node_list)):
        for j in range(i + 1, len(node_list)):
            a, b = node_list[i], node_list[j]
            if a != b:
                a.addEdgeTo(b)
                b.addEdgeTo(a)

def createGraphFromCSVFile(file_path):
    
    if file_path and os.path.exists(file_path):
        with open(file_path) as f:
            first_line = True
            last_user = None
            last_cart = None
            this_user, this_cart = [], []

            graph = KeyedGraph()

            counter_lines = 0
            for line in f:
                if not first_line:

                    counter_lines += 1
                    if counter_lines % 1000 == 0:
                        break
                        print(counter_lines)

                    # Get data from row
                    components = line.strip().split(",")
                    current_user = components[1]
                    current_cart = components[2]
                    product_id = components[-2]

                    # Get node for product in graph, create it if not in graph yet
                    node = graph.nodeForId(product_id)
                    if not node:
                        node = ProductNode(product_id)
                        graph.addNode(node)

                    # Check if it is time to clean up any of the temporary lists
                    if current_cart != last_cart:
                        # Loop over all products in this cart and add +1 weight to links
                        connect_nodes_in_list(this_cart)

                        # Clean up temp list
                        this_cart = []

                    if current_user != last_user:
                        # Loop over all products by this user and add +1 weight to links
                        connect_nodes_in_list(this_user)

                        # Clean up temp list
                        this_user = []

                    # Add the product to the temp lists
                    this_cart.append(node)
                    this_user.append(node)

                    # Update last* pointers for next iteration
                    last_user = current_user
                    last_cart = current_cart
                    
                first_line = False
            
            # Take care of reamining elements at the end
            connect_nodes_in_list(this_cart)
            connect_nodes_in_list(this_user)

            # See how many entries processed
            print(counter_lines, " is the number of entries processed")
            print(len(graph.nodes), " is the number of nodes in the graph")



if __name__ == '__main__':

    print("Testing product node ______")

    product = ProductNode('cookies')
    test_data = (
        (5, 'milk'),
        (4, 'chocolate'),
        (3, 'sugar'),
        (2, 'spoon'),
    )
    for pair in test_data:
        for _ in range(pair[0]):
            product.addEdgeTo(pair[1])
    
    print(product.mostCommonConnections(2))
    
    print("Testing Reading file ______")

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="Filename", type=str)
    args = parser.parse_args()
    createGraphFromCSVFile(args.filename)

    
