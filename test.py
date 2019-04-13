import requests
from auth import *
from employee import *
from package import *
from vehicle import *
from facility import *

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
    print(dropoffPackage({'packageID': 9, 'facilityID': 3}))

#create employee
def testcase5():
    payload = {'managerID': 9, 'firstName':'Postal', 'lastName': 'Worker', 'address' : '4205 Clay', 'email': 'pw14@gmail.com', 'phoneNum':'8325556642', 'password': 'pass',
               'city': 'Houston', 'state': 'Texas', 'zip': 77080, 'position': 'Clerk', 'role': 'Facility', 'facilityID': 1, 'salary': 25000 }
    r = requests.post('http://127.0.0.1:8000/manager/addEmployee', json=payload)
    print(r.text)
    print(r.headers)

#packagesSent or packages incoming
def testcase6():
    payload = {'id': 25 }
    r = requests.post('http://127.0.0.1:8000/customer/incomingpackages', json=payload)
    print(r.text)
    print(r.headers)

#truck type
def testcase7():
    payload = {'id': 25, 'truckID': 13}
    r = requests.post('http://127.0.0.1:8000/truck/type', json=payload)
    print(r.text)
    print(r.headers)

#create package
def testcase8():
    payload = {'senderID': 8, 'recipientEmail': 'new@gmail.com', 'recipientAddress': '456 New Rd', 'weight': 5.5}
    r = requests.post('http://127.0.0.1:8000/customer/newPackage', json=payload)
    print(r.text)
    print(r.headers)

#get all employees in facility
def testcase9():
    payload = {'managerID': 9, 'facilityID': 9}
    r = requests.post('http://127.0.0.1:8000/facility/employees', json=payload)
    print(r.text)
    print(r.headers)

#get all packages in facility
def testcase10():
    payload = {'facilityID': 1}
    r = requests.post('http://127.0.0.1:8000/facility/packages', json=payload)
    print(r.text)
    print(r.headers)

#get all trucks in facility
def testcase11():
    payload = {'facilityID': 4}
    r = requests.post('http://127.0.0.1:8000/facility/trucks', json=payload)
    print(r.text)
    print(r.headers)

#move from facility to truck
def testcase12():
    payload = {'packages': [12], 'truckID': 4, 'facilityID': 3}
    r = requests.post('http://127.0.0.1:8000/facility/move', json=payload)
    print(r.text)
    print(r.headers)

#deliver package
def testcase13():
    payload = {'packageID': 6, 'driverID': 4}
    r = requests.post('http://127.0.0.1:8000/truck/deliver', json=payload)
    print(r.text)
    print(r.headers)

#move from truck to facility
def testcase14():
    payload = {'packages': [13, 14, 15], 'truckID': 4, 'facilityID': 2}
    r = requests.post('http://127.0.0.1:8000/truck/travel', json=payload)
    print(r.text)
    print(r.headers)

#get all packages on truck
def testcase15():
    payload = {'truckID': 4}
    r = requests.post('http://127.0.0.1:8000/truck/packages', json=payload)
    print(r.text)
    print(r.headers)

def testcase16():
    payload = {}
    r = requests.post('http://127.0.0.1:8000/facility/all', json=payload)
    print(r.text)
    print(r.headers)

def testcase17():
    payload = {'facilityID': 3}
    r = requests.post('http://127.0.0.1:8000/facility/type', json=payload)
    print(r.text)
    print(r.headers)

def testcase18():
    payload = {'packageID': 12}
    r = requests.post('http://127.0.0.1:8000/package/history', json=payload)
    print(r.text)
    print(r.headers)

def testcase19():
    payload = {'packageID': 20, 'facilityID': 3}
    r = requests.post('http://127.0.0.1:8000/facility/checkin', json=payload)
    print(r.text)
    print(r.headers)

if __name__ == '__main__':
    testcase6()
