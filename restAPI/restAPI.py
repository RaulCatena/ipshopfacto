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
    print(json_object)
    data = getDifferentData()
    data['item'] = json_object
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