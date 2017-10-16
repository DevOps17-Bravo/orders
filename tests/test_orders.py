# Test cases can be run with either of the following:
# python -m unittest discover
# nosetests -v --rednose --nologcapture

import unittest
import json
from models import Pet, DataValidationError

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPets(unittest.TestCase):

    def setUp(self):
        Order.remove_all()

    def test_create_an_order(self):
        # Create an order and assert that it exists
        order = Order("123", "321", 999, "98765", [("1", 3)])
        self.assertTrue( order != None )
        self.assertEqual( order.order_id, "123" )
        self.assertEqual( order.customer_id, "321" )
        self.assertEqual( order.order_total, 999 )
        self.assertEqual( order.order_time, "98765" )
        self.assertEqual( order.order_items, [("1", 3)] )

    def test_add_an_order(self):
        # Create a pet and add it to the database
        orders = Order.all()
        self.assertEqual( orders, [] )
        order = Order("123", "321", 999, "98765", [("1", 3)] )
        self.assertTrue( order != None )
        self.assertEqual( order.order_id, "123" )
        order.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual( order.order_id, "123" )
        orders = Order.all()
        self.assertEqual( len(orders), 1)

    def test_update_a_pet(self):
        order = Order("12345", "54321", "9999", "98765", [("123", 3)])
        pet.save()
        self.assertEqual( order.customer_id, "12345")
        # Change order_total an save it
        order.order_total = "100"
        order.save()
        self.assertEqual( order.order_total, "100")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        orders = Order.all()
        self.assertEqual( len(orders), 1)
        self.assertEqual( orders[0].order_total, "100")

    def test_delete_a_pet(self):
        order = Order("1", "", 0, "", [])
        order.save()
        self.assertEqual( len(Order.all()), 1)
        # delete the pet and make sure it isn't in the database
        order.delete()
        self.assertEqual( len(Order.all()), 0)

    def test_serialize_an_order(self):
        order = Order("123", "321", 999, "98765", [("1", 3)])
        data = order.serialize()
        self.assertNotEqual( data, None )
        self.assertIn( "order_id", data )
        self.assertEqual( data["order_id"], "123" )
        self.assertIn( "customer_id", data )
        self.assertEqual( data["customer_id"], "321" )
        self.assertIn( "order_total", data )
        self.assertEqual( data["order_total"], 999 )
        self.assertIn( "order_time", data )
        self.assertEqual( data["order_time"], "98765" )
        self.assertIn( "order_items", data )
        self.assertEqual( data["order_items"], [("1", 3)] )

    def test_deserialize_an_order(self):
        data = {"order_id":"123", "customer_id": "321", "order_total": 999, "order_time": "98765", "order_items":[("1", 3)]}
        order = Order()
        order.deserialize(data)
        self.assertNotEqual( order, None )
        self.assertNotEqual( order.order_id, "123" )
        self.assertEqual( order.customer_id, "321" )
        self.assertEqual( order.order_total, 999 )
        self.assertEqual( order.order_time, "98765" )
        self.assertEqual( order.order_items, [("1", 3)] )


    def test_deserialize_an_order_with_no_customer_id(self):
        order = Order()
        data = {"order_id":"123", "order_total": 999, "order_time": "98765", "order_items":[("1", 3)]}
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_deserialize_an_order_with_no_data(self):
        pet = Pet()
        self.assertRaises(DataValidationError, order.deserialize, None)

    def test_deserialize_an_order_with_bad_data(self):
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, "data")

    def test_find_order(self):
        Pet("1", "", 0, "", []).save()
        Pet("2", "", 0, "", []).save()
        order = Order.find("2")
        self.assertIsNot( order, None)
        self.assertEqual( order.order_id, "2" )
        self.assertEqual( order.name, "" )

    def test_find_with_no_orders(self):
        order = Order.find("1")
        self.assertIs( order, None)

    def test_order_not_found(self):
        Order("1", "", 1, "", []).save()
        order = Order.find("2")
        self.assertIs( order, None)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestPets)
    # unittest.TextTestRunner(verbosity=2).run(suite)
