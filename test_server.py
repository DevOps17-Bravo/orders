# run with:
# python -m unittest discover
# nosetests --nologcapture
# nosetests -v --rednose

import unittest
import logging
import json
from app import server

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrderServer(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        server.initialize_logging(logging.CRITICAL)
        server.init_db()
        server.data_reset()
        server.data_load({"customer_id": "2", "order_total": 3, "order_time": "4", "order_status": 1})
        server.data_load({"customer_id": "6", "order_total": 7, "order_time": "8", "order_status": 1})

    def tearDown(self):
        server.Order.remove_all()

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertIn('Order Demo REST API Service', resp.data)


    def test_get_order_list(self):
        resp = self.app.get('/orders')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )

    def test_get_order(self):
        resp = self.app.get("/orders/2")
        #print 'resp_data: ' + resp.data
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual(data["customer_id": "6"])

    def test_get_order_not_found(self):
        resp = self.app.get('/orders/0')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)
        data = json.loads(resp.data)
        self.assertIn('was not fount', data['message'])

    def test_create_order(self):
        # save the current number of orders for later comparison
        order_count = self.get_order_count()
        # add a new pet
        new_order = {"customer_id": "2", "order_total": 3, "order_time": "4", "order_status": 1}
        data = json.dumps(new_order)
        resp = self.app.post("/orders", data=data, content_type="application/json")
        self.assertEqual( resp.status_code, HTTP_201_CREATED )
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertNotEqual( location, None)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual (new_json["order_id"], 3)
        # check that count has gone up and includes sammy
        resp = self.app.get("/orders")
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertEqual( len(data), order_count + 1 )
        self.assertIn( new_json, data )

    def test_update_order(self):
        new_order = {"customer_id": "2", "order_total": 5, "order_time": "4", "order_status": 1}
        data = json.dumps(new_order)
        resp = self.app.put("/orders/2", data=data, content_type="application/json")
        self.assertEqual( resp.status_code, HTTP_200_OK )
        resp = self.app.get("/orders/2", content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertEqual (new_json["order_total"], 5)

    def test_update_order_with_nonexisting_order(self):
        new_order = {"customer_id": "100" ,"order_total" : 3, "order_time": "4", "order_status": 1}
        data = json.dumps(new_order)
        resp = self.app.put('/orders/2', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_404_NOT_FOUND )

    def test_delete_order(self):
        # save the current number of pets for later comparrison
        order_count = self.get_order_count()
        # delete a order
        resp = self.app.delete('/orders/2', content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_204_NO_CONTENT )
        self.assertEqual( len(resp.data), 0 )
        new_count = self.get_order_count()
        self.assertEqual( new_count, order_count - 1)

    def test_create_order_with_no_customer_id(self):
        #new_order = {"order_id": 10, "order_total": 100, "order_time": "10112017"}
        new_order = {"order_total": 100}
        data = json.dumps(new_order)
        resp = self.app.post('/orders', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_400_BAD_REQUEST )

    def test_create_order_with_no_order_total(self):
        new_order = {"customer_id": "50"}
        data = json.dumps(new_order)
        resp = self.app.post('/orders', data=data)
        self.assertEqual( resp.status_code, HTTP_400_BAD_REQUEST )

    def test_create_order_with_no_order_time(self):
        new_order = {"customer_id": "01","order_total": 100}
        data = json.dumps(new_order)
        resp = self.app.post('/orders', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_400_BAD_REQUEST )

    def test_get_nonexisting_order(self):
        resp = self.app.get("/orders/9")
        self.assertEqual( resp.status_code, HTTP_404_NOT_FOUND )

    def test_query_order_list(self):
        resp = self.app.get("/orders", query_string="order_id=1")
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item["order_id"], 1)

    def test_cancel_an_order(self):
        resp = self.app.put('/orders/1/cancel')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data["order_status"], 0)

    def test_cancel_an_order_with_nonexisting_order(self):
        resp = self.app.put('/orders/3/cancel')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)


######################################################################
# Utility functions
######################################################################

    def get_order_count(self):
        # save the current number of pets
        resp = self.app.get("/orders")
        self.assertEqual( resp.status_code, HTTP_200_OK )
        # print 'resp_data: ' + resp.data
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
