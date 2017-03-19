#!/bin/python
# imports
import socket, sys 
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
from ip import IPSocket, IPv4Packet
from tcp import TCPSocket, TCPPack


# main function
def main(raw_url):
    host, dest_ip, filename = parse_raw_url(raw_url) 
    print (dest_ip)
    tcpS = TCPSocket(raw_url)
    tcpS.hand_shake()




