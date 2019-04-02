import requests

#isCustomer
def testcase1():
    payload = {'email': 'notexistent@hotmail.com', 'password': 'password'}
    r = requests.post('http://127.0.0.1:8000/auth', json=payload)
    print(r.text)
    print(r.headers)

#create customer
def testcase2():
    payload = {'firstName':'Cash', 'lastName': 'DeLeon', 'address' : '123 GH', 'email': 'money@gmail.com', 'phoneNum':'324502345', 'password': 'plooploo', 'cityid': 'Houston', 'stateid': 'Texas', 'zipcode': 77259}
    r = requests.post('http://127.0.0.1:8000/signupCustomer', json=payload)
    print(r.text)
    print(r.headers)
#isManagerFacility
def testcase3():
    payload = {'email': 'sosu@gmail.com', 'password': 'pwd123'}
    r = requests.post('http://127.0.0.1:8000/auth', json=payload)
    print(r.text)
    print(r.headers)

if __name__ == '__main__':
    testcase2()
