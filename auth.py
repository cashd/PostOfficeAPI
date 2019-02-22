import pymysql.cursors
from customer import getIDfromEmail


def isConsumer(email, password):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute(
        """ select exists(select 1 from Customer where Customer_Email = \'{}\' and Customer_Password = \'{}\') """
            .format(email, password))
    result = bool(cursor.fetchone()[0])
    db.close()
    return result


def isFacility(request):
    return False


def isDriver(request):
    return False


def isAnyRole():
    return isConsumer() or isFacility() or isDriver()

def setAuthCookiesResponse(resp, email, role):
    resp.set_cookie('user_id', getIDfromEmail(email))
    resp.set_cookie('role', role)
    return resp




