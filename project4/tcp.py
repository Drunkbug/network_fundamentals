#!/bin/python3
#imports
import socket, sys
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
class TCPSocket(object):
    seq_num = 0
    ack_num = 0
    # buffer to handle out-of-order packets and identify dup pkts
    send_buffer = ''
    recv_buffer = ''
    # TCP flow control
    # TODO set a fit number
    adv_wnd = 0
    # TCP congestion control
    cwnd = 1
    max_cwnd = 1000
     # set timeout in 60 seconds, if rto set cwnd to 1
    rto = 60
    # source and destination ip
    src_ip = ''
    # need to select a random free port from 1024 to 65535
    src_port = -1
    #dst_ip = ''
    # packet to construct
    packet = ''

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

        self.format = '!HHLLBBHHH'
        self.psh_format = '!4s4sBBH'

    def pack(self, usrdata = ''):
        tcp_flags = self.tcp_fin + (self.tcp_syn << 1) + (self.tcp_rst << 2) + (self.tcp_psh <<3) + (self.tcp_ack << 4) + (self.tcp_urg << 5)
        tcp_header = pack(self.format, \
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

        tcp_check = checksum(psh)

        # tcp header with checksum
        tcp_header = pack('!HHLLBBH', \
                        self.src_port, \
                        self.dst_port, \
                        self.tcp_seq, \
                        self.tcp_ack_seq, \
                        self.tcp_offset_res, \
                        tcp.flags, \
                        self.tcp_window) + \
                     pack('H', self.tcp_checksum) + \
                     pack('!H', self.tcp_urg_ptr)

       return tcp_header +  usrdata
