from flask import *
from auth import *
from customer import createCustomer
from employee import *
from package import *
from vehicle import getTruckTypeFromID
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
    if not isManager(data['managerId']):
        return make_response(jsonify(message='Not Authorized'), 400)
    else:
        isSuccess = createEmployee(request)
        if isSuccess:
            return make_response(jsonify({ "success": isSuccess }), 200)
        else:
            return make_response(jsonify({ "success": isSuccess }), 400)

@app.route('/customer/packages', methods=['POST'])
def packagesSent():
    data = request.json
    id = data['id']
    return make_response(jsonify(getAllSentPackages(id)), 200)

@app.route('/customer/incomingpackages', methods=['POST'])
def packagesIncoming():
    data = request.json
    id = data['id']
    return make_response(jsonify(getAllIncomingPackages(id)), 200)

@app.route('/truck/type', methods=['POST'])
def truckType():
    data = request.json
    truckID = data['truckID']
    return make_response(jsonify({"truckType": getTruckTypeFromID(truckID)}), 200)

@app.route('/customer/newPackage', methods=['POST'])
def newPackage():
    createPackage(request)
    return make_response(jsonify({"success": True}), 200)

@app.route('/facility/employees', methods=['POST'])
def employeesInFacility():
    data = request.json
    if not isManager(data['managerID']):
        return make_response(jsonify(message='Not Authorized'), 400)
    else:
        facilityid = data['facilityID']
        return make_response(jsonify(getAllEmployeesInFacility(facilityid), 200))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
