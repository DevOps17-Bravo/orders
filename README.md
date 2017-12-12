# orders
A collection of orders created from products

[![Build Status](https://travis-ci.org/DevOps17-Bravo/orders.svg?branch=master)](https://travis-ci.org/DevOps17-Bravo/orders)
[![Codecov](https://img.shields.io/codecov/c/github/DevOps17-Bravo/orders.svg)]()

Finally you can see the microservice at: http://localhost:8080/

The Swagger docs can be accessed at: http://localhost:8080/apidocs/index.html

The raw Swagger specification JSON can be found at: http://localhost:8080/v1/spec


## 1. Instructions for using the environment 

-**Download from github:**
```
git clone https://github.com/DevOps17-Bravo/orders.git
```

-**Enter the folder:**
```
cd orders
```

-**to start vm:**
```
vagrant up
```

-**to update vagrantfile:**
```
vagrant provision
```

-**connect to the environment:**
```
vagrant ssh
```

-**get into folder:** 
```
cd /vagrant
```

-**run server:**
```
python server.py
```

-**exit environment:**
```
exit
```

-**shut down vm:**
```
vagrant halt
```

-**how to run coverage:**
```
 coverage run --omit "venv/*" test_server.py

 coverage report -m --include= server.py

 result coverage: 91%

 coverage run --omit "venv/*" test_orders.py

 coverage report -m --include= models.py

 result coverage: 98%
 ```
 
 -**how to run the BDD and TDD tests:**
 ```
 cd /vagrant

 # BDD
 python run.py &
 behave

 # TDD
 nosetests
 ```
 
