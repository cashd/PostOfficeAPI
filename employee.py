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
    fname = data['firstName']
    lname = data['lastName']
    position = data['position']
    address = data['address']
    email = data['email']
    city = data['cityid']
    cityid = getCityID(city)
    state = data['stateid']
    stateid = getStateID(state)
    phone = data['phoneNum']
    #workphone = data['workNum']
    zipcode = str(data['zipcode'])
    password = data['password']
    #startdate = data['startdate']
    #salary = float(data['salary'])
    #dob = data['dob']
    role = data['role']
    fkid = int(data['fkid'])
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
     `employee_zip_code`,
     `employee_cell_number`)
    VALUES
    (\'{}\',
     \'{}\',
     \'{}\',
     \'{}\',
     \'{}\',
     {},
     {},
     \'{}\',
     \'{}\');""".format(fname,lname,position,email,address,cityid,stateid,zipcode,phone))
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

    if role == 'driver':
        cursor.execute("""update employee set vehicle_fk_id = {} where employee_id = {} """.format(fkid,id))
    if role == 'facility' or role == 'supervisor':
        cursor.execute("""update employee set facility_id = {} where employee_id = {} """.format(fkid, id))
    db.commit()

    #except Exception:
    #    db.close()
    #    return False
    db.close()
    return True