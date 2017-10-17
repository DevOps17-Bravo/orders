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
import threading

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Order(object):
    """
    Class that represents an Order

    This version uses an in-memory collection of orders for testing
    """
    lock = threading.Lock()
    data = []
    index = 0

    def __init__(self, order_id=0, customer_id='', order_total=0, order_time=''):
        """ Initialize an Order """
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_total = order_total
        self.order_time = order_time

    def save(self):
        """
        Saves an Order to the data store
        """
        if self.order_id == 0:
            self.order_id = self.__next_index()
            Order.data.append(self)
        else:
            for i in range(len(Order.data)):
                if Order.data[i].order_id == self.order_id:
                    Order.data[i] = self
                    break

    def delete(self):
        """ Removes an Order from the data store """
        Order.data.remove(self)

    def serialize(self):
        """ Serializes an Order into a dictionary """
        return {"order_id": self.order_id, "customer_id": self.customer_id, "order_total": self.order_total,
                "order_time": self.order_time}

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the Order data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid order: body of request contained bad or no data')
        if data.has_key("order_id"):
            self.order_id = data["order_id"]
        try:
            self.customer_id= data["customer_id"]
            self.order_total = data["order_total"]
            self.order_time = data["order_time"]
        except KeyError as err:
            raise DataValidationError("Invalid order: missing " + err.args[0])
        return

    @staticmethod
    def __next_index():
        """ Generates the next index in a continual sequence """
        with Order.lock:
            Order.index += 1
        return Order.index

    @staticmethod
    def all():
        """ Returns all of the Orders in the database """
        return [order for order in Order.data]

    @staticmethod
    def remove_all():
        """ Removes all of the Orders from the database """
        del Order.data[:]
        Order.index = 0
        return Order.data

    @staticmethod
    def find(order_id):
        """ Finds an Order by it's ID """
        if not Order.data:
            return None
        orders = [order for order in Order.data if order.order_id == order_id]
        if orders:
            return orders[0]
        return None

    @staticmethod
    def find_by_customer_id(customer_id):
        """ Returns all Orders with the given name

        Args:
            name (string): the name of the Orders you want to match
        """
        return [order for order in Order.data if order.customer_id == customer_id]
