import requests
from auth import isManagerFacility
from auth import isEmployeeFacility
from auth import isEmployeeDriver
from auth import isEmployee

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

#isEmployee()
def testcase4():
#    payload = {'email': 'sosu@gmail.com', 'password': 'pwd123'}
#    r = requests.post('http://127.0.0.1:8000/auth', json=payload)
#    print(r.text)
#    print(r.headers)
    print(isEmployee('fastguy@gmail.com','speedy'))

if __name__ == '__main__':
    testcase2()
