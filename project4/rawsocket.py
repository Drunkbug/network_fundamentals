#!/bin/python3
# imports
import socket, sys 
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
from ip import IPSocket, IPv4Packet
from tcp import TCPSocket, TCPPack


# main function
def main(raw_url):
    host, dest_ip, filename = parse_raw_url(raw_url) 
    test = IPv4Packet()
    ip = IPSocket()
    tcp = TCPPack()
    tcpS = TCPSocket(ip)

# end of main function

if len(sys.argv) != 2:
    sys.exit('Please type valid arguments: ./rawhttpget url')
    
raw_url = sys.argv[1]
main(raw_url)

