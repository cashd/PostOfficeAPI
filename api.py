from flask import *
from auth import *
from customer import createCustomer
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
        if isCustomer(email, password):
            respBody = {'isAuth': True, 'role': 'Customer'}
            resp = make_response(jsonify(respBody))
            resp = setAuthCookiesResponse(resp, email, 'Customer')
            return resp
        elif isManagerFacility(email, password):
            respBody = {'isAuth': True, 'role': 'ManagerFacility'}
            resp = make_response(jsonify(respBody))
            resp = setAuthCookiesResponse(resp, email, 'ManagerFacility')
            return resp
        elif isEmployeeFacility(request):
            respBody = {'isAuth': True, 'role': 'Facility'}
            resp = make_response(jsonify(respBody))
            resp = setAuthCookiesResponse(resp, email, 'Facility')
            return resp
        elif isEmployeeDriver(request):
            respBody = {'isAuth': True, 'role': 'Driver'}
            resp = make_response(jsonify(respBody))
            resp = setAuthCookiesResponse(resp, email, 'Driver')
            return resp
        else:
            return make_response(jsonify({'isAuth': False}))

@app.route('/signup/customer', methods=['POST'])
def signup():
    if "user_id" in request.cookies and 'role' in request.cookies:
        return make_response(jsonify(message='Signup Failed: You are already logged in.'), 400)
    else:
        createCustomer(request)
        return make_response(jsonify({ "success": True }), 200)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
