#!/bin/python3
#imports
import socket, sys
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
class TCPSocket(object):
    # send and receive socket
    send_socket = None
    receive_socket = None
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
    # format
    ip_header_format = '!BBHHHBBH4s4s'

    # init function for TCPSub class
    def __init__(self):
        # create a raw send and receive socket
        # a send socket must be of type SOCK_RAW/IPPROTO_RAW
        try:
            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except (socket.error, msg):
            print ('Send socket could not be created. Error Code: ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        # a receive socket must be of type SOCK_STREAM/IPPROTO_IP
        try:
            self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
        except (socket.error, msg):
            print ('Receive socket could not be created. Error Code: ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        self.src_ip = get_source_ip()
        self.src_port = get_valid_port()
    # end init

