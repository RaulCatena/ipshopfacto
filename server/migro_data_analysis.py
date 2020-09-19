from collections import Counter
import os
import argparse
import pickle
import random
import requests
import json
import time

HACK_ZURICH_API_USER='hackzurich2020'
HACK_ZURICH_API_PASS='uhSyJ08KexKn4ZFS'
DEFAULT_GRAPH_FILE = "graph.ipfct" # Extension I make up for ipsofact

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
        return self.edges.most_common(min(n, len(self.edges) - 1))

    def getInfo(self):
        response = requests.get('https://hackzurich-api.migros.ch/products.json?ids=' + self.product_id,
                                auth=(HACK_ZURICH_API_USER, HACK_ZURICH_API_PASS))
        if response.status_code == 200:
            return json.loads(response.text)
        return None

    @staticmethod
    def getInfoForProducts(list_ids):
        response = requests.get('https://hackzurich-api.migros.ch/products.json?ids=' + ",".join(list_ids),
                                auth=(HACK_ZURICH_API_USER, HACK_ZURICH_API_PASS))
        if response.status_code == 200:
            return json.loads(response.text)
        return None

    @staticmethod
    def fromSerializedString(string):
        comps = string.split('\t')
        node = ProductNode(comps[0])
        for i in range(1, len(comps), 2):
            node.addEdgeTo(comps[i], int(comps[i + 1]))
        return node

    def toSerializedString(self):

        pairs = ['{}\t{}'.format(edge[0], str(edge[1])) for edge in self.edges]
        return self.product_id + '\t' + '\t'.join(pairs)

def getIdForScanned(barcode):
    response = requests.get('https://hackzurich-api.migros.ch/products.json?gtins=' + str(barcode),
                                auth=(HACK_ZURICH_API_USER, HACK_ZURICH_API_PASS))
    if response.status_code == 200:
        obj = json.loads(response.text)
        if obj:
            if 'products' in obj:
                if len(obj['products']):
                    p = obj['products'][0]
                    return p['id'], p['name']
    return None, None

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

    def getRandomNode(self):
        key = random.choice(list(self.nodes.keys()))
        return self.nodes[key]

def connect_nodes_in_list(node_list):
    for i in range(len(node_list)):
        for j in range(i + 1, len(node_list)):
            a, b = node_list[i], node_list[j]
            if a != b:
                a.addEdgeTo(b.product_id)
                b.addEdgeTo(a.product_id)


def saveGraphToFile(graph, file):
    '''
    Serialize graph in a simple text format
    '''
    with open(file, 'w') as f:
        for node in graph.nodes.values():
            f.write(node.toSerializedString())
            f.write("\n")


def openGraphFromFile(file):
    '''
    Open Serialized graph in a simple text format to a graph
    '''
    nodes = []
    with open(file) as f:
        for line in f:
            nodes.append(ProductNode.fromSerializedString(line))
    
    return KeyedGraph.fromProductNodeList(nodes)


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
                    if counter_lines % 10000 == 0:
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

        return graph
    return None

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
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="Filename", type=str)
    args = parser.parse_args()
    graph = createGraphFromCSVFile(args.filename)
    print("It took to generate the graph this many seconds: ", time.time() - start)
    
    # random_node = graph.nodeForId('521007300000')
    
    print("Testing serialize deserialize ______")

    start = time.time()
    saveGraphToFile(graph, DEFAULT_GRAPH_FILE)
    print("It took to save the graph to file this many seconds: ", time.time() - start)
    start = time.time()
    graph_new = openGraphFromFile(DEFAULT_GRAPH_FILE)
    print("It took to open a graph from a file this many seconds: ", time.time() - start)

    print("Testing find related ______")

    random_node = graph.getRandomNode()
    related = random_node.mostCommonConnections(10)

    print("Testing retrieve info for node and related ______")

    p_info_all = ProductNode.getInfoForProducts([random_node.product_id] + [rel[0] for rel in related]) 

    print("Show the info")
    print("Selected a random product with ID: ", random_node.product_id, p_info_all['products'][0]['name'] if p_info_all else "No info")
    if p_info_all:
        print("The most related products are:")
        for i in range(1, len(p_info_all['products'])):
            p_info = None
            if p_info_all:
                p_info = p_info_all['products'][i]
            print(related[i - 1][0], p_info['name'] if p_info else "No info", " with ", related[i - 1][1], " connections")
    

    print("Testing a full case: give barcode, get ID from it, and then query the graph and return related products")

    id, name = getIdForScanned(7616800831954)
    if id:
        found_product = graph.nodeForId(id)

        related = random_node.mostCommonConnections(10)
        p_info_all = ProductNode.getInfoForProducts([found_product.product_id] + [rel[0] for rel in related])
        
        print("Found product with ID: ", found_product.product_id, "y nombre: ", name, p_info_all['products'][0]['name'] if p_info_all else "No info")
        if p_info_all:
            print("The most related products are:")
            for i in range(1, len(p_info_all['products'])):
                p_info = None
                if p_info_all:
                    p_info = p_info_all['products'][i]
                print(related[i - 1][0], p_info['name'] if p_info else "No info", " with ", related[i - 1][1], " connections")
    