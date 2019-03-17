from twisted.internet.defer import Deferred


def mycallback(data):
    print(data)


def myerrback(data):
    print(data)


d = Deferred()
d.addCallbacks(mycallback, myerrback)
d.callback(456)
# d.errback(123)
