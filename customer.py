import pymysql.cursors

def getIDfromEmail(email):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select customer_id from customer where customer_email = \'{}\';""".format(email))
    result = str(cursor.fetchone()[0])
    db.close()
    return result
