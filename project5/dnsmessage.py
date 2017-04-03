import sys
import struct

class DNSMessageHandler(object):

    def __init__(self):
        self.id = 0

class DNSHeader(object):

    def __init__(self):
        self.id = 0
        self.flags = 0
        self.qdcount = 0
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0

    def fetch(self, data):
        return

    def pack(self):
       header_packet = struct.pack('!hhhhhh', 
                                    self.id, 
                                    self.flags, 
                                    self.qdcount, 
                                    self.ancount, 
                                    self.nscount, 
                                    self.arcount)
       return header_packet

class DNSQuestion(object):

    def __init__(self, qname_):
        self.qname = qname_
        self.qtype = 0
        self.qclass = 0

    def fetch(self, data):
        return

    def pack(self):
        question_packet = struct.pack('!hhh', 
                                       self.qtype, 
                                       self.qclass)
        return question_packet

class DNSAnswer(object):

    def __init__(self):
        self.name = ''
        self.type = ''
        self.aclass = ''
        self.ttl = 0
        self.rlength = 0
        self.rdata = ''

    def fetch(self, data):
        return

    def pack(self, ip_address):
        self.type = 0x0001
        self.aclass = 0x0001
        self.ttl = 60
        self.rlength = 0
        self.data = ip_address
        answer_packet = struct.pack('!hhLh4s', 
                                     self.type, 
                                     self.aclass,
                                     self.ttl,
                                     self.rlength,
                                     self.rdata)
        return answer_packet

