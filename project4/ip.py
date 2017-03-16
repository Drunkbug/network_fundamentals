#!/bin/python3
import socket, sys
from random import randint
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
class IPSocket(object):
    def __init__(self, src_ = '', src_port_ = '', dest_ = ''):
        # create a raw send and receive socket
        # a send socket must be of type SOCK_RAW/IPPROTO_RAW
        try:
            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except socket.error as se:
            raise se
            sys.exit()

        # a receive socket must be of type SOCK_STREAM/IPPROTO_IP
        try:
            self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
        except socket.error as se:
            raise se
            sys.exit()

        self.dest_ip = dest_
        self.src_ip = src_
        self.src_port = src_port_

        # self.src_ip = get_source_ip()
        #self.src_port = get_valid_port()

    # send and receive data
    # based onISOOSI model, network layer is under transport layer, so we implement socket connection here
    def send(self, dest_ip_, data_):
        self.dest_ip = dest_ip_
        raw_packet = IPv4Packet()
        packet = raw_packet.pack(data_)
        self.send_socket.sendto(packet, (self.dest_ip, self.src_port))
    # receive datagram
    def receive(self):
        print ("")

class IPv4Packet(object):
    def __init__(self, src = '', dest = '', dat = ''):
        # ip header fields
        self.ip_ihl = 5
        self.ip_ver = 4
        self.ip_tos = 0
        self.ip_tot_len = 20
        self.ip_id = randint(0, 65535) 
        # assume MTU are same for the CCIS network
        self.ip_frag_off = 0 

        self.ip_ttl = 255 # time to live
        self.ip_proto = socket.IPPROTO_TCP
        self.ip_checksum = 0 # Let checksum be 0 first then calculate later 
        self.src_ip = src#socket.inet_aton (self.src_ip)
        self.dest_ip = dest#socket.inet_aton (dest_ip)
        self.data = dat
        self.format = '!BBHHHBBH4s4s'

        self.ip_ihl_ver = (self.ip_ver << 4) + self.ip_ihl
        self.data = dat


    # packet the header
    def pack(self, data):
        ip_saddr = socket.inet_aton (self.src_ip)
        ip_daddr = socket.inet_aton (self.dest_ip)
        # the ! in the pack format string means network order
        ip_header = pack(self.format, \
                        self.ip_ihl_ver, \
                        self.ip_tos, \
                        self.ip_tot_len, \
                        self.ip_id, \
                        self.ip_frag_off, \
                        self.ip_ttl, \
                        self.ip_proto, \
                        self.ip_checksum, \
                        ip_saddr, \
                        ip_daddr)
        #calculate the checksum
        self.ip_checksum = checksum(ip_header)
        ip_header = pack(self.format, \
                        self.ip_ihl_ver, \
                        self.ip_tos, \
                        self.ip_tot_len, \
                        self.ip_id, \
                        self.ip_frag_off, \
                        self.ip_ttl, \
                        self.ip_proto, \
                        self.ip_checksum, \
                        ip_saddr, \
                        ip_daddr)
        return ip_header + data

    # unpack and validate received data
    def unpack(self, data):
        ip_fields = struct.unpack(self.format, data[:20]) 
        ip_ihl = ip_fields[0] - (self.ip_ver << 4)



