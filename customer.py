import pymysql.cursors

def getIDfromEmail(email):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select customer_id from customer where customer_email = \'{}\';""".format(email))
    result = str(cursor.fetchone()[0])
    db.close()
    return result

def createCustomer(request):
    data = request.json
    fname = data['firstName']
    lname = data['lastName']
    address = data['address']
    email = data['email']
    cityid = int(data['cityid'])
    stateid = int(data['stateid'])
    phone = data['phoneNum']
    zipcode = data['zipcode']
    password = data['password']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
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
#reduce all the redundancies in the auth and customer, right now they link to each other in too many ways making updates difficult
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
    db.close()
