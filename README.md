# orders
A collection of orders created from products

[![Build Status](https://travis-ci.org/DevOps17-Bravo/orders.svg?branch=master)](https://travis-ci.org/DevOps17-Bravo/orders)
[![Codecov](https://img.shields.io/codecov/c/github/DevOps17-Bravo/orders.svg)]()

Finally you can see the microservice at: http://localhost:8080/

The Swagger docs can be accessed at: http://localhost:8080/apidocs/index.html

The raw Swagger specification JSON can be found at: http://localhost:8080/v1/spec


## Prerequisite : Vagrant and VirtualBox

## Get the code
From a terminal navigate to a location where you want this application code to be downloaded to and issue:
```
git clone https://github.com/DevOps17-Bravo/orders.git
cd orders
vagrant up
vagrant ssh
cd /vagrant
```
This will place you into an Ubuntu VM all set to run the code.

You can run the code to test it out in your browser with the following command:
```
python run.py
```

You should be able to see it at: http://localhost:8080/

Swagger doc page: http://localhost:8080/apidocs/index.html

When you are done, you can use `Ctrl+C` to stop the server and then exit and shut down the vm with:
```
vagrant halt
```

## BlueMix deployment

Once there is an update on the master branch, BlueMix will auto build/deploy the latest working copy.
```
URL of your Swagger docs:
http://nyu-order-service-f17.mybluemix.net/apidocs/
http://pipeline-nyu-order-service-f17.mybluemix.net/apidocs/

PROD:
http://pipeline-nyu-order-service-f17.mybluemix.net/

DEV:
http://nyu-order-service-f17.mybluemix.net/
```

## BDD / TDD tests command when running locally

Use the following commands to test BDD and TDD results.
```
BDD: 
behave

TDD:
nosetests
```
 
