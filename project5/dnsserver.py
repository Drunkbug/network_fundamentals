import sys
from util import *
from dnsmessage import DNSMessageHandler
from SocketServer import UDPServer, BaseRequestHandler

# read and parse inputs
inputs = sys.argv
PORT, DOMAIN= parse_dns_server_input(inputs)
RECORD = 'ec2-54-85-79-138.compute-1.amazonaws.com'

class MyUDPHandler(BaseRequestHandler):
    # use dig/drill @<ip> cs5700cdn.example.com -p <port> to test
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        # TODO choose best replica
        client_ip = format(self.client_address[0])
        ip_address = '54.85.79.138'
        
        dns_message_handler = DNSMessageHandler(DOMAIN, ip_address)
        dns_message_packet = dns_message_handler.build_dns_message(data)
        print dns_message_packet

        socket.sendto(dns_message_packet, self.client_address)


# establish DNS server
server = UDPServer(('', PORT), MyUDPHandler)
# start DNS server
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

