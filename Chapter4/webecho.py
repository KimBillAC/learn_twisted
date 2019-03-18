from twisted.internet import reactor, protocol
from twisted.protocols import basic


class HTTPEchoProtocol(basic.LineReceiver):

    def __init__(self):
        self.lines = []

    def lineReceived(self, line):
        self.lines.append(line.decode())
        if not line:
            self.sendResponse()

    def sendResponse(self):

        self.sendLine('HTTP/1.1 200 OK'.encode())
        self.sendLine(''.encode())
        respond_body = 'you said:\r\n\r\n' + '\r\n'.join(self.lines)
        self.sendLine(respond_body.encode())
        self.transport.loseConnection()


class HTTPFactory(protocol.ServerFactory):

    protocol = HTTPEchoProtocol


reactor.listenTCP(8000, HTTPFactory())
reactor.run()