import pymysql.cursors
from customer import getIDfromEmail


def isCustomer(email, password):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute(
        """ SELECT EXISTS(select 1 FROM customer, auth_password_customer
        WHERE customer_password= \'{}\' AND customer_email = \'{}\' and customer_fk_pw_id = customer_id);"""
            .format(password, email))
    result = bool(cursor.fetchone()[0])
    db.close()
    print(result)
    return result


def isEmployeeFacility(email,password):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute(
        """ SELECT EXISTS(select * FROM employee, auth_password_employee
        WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id and employee_role = \'facility\');"""
            .format(password, email))
    result = bool(cursor.fetchone()[0])
    db.close()
    print(result)
    return result


def isEmployeeDriver(password, email):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute(
        """ SELECT EXISTS(select * FROM employee, auth_password_employee
        WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id and employee_role = \'driver\');"""
            .format(password, email))
    result = bool(cursor.fetchone()[0])
    db.close()
    print(result)
    return result

#see who is authorized to create employees and assign them to specific vehicles or facilities
def isManagerFacility(email,password):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute(
        """ SELECT EXISTS(select * FROM employee, auth_password_employee
        WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id and employee_role = \'supervisor\');"""
            .format(password, email))
    result = bool(cursor.fetchone()[0])
    db.close()
    print(result)
    return result

def isEmployee(email, password):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute(
        """ SELECT EXISTS(select * FROM employee, auth_password_employee
        WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id);"""
            .format(password, email))
    result = bool(cursor.fetchone()[0])

    db.close()
    #print(result)
    return result


def isAnyRole():
    return isCustomer() or isManagerFacility() or isEmployeeDriver() or isEmployeeFacility()

def setAuthCookiesResponse(resp, email, role):
    #change this to use the getEmpIDfromEmail function in employee.py
    if role == 'ManagerFacility':
        return resp
    resp.set_cookie('user_id', getIDfromEmail(email), domain='.team9postoffice.ga')
    resp.set_cookie('role', role, domain='.team9postoffice.ga')
    return resp

def makeEmpResponse(email,password):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()

    cursor.execute("""select employee_role FROM employee, auth_password_employee
            WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id;"""
                   .format(password, email))
    role = str(cursor.fetchone()[0])

    cursor.execute(""" SELECT employee_id FROM employee, auth_password_employee
                WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id;"""
                   .format(password, email))
    id = str(cursor.fetchone()[0])

    respBody = {'empty': 0}

    if role == 'supervisor':
        cursor.execute(""" SELECT facility_id FROM employee, auth_password_employee
                                            WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id;"""
                       .format(password, email))
        id2 = str(cursor.fetchone()[0])
        respBody = {'isAuth': True, 'role': 'employee', 'id': id, 'isManager': True, 'facilityID': id2}
        print('here1')

    if role == 'driver':
        cursor.execute(""" SELECT vehicle_fk_id FROM employee, auth_password_employee
                        WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id;"""
                       .format(password, email))
        id2 = str(cursor.fetchone()[0])
        respBody = {'isAuth': True, 'role': 'employee', 'id': id, 'isManager': False, 'truckID': id2}
        print('here3')

    if role == 'facility':
        cursor.execute(""" SELECT facility_id FROM employee, auth_password_employee
                                    WHERE employee_password= \'{}\' AND employee_work_email = \'{}\' and employee_id_fk = employee_id;"""
                       .format(password, email))
        id2 = str(cursor.fetchone()[0])
        respBody = {'isAuth': True, 'role': 'employee', 'id': id, 'isManager': False, 'facilityID': id2}
        print('here4')



    # print(role)
    # print(id)
    # print(isManager)
    db.close()
    return respBody