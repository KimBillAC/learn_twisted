from twisted.internet import reactor, protocol


class QuoteProtocol(protocol.Protocol):

    def connectionMade(self):
        self.factory.numConnection += 1

    def dataReceived(self, data):
        d = data.decode()
        print('Number of active connection: {}'.format(self.factory.numConnection))
        print('> Receive: {0}\n> Sending: {1}'.format(d, self.getQuote()))
        self.transport.write(self.getQuote().encode())
        self.updateQuote(d)

    def connectionLost(self, reason):
        self.factory.numConnection -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote


class QuoteFactory(protocol.Factory):
    numConnection = 0
    protocol = QuoteProtocol

    def __init__(self, quote=None):
        self.quote = quote or "An apple a day keeps the doctor away"

    # def buildProtocol(self, addr):
    #     return QuoteProtocol(self)


reactor.listenTCP(8000, QuoteFactory())
reactor.run()