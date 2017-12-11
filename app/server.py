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
Order Shop Demo

This is an example of Order service written with Python Flask
It demonstraits how a RESTful service should be implemented.

Paths
-----
GET / - Displays a UI for Selenium testing
GET  /orders - Retrieves a list of orders from the database
GET  /orders{id} - Retrirves an Order with a specific id
POST /orders - Creates an Order in the datbase from the posted database
PUT  /orders/{id} - Updates a Order in the database fom the posted database
DELETE /orders{id} - Removes a Order from the database that matches the id
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
@app.route("/")
def index():
    """ Return something useful by default """
    #return jsonify(name="Order Demo REST API Service",
    #              version="1.0",
    #               url=url_for("list_orders", _external=True)), HTTP_200_OK
    return app.send_static_file('index.html')


######################################################################
# LIST ALL ORDERS
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
    """ Retrieves a list of orders from the database """
    orders = []
    customer_id = request.args.get("customer_id")
    if customer_id:
        orders = Order.find_by_customer_id(customer_id)
    else:
        orders = Order.all()

    results = [order.serialize() for order in orders]

    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A ORDER
######################################################################
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_orders(order_id):
    """ Retrieves a Order with a specific id """
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW ORDER
######################################################################

@app.route('/orders', methods=['POST'])
def create_orders():
    data = {}
    """ Creates a Order in the database from the posted database """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        app.logger.info('Getting data from form submitted')
        data = {
            "customer_id": request.form["customer_id"],
            "order_total": request.form["order_total"],
            "order_time": request.form["order_time"],
            "order_status": 1
        }
    else:
        app.logger.info('Getting data from API call')
        data = request.get_json()
    app.logger.info(data)
    order = Order()
    order.deserialize(data)
    order.save()
    message = order.serialize()
    location_url = url_for('get_orders', order_id=order.order_id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, {'Location': location_url})

######################################################################
# UPDATE AN EXISTING ORDER
######################################################################

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    """ Updates a Order in the database fom the posted database """
    check_content_type('application/json')
    order = Order.find(order_id)
    if not order:
        raise NotFound("Order with id '{}' was not found.".format(order_id))

    data = request.get_json()
    app.logger.info(data)
    order.deserialize(data)
    order.order_id = order_id
    order.save()

    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE A ORDER
######################################################################

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_orders(order_id):
    """ Removes a Order from the database that matches the id """
    order = Order.find(order_id)
    if order:
        order.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# CANCEL AN ORDER
######################################################################

@app.route('/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_an_order(order_id):
    order = Order.find(order_id)
    if order:
        order.order_status = 0
        order.save()
        message = order.serialize()
        return_code = status.HTTP_200_OK
    else:
        message = {"error" : "Order with id: %s was not found" % str(order_id)}
        return_code = status.HTTP_404_NOT_FOUND

    return make_response(jsonify(message), return_code)

######################################################################
# DELETE ALL PET DATA (for testing only)
######################################################################
@app.route('/orders/reset', methods=['DELETE'])
def pets_reset():
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
    """ Loads a Pet into the database """
    order = Order(0, payload['customer_id'], payload['order_total'], payload['order_time'], payload["order_status"])
    order.save()

def data_reset():
    """ Removes all Pets from the database """
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