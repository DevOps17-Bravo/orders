# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Models for Order Demo Service

All of the models are stored in this module

Models
------
Order - An Order used in the E-Commerce

"""
import os
import json
import logging
import pickle
from cerberus import Validator
from redis import Redis
from redis.exceptions import ConnectionError
from app.custom_exceptions import DataValidationError


######################################################################
# Order Model for database
#   This class must be initialized with use_db(redis) before using
#   where redis is a value connection to a Redis database
######################################################################
class Order(object):
    """
    Order interface to database
    """
    logger = logging.getLogger(__name__)
    redis = None
    schema = {
        'order_id': {'type': 'integer'},
        'customer_id': {'type': 'string', 'required': True},
        'order_total': {'type': 'integer', 'required': True},
        'order_time': {'type': 'string', 'required': True},
        'order_status': {'type': 'integer', 'required': True}
        }
    __validator = Validator(schema)

    def __init__(self, order_id=0, customer_id='', order_total=0, order_time='', order_status=1):
        """ Initialize an Order """
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_total = order_total
        self.order_time = order_time
        self.order_status = order_status

    def save(self):
        """
        Saves an Order in the database
        """
        if self.order_id == 0:
            self.order_id = Order.__next_index()
        Order.redis.set(self.order_id, pickle.dumps(self.serialize()))

    def delete(self):
        """ Removes an Order from the data store """
        Order.redis.delete(self.order_id)

    def serialize(self):
        """ Serializes an Order into a dictionary """
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_total": self.order_total,
            "order_time": self.order_time,
            "order_status": self.order_status
        }

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the Order data
        """
        if isinstance(data, dict) and Order.__validator.validate(data):
            self.customer_id = data['customer_id']
            self.order_total = data['order_total']
            self.order_time = data['order_time']
            self.order_status = data['order_status']
        else:
            raise DataValidationError('Invalid order data: ' + str(Order.__validator.errors))
        return self


######################################################################
#  S T A T I C   D A T A B S E   M E T H O D S
######################################################################

    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return Order.redis.incr('index')

    @staticmethod
    def remove_all():
        """ Removes all of the Orders from the database """
        Order.redis.flushall()

    @staticmethod
    def all():
        """ Returns all of the Orders in the database """
        results = []
        for key in Order.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Order.redis.get(key))
                order = Order(data['order_id']).deserialize(data)
                results.append(order)
        return results


######################################################################
#  F I N D E R   M E T H O D S
######################################################################

    @staticmethod
    def find(order_id):
        """ Finds an Order by its order ID """
        if Order.redis.exists(order_id):
            data = pickle.loads(Order.redis.get(order_id))
            order = Order(data['order_id']).deserialize(data)
            return order
        return None

    @staticmethod
    def __find_by(attribute, value):
        """ Generic Query that finds a key with a specific value """
        # return [order for order in Order.__data if order.category == category]
        Order.logger.info('Processing %s query for %s', attribute, value)
        results = []
        for key in Order.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Order.redis.get(key))
                results.append(Order(data['order_id']).deserialize(data))
        return results

    @staticmethod
    def find_by_customer_id(customer_id):
        """ Returns all Orders with the given name

        Args:
            name (string): the name of the Orders you want to match
        """
        return Order.__find_by('customer_id', customer_id)


######################################################################
#  R E D I S   D A T A B A S E   C O N N E C T I O N   M E T H O D S
######################################################################

    @staticmethod
    def connect_to_redis(hostname, port, password):
        Order.logger.info("Testing Connection to: %s:%s", hostname, port)
        Order.redis = Redis(host=hostname, port=port, password=password)
        try:
            Order.redis.ping()
            Order.logger.info("Connection established")
        except ConnectionError:
            Order.logger.info("Connection Error from: %s:%s", hostname, port)
            Order.redis = None
        return Order.redis

    @staticmethod
    def init_db(redis=None):
        """
        Initialized Redis database connection
        This method will work in the following conditions:
          1) In Bluemix with Redis bound through VCAP_SERVICES
          2) With Redis running on the local server as with Travis CI
          3) With Redis --link in a Docker container called 'redis'
          4) Passing in your own Redis connection object
        Exception:
        ----------
          redis.ConnectionError - if ping() test fails
        """
        if redis:
            Order.logger.info("Using client connection...")
            Order.redis = redis
            try:
                Order.redis.ping()
                Order.logger.info("Connection established")
            except ConnectionError:
                Order.logger.error("Client Connection Error!")
                Order.redis = None
                raise ConnectionError('Could not connect to the Redis Service')
            return
        # Get the credentials from the Bluemix environment
        if 'VCAP_SERVICES' in os.environ:
            Order.logger.info("Using VCAP_SERVICES...")
            vcap_services = os.environ['VCAP_SERVICES']
            services = json.loads(vcap_services)
            creds = services['rediscloud'][0]['credentials']
            Order.logger.info("Conecting to Redis on host %s port %s",
                            creds['hostname'], creds['port'])
            Order.connect_to_redis(creds['hostname'], creds['port'], creds['password'])
        else:
            Order.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
            Order.connect_to_redis('127.0.0.1', 6379, None)
            if not Order.redis:
                Order.logger.info("No Redis on localhost, looking for redis host")
                Order.connect_to_redis('redis', 6379, None)
        if not Order.redis:
            # if you end up here, redis instance is down.
            Order.logger.fatal('*** FATAL ERROR: Could not connect to the Redis Service')
            raise ConnectionError('Could not connect to the Redis Service')