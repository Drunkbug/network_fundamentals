import sys
from socketserver import UDPServer, BaseRequestHandler
import util

class MyUDPHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print (data)
        print (socket)

class DNSServer(object):
    def __init__(self, port_, domain_):
        self.port = port_
        self.domain = domain_

inputs = sys.argv
port, domain = util.parse_dns_server_input(inputs)

# run dns server
dns_server = DNSServer(port, domain)
server = UDPServer(('', port), MyUDPHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

