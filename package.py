from customer import getEmailFromID
from customer import getAddressFromID
import pymysql.cursors

def getAllSentPackages(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS (SELECT * FROM package WHERE sender_customer_id = {});  """.format(str(id)))
    result = bool(cursor.fetchone()[0])
    if not result:
        respBody = {'empty': True}
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
        respBody = {'empty': True}
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

