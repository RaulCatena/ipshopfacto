from flask import Flask, render_template
from fake_data import Faker
from migro_data_analysis import openGraphFromFile, DEFAULT_GRAPH_FILE, getIdForScanned

app = Flask(__name__)

graph = openGraphFromFile(DEFAULT_GRAPH_FILE)

@app.route('/')
def hello_world():
    return "Team Awesome HackZürich´s project Hello World"

@app.route('/test_html')
def hello_html():
    return render_template('index.html')

@app.route('/shopping_list')
def shopping_list():
    return Faker.generateShoppingList()

@app.route('/suggestions_to_bc/<barcode>/<preference>')
def suggestons_to_bc(barcode, preference):
    '''
    The main call, takes a barcode and a prefences enum or string value (TBD). Will return results
    '''

    # Check the id for the product using the Migros API
    id, name = getIdForScanned(int(barcode))
    if id:

        # Pull the node for the product
        found_product = graph.nodeForId(id) 

        if found_product:

            # Get related
            related = random_node.mostCommonConnections(100)

            ### HERE Magic happens

            # This is an example on how to retrieve details from the found product and the suggestions. Just to showcase
            p_info_all = ProductNode.getInfoForProducts([found_product.product_id] + [rel[0] for rel in related])
            if p_info_all:
                print("The most related products are:")
                for i in range(1, len(p_info_all['products'])):
                    p_info = None
                    if p_info_all:
                        p_info = p_info_all['products'][i]
                    print(related[i - 1][0], p_info['name'] if p_info else "No info", " with ", related[i - 1][1], " connections")

    return "Will return here the results"


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)
