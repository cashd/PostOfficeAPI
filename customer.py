import pymysql.cursors

def getIDfromEmail(email):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute("""select Customer_Id from Customer where Customer_Email = \'{}\';""".format(email))
    result = str(cursor.fetchone()[0])
    db.close()
    return result
