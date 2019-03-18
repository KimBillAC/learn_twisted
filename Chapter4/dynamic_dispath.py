from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from twisted.web.util import redirectTo
from datetime import datetime
from calendar import calendar


class YearPage(Resource):
    def __init__(self, year):
        Resource.__init__(self)
        self.year = year

    def render_GET(self, request):
        return '<html><body><pre>{}</pre></body></html>'.format(calendar(self.year)).encode()


class CalendarHome(Resource):
    def getChild(self, path, request):
        name = path.decode()
        if name == '':
            return self
        if name.isdigit():
            return YearPage(int(name))
        else:
            return NoResource()

    def render_GET(self, request):
        return redirectTo(str(datetime.now().year).encode(), request)


root = CalendarHome()
factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()