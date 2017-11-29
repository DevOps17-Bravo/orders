# orders
A collection of order items created from products

##1. Instructions for using the environment 

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
 
 #BDD
 python run.py &
 behave
 
 #TDD
 nosetests
 ```
 
