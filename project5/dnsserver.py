import sys
from util import *
from dnsmessage import *
from SocketServer import UDPServer, BaseRequestHandler

class MyUDPHandler(BaseRequestHandler):
    # use dig/drill @domain cs5700cdn.example.com to test
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        client_address = format(self.client_address[0])

        socket.sendto(data.upper(), self.client_address)


inputs = sys.argv
port, domain = parse_dns_server_input(inputs)

server = UDPServer(('', port), MyUDPHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

