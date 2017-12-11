"""
Order Steps

Steps file for Order.feature
"""

from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app import server

WAIT_SECONDS = 30
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given(u'the following orders')
def step_impl(context):
    """ Delete all Orders and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/orders/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/pets'
    for row in context.table:
        data = {
            "customer_id": row['customer_id'],
            "order_total": row['order_total'],
            "order_time": row['order_time'],
            "order_status": row['order_status']
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@when(u'I visit the "home page"')
def step_impl(context):
    context.driver.get(context.base_url)

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    expect(context.driver.title).to_contain(message)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when(u'I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'order_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

#######################################################################

@when(u'I visit "{url}"')
def step_impl(context, url):
    context.resp = context.app.get(url)
    assert context.resp.status_code == 200

@when(u'I attempt to query for "{url}" and search by customer id "{customer_id}"')
def step_impl(context, url, customer_id):
    context.resp = context.app.get(url + '?customer_id=' + customer_id)
    assert context.resp.status_code == 200

@when(u'I delete "{url}" with order id "{order_id}"')
def step_impl(context, url, order_id):
    target_url = url + '/' + order_id
    context.resp = context.app.delete(target_url)
    assert context.resp.status_code == 204
    assert context.resp.data is ""

@when(u'I retrieve "{url}" with order id "{order_id}"')
def step_impl(context, url, order_id):
    target_url = url + '/' + order_id
    context.resp = context.app.get(target_url)
    assert context.resp.status_code == 200

@when(u'I change "{key}" to "{value}"')
def step_impl(context, key, value):
    data = json.loads(context.resp.data)
    data[key] = value
    context.resp.data = json.dumps(data)

@when(u'I update "{url}" with order id "{order_id}"')
def step_impl(context, url, order_id):
    target_url = url + '/' + order_id
    context.resp = context.app.put(target_url, data=context.resp.data, content_type='application/json')
    assert context.resp.status_code == 200

@when(u'I use "{url}" the order id "{order_id}" of that order so the customer can re-order their previous order')
def step_impl(context, url, order_id):
    target_url = url + '/' + order_id + '/duplicate'
    context.resp = context.app.put(target_url, data=context.resp.data, content_type='application/json')
    assert context.resp.status_code == 201

@then(u'I should see an order on "{url}" with the same customer_id, order_total, order_time and order_status as the original order')
def step_impl(context, url):
    context.resp = context.app.get(url, data=context.resp.data, content_type='application/json')
    data = json.loads(context.resp.data)
    found = False

    for entry in data:
        for compare_entry in data:
            if entry['id'] == compare_entry['id']:
                continue
            if entry['customer_name'] == compare_entry['customer_name'] and entry['amount_paid'] == compare_entry['amount_paid']:
                found = True

    assert found == True
