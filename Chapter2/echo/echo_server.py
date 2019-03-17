from twisted.internet import reactor, protocol


class EchoProtocol(protocol.Protocol):

    def dataReceived(self, data):
        self.transport.write(data)


class EchoFactory(protocol.Factory):

    protocol = EchoProtocol


reactor.listenTCP(8000, EchoFactory())
reactor.run()