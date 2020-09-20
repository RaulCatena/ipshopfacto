from flask import Flask, render_template
from fake_data import Faker
from migro_data_analysis import openGraphFromFile, DEFAULT_GRAPH_FILE, getIdForScanned

import json

app = Flask(__name__)

graph = openGraphFromFile(DEFAULT_GRAPH_FILE, binary = True)

@app.route('/')
def hello_world():
    return "Team Awesome HackZürich´s project Hello World"

@app.route('/test_html')
def hello_html():
    return render_template('index.html')

@app.route('/shopping_list')
def shopping_list():
    return Faker.generateShoppingList()

@app.route('/product/<barcode>')
def product(barcode):
    '''
    The main call, takes a barcode and a prefences enum or string value (TBD). Will return results
    GET /product/{barcode} (EAN 13 String)
    Description: Return product data of a single product
    Fields: title (string), subtitle (string), price (double), imageUrl (string), barcode (string), rating (decimal, 0-5), ratingCount (int)
    '''

    # Check the id for the product using the Migros API
    id, name = getIdForScanned(int(barcode))
    if id:

        # Pull the node for the product
        found_product = graph.nodeForId(id) 

        if found_product:

            # Get related
            related = found_product.mostCommonConnections(100)

            ### HERE Magic happens

            # This is an example on how to retrieve details from the found product and the suggestions. Just to showcase
            p_info_all = ProductNode.getInfoForProducts([found_product.product_id] + [rel[0] for rel in related])
            products = []
            if p_info_all and 'products' in p_info_all:
                print("The most related products are:")
                for i in range(0, len(p_info_all['products'])):
                    p_info = None
                    if p_info_all:
                        p_info = p_info_all['products'][i]
                    if p_info:
                        products.append(
                            {
                                'name': p_info['name'],
                                'brand': p_info['brand']['name'],
                                'imageUrl': p_info['image']['original'],
                                'imageTransparentUrl': p_info['image_transparent']['original'],
                                'price': p_info['price']['item']['price'],
                                'priceUnit': p_info['price']['currency'],
                                'rating': p_info['ratings']['average_all'],
                                'votes': p_info['ratings']['count_all']
                            }
                        )
            return json.dumps({'status': 'ok', 'products': products)
    return "{'status':'Error'}"


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)
