import pymysql.cursors
from customer import getEmailFromID, getAddressFromID
from facility import getFacilityType

#input: vehicle_id
def getTruckTypeFromID(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT destination_type FROM vehicle where vehicle_id = {} ;""".format(id))
    result = str(cursor.fetchone()[0])
    db.close()
    return result

#input: facilityID
def getAllTrucksAtFacility(facilityID):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS (SELECT * FROM vehicle WHERE vfacility_fk_id = {});  """.format(str(facilityID)))
    result = bool(cursor.fetchone()[0])
    if not result:
        respBody = {'empty': True, 'trucks': []}
    else:
        respBody = {'empty': False, 'trucks': []}
        cursor.execute("""SELECT vehicle.vehicle_id, employee.employee_first_name, employee.employee_last_name, vehicle.destination_type 
        FROM vehicle, employee WHERE vehicle.vfacility_fk_id = {} and vehicle.vehicle_id = employee.vehicle_fk_id;  """.format(str(facilityID)))
        results = cursor.fetchall()
        for row in results:
            #print(row[0])
            #print(row[1])
            #print(row[2])
            #print(row[3])
            respBody['trucks'].append({'truckID': row[0], 'driverFirstName': row[1], 'driverLastName': row[2],
                                         'type': row[3]})
    db.close()
    #print(respBody)
    return respBody

def moveFromFacilityToTruck(data):
    packages = data['packages']
    truckID = data['truckID']
    facilityID = data['facilityID']

    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    for row in packages:
        cursor.execute("""UPDATE package SET pfacility_fk_id = NULL, vehicle_id = {} WHERE package_id = {}""".format(truckID, row))
        cursor.execute("""INSERT INTO tracking (event_type, facility_fk_id, package_fk_id)
        VALUES( \'Left Facility\', {}, {})""".format(facilityID, row))
        db.commit()

    return {'success': True}

def deliverPackage(data):
    package = data['packageID']
    driverID = data['driverID']

    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""UPDATE package SET pfacility_fk_id = NULL, vehicle_id = NULL WHERE package_id = {}""".format(package))
    cursor.execute("""INSERT INTO tracking (event_type, package_fk_id)
        VALUES( \'Delivered\', {})""".format(package))
    db.commit()

    return {'success': True}

def dropoffPackage(data):
    package = data['packageID']
    facilityID = data['facilityID']

    data2 = getFacilityType({'facilityID': facilityID})

    if data2['type'] == "Drop Off":
        db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
        cursor = db.cursor()
        cursor.execute("""UPDATE package SET pfacility_fk_id = {}, vehicle_id = NULL WHERE package_id = {}""".format(facilityID, package))
        cursor.execute("""INSERT INTO tracking (event_type, facility_fk_id, package_fk_id)
            VALUES( \'Dropped Off\', {}, {})""".format(facilityID, package))
        db.commit()
        return {'success': True}
    else:
        return {'error': 'Facility is not a Drop Off facility.'}


def moveFromTruckToFacility(data):
    packages = data['packages']
    truckID = data['truckID']
    facilityID = data['facilityID']

    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    for row in packages:
        cursor.execute("""UPDATE package SET pfacility_fk_id = {}, vehicle_id = NULL WHERE package_id = {}""".format(facilityID, row))
        cursor.execute("""INSERT INTO tracking (event_type, facility_fk_id, package_fk_id)
        VALUES( \'Arrived to Facility\', {}, {})""".format(facilityID, row))
        db.commit()

    return {'success': True}

def getAllPackagesOnTruck(data):
    id = data['truckID']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT EXISTS (SELECT * FROM package WHERE vehicle_id = {});  """.format(str(id)))
    result = bool(cursor.fetchone()[0])
    if not result:
        respBody = {'empty': True, 'packages': []}
    else:
        respBody = {'empty': False, 'packages': []}
        cursor.execute("""SELECT package_id, sender_customer_id, recepient_customer_id, delivery_status, package_weight 
        FROM package WHERE vehicle_id = {};  """.format(str(id)))
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
