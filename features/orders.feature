Feature: The orders service back-end
    As a API user
    I need a RESTful catalog service
    So that I can keep track of all orders

Background:
    Given the following orders
        | order_id | customer_id | order_total | order_time | order_status |  
        |  1       | alpha       | 100         | 06/06/2017 | 1            |
        |  2       | beta        | 500         | 09/15/2017 | 0            |
        |  3       | gamma       | 1000        | 04/14/2017 | 1            |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Order Demo RESTful Service"
    Then I should not see "404 Not Found"

Scenario: List all orders
    When I visit "/orders"
    Then I should see "alpha"
    And I should see "beta"
    And I should see "gamma"

Scenario: Query for Customer ID
    When I attempt to query for "/orders" and search by customer id "alpha"
    Then I should see "1"
    And I should see "alpha"
    And I should see "100"
    And I should see "06/06/2017"
    And I should see "1"

Scenario: Get a order
    When I retrieve "/orders" with order id "1"
    Then I should see "1"
    And I should see "alpha"
    And I should see "100"
    And I should see "06/06/2017"
    And I should see "1"

Scenario: Update a order
    When I retrieve "/orders" with order id "1"
    And I change "order_total" to "200"
    And I update "/orders" with order id "1"
    Then I should see "200"

Scenario: Delete a order
    When I visit "/orders"
    Then I should see "alpha"
    And I should see "beta"
    And I should see "gamma"
    When I delete "/orders" with order id "3"
    And I visit "/orders"
    Then I should see "alpha"
    And I should see "beta"

Scenario: Duplicate an order
    When I retrieve "/orders" with order id "1"
    And I use "/orders" the order id "1" of that order so the customer can re-order their previous order
    Then I should see an order on "/orders" with the same customer_id, order_total, order_time and order_status as the original order