import sys
import struct
from util import *

class DNSMessageHandler(object):

    def __init__(self, domain_, client_address_):
        self.dns_header_data = ''
        self.dns_question_data = ''
        self.dns_answer_data = ''
        self.domain = domain_
        self.client_address = client_address_

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
        answer_data = dns_answer.build(self.domain, self.client_address)
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
        self.arcount] = struct.unpack('!Hhhhhh', data)
        print ("dns header id:")
        print (self.id)

    def pack(self):
        self.ancount = 1 
        print ("dns pack flags")
        print (self.flags)

        header_packet = struct.pack('!Hhhhhh', 
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

    def fetch(self, data, domain):
        [self.qtype,
        self.qclass,
        ending] = struct.unpack('!hhs', data)
        self.qname = domain

    def pack(self):
        qname = encode_domain(self.qname)
        question_packet = struct.pack('!hh', 
                                       self.qtype, 
                                       self.qclass)
        return qname + question_packet

    def build(self, data, domain):
        self.fetch(data, domain)
        return self.pack()


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

    def pack(self, domain, ip_address):
        rname = encode_domain(domain)
        self.type = 0x0001
        self.rclass = 0x0001
        self.ttl = 60
        self.rlength = 4
        self.data = ip_address
        answer_packet = struct.pack('!hhLh4s', 
                                     self.type, 
                                     self.rclass,
                                     self.ttl,
                                     self.rlength,
                                     self.rdata)
        return rname + answer_packet

    def build(self, data, domain):
        return self.pack(data, domain)

