import pymysql.cursors


#input: vehicle_id
def getTruckTypeFromID(id):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""SELECT destination_type FROM vehicle where vehicle_id = {} ;""".format(id))
    result = str(cursor.fetchone()[0])
    db.close()
    return result

