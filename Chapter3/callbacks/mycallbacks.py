from twisted.internet.defer import Deferred


def addB(res):
    return '<b>{}</b>'.format(res)


def addI(res):
    return '<i>{}</i>'.format(res)


def printHTML(res):
    print(res)


d = Deferred()
d.addCallback(addB)
d.addCallback(addI)
d.addCallback(printHTML)
d.callback('jjj')