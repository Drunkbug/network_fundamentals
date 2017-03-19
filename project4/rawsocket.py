#!/bin/python
# imports
import socket, sys 
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
from ip import IPSocket, IPv4Packet
from tcp import TCPSocket, TCPPack

class RawSocket(object):
    def __init__(self, raw_url_ = ''):
        self.raw_url = raw_url_
        self.host = ''
        self.dest_ip = ''
        self.filename = ''

    def http_get(self):
        request = "GET {self.path} HTTP/1.0\r\n" \
                "Host: {self.host}\r\n" \
                "Accept: text/html,application/xhtml+xml, */*\r\n" \
                "Connection: keep-alive\r\n\r\n"
        return request
    

    # main function
    def main(self):
        # parse url
        self.host, \
        self.dest_ip, \
        self.filename, \
        self.path = parse_raw_url(self.raw_url)
        print (self.dest_ip)
        # establish TCP socket
        sock = TCPSocket(self.raw_url)
        # establish connection 
        sock.hand_shake()
        # send get request
        # sock.send_request(self.http_get())

        #self.receive()

    def receive(self):
        print ("")




