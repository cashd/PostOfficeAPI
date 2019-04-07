import pymysql.cursors


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
        cursor.execute("""INSERT INTO tracking (event_type, vehicle_fk_id, package_fk_id)
        VALUES( \'In Vehicle\', {}, {})""".format(truckID, row))
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

def moveFromTruckToFacility(data):
    packages = data['packages']
    truckID = data['truckID']
    facilityID = data['facilityID']

    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    for row in packages:
        cursor.execute("""UPDATE package SET pfacility_fk_id = {}, vehicle_id = NULL WHERE package_id = {}""".format(facilityID, row))
        cursor.execute("""INSERT INTO tracking (event_type, vehicle_fk_id, package_fk_id)
        VALUES( \'Arrived to Facility\', {}, {})""".format(facilityID, row))
        db.commit()

    return {'success': True}
