import sys
from util import *
from dnsmessage import DNSMessageHandler
import socket


class DNSServer(object):

    """ DNS server object
    establish and run the server with socket

    Attributes:
        udp_server: a socket object for establishing dns server
    """
    def __init__(self):
        self.udp_server = None

    def build_server(self):
        """ init dns server class with socket"""
        self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print (PORT)
        self.udp_server.bind(('', PORT))

    def serve_forever(self):
        """ parsing client information and request
            send dns message back to client
        """
        try:
            while 1:
                data, client_address = self.udp_server.recvfrom(1024)
                ip_address = '54.85.79.138'
                # parse and bulid dns message
                dns_message_handler = DNSMessageHandler(DOMAIN, ip_address)
                dns_message_packet = dns_message_handler.build_dns_message(data)
                print repr(dns_message_packet)
                self.udp_server.sendto(dns_message_packet, client_address)
        except KeyboardInterrupt:
            self.udp_server.close()
            sys.close(0)


if __name__ == '__main__':
    # read and parse inputs
    inputs = sys.argv
    PORT, DOMAIN= parse_dns_server_input(inputs)
    RECORD = 'ec2-54-85-79-138.compute-1.amazonaws.com'
    # start dns server
    dns_server = DNSServer()                
    dns_server.build_server()
    dns_server.serve_forever()
    
