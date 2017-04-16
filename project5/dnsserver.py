import sys
from util import *
from dnsmessage import DNSMessageHandler
from measureserver import MeasureServer
import socket

EC2_HOSTS = {"Origin": ("54.166.234.74", 
                        "ec2-54-166-234-74.compute-1.amazonaws.com"),
            "Virginia": ("52.90.80.45",
                        "ec2-52-90-80-45.compute-1.amazonaws.com"),
            "California": ("54.183.23.203",
                        "ec2-54-183-23-203.us-west-1.compute.amazonaws.com"),
            "Oregon": ("54.70.111.57",
                        "ec2-54-70-111-57.us-west-2.compute.amazonaws.com"),
            "Ireland": ("52.215.87.82", 
                        "ec2-52-215-87-82.eu-west-1.compute.amazonaws.com"),
            "Frankfurt": ("52.28.249.79", 
                      "ec2-52-28-249-79.eu-central-1.compute.amazonaws.com"),
            "Singapore": ("54.169.10.54", 
                    "ec2-54-169-10-54.ap-southeast-1.compute.amazonaws.com"),
            "Sydney": ("52.62.198.57", 
                    "ec2-52-62-198-57.ap-southeast-2.compute.amazonaws.com"),
            "Tokyo": ("52.192.64.163",
                   "ec2-52-192-64-163.ap-northeast-1.compute.amazonaws.com"),
            "SaoPaolo": ("54.233.152.60",
                    "ec2-54-233-152-60.sa-east-1.compute.amazonaws.com")
}

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
                data, address_tuple = self.udp_server.recvfrom(1024)

                measure_server = MeasureServer(PORT)
                print (measure_server)
                ip_address = measure_server.best_replica(address_tuple[0])
                # parse and bulid dns message
                dns_message_handler = DNSMessageHandler(DOMAIN, ip_address)
                dns_message_packet = dns_message_handler.build_dns_message(data)
                #print repr(dns_message_packet)
                self.udp_server.sendto(dns_message_packet, address_tuple)
        except KeyboardInterrupt:
            self.udp_server.close()
            sys.close(0)


if __name__ == '__main__':
    # read and parse inputs
    inputs = sys.argv
    PORT, DOMAIN= parse_dns_server_input(inputs)
    # start dns server
    dns_server = DNSServer()
    dns_server.build_server()
    dns_server.serve_forever()
