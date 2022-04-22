import datetime


def str2datetime(mmddyy):
    return datetime.datetime.strptime(mmddyy, '%d%m%y')

def aggiungi_anni(data, anni=1):
    return datetime.date(data.year + anni, data.month, data.day)
