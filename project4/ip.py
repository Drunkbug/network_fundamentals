#!/bin/python3
import socket, sys
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
class IPv4PacketManager(object):
    def __init__(self, src = '', dest = '', dat = ''):
        # ip header fields
        self.ip_ihl = 5
        self.ip_ver = 4
        self.ip_tos = 0
        self.ip_tot_len = 20
        self.ip_id = randint(0, 65535) 
        # for ip fragmentation
        self.ip_frag_off = 0 

        self.ip_ttl = 255 # time to live
        self.ip_proto = socket.IPROTO_TCP
        self.ip_checksum = 0 # Let checksum be 0 first then calculate later 
        self.src_ip = src#socket.inet_aton (self.src_ip)
        self.dest_ip = dest#socket.inet_aton (dest_ip)
        self.data = dat
        self.format = '!BBHHHBBH4s4s'

        self.ip_ihl_ver = (ip_ver << 4) + ip_ihl
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
        return ip_header + self.data

    # unpack and validate received data
    def unpack(self, data):
        ip_fields = struct.unpack(self.format, data[:20]) 
        ip_ihl = ip_fields[0] - (self.ip_ver << 4)

    # send datagram
    def send(self):
        print ""

    # receive datagram
    def receive(self):
        print ""

