from twisted.internet import reactor, protocol


class QuoteProtocol(protocol.Protocol):

    def connectionMade(self):
        self.sendQuote()

    def sendQuote(self):
        self.transport.write(self.factory.quote.encode())

    def dataReceived(self, data):
        print('receive quote: ' + data.decode())
        self.transport.loseConnection()


class QuoteFactory(protocol.ClientFactory):

    protocol = QuoteProtocol

    def __init__(self, quote):
        self.quote = quote

    def clientConnectionFailed(self, connector, reason):
        print('connection failed: ' + reason.getErrorMessage())
        maybeStopReactor()

    def clientConnectionLost(self, connector, reason):
        print('connection lost: ' + reason.getErrorMessage())
        maybeStopReactor()


def maybeStopReactor():
    global quote_counter
    quote_counter -= 1
    if not quote_counter:
        reactor.stop()


quotes = [
    'You snooze you lose',
    'The early bird gets the worm',
    'Carpe diem'
]
quote_counter = len(quotes)

for quote in quotes:
    reactor.connectTCP('localhost', 8000, QuoteFactory(quote))
reactor.run()