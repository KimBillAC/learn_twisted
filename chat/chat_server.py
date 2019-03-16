from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver


class ChatProtocol(LineReceiver):

    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = 'REGISTER'

    def connectionMade(self):
        self.sendLine("What is your name?".encode())
        self.sendLine(str(id(self)).encode())

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.boardcastMessage('{} has left the channel'.format(self.name))

    def lineReceived(self, line):
        if self.state == 'REGISTER':
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        if name in self.factory.users:
            self.sendLine('Name exist, please choose another'.encode())
            return
        self.sendLine('Welcome {}'.format(name).encode())
        self.boardcastMessage('{} has joined the channel'.format(name))
        self.name = name
        self.factory.users[name] = self
        self.state = 'CHAT'

    def handle_CHAT(self, message):
        m = '<{0}> {1}'.format(self.name, message)
        self.boardcastMessage(m)

    def boardcastMessage(self, message):
        for name, p in self.factory.users.items():
            if p != self:
                p.sendLine(message.encode())


class ChatFactory(protocol.Factory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)


reactor.listenTCP(8000, ChatFactory())
reactor.run()