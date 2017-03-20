#!/bin/python
# imports
import socket, sys 
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
from ip import IPSocket, IPv4Packet
from tcp import TCPSocket, TCPPack
import time

class RawSocket(object):
    def __init__(self, raw_url_ = ''):
        self.raw_url = raw_url_
        self.host = ''
        self.dest_ip = ''
        self.filename = ''
        self.ack_timeout = 60
        self.data = ''
        self.sock = None

    def http_get(self):
        request = "GET " + self.path + " HTTP/1.1\r\n" \
                "Host: " + self.host + "\r\n" \
                "Accept: text/html\r\n" \
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
        self.sock = TCPSocket(self.raw_url)
        # establish connection 
        self.sock.hand_shake()
        # send get request
        self.sock.send_request(self.http_get())

        self.receive()

    def receive(self):
        start_time = time.time()
        #while time.time() - start_time <= self.ack_timeout:
        flag = 2
        while flag:
            self.data += self.sock.recv_data().decode()
            print (self.data)
            flag -= 1
            




