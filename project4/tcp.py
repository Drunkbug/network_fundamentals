#!/bin/python3
#imports
import socket, sys
from random import randint
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
from ip import IPSocket
# TCPSocket class
class TCPSocket:
    def __init__(self, ip_socket_):
        # socket with ip
        self.ip_socket = ip_socket_ 
        # src and dst ip/port
        self.src_ip = get_source_ip()
        self.src_port = randint(1024, 65535)
        self.des_ip = ''
        self.des_port = 80

        self.seq_num = 0
        self.ack = 0
        self.syn = 0
        # TCP congestion control
        cwnd = 1
        max_cwnd = 1000
        # set timeout in 60 seconds, if rto set cwnd to 1
        # TODO maybe longer timeout?
        rto = 60
    #def syn(self):
    #    print ("")

    #def ack(self):
    #    print ("")

    #def fin(self):
    #    print ("")

    def send(self):
        print ("")

    def recv(self):
        print ("")

    def _recv(self):
        print ("")

    def close(self):
        print ("")

    # establish connection
    def hand_shake(self):
        print ("")

    def reset(self):
        print ("")



# TCPPack class: handle tcp package pack/unpack
class TCPPack(object):

    def __init__(self, src_ = '', src_port_ = '', dst_ = ''):
        # set up src and dst ip and port
        self.src_port = src_port_
        self.src_id = src_
        self.dst_port = 80
        self.dst_id = dst_
        
        tcp_seq = 0
        tcp_ack_seq = 0
        tcp_doff = 5
        #tcp flags
        tcp_fin = 0
        tcp_syn = 0
        tcp_rst = 0
        tcp_psh = 0
        tcp_ack = 0
        tcp_urg = 0
        tcp_window = socket.htons (5840) # for flow control
        tcp_checksum = 0
        tcp_urg_ptr = 0

        tcp_offset_res = (tcp_doff << 4) + 0

        self.format = '!HHLLBBH'
        self.psh_format = '!4s4sBBH'

        self.data = ''
        self.tcp_flags = 0

    def pack(self, usrdata = ''):
        self.tcp_flags = self.tcp_fin + \
                    (self.tcp_syn << 1) + \
                    (self.tcp_rst << 2) + \
                    (self.tcp_psh <<3) + \
                    (self.tcp_ack << 4) + \
                    (self.tcp_urg << 5)
        tcp_header = pack(self.format+'BH', \
                        self.src_port, \
                        self.dst_port, \
                        self.tcp_seq, \
                        self.tcp_ack_seq, \
                        self.tcp_offset_res, \
                        tcp.flags, \
                        self.tcp_window, \
                        self.tcp_checksum, \
                        self.tcp_urg_ptr)
        # pseudo header fields
        source_addr = socket.inet_aton( self.src_id )
        dest_addr = socket.inet_aton( self.dst_id )
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + len(usrdata)

        psh = pack(self.psh_format, \
                    source_addr, \
                    dest_addr, \
                    placeholder, \
                    protocol, \
                    tcp_length)
        psh = psh + tcp_header + user_data

        tcp_checksum = checksum(psh)

        # tcp header with checksum
        tcp_header = pack(self.format, \
                        self.src_port, \
                        self.dst_port, \
                        self.tcp_seq, \
                        self.tcp_ack_seq, \
                        self.tcp_offset_res, \
                        tcp.flags, \
                        self.tcp_window) + \
                     pack('H', self.tcp_checksum) + \
                     pack('!H', self.tcp_urg_ptr)
        self.data = usrdata

        return tcp_header + usrdata

    def unpack(self, data):
        tcph = unpack(self.format+'HH', data)
        self.src_port = tcph[0]
        self.dst_port = tcph[1]
        self.tcp_seq = tcph[2]
        self.tcp_ack_seq = tcph[3]
        tcp_offset_res_ = tcph[4]
        self.tcp.flags = tcph [5]
        self.tcp_window = tcph[6]
        self.tcp_checksum = tcph[7]
        self.tcp_urg_ptr = tcph[8]

        self.tcp_offset_res = tcp_offset_res_ >> 4
        data_offset = len(data) - self.tcp_offset_res
        self.data = data[data_offset:]

        # fetch flags
        self.tcp_fin = (self.flags & 1) 
        self.tcp_syn = (self.flags & 2) >> 1 
        self.tcp_rst = (self.flags & 4) >> 2
        self.tcp_psh = (self.flags & 8) >> 3 
        self.tcp_ack = (self.flags & 16) >> 4
        self.tcp_urg = (self.flags & 32) >> 5 

        #TODO checksum
        
        
