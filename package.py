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
        cursor.execute("""SELECT package_id, recepient_customer_id, delivery_status, package_weight FROM package WHERE sender_customer_id = {};  """.format(str(id)))
        results = cursor.fetchall()
        for row in results:
            #print(row[0])
            #print(row[1])
            #print(row[2])
            weight = (str(row[3]) + 'oz')
            respBody['packages'].append({'id': row[0], 'senderEmail': senderEmail, 'recipientEmail': getEmailFromID(row[1]),
                                         'senderAddress': getAddressFromID(id), 'recipientAddress': getAddressFromID(row[1]),
                                         'deliveryStatus': row[2], 'packageWeight': weight})

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
        cursor.execute("""SELECT package_id, sender_customer_id, delivery_status, package_weight FROM package WHERE recepient_customer_id = {};  """.format(str(id)))
        results = cursor.fetchall()
        for row in results:
            #print(row[0])
            #print(row[1])
            #print(row[2])
            weight = (str(row[3]) + 'oz')
            respBody['packages'].append({'id': row[0], 'senderEmail': getEmailFromID(row[1]), 'recipientEmail': receiverEmail,
                                         'senderAddress': getAddressFromID(row[1]), 'recipientAddress': getAddressFromID(id),
                                         'deliveryStatus': row[2], 'packageWeight': weight})

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
    #data = request
    recipientEmail = data['recipientEmail']
    weight = float(data['weight'])
    senderID = data['senderID']
    recipientID = getIDfromEmail(recipientEmail)

    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("SELECT NOW()")
    date = str(cursor.fetchone()[0])

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

    cursor.execute("""INSERT INTO `package`
(`package_type`,
`sender_customer_id`,
`recepient_customer_id`,
`package_category`,
`delivery_status`,
`package_weight`)
VALUES
(\'{}\',
{},
{},
\'{}\',
\'Label Created\',
{});""".format(packageType,senderID,recipientID,packageCategory,weight))
    db.commit()
    db.close()
    return
