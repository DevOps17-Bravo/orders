# run with:
# python -m unittest discover
# nosetests --nologcapture
# nosetests -v --rednose

import logging
import unittest
import json
import server

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPetServer(unittest.TestCase):

    def setUp(self):
        server.app.debug = True
        self.app = server.app.test_client()
        server.Pet(0,'fido','dog').save()
        server.Pet(0,'kitty','cat').save()

    def tearDown(self):
        server.Pet.remove_all()

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertTrue ('Pet Demo REST API Service' in resp.data)

    def test_get_pet_list(self):
        resp = self.app.get("/pets")
        #print 'resp_data: ' + resp.data
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )

    def test_get_order(self):
        resp = self.app.get("/orders/1")
        #print 'resp_data: ' + resp.data
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertEqual (data["order_id"], "5")

    def test_create_order(self):
        # save the current number of orders for later comparison
        order_count = self.get_order_count()
        # add a new pet
        new_order = {"order_id": "1", "customer_id": "2", "order_total": 3, "order_time": "4"}
        data = json.dumps(new_order)
        resp = self.app.post("/orders", data=data, content_type="application/json")
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue( location != None)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual (new_json["order_id"], "1")
        # check that count has gone up and includes sammy
        resp = self.app.get("/orders")
        # print 'resp_data(2): ' + resp.data
        data = json.loads(resp.data)
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertEqual( len(data), order_count + 1 )
        self.assertIn( new_json, data )

    def test_update_order(self):
        new_order = {"order_id": "1", "customer_id": "2", "order_total": 5, "order_time": "4"}
        data = json.dumps(new_order)
        resp = self.app.put("/orders/1a", data=data, content_type="application/json")
        self.assertEqual( resp.status_code, HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertEqual (new_json["order_total"], 5)

    def test_update_pet_with_no_name(self):
        new_pet = {'category': 'dog'}
        data = json.dumps(new_pet)
        resp = self.app.put('/pets/2', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_400_BAD_REQUEST )

    def test_delete_order(self):
        # save the current number of pets for later comparrison
        order_count = self.get_order_count()
        # delete a pet
        resp = self.app.delete('/orders/2', content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_204_NO_CONTENT )
        self.assertEqual( len(resp.data), 0 )
        new_count = self.get_order_count()
        self.assertEqual( new_count, order_count - 1)

    def test_create_pet_with_no_name(self):
        new_pet = {'category': 'dog'}
        data = json.dumps(new_pet)
        resp = self.app.post('/pets', data=data, content_type='application/json')
        self.assertEqual( resp.status_code, HTTP_400_BAD_REQUEST )

    def test_create_pet_with_no_content_type(self):
        new_pet = {'category': 'dog'}
        data = json.dumps(new_pet)
        resp = self.app.post('/pets', data=data)
        self.assertEqual( resp.status_code, HTTP_400_BAD_REQUEST )

    def test_get_nonexisting_pet(self):
        resp = self.app.get('/pets/5')
        self.assertEqual( resp.status_code, HTTP_404_NOT_FOUND )

    def test_query_pet_list(self):
        resp = self.app.get('/pets', query_string='category=dog')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['category'], 'dog')


######################################################################
# Utility functions
######################################################################

    def get_pet_count(self):
        # save the current number of pets
        resp = self.app.get('/pets')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        # print 'resp_data: ' + resp.data
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
