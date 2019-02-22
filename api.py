from flask import *
from auth import *
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/auth', methods=['POST'])
def authenticate():
        # Check to see if the username is already authenticated
    if "user_id" in request.cookies and 'role' in request.cookies:
        data = {'isAuth': True, 'role': str(request.cookies['role'])}
        return jsonify(data)
    else:
        # Else we need to verify to see if the provided information is valid
        data = request.json
        email = data['email']
        password = data['password']
        if isConsumer(email, password):
            respBody = {'isAuth': True, 'role': 'Customer'}
            resp = make_response(jsonify(respBody))
            resp = setAuthCookiesResponse(resp, email, 'Customer')
            return resp
        if isFacility(request):
            respBody = {'isAuth': True, 'role': 'Facility'}
            resp = make_response(jsonify(respBody))
            resp = setAuthCookiesResponse(resp, email, 'Facility')
            return resp
        if isDriver(request):
            respBody = {'isAuth': True, 'role': 'Driver'}
            resp = make_response(jsonify(respBody))
            resp = setAuthCookiesResponse(resp, email, 'Driver')
            return resp

