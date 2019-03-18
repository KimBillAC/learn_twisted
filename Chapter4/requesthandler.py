from twisted.internet import reactor
from twisted.web import http


class MyRequestHandler(http.Request):

    resource = {
        '/': '<h1>Home</h1> Home Page',
        '/about': '<h1>About</h1> all about me'
    }

    def process(self):

        self.setHeader('Content-Type'.encode(), 'text/html'.encode())
        path = self.path.decode()
        if path in self.resource:
            self.write(self.resource[path].encode())
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('<h1>Not Found</h1> no such resource'.encode())
        self.finish()


class MyHTTP(http.HTTPChannel):

    requestFactory = MyRequestHandler


class MyHTTPFactory(http.HTTPFactory):

    protocol = MyHTTP


reactor.listenTCP(8000, MyHTTPFactory())
reactor.run()