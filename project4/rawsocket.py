#!/bin/python
# imports
import socket, sys 
from util import * 
from ip import IPSocket, IPv4Packet
from tcp import TCPSocket, TCPPack
import time
import binascii

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
        request = "GET " + self.raw_url + " HTTP/1.1\r\n" \
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
        flag = 20
        while time.time() - start_time<=20:
            data = self.sock.recv_data()
            if data:
                self.data += convert_bytes_to_str(data, len(data))
            flag -= 1
        print ("======================================")
        #print (binascii.unhexlify(self.data).decode('utf8'))
        #print (self.data)
        f = open('test.txt', 'w')
        f.write(self.data)
        f.close()




            
