import requests
if __name__ == '__main__':
    payload = {'email': 'bob@gmail.com', 'password': 'burger'}
    r = requests.post('http://api.team9postoffice.ga/auth', json=payload)
    print(r.text)
    print(r.headers)
