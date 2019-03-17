from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):

    def connectionMade(self):
        self.transport.write('Hello world!!'.encode())

    def dataReceived(self, data):
        print('server said: ' + data.decode())
        self.transport.loseConnection()


class EchoFactory(protocol.ClientFactory):

    protocol = EchoClient

    def clientConnectionLost(self, connector, reason):
        print('connection lost')
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed')
        reactor.stop()


reactor.connectTCP('localhost', 8000, EchoFactory())
reactor.run()