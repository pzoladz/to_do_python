import helper
from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!\n'

@app.route('/item/new', methods=['POST'])
def add_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Add item to the list
    res_data = helper.add_to_list(item)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error'}: 'Item not added -" + item + "'}", status=400, mimetype='application.json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/items/all')
def get_all_items():
    res_data = helper.get_all_items()

    # Return error if item not added
    if res_data is None:
        response = Response("{'error'}: 'Cannot get all items'}", status=400, mimetype='application.json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/item/status', methods=['GET'])
def get_item():
    item_name = request.args.get('name')
    status = helper.get_item(item_name)

    if status is None:
        response = Response("{'error'}: 'Item not found - %s'}" % item_name, status=400, mimetype='application.json')
        return response

    res_data = { 'status': status}

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response


@app.route('/item/update', methods=['PUT'])
def update_status():
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']

    res_data = helper.update_status(item, status)

    if res_data is None:
        response = Response("{'error'}: 'Error updating item - %s'}" % item, status=400, mimetype='application.json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/item/remove', methods=['DELETE'])
def delete_item():
    req_data = request.get_json()
    item = req_data['item']

    res_data = helper.delete_item(item)

    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" + item + "}", status=400, mimietype='application/json')
        return response

    response = Response(json.dumps(res_data), mimetype='application/json')

    return response
