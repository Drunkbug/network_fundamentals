import sys
from util import *
from dnsmessage import DNSMessageHandler
import socket

# read and parse inputs
inputs = sys.argv
PORT, DOMAIN= parse_dns_server_input(inputs)
RECORD = 'ec2-54-85-79-138.compute-1.amazonaws.com'

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('', PORT))

try:
    while 1:
        data, client_address = udp_server.recvfrom(1024)
        print ("data:")
        print (data)
        print (client_address)
        ip_address = '54.85.79.138'
        dns_message_handler = DNSMessageHandler(DOMAIN, ip_address)
        dns_message_packet = dns_message_handler.build_dns_message(data)
        print repr(dns_message_packet)
        udp_server.sendto(dns_message_packet, client_address)
except KeyboardInterrupt:
    udp_server.close()

