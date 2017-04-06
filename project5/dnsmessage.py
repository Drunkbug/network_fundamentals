import sys
import struct
import socket
from util import *

class DNSMessageHandler(object):
    """ Class for handling DNS message
    DNS message handler parses client request
    then return the packed dns answer back to client

    Attributes:
        dns_header_data: A byte string for storing dns header data
        dns_question_data: A byte string for storing dns query data
        dns_answer_data: A byte string for storing dns answer data
        domain: A string indicating the dns server domain
        ip_address: A string indicating client's ip address
    """

    def __init__(self, domain_, ip_address_):
        """ Init DNS message handler with domain and client's ip address"""
        self.dns_header_data = ''
        self.dns_question_data = ''
        self.dns_answer_data = ''
        self.domain = domain_
        self.ip_address = ip_address_

    def build_header_data(self, header_data):
        """ Construct server dns header data 

        Args:
            header_data: A byte string from client's request header data
        """
        dns_header = DNSHeader()
        header_data = dns_header.build(header_data)
        return header_data 

    def build_question_data(self, question_data):
        """ Construct server dns query data 

        Args:
            header_data: A byte string from client's request query data
        """
        dns_question = DNSQuestion()
        question_data = dns_question.build(question_data, self.domain)
        return question_data 

    def build_answer_data(self):
        """ Construct server dns answer data 
        """
        dns_answer = DNSAnswer()
        answer_data = dns_answer.build(self.domain, self.ip_address)
        return answer_data

    def build_dns_message(self, data):
        """ Build the dns message
        parsing client's dns request
        parse and reconstruct header, question and answer data
        build server dns message

        Args: 
            data: A byte string from client's dns request
        """
        self.dns_header_data = data[0:12]
        self.dns_question_data = data[12:]

        header_data = self.build_header_data(self.dns_header_data)
        question_data = self.build_question_data(self.dns_question_data)
        answer_data = self.build_answer_data()

        return header_data + question_data + answer_data
        

class DNSHeader(object):
    """ DNS Header object
    DNS header obejct for parsing and pack dns header fields
    
    Attributes:
        id: A 16 bit integer supplied by client and respond back unchanged by server
        flags: A 16 bit hex number that contains 
               QR, OPCODE, AA, TC, RD, RA, res1, res2, res3, RCODE flags 
        qdcount: Unsigned 16 bit integer specifying the number of entries
                 in question session
        ancount: Unsigned 16 bit integer specifying # of entries in answer part
        nscount: Unsigned 16 bit integer indicates the # of name server resource
        arcount: Unsigned 16 bit integer indicates # of additional section
    """

    def __init__(self):
        """ initialize DNS Header fields"""
        self.id = 0
        self.flags = 0
        self.qdcount = 0
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0

    def fetch(self, data):
        """ get client's header data and parse it
        
        Args:
            data: A string from client's header data
        """
        # ancount: number of items in answer section
        [self.id,
        self.flags,
        self.qdcount,
        self.ancount,
        self.nscount,
        self.arcount] = struct.unpack('!HHHHHH', data)

    def pack(self):
        """ pack server header data """
        self.ancount = 1 
        # flags: 1 0000 0 0 1 0 0 0 0001
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
        """ unpack client's header data and pack server header data """
        self.fetch(data)
        return self.pack()

class DNSQuestion(object):
    """DNS question object
    Handling client's question request and pack server question session

    Attributes:
        qname: A string. The name being required.
        qtype: Unsigned 16 bit integer.
        qclass: Unsigned 16 bit integer.
    """

    def __init__(self):
        """ initialize dns question object"""
        self.qname = ''
        self.qtype = 0
        self.qclass = 0

    def fetch(self, data):
        """ fetch client's question session
        fetches client's qtype and qclass data
        Since qtype and qclass are the last four bytes
        We unpack them from data[-4:]

        Args:
            data: client's question sessiont
        """
        [self.qtype,
        self.qclass] = struct.unpack('!HH', data[-4:])
        self.qname = data[:-4]
        #print repr(hex_qname)

    def pack(self, domain):
        """
        """
        #qname = encode_domain(domain)
        question_packet = struct.pack('!HH', 
                                       self.qtype, 
                                       self.qclass)
        return self.qname + question_packet

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
        self.rname = encode_domain(domain)
        self.type = 0x0001
        self.rclass = 0x0001
        self.ttl = 60
        self.rdata = socket.inet_aton(ip_address)
        self.rlength = len(self.rdata)
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

