from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

barcode = int()
settings = []
username = 'hackzurich2020'
password = 'uhSyJ08KexKn4ZFS'

@app.route('/')
def hello_world():
    return jsonify({"about": "Team Awesome HackZurich's project Hello World"})

@app.route('/data/settings/barcode')
def index():
    global barcode
    global settings
    json_data = request.get_json()
    barcode = json_data['barcode']
    settings = json_data['settings']
    payload = {'gtins': barcode}
    r = requests.get('https://hackzurich-api.migros.ch/products', params=payload, auth=(username, password))
    json_object = r.json()
    r = requests.get('https://eatfit-service.foodcoa.ch/products/' + str(barcode), auth=('eatfit_hackzurich', 'XmU8G2jeAwYzrU9K'))
    json_object_css = r.json()
    print(json_object_css)
    products = json_object.get("products")[0]
    base_price = products.get("price").get("base").get("price")
    average_all = products.get("ratings").get("average_all")
    product_id = products.get("id")
    categories_code = products.get("categories")[0].get("code")
    data = getDifferentData()
    data['item'] = json_object
    data['base_price'] = base_price
    data['average_all'] = average_all
    data['product_id'] = product_id
    data['categories_code'] = categories_code
    return jsonify(data)

def getDifferentData():
    data = {}
    for setting in settings:
        data[setting] = switch_setting(setting)
    return data

def switch_setting(argument):
    switcher = {
        "hallo": barcode,
        "test": "February",
        "okay": barcode,
        "fine": "April",
    }
    return switcher.get(argument, "Invalid month")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8080)