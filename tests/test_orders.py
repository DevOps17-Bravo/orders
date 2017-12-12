# Test cases can be run with either of the following:
# python -m unittest discover
# nosetests -v --rednose --nologcapture

import unittest
import json
import os
from app.models import Order, DataValidationError
from mock import patch
from redis import Redis, ConnectionError
from werkzeug.exceptions import NotFound
from app.custom_exceptions import DataValidationError
from app import server  # to get Redis


VCAP_SERVICES = os.getenv('VCAP_SERVICES', None)
if not VCAP_SERVICES:
    VCAP_SERVICES = '{"rediscloud": [{"credentials": {' \
        '"password": "", "hostname": "127.0.0.1", "port": "6379"}}]}'
######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrders(unittest.TestCase):

    def setUp(self):
        Order.init_db()
        Order.remove_all()

    def test_create_an_order(self):
        # Create an order and assert that it exists
        order = Order(0, "321", 999, "98765")
        self.assertNotEqual(Order, None)
        self.assertEqual( order.order_id, 0 )
        self.assertEqual( order.customer_id, "321" )
        self.assertEqual( order.order_total, 999 )
        self.assertEqual( order.order_time, "98765" )

    def test_add_an_order(self):
        # Create an order and add it to the database
        orders = Order.all()
        self.assertEqual( orders, [] )
        order = Order(0, "321", 999, "98765" )
        self.assertTrue( order != None )
        self.assertEqual( order.order_id, 0 )
        order.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual( order.order_id, 1 )
        orders = Order.all()
        self.assertEqual( len(orders), 1)
        self.assertEqual(orders[0].order_id, 1)
        self.assertEqual(orders[0].customer_id, "321")
        self.assertEqual(orders[0].order_total, 999)
        self.assertEqual(orders[0].order_time, "98765")

    def test_update_an_order(self):
        order = Order(0, "54321", 9999, "98765" )
        order.save()
        self.assertEqual( order.order_id, 1)
        # Change order_total an save it
        order.order_total = 100
        order.save()
        self.assertEqual( order.order_id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        orders = Order.all()
        self.assertEqual( len(orders), 1 )
        self.assertEqual( orders[0].order_total, 100 )
        self.assertEqual( orders[0].customer_id, "54321")

    def test_delete_an_order(self):
        order = Order(0, "123", 0, "321")
        order.save()
        self.assertEqual( len(Order.all()), 1 )
        # delete the order and make sure it isn't in the database
        order.delete()
        self.assertEqual( len(Order.all()), 0 )

    def test_serialize_an_order(self):
        order = Order(0, "321", 999, "98765" )
        data = order.serialize()
        self.assertNotEqual( data, None )
        self.assertIn( "order_id", data )
        self.assertEqual( data["order_id"], 0 )
        self.assertIn( "customer_id", data )
        self.assertEqual( data["customer_id"], "321" )
        self.assertIn( "order_total", data )
        self.assertEqual( data["order_total"], 999 )
        self.assertIn( "order_time", data )
        self.assertEqual( data["order_time"], "98765" )

    def test_deserialize_an_order(self):
        data = {"order_id": 1, "customer_id": "321", "order_total": 999, "order_time": "98765", "order_status": 1}
        order = Order(data["order_id"])
        order.deserialize(data)
        self.assertNotEqual( order, None )
        self.assertEqual( order.order_id, 1 )
        self.assertEqual( order.customer_id, "321" )
        self.assertEqual( order.order_total, 999 )
        self.assertEqual( order.order_time, "98765")
        self.assertEqual( order.order_status, 1)


    def test_deserialize_an_order_with_no_customer_id(self):
        data = {"order_id": 0, "order_total": 999, "order_time": "98765", "order_status": 1}
        order = Order(0)
        self.assertRaises(DataValidationError, order.deserialize, data )

    def test_deserialize_an_order_with_no_data(self):
        order = Order(0)
        self.assertRaises(DataValidationError, order.deserialize, None )

    def test_deserialize_an_order_with_bad_data(self):
        order = Order(0)
        self.assertRaises( DataValidationError, order.deserialize, "data" )

    def test_find_order(self):
        Order(0, "1", 10, "111").save()
        Order(0, "2", 100, "222").save()
        order = Order.find(2)
        self.assertIsNot( order, None)
        self.assertEqual( order.order_id, 2 )
        self.assertEqual( order.customer_id, "2")
        self.assertEqual( order.order_total, 100)
        self.assertEqual( order.order_time, "222")

    def test_find_with_no_orders(self):
        order = Order.find(1)
        self.assertIs( order, None)

    def test_order_not_found(self):
        Order(0, "5", 1, "1221").save()
        order = Order.find(2)
        self.assertIs( order, None)

    def test_find_by_customer_id(self):
        Order(0, "1", 10, "111").save()
        Order(0, "2", 100, "222").save()
        orders = Order.find_by_customer_id("2")
        self.assertNotEqual(len(orders), 0)
        self.assertEqual(orders[0].customer_id, "2")
        self.assertEqual(orders[0].order_total, 100)



#    @patch.dict(os.environ, {'VCAP_SERVICES': json.dumps(VCAP_SERVICES).encode('utf8')})
    @patch.dict(os.environ, {'VCAP_SERVICES': VCAP_SERVICES})
    def test_vcap_services(self):
        """ Test if VCAP_SERVICES works """
        Order.init_db()
        self.assertIsNotNone(Order.redis)

    @patch('redis.Redis.ping')
    def test_redis_connection_error(self, ping_error_mock):
        """ Test a Bad Redis connection """
        ping_error_mock.side_effect = ConnectionError()
        self.assertRaises(ConnectionError, Order.init_db)
        self.assertIsNone(Order.redis)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestOrders)
    # unittest.TextTestRunner(verbosity=2).run(suite)
