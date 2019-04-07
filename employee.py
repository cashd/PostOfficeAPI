import pymysql.cursors
from customer import getStateID
from customer import getCityID
from auth import isManager

def getEmpIDfromEmail(email):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select employee_id from employee where employee_work_email = \'{}\';""".format(email))
    result = str(cursor.fetchone()[0])
    db.close()
    return result

def createEmployee(request):
    data = request.json
    managerID = data['managerID']
    fname = data['firstName']
    lname = data['lastName']
    position = data['position']
    address = data['address']
    email = data['email']
    city = data['city']
    cityid = getCityID(city)
    state = data['state']
    stateid = getStateID(state)
    phone = data['phoneNum']
    #workphone = data['workNum']
    zipcode = str(data['zip'])
    password = data['password']
    #startdate = data['startdate']
    salary = float(data['salary'])
    #dob = data['dob']
    role = data['role']
    fkid = int(data['facilityID'])
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    #try:
    cursor.execute("""
    INSERT
    INTO
    `PostOffice`.
    `employee`
    (`employee_first_name`,
     `employee_last_name`,
     `employee_position`,
     `employee_work_email`,
     `employee_address`,
     `city_id`,
     `state_id`,
     `employee_salary`,
     `employee_zip_code`,
     `employee_work_number`)
    VALUES
    (\'{}\',
     \'{}\',
     \'{}\',
     \'{}\',
     \'{}\',
     {},
     {},
     {},
     \'{}\',
     \'{}\');""".format(fname,lname,position,email,address,cityid,stateid,salary,zipcode,phone))
    db.commit()

    cursor.execute("""select employee_id from employee
    where employee_work_email = \'{}\'""".format(email))
    id = int(cursor.fetchone()[0])

    cursor.execute("""INSERT INTO
    `PostOffice`.
    `auth_password_employee`
    (`employee_id_fk`,
     `employee_password`,
     `employee_role`)
    VALUES
    ({},
     \'{}\',
     \'{}\');""".format(id,password,role))
    db.commit()

    #if role == 'Driver':
        #cursor.execute("""update employee set vehicle_fk_id = {} where employee_id = {} """.format(fkid,id))
    #if role == 'Facility' or role == 'Supervisor':
    cursor.execute("""update employee set facility_id = {} where employee_id = {} """.format(fkid, id))
    db.commit()

    #except Exception:
    #    db.close()
    #    return False
    db.close()
    return True

def getAllEmployeesInFacility(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS (SELECT * FROM employee WHERE facility_id = {});  """.format(str(id)))
    result = bool(cursor.fetchone()[0])
    if not result:
        respBody = {'empty': True, 'employees': []}
    else:
        respBody = {'empty': False, 'employees': []}
        cursor.execute("""SELECT employee_id, employee_first_name, employee_last_name, employee_position, employee_work_number, 
        employee_work_email ,employee_salary FROM employee WHERE facility_id = {};  """.format(str(id)))
        results = cursor.fetchall()
        for row in results:
            #print(row[0])
            #print(row[1])
            print(row[6])
            respBody['employees'].append({'id': row[0], 'firstName': row[1], 'lastName': row[2],
                                         'position': row[3], 'workPhoneNum': row[4], 'workEmail': row[5], 'salary': int(row[6])})
    db.close()

    print(result)
    print(respBody)
    return respBody