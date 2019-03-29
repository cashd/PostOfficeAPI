import pymysql.cursors
from customer import getIDfromEmail


def isCustomer(email, password):
    db = pymysql.connect('178.128.64.18', 'team9', 'team9PostOffice', 'PostOffice')
    cursor = db.cursor()
    cursor.execute(
        """ SELECT EXISTS(select 1 FROM customer, auth_password_customer
        WHERE customer_password= \'{}\' AND customer_email = \'{}\' and customer_fk_pw_id = customer_id);"""
            .format(password, email))
    result = bool(cursor.fetchone()[0])
    db.close()
    print(result)
    return result


def isFacility(request):
    return False


def isDriver(request):
    return False


def isAnyRole():
    return isCustomer() or isFacility() or isDriver()

def setAuthCookiesResponse(resp, email, role):
    resp.set_cookie('user_id', getIDfromEmail(email), domain='.team9postoffice.ga')
    resp.set_cookie('role', role, domain='.team9postoffice.ga')
    return resp




