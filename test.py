import requests
if __name__ == '__main__':
    payload = {'email': 'bob@gmail.com', 'password': 'burger'}
    r = requests.post('http://127.0.0.1:5000/auth', json=payload)
    print(r.text)
    print(r.headers)
