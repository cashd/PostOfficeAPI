import pymysql.cursors

def getAllFacilities():

    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()

    respBody = {'empty': False, 'facilities': []}
    cursor.execute("""SELECT facility_id, facility_address, city_id, state_id, facility_zip_code 
        FROM facility;""")
    results = cursor.fetchall()
    for row in results:
       # print(row[0])
       # print(row[1])
       # print(row[2])
       # print(row[3])
       # print(row[4])
        cursor.execute("""SELECT city FROM city_lookup_table WHERE city_id = {}""".format(row[2]))
        city = cursor.fetchone()[0]
        cursor.execute("""SELECT state_name FROM state_lookup_table WHERE state_id = {}""".format(row[3]))
        state = cursor.fetchone()[0]
        respBody['facilities'].append({'facilityID': row[0], 'address': row[1], 'city': city, 'state': state, 'zip': row[4]})
    db.close()
    print(respBody)
    return respBody

def getFacilityType(data):
    facilityID = data['facilityID']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT facility_type FROM facility WHERE facility_id = {};""".format(facilityID))
    result = cursor.fetchone()[0]
    db.close()
    return {'type': result}

def facilityReport(data):
    facilityID = data['facilityID']
    month = data['month']
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT DATE(`tracking`.`time_of_event`) AS `Date`,
COUNT(*) AS `Packages Arrived`
FROM `PostOffice`.`tracking`
WHERE `tracking`.`event_type` = 'Arrived to Facility' AND `tracking`.`facility_fk_id`= {}
AND MONTH(time_of_event) = {}
GROUP BY DATE(`tracking`.`time_of_event`);""".format(facilityID, month))
    results = cursor.fetchall()
    respBody = {'list': []}
    for row in results:
        print(row[0], row[1])
        respBody['list'].append({'Date': row[0], 'value': row[1]})
    db.close()
    return respBody