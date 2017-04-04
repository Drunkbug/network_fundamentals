import sys
import struct
import socket
from util import *

class DNSMessageHandler(object):

    def __init__(self, domain_, ip_address_):
        self.dns_header_data = ''
        self.dns_question_data = ''
        self.dns_answer_data = ''
        self.domain = domain_
        self.ip_address = ip_address_

    def build_header_data(self, header_data):
        dns_header = DNSHeader()
        header_data = dns_header.build(header_data)
        return header_data 

    def build_question_data(self, question_data):
        dns_question = DNSQuestion()
        question_data = dns_question.build(question_data, self.domain)
        return question_data 

    def build_answer_data(self):
        dns_answer = DNSAnswer()
        answer_data = dns_answer.build(self.domain, self.ip_address)
        return answer_data

    def build_dns_message(self, data):
        self.dns_header_data = data[0:12]
        self.dns_question_data = data[12:]

        header_data = self.build_header_data(self.dns_header_data)
        question_data = self.build_question_data(self.dns_question_data)
        answer_data = self.build_answer_data()

        return header_data + question_data + answer_data
        

class DNSHeader(object):

    def __init__(self):
        self.id = 0
        self.flags = 0
        self.qdcount = 0
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0

    def fetch(self, data):
        # ancount: number of items in answer section
        [self.id,
        self.flags,
        self.qdcount,
        self.ancount,
        self.nscount,
        self.arcount] = struct.unpack('!HHHHHH', data)
        print ("dns header id:")
        print (self.id)

    def pack(self):
        self.ancount = 1 
        self.flags = 0x8180

        header_packet = struct.pack('!HHHHHH', 
                                     self.id, 
                                     self.flags, 
                                     self.qdcount, 
                                     self.ancount, 
                                     self.nscount, 
                                     self.arcount)
        return header_packet

    def build(self, data):
        self.fetch(data)
        return self.pack()

class DNSQuestion(object):

    def __init__(self):
        self.qname = ''
        self.qtype = 0
        self.qclass = 0

    def fetch(self, data):
        [self.qtype,
        self.qclass] = struct.unpack('!HH', data[-4:])
        hex_qname = data[:-4]
        #print repr(hex_qname)

    def pack(self, domain):
        qname = encode_domain(domain)
        question_packet = struct.pack('!HH', 
                                       self.qtype, 
                                       self.qclass)
        print ("xxxx")
        print (qname)
        return qname + question_packet

    def build(self, data, domain):
        self.fetch(data)
        return self.pack(domain)


class DNSAnswer(object):

    def __init__(self):
        self.rname = ''
        self.type = ''
        self.aclass = ''
        self.ttl = 0
        self.rlength = 0
        self.rdata = ''

    def fetch(self, data):
        return

    def pack(self, domain, ip_address):
        self.rname = 0xC00C#encode_domain(domain)
        self.type = 0x0001
        self.rclass = 0x0001
        self.ttl = 60
        self.rlength = 4
        self.data = socket.inet_aton(ip_address)
        answer_packet = struct.pack('!HHHLH4s', 
                                     self.rname,
                                     self.type, 
                                     self.rclass,
                                     self.ttl,
                                     self.rlength,
                                     self.rdata)
        return answer_packet

    def build(self, domain, ip_address):
        return self.pack(domain, ip_address)

