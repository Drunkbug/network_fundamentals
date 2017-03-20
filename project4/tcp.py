#!/bin/python3
#imports
import socket, sys
from random import randint
from util import get_source_ip, parse_raw_url, checksum, get_valid_port
from ip import IPSocket
from struct import *
import time
# TCPSocket class
class TCPSocket:
    def __init__(self, raw_url_ = ''):
        # socket with ip
        self.ip_socket = IPSocket()
        # src and dst ip/port
        self.src_ip = get_source_ip()
        self.src_port = randint(1024, 65535)
        self.host, self.des_ip, self.filename, self.path = parse_raw_url(raw_url_)
        self.des_port = 80

        # seq number and ack number for handle out of order packets
        self.seq_num = 0
        self.ack = 0
        self.seq_acc = 0
        self.ack_acc = 0
        #self.syn = 0
        # TCP congestion control
        self.cwnd = 1
        self.max_cwnd = 1000
        # set timeout in 60 seconds, if rto set cwnd to 1
        # TODO maybe longer timeout?
        self.rto = 60

        self.get_data= ''
        
    def send_request(self, data):
        # initialize
        print (data)
        tcp_pack = self.initialize_tcp_pack()
        tcp_pack.tcp_ack = 1
        tcp_pack.tcp_psh = 1
        tcp_pack.data = data
        # wrap ip header and send request
        self.send(tcp_pack)
        self.recv_data()

        
    def send(self, tcp_pack):
        self.ip_socket.send(self.src_ip, self.des_ip, self.src_port, tcp_pack.pack(tcp_pack.data)) 

    # receive function for three way handshake
    def recv(self):
        tcp_pack = self.initialize_tcp_pack()
        start_time = time.time()
        recv_pkt = None
        while 1:
            if time.time() - start_time >= self.rto:
                print ("Time out, change cwnd to 1")
                self.cwnd = 1
                return 
            recv_pkt = self.ip_socket.receive()
            if (recv_pkt):
                tcp_pack.unpack(recv_pkt)
                tcp_pack.src_ip = self.des_ip
                tcp_pack.dst_ip = self.src_ip
                return tcp_pack

    # receive data from sender 
    def recv_data(self):
        # receive packet
        tcp_pack = self.recv()

        #if tcp_pack:
        #    print ("Timeout")
        print (str(self.seq_num) + "==" + str(tcp_pack.tcp_ack_seq))
        print (tcp_pack.data)
        print (tcp_pack.data.encode())
        if tcp_pack.tcp_ack_seq == self.seq_num + len(tcp_pack.data):
            self.ack = tcp_pack.tcp_seq + len(tcp_pack.data)
            self.seq_num = tcp_pack.tcp_ack_seq
            self.get_data = tcp_pack.data
        else :
            print ("Incorrect SYN/ACK sequence")
        tcp_pack = self.initialize_tcp_pack()
        tcp_pack.tcp_ack = 1
        self.send(tcp_pack)
        return self.get_data 


    def fin(self):
        print ("")

    # establish connection
    def hand_shake(self):
        self.src_ip = get_source_ip()
        self.src_port = randint(1024, 65535)
        self.seq_num = randint(0, 65535)
        # initialize
        tcp_pack = self.initialize_tcp_pack()

        # set syn flag in tcp
        tcp_pack.tcp_syn = 1
        # send first syn
        self.send(tcp_pack)
        #self.ip_socket.send(self.src_ip, self.des_ip, self.src_port, tcp_pack.pack()) 
        # receive
        recv_pkt = None
        cur_time = time.time()
        tcp_pack = self.initialize_tcp_pack()
        while 1:
            if time.time() - cur_time >= self.rto:
                print ("Handshake timeout")
                sys.exit(0)
            recv_pkt = self.ip_socket.receive()
            if (recv_pkt):
                tcp_pack.unpack(recv_pkt)
                tcp_pack.src_ip = self.des_ip
                tcp_pack.dst_ip = self.src_ip
                valid_flag = (tcp_pack.tcp_ack == 1 and \
                            tcp_pack.tcp_syn == 1)
                valid_seq = (tcp_pack.tcp_ack_seq == (self.seq_num + 1))
                valid_port = (tcp_pack.src_port == self.des_port and \
                            tcp_pack.src_ip == self.des_ip and \
                            tcp_pack.dst_port == self.src_port and \
                            tcp_pack.dst_ip == self.src_ip)
                if valid_flag and valid_seq and valid_port: 
                    self.seq_num = tcp_pack.tcp_ack_seq
                    self.ack = tcp_pack.tcp_seq + 1
                    break
                else:
                    print ("Wrong Pakcet")
            else:
                print("Handshake time out")
                sys.exit(0)
        # send ack
        tcp_pack = self.initialize_tcp_pack()
        tcp_pack.tcp_ack = 1
        # send packet
        self.ip_socket.send(self.src_ip, self.des_ip, self.src_port, tcp_pack.pack()) 

        

    def initialize_tcp_pack(self):
        tcp_pack = TCPPack()
        tcp_pack.src_ip = self.src_ip
        tcp_pack.src_port = self.src_port
        tcp_pack.dst_ip = self.des_ip
        tcp_pack.tcp_seq = self.seq_num
        tcp_pack.tcp_ack_seq = self.ack
        return tcp_pack




# TCPPack class: handle tcp package pack/unpack
class TCPPack(object):

    def __init__(self):
        # set up src and dst ip and port
        self.src_port = 0
        self.src_ip = ''
        self.dst_port = 80
        self.dst_ip = ''
        
        self.tcp_seq = 0
        self.tcp_ack_seq = 0
        self.tcp_doff = 5
        #tcp flags
        self.tcp_fin = 0
        self.tcp_syn = 0
        self.tcp_rst = 0
        self.tcp_psh = 0
        self.tcp_ack = 0
        self.tcp_urg = 0
        self.tcp_window = socket.htons (5840) # for flow control
        self.tcp_checksum = 0
        self.tcp_urg_ptr = 0

        self.tcp_offset_res = (self.tcp_doff << 4) + 0

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

        tcp_header = pack(self.format+'HH', \
                        self.src_port, \
                        self.dst_port, \
                        self.tcp_seq, \
                        self.tcp_ack_seq, \
                        self.tcp_offset_res, \
                        self.tcp_flags, \
                        self.tcp_window, \
                        self.tcp_checksum, \
                        self.tcp_urg_ptr)
        # pseudo header fields
        source_addr = socket.inet_aton( self.src_ip )
        dest_addr = socket.inet_aton( self.dst_ip )
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + len(usrdata)

        psh = pack(self.psh_format, \
                    source_addr, \
                    dest_addr, \
                    placeholder, \
                    protocol, \
                    tcp_length)
        psh = psh + tcp_header + usrdata.encode()
        

        self.tcp_checksum = checksum(psh)

        # tcp header with checksum
        tcp_header = pack(self.format, \
                        self.src_port, \
                        self.dst_port, \
                        self.tcp_seq, \
                        self.tcp_ack_seq, \
                        self.tcp_offset_res, \
                        self.tcp_flags, \
                        self.tcp_window) + \
                     pack('H', self.tcp_checksum) + \
                     pack('!H', self.tcp_urg_ptr)
        self.data = usrdata

        return tcp_header + usrdata.encode()

    def unpack(self, data):
        tcph = unpack(self.format+'HH', data[0:20])
        self.src_port = tcph[0]
        self.dst_port = tcph[1]
        self.tcp_seq = tcph[2]
        self.tcp_ack_seq = tcph[3]
        tcp_offset_res_ = tcph[4]
        self.tcp_flags = tcph [5]
        self.tcp_window = tcph[6]
        self.tcp_checksum = tcph[7]
        self.tcp_urg_ptr = tcph[8]

        self.tcp_offset_res = tcp_offset_res_ >> 4
        self.data = data[self.tcp_offset_res:]

        # fetch flags
        self.tcp_fin = (self.tcp_flags & 1) 
        self.tcp_syn = (self.tcp_flags & 2) >> 1 
        self.tcp_rst = (self.tcp_flags & 4) >> 2
        self.tcp_psh = (self.tcp_flags & 8) >> 3 
        self.tcp_ack = (self.tcp_flags & 16) >> 4
        self.tcp_urg = (self.tcp_flags & 32) >> 5 

        # TODO checksum
        data_check = data[0:16] + pack('H', 0) + data[18:]
        check_valid = checksum(data_check)
        #if check_valid != self.tcp_checksum:
        #    print ("broken TCP packet")
        
        
