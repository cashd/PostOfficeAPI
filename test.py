import requests
from auth import *
from employee import getEmpIDfromEmail
from package import *

#isCustomer
def testcase1():
    payload = {'email': 'money@gmail.com', 'password': 'plooploo'}
    r = requests.post('http://127.0.0.1:8000/auth', json=payload)
    print(r.text)
    print(r.headers)

#create customer
def testcase2():
    payload = {'firstName':'John', 'lastName': 'Doe', 'address' : '4412 Providence', 'email': 'jdoe@gmail.com', 'phoneNum':'3245552345', 'password': 'seven', 'cityid': 'Dallas', 'stateid': 'Texas', 'zipcode': 77559}
    r = requests.post('http://127.0.0.1:8000/signup/customer', json=payload)
    print(r.text)
    print(r.headers)
#isEmployee()
def testcase3():
    payload = {'email': 'test@usps.gov', 'password': 'test'}
    r = requests.post('http://127.0.0.1:8000/auth', json=payload)
    print(r.text)
    print(r.headers)

#test random functions here
def testcase4():
    getAllIncomingPackages(25)

#create employee
def testcase5():
    payload = {'managerId': 9, 'firstName':'Postal', 'lastName': 'Worker', 'address' : '4205 Clay', 'email': 'pw7@gmail.com', 'phoneNum':'8325556642', 'password': 'pass', 'cityid': 'Houston', 'stateid': 'Texas', 'zipcode': 77080, 'position': 'Clerk', 'role': 'facility', 'fkid': 1}
    r = requests.post('http://127.0.0.1:8000/manager/addEmployee', json=payload)
    print(r.text)
    print(r.headers)

#packagesSent or packages incoming
def testcase6():
    payload = {'id': 25 }
    r = requests.post('http://127.0.0.1:8000/customer/incomingpackages', json=payload)
    print(r.text)
    print(r.headers)

if __name__ == '__main__':
    testcase6()
