from twisted.internet import reactor, defer


class HeadLineReceiver:

    def processHeadLine(self, line):
        if len(line) > 50:
            self.d.errback(['the headline is too long'])
        else:
            self.d.callback(line)

    def _toHTML(self, res):
        return '<h1>{}</h1>'.format(res)

    def getHeadLine(self, input):
        self.d = defer.Deferred()
        reactor.callLater(1, self.processHeadLine, input)
        self.d.addCallback(self._toHTML)
        return self.d


def printData(res):
    print(res)


def printErr(err):
    print(err)


def stop(res):
    reactor.stop()


h = HeadLineReceiver()
d = h.getHeadLine('Breaking News: Twisted takes us to the moon')
# d = h.getHeadLine('Breaking News: Twisted takes us to the moon' + 'd' * 50)
d.addCallbacks(printData, printErr)
d.addCallback(stop)

reactor.run()