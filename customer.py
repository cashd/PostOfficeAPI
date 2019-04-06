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
        return False

    db.close()
    return True