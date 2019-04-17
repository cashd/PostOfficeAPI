import pymysql.cursors

def getIDfromEmail(email):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select customer_id from customer where customer_email = \'{}\';""".format(email))
    result = str(cursor.fetchone()[0])
    db.close()
    return result

def getEmailFromID(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select customer_email from customer where customer_id = {};""".format(id))
    result = str(cursor.fetchone()[0])
    db.close()
    return result

def getAddressFromID(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select customer_street_address from customer where customer_id = {};""".format(id))
    result = str(cursor.fetchone()[0])
    db.close()
    return result


def getStateID(state):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select state_id from state_lookup_table where state_name = \'{}\';""".format(state))
    stateid = int(cursor.fetchone()[0])
    db.close()
    return stateid

def getCityID(city):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select city_id from city_lookup_table where city = \'{}\';""".format(city))
    cityid = int(cursor.fetchone()[0])
    db.close()
    return cityid

def getStateFromStateID(stateID):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select state_name from state_lookup_table where state_id = {};""".format(stateID))
    state = str(cursor.fetchone()[0])
    db.close()
    return state

def getCityFromCityID(cityID):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select city from city_lookup_table where city_id = {};""".format(cityID))
    city = str(cursor.fetchone()[0])
    db.close()
    return city

def createCustomer(request):
    data = request.json
    fname = data['firstName']
    lname = data['lastName']
    address = data['address']
    email = data['email']
    city = data['cityid']
    cityid = getCityID(city)
    state = data['stateid']
    stateid = getStateID(state)
    phone = data['phoneNum']
    zipcode = str(data['zipcode'])
    password = data['password']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO `PostOffice`.`customer`
                (`customer_first_name`,
                `customer_last_name`,
                `customer_street_address`,
                `city_id`,
                `state_id`,
                `customer_zip_code`,
                `customer_phone_number`,
                `customer_email`)
                VALUES
                ( \'{}\',
                \'{}\',
                \'{}\',
                {},
                {},
                \'{}\',
                \'{}\',
                \'{}\');
    """.format(fname, lname, address, cityid, stateid, zipcode, phone, email))
        db.commit()

        cursor.execute("""select customer_id from PostOffice.customer
    where customer_email = \'{}\'""".format(email))

        id = int(cursor.fetchone()[0])

        cursor.execute("""INSERT INTO `PostOffice`.`auth_password_customer`
    (`customer_password`,
    `customer_fk_pw_id`)
    VALUES
    (\'{}\',
    {});""".format(password, id))
        db.commit()
    except Exception:
        db.close()
        return False

    db.close()
    return True

def getCustomerinfo(data):
    id = data['ID']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()

    cursor.execute("""SELECT `customer_first_name`,
                `customer_last_name`,
                `customer_street_address`,
                `city_id`,
                `state_id`,
                `customer_zip_code`,
                `customer_phone_number`,
                `customer_email`
                 FROM customer WHERE customer_id = {}""".format(id))
    results = cursor.fetchone()

    respBody = {'firstName': results[0], 'lastName': results[1], 'address': results[2], 'city': getCityFromCityID(results[3]),
                'state': getStateFromStateID(results[4]), 'zip': results[5], 'phoneNum': results[6],
                'email': results[7]}

    db.close()
    return respBody

def updateCustomerinfo(data):
    id = data['ID']
    fname = data['firstName']
    lname = data['lastName']
    address = data['address']
    city = data['city']
    cityid = getCityID(city)
    state = data['state']
    stateid = getStateID(state)
    zipcode = data['zip']
    phone = data['phoneNum']
    email = data['email']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')

    cursor = db.cursor()
    cursor.execute("""UPDATE `customer` SET 
                `customer_first_name` = \'{}\',
                `customer_last_name` = \'{}\',
                `customer_street_address` = \'{}\',
                `city_id` = {},
                `state_id` = {},
                `customer_zip_code` = \'{}\',
                `customer_phone_number` = \'{}\',
                `customer_email` = \'{}\'
                 WHERE customer_id = {};""".format(fname, lname, address, cityid, stateid, zipcode, phone, email, id))
    db.commit()
    db.close()
    respBody = {'success': True}
    return respBody