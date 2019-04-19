from customer import *
import pymysql.cursors

def getAllSentPackages(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS (SELECT * FROM package WHERE sender_customer_id = {});  """.format(str(id)))
    result = bool(cursor.fetchone()[0])
    if not result:
        respBody = {'empty': True, 'packages': []}
    else:
        senderEmail = getEmailFromID(id)
        respBody = {'empty': False, 'packages': []}
        cursor.execute("""SELECT package_id, recepient_customer_id, delivery_status, package_weight, postage_paid FROM package WHERE sender_customer_id = {};  """.format(str(id)))
        results = cursor.fetchall()
        for row in results:
            #print(row[0])
            #print(row[1])
            #print(row[2])
            weight = (str(row[3]) + 'oz')
            respBody['packages'].append({'id': row[0], 'senderEmail': senderEmail, 'recipientEmail': getEmailFromID(row[1]),
                                         'senderAddress': getAddressFromID(id), 'recipientAddress': getAddressFromID(row[1]),
                                         'deliveryStatus': row[2], 'packageWeight': weight, 'price': float(row[4])})

    db.close()

    print(result)
    print(respBody)
    return respBody

def getAllIncomingPackages(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS (SELECT * FROM package WHERE recepient_customer_id = {});  """.format(str(id)))
    result = bool(cursor.fetchone()[0])
    if not result:
        respBody = {'empty': True, 'packages': []}
    else:
        receiverEmail = getEmailFromID(id)
        respBody = {'empty': False, 'packages': []}
        cursor.execute("""SELECT package_id, sender_customer_id, delivery_status, package_weight, postage_paid FROM package WHERE recepient_customer_id = {};  """.format(str(id)))
        results = cursor.fetchall()
        for row in results:
            #print(row[0])
            #print(row[1])
            #print(row[2])
            weight = (str(row[3]) + 'oz')
            respBody['packages'].append({'id': row[0], 'senderEmail': getEmailFromID(row[1]), 'recipientEmail': receiverEmail,
                                         'senderAddress': getAddressFromID(row[1]), 'recipientAddress': getAddressFromID(id),
                                         'deliveryStatus': row[2], 'packageWeight': weight, 'price': float(row[4])})

    db.close()

    print(result)
    print(respBody)
    return respBody

def getAllPackagesInFacility(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS (SELECT * FROM package WHERE pfacility_fk_id = {});  """.format(str(id)))
    result = bool(cursor.fetchone()[0])
    if not result:
        respBody = {'empty': True, 'packages': []}
    else:
        respBody = {'empty': False, 'packages': []}
        cursor.execute("""SELECT package_id, sender_customer_id, recepient_customer_id, delivery_status, package_weight 
        FROM package WHERE pfacility_fk_id = {};  """.format(str(id)))
        results = cursor.fetchall()
        for row in results:
            #print(row[0])
            #print(row[1])
            #print(row[2])
            #print(row[3])
            #print(row[4])
            senderEmail = getEmailFromID(row[1])
            receiverEmail = getEmailFromID(row[2])
            weight = (str(row[4]) + 'oz')
            respBody['packages'].append({'id': row[0], 'senderEmail': senderEmail, 'recipientEmail': receiverEmail,
                                         'senderAddress': getAddressFromID(row[1]), 'recipientAddress': getAddressFromID(row[2]),
                                         'deliveryStatus': row[3], 'packageWeight': weight})

    db.close()
    #print(respBody)
    return respBody


def createPackage(request):
    data = request.json
    recipientEmail = data['recipientEmail']
    weight = float(data['weight'])
    senderID = data['senderID']
    recipientAddress = data['recipientAddress']


    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')

    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS(SELECT * FROM customer WHERE customer_email = \'{}\');""".format(recipientEmail));
    found = bool(cursor.fetchone()[0])
    if not found:
        cursor.execute("""INSERT INTO `PostOffice`.`customer`
                     (`customer_first_name`,
                     `customer_last_name`,
                     `customer_street_address`,
                     `city_id`,
                     `state_id`,
                     `customer_zip_code`,
                     `customer_email`)
                     VALUES
                     ( \'{}\',
                     \'{}\',
                     \'{}\',
                     {},
                     {},
                     \'{}\',
                     \'{}\');
         """.format('###', '###', recipientAddress, 0, 0, '###', recipientEmail))
        db.commit()
        recipientID = cursor.lastrowid
    else:
        recipientID = getIDfromEmail(recipientEmail)
    price = .49
    if weight <= 2:
        packageCategory = 'small'
        packageType = 'Letter'
    else:
        if weight > 2 and weight <= 32:
            packageCategory = 'Small'
            packageType = 'Flat Envelope'
        else:
            packageCategory = 'Large'
            packageType = 'Parcel'
        price += .1 * (weight - 2)

    cursor.execute("""INSERT INTO `package`
(`package_type`,
`sender_customer_id`,
`recepient_customer_id`,
`package_category`,
`delivery_status`,
`package_weight`,
`postage_paid`)
VALUES
(\'{}\',
{},
{},
\'{}\',
\'Label Created\',
{},
{});""".format(packageType,senderID,recipientID,packageCategory,weight,price))
    db.commit()
    packageID = cursor.lastrowid
    cursor.execute("""INSERT INTO tracking (event_type, package_fk_id)
        VALUES( \'Label Created\', {})""".format(packageID))
    db.commit()
    db.close()
    return

def getHistory(data):
    packageID = data['packageID']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    respBody = {'packageID': packageID, 'history': []}
    cursor.execute("""SELECT event_type, time_of_event, facility_fk_id FROM tracking WHERE package_fk_id = {}""".format(packageID))
    results = cursor.fetchall()
    for row in results:
        print(row[0])
        print(row[1])
        print(row[2])
        if row[0] == "Arrived to Facility" or row[0] == "Dropped Off" or row[0] == "Left Facility":
            cursor.execute("""SELECT facility_address FROM facility WHERE facility_id = {}""".format(row[2]))
            address = cursor.fetchone()[0]
            respBody['history'].append({'eventType': row[0], 'timeOfEvent': row[1], 'locationOfEvent': address})
        if row[0] == "Delivered":
            cursor.execute("""SELECT customer_street_address FROM package, customer WHERE package.package_id = {} AND 
            customer_id = recepient_customer_id""".format(packageID))
            address = cursor.fetchone()[0]
            respBody['history'].append({'eventType': row[0], 'timeOfEvent': row[1], 'locationOfEvent': address})
        if row[0] == "Label Created":
            cursor.execute("""SELECT customer_street_address FROM package, customer WHERE package.package_id = {} AND 
            customer_id = sender_customer_id""".format(packageID))
            address = cursor.fetchone()[0]
            respBody['history'].append({'eventType': row[0], 'timeOfEvent': row[1], 'locationOfEvent': address})
    db.close()
    return respBody


def packageReport():
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT delivery_status, COUNT(*) FROM package GROUP BY delivery_status;""")
    results = cursor.fetchall()
    cursor.execute("""SELECT SUM(postage_paid), AVG(postage_paid) FROM package;""")
    stats = cursor.fetchone()
    respBody = {'counts': [], 'sumPrice': float(stats[0]), 'avgPrice': float(stats[1])}
    for row in results:
        print(row[0])
        print(row[1])
        respBody['counts'].append({'eventType': row[0], 'count': row[1]})
    db.close()
    return respBody

def packageRevenueReport():
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT date(date_received) AS Day, SUM(postage_paid) FROM package GROUP BY
    date(date_received)
    order by Day;""")
    results = cursor.fetchall()
    respBody = {'Revenue By Day': []}
    for row in results:
        print(row[0], row[1])
        #print(row[1])
        respBody['Revenue By Day'].append({'Date': row[0], 'Postage Revenue': float(row[1])})
    db.close()
    return respBody