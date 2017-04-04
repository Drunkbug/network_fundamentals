import sys
from util import *
from dnsmessage import DNSMessageHandler
from SocketServer import UDPServer, BaseRequestHandler

# read and parse inputs
inputs = sys.argv
PORT, DOMAIN= parse_dns_server_input(inputs)

class MyUDPHandler(BaseRequestHandler):
    # use dig/drill @<ip> cs5700cdn.example.com -p <port> to test
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        client_address = format(self.client_address[0])
        
        dns_message_handler = DNSMessageHandler(DOMAIN, client_address)
        dns_message_handler.build_dns_message(data)

        socket.sendto(data.upper(), self.client_address)


# establish DNS server
server = UDPServer(('', PORT), MyUDPHandler)
# start DNS server
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

