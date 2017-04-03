import sys
import struct

class DNSMessageHandler(object):

    def __init__(self):
        self.dns_header_data = ''
        self.dns_question_data = ''
        self.dns_answer_data = ''

    def fetch(self, data):
        self.dns_header_data = data[0:12]
        self.dns_question_data = data[12:]

    def build_header_data(self, header_data):
        dns_header = DNSHeader()
        dns_header.build(header_data)
        return dns_header 

    def build_question_data(self, question_data):
        dns_question = DNSQuestion()
        dns_question.build()
        return dns_question 

    def build_answer_data(self, answer_data):
        dns_answer = DNSAnswer()
        dns_answer.pack()
        return dns_answer 

class DNSHeader(object):

    def __init__(self):
        self.id = 0
        self.flags = 0
        self.qdcount = 0
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0

    def fetch(self, data):
        self.id,
        self.flags,
        self.qdcount,
        # number of items in answer section
        self.ancount,
        self.nscount,
        self.arcount = struct.unpack('!hhhhhh', data)

    def pack(self):
        self.ancount = 1 
        header_packet = struct.pack('!hhhhhh', 
                                    self.id, 
                                    self.flags, 
                                    self.qdcount, 
                                    self.ancount, 
                                    self.nscount, 
                                    self.arcount)
       return header_packet

    def build(self, data):
        self.fetch(data)
        self.pack()

class DNSQuestion(object):

    def __init__(self, qname_):
        self.qname = qname_
        self.qtype = 0
        self.qclass = 0

    def fetch(self, data):
        print (len(data))
        print (data)
        self.qtype,
        self.qclass,
        ending = struct.unpack('!hh', data)

    def pack(self):
        question_packet = struct.pack('!hhh', 
                                       self.qtype, 
                                       self.qclass)
        return question_packet

    def build(self, data):
        self.fetch(data)
        self.pack()


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

