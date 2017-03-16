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


