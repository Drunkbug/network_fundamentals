import sys
from util import *
from dnsmessage import DNSMessageHandler
from measureserver import MeasureServer
from geolocation import GeoLocator
import socket
import time
from IPy import IP

"""
ec2-54-166-234-74.compute-1.amazonaws.com"
"""
EC2_HOSTS = ["ec2-52-90-80-45.compute-1.amazonaws.com",
             "ec2-54-183-23-203.us-west-1.compute.amazonaws.com",
             "ec2-54-70-111-57.us-west-2.compute.amazonaws.com",
             "ec2-52-215-87-82.eu-west-1.compute.amazonaws.com",
             "ec2-52-28-249-79.eu-central-1.compute.amazonaws.com",
             "ec2-54-169-10-54.ap-southeast-1.compute.amazonaws.com",
             "ec2-52-62-198-57.ap-southeast-2.compute.amazonaws.com",
             "ec2-52-192-64-163.ap-northeast-1.compute.amazonaws.com",
             "ec2-54-233-152-60.sa-east-1.compute.amazonaws.com"]

EC2_IPS = {"ec2-52-90-80-45.compute-1.amazonaws.com": "52.90.80.45",
             "ec2-54-183-23-203.us-west-1.compute.amazonaws.com": "54.183.23.203",
             "ec2-54-70-111-57.us-west-2.compute.amazonaws.com": "54.70.111.57",
             "ec2-52-215-87-82.eu-west-1.compute.amazonaws.com": "52.215.87.82",
             "ec2-52-28-249-79.eu-central-1.compute.amazonaws.com": "52.28.249.79",
             "ec2-54-169-10-54.ap-southeast-1.compute.amazonaws.com": "54.169.10.54",
             "ec2-52-62-198-57.ap-southeast-2.compute.amazonaws.com": "52.62.198.57",
             "ec2-52-192-64-163.ap-northeast-1.compute.amazonaws.com": "52.192.64.163",
             "ec2-54-233-152-60.sa-east-1.compute.amazonaws.com": "54.233.152.60"}

class DNSServer(object):

    """ DNS server object
    establish and run the server with socket

    Attributes:
        udp_server: a socket object for establishing dns server
    """
    def __init__(self):
        self.udp_server = None
        self.locator = None
        self.client_replica_cache = {}

    def build_server(self):
        """ init dns server class with socket"""
        self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server.bind(('', PORT))

    def get_locations(self):
        self.locator = GeoLocator(EC2_HOSTS)
        self.locator.get_ec2_locations()

    def serve_forever(self):
        """ parsing client information and request
            send dns message back to client
        """
        try:
            while 1:
                data, address_tuple = self.udp_server.recvfrom(1024)
                ip = IP(address_tuple[0])
                ip_type = ip.iptype()

                if (address_tuple[0] in self.client_replica_cache.keys() and 
                    time.time() - self.client_replica_cache[address_tuple[0]][1] <= 60):
                    ip_address = self.client_replica_cache[address_tuple[0]][0]
                    ttl = 60 - (int(time.time()) - int(self.client_replica_cache[address_tuple[0]][1]))
                    self.send(socket.inet_aton(ip_address), data, address_tuple, ttl)
                    continue
                top_three_hosts = EC2_HOSTS
                if ip_type != 'PRIVATE':
                    # get top three closest locations
                    self.locator.reset()
                    self.locator.get_distances_to_client(address_tuple[0])
                    top_three_locations_tuple = self.locator.get_top_three_locations()
                    top_three_hosts = [tup[0] for tup in top_three_locations_tuple]
                # get latency
                measure_server = MeasureServer(PORT, top_three_hosts)
                host_name = measure_server.best_replica(address_tuple[0])
                ip_address = EC2_IPS[host_name]
                self.send(ip_address, data, address_tuple, 60)
                self.client_replica_cache[address_tuple[0]] = (ip_address, time.time())

        except KeyboardInterrupt:
            self.udp_server.close()
            sys.close(0)

    def send(self, ip_address, data, address_tuple, ttl):
        # message handler
        dns_message_handler = DNSMessageHandler(DOMAIN, ip_address, ttl)
        # parse and bulid dns message
        dns_message_packet = dns_message_handler.build_dns_message(data)
        #print repr(dns_message_packet)
        self.udp_server.sendto(dns_message_packet, address_tuple)
        

if __name__ == '__main__':
    # read and parse inputs
    inputs = sys.argv
    PORT, DOMAIN= parse_dns_server_input(inputs)
    # start dns server
    dns_server = DNSServer()
    dns_server.build_server()
    dns_server.get_locations()
    dns_server.serve_forever()
