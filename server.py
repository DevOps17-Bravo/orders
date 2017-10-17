# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pet Shop Demo

This is an example of a pet shop service written with Python Flask
It demonstraits how a RESTful service should be implemented.

Paths
-----
GET  /pets - Retrieves a list of pets from the database
GET  /pets{id} - Retrirves a Pet with a specific id
POST /pets - Creates a Pet in the datbase from the posted database
PUT  /pets/{id} - Updates a Pet in the database fom the posted database
DELETE /pets{id} - Removes a Pet from the database that matches the id
"""

import os
import logging
from flask import Flask, Response, jsonify, request, json, url_for, make_response
from models import Pet, DataValidationError

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

# Create Flask application
app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles all data validation issues from the model """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles requests that have bad or malformed data """
    return jsonify(status=400, error='Bad Request', message=error.message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles Pets that cannot be found """
    return jsonify(status=404, error='Not Found', message=error.message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles bad method calls """
    return jsonify(status=405, error='Method not Allowed',
                   message='Your request method is not supported.' \
                   ' Check your HTTP method and try again.'), 405

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles catostrophic errors """
    return jsonify(status=500, error='Internal Server Error', message=error.message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return something useful by default """
    return jsonify(name='Pet Demo REST API Service',
                   version='1.0',
                   url=url_for('list_pets', _external=True)), HTTP_200_OK

######################################################################
# LIST ALL ORDERS
######################################################################
@app.route('/orders', methods=['GET'])
def list_pets():
    """ Retrieves a list of orders from the database """
    results = []
    category = request.args.get('category')
    if category:
        results = Pet.find_by_category(category)
    else:
        results = Pet.all()

    return jsonify([pet.serialize() for pet in results]), HTTP_200_OK

######################################################################
# RETRIEVE A ORDER
######################################################################
@app.route('/orders/<int:id>', methods=['GET'])
def get_pets(id):
    """ Retrieves a Order with a specific id """
    pet = Pet.find(id)
    if pet:
        message = pet.serialize()
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Pet with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code

######################################################################
# ADD A NEW ORDER
######################################################################
@app.route('/orders', methods=['POST'])
def create_orders():
    """ Creates a Order in the datbase from the posted database """
    payload = request.get_json()
    order = Order()
    order.deserialize(payload)
    order.save()
    message = order.serialize()
    response = make_response(jsonify(message), HTTP_201_CREATED)
    response.headers['Location'] = url_for('get_orders', id=order.order_id, _external=True)
    return response

######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route('/orders/<int:id>', methods=['PUT'])
def update_orders(id):
    """ Updates a Order in the database fom the posted database """
    pet = Pet.find(id)
    if pet:
        payload = request.get_json()
        pet.deserialize(payload)
        pet.save()
        message = pet.serialize()
        return_code = HTTP_200_OK
    else:
        message = {'error' : 'Pet with id: %s was not found' % str(id)}
        return_code = HTTP_404_NOT_FOUND

    return jsonify(message), return_code

######################################################################
# DELETE A ORDER
######################################################################
@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_orders(id):
    """ Removes a Order from the database that matches the id """
    order = Order.find(id)
    if order:
        orders.delete()
    return make_response('', HTTP_204_NO_CONTENT)

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # dummy data for testing

    Order(0,"01",10,"11:01").save()
    Order(0,"02",20,"17:11").save()

    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
