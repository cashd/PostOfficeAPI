from flask import *
from auth import *
from customer import createCustomer
from employee import createEmployee
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
            id = getIDfromEmail(email)
            respBody = {'isAuth': True, 'role': 'customer' , 'id': id }
            resp = make_response(jsonify(respBody))
            #resp = setAuthCookiesResponse(resp, email, 'Customer')
            return resp
        elif isEmployee(email, password):
            resp = jsonify(makeEmpResponse(email,password))
            return resp
        else:
            return make_response(jsonify({'isAuth': False}))

@app.route('/signup/customer', methods=['POST'])
def signup():
    if "user_id" in request.cookies and 'role' in request.cookies:
        return make_response(jsonify(message='Signup Failed: You are already logged in.'), 400)
    else:
        isSuccess = createCustomer(request)
        if isSuccess:
            return make_response(jsonify({ "success": isSuccess }), 200)
        else:
            return make_response(jsonify({ "success": isSuccess }), 400)

@app.route('/manager/addEmployee', methods=['POST'])
def empSignup():
    data = request.json
    if isManager(data['managerId']) == False:
        return make_response(jsonify(message='Not Authorized'), 400)
    else:
        isSuccess = createEmployee(request)
        if isSuccess:
            return make_response(jsonify({ "success": isSuccess }), 200)
        else:
            return make_response(jsonify({ "success": isSuccess }), 400)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
