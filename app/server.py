######################################################################
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
######################################################################

"""
Order Store Service with UI

Paths:
------
GET / - Displays a UI for Selenium testing
GET /orders - Returns a list all of the Orders
GET /orders/{id} - Returns the Order with a given id number
POST /orders - creates a new Order record in the database
PUT /orders/{id} - updates a Order record in the database
DELETE /orders/{id} - deletes a Order record in the database
"""

import sys
import logging
from flask import jsonify, request, json, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound
from app.models import Order
from . import app

# Error handlers reuire app to be initialized so we must import
# then only after we have initialized the Flask app instance
import error_handlers

######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    # data = '{name: <string>, time: <string>}'
    # url = request.base_url + 'orders' # url_for('list_orders')
    # return jsonify(name='Order Demo REST API Service', version='1.0', url=url, data=data), status.HTTP_200_OK
    return app.send_static_file('index.html')

######################################################################
# LIST ALL ORDERS
######################################################################
@app.route('/orders', methods=['GET'])
def list_orders():
    """
    Retrieve a list of Orders
    This endpoint will return all Orders unless a query parameter is specificed
    ---
    tags:
      - Orders
    description: The Orders endpoint allows you to query Orders
    parameters:
      - name: name
        in: query
        description: the customer of Order you are looking for
        required: false
        type: string
      - name: time
        in: query
        description: the time of Order you are looking for
        required: false
        type: string
      - name: status
        in: query
        description: the status of the order
        required: false
        type: boolean
    responses:
      200:
        description: An array of Orders
        schema:
          type: array
          items:
            schema:
              id: Order
              properties:
                id:
                  type: integer
                  description: unique id assigned internallt by service
                name:
                  type: string
                  description: the customer's name
                time:
                  type: string
                  description: the time of an order placed
                status:
                  type: boolean
                  description: the status of the order
    """
    orders = []
    time = request.args.get('time')
    name = request.args.get('name')
    if time:
        orders = Order.find_by_time(time)
    elif name:
        orders = Order.find_by_name(name)
    else:
        orders = Order.all()

    results = [order.serialize() for order in orders]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN ORDER
######################################################################
@app.route('/orders/<int:id>', methods=['GET'])
def get_orders(id):
    """
    Retrieve a single Order
    This endpoint will return a Order based on it's id
    ---
    tags:
      - Orders
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of oRDER to retrieve
        type: integer
        required: true
    responses:
      200:
        description: Order returned
        schema:
          id: Order
          properties:
            id:
              type: integer
              description: unique id assigned internallt by service
            name:
              type: string
              description: the order's customer name
            time:
              type: string
              description: the time of order placed
            status:
              type: boolean
              description: the status of the order

      404:
        description: Order not found
    """
    order = Order.find(id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(id))
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW ORDER
######################################################################
@app.route('/orders', methods=['POST'])
def create_orders():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
    ---
    tags:
      - Orders
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: data
          required:
            - name
            - time
            - status
          properties:
            name:
              type: string
              description: customer name for the order
            time:
              type: string
              description: the time of order placed
            status:
              type: boolean
              description: the status of the order
    responses:
      201:
        description: Order created
        schema:
          id: Order
          properties:
            id:
              type: integer
              description: unique id assigned internally by service
            name:
              type: string
              description: the Order's cutomer name
            time:
              type: string
              description: the time of order placed
            status:
              type: boolean
              description: the status of the order
      400:
        description: Bad Request (the posted data was not valid)
    """
    data = {}
    # Check for form submission data
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        app.logger.info('Getting data from form submit')
        data = {
            'name': request.form['name'],
            'time': request.form['time'],
            'status': True
        }
    else:
        app.logger.info('Getting data from API call')
        data = request.get_json()
    app.logger.info(data)
    order = Order()
    order.deserialize(data)
    order.save()
    message = order.serialize()
    location_url = url_for('get_orders', id=order.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {'Location': location_url})


######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route('/orders/<int:id>', methods=['PUT'])
def update_orders(id):
    """
    Update a Order
    This endpoint will update a Order based the body that is posted
    ---
    tags:
      - Orders
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        description: ID of order to retrieve
        type: integer
        required: true
      - in: body
        name: body
        schema:
          id: data
          required:
            - name
            - time
            - status
          properties:
            name:
              type: string
              description: name for the Order
            time:
              type: string
              description: the time of order palced
            status:
              type: boolean
              description: the status of the order
    responses:
      200:
        description: Order Updated
        schema:
          id: Order
          properties:
            id:
              type: integer
              description: unique id assigned internallt by service
            name:
              type: string
              description: the order's cutomer name
            time:
              type: string
              description: the time of order placed
            status:
              type: boolean
              description: the status of the order
      400:
        description: Bad Request (the posted data was not valid)
    """
    check_content_type('application/json')
    order = Order.find(id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(id))
    data = request.get_json()
    app.logger.info(data)
    order.deserialize(data)
    order.id = id
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE AN ORDER
######################################################################
@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_orders(id):
    """
    Delete a Order
    This endpoint will delete a Order based the id specified in the path
    ---
    tags:
      - Orders
    description: Deletes a Order from the database
    parameters:
      - name: id
        in: path
        description: ID of order to delete
        type: integer
        required: true
    responses:
      204:
        description: Order deleted
    """
    order = Order.find(id)
    if order:
        order.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# PURCHASE AN ORDER
#############################g#########################################
@app.route('/orders/<int:id>/purchase', methods=['PUT'])
def purchase_orders(id):
    """ Purchasing an Order makes it unstatus """
    order = Order.find(id)
    if not order:
        abort(status.HTTP_404_NOT_FOUND, "Order with id '{}' was not found.".format(id))
    if not order.status:
        abort(status.HTTP_400_BAD_REQUEST, "Order with id '{}' is not status.".format(id))
    order.status = False
    order.save()
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE ALL PET DATA (for testing only)
######################################################################
@app.route('/orders/reset', methods=['DELETE'])
def orders_reset():
    """ Removes all orders from the database """
    Order.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

@app.before_first_request
def init_db(redis=None):
    """ Initlaize the model """
    Order.init_db(redis)

# load sample data
def data_load(payload):
    """ Loads a Order into the database """
    order = Order(0, payload['name'], payload['time'])
    order.save()

def data_reset():
    """ Removes all Orders from the database """
    Order.remove_all()

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))

#@app.before_first_request
def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')