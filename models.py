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

    def __init__(self, order_id='', customer_id='', order_total=0, order_time='', order_items=[]):
        """ Initialize an Order """
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_total = order_total
        self.order_time = order_time
        self.order_items = order_items

    def save(self):
        """
        Saves an Order to the data store
        """
        if self.id == 0:
            self.id = self.__next_index()
            Pet.data.append(self)
        else:
            for i in range(len(Pet.data)):
                if Pet.data[i].id == self.id:
                    Pet.data[i] = self
                    break

    def delete(self):
        """ Removes an Order from the data store """
        Pet.data.remove(self)

    def serialize(self):
        """ Serializes an Order into a dictionary """
        return {"id": self.id, "name": self.name, "category": self.category}

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the Order data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid pet: body of request contained bad or no data')
        if data.has_key('id'):
            self.id = data['id']
        try:
            self.name = data['name']
            self.category = data['category']
        except KeyError as err:
            raise DataValidationError('Invalid pet: missing ' + err.args[0])
        return

    @staticmethod
    def __next_index():
        """ Generates the next index in a continual sequence """
        with Pet.lock:
            Pet.index += 1
        return Pet.index

    @staticmethod
    def all():
        """ Returns all of the Orders in the database """
        return [pet for pet in Pet.data]

    @staticmethod
    def remove_all():
        """ Removes all of the Orders from the database """
        del Pet.data[:]
        Pet.index = 0
        return Pet.data

    @staticmethod
    def find(pet_id):
        """ Finds an Order by it's ID """
        if not Pet.data:
            return None
        pets = [pet for pet in Pet.data if pet.id == pet_id]
        if pets:
            return pets[0]
        return None

    @staticmethod
    def find_by_category(category):
        """ Returns all of the Orders in a category

        Args:
            category (string): the category of the Orders you want to match
        """
        return [pet for pet in Pet.data if pet.category == category]

    @staticmethod
    def find_by_name(name):
        """ Returns all Orders with the given name

        Args:
            name (string): the name of the Orders you want to match
        """
        return [pet for pet in Pet.data if pet.name == name]
