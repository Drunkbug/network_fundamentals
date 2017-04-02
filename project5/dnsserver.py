import sys
from socketserver import UDPServer, BaseRequestHandler
import util

class MyUDPHandler(BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print (self.data)

class DNSServer(object):
    def __init__(self, port_, domain_):
        self.port = port_
        self.domain = domain_

    def run(self):
        HOST, PORT = self.domain, self.port
        server = UDPServer((HOST, PORT), MyUDPHandler)
        server.serve_forever()

inputs = sys.argv
port, domain = util.parse_dns_server_input(inputs)
dns_server = DNSServer(port, domain)

