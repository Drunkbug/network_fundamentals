#!/bin/python3
# imports
import socket
import array
from random import randint
#from urllib.parse import urlparse
from urlparse import urlparse
def get_source_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        source_ip = s.getsockname()[0]
        s.close()
    except (socket.error, msg):
        print ('Error occurs. Err: ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    finally:
        s.close()
    return source_ip

def parse_raw_url(raw_url):
    url = urlparse(raw_url) 
    host = url.netloc
    dest_ip = socket.gethostbyname(host)
    path = url.path
    filename = path.split('/')[-1]
    if not filename:
        filename = 'index.html'
        path += filename
    return host, dest_ip, filename, path

def checksum(msg):
    if len(msg) % 2 == 1:
        msg += '\0'#.encode()
    s = 0
    s = sum(array.array("H", msg))
    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)

    #complement and mask to 4 byte short
    s = (~s) & 0xffff

    return s

def get_valid_port():
    port = randint(1024, 65535)
    return port

#def convert_bytes_to_str(data, l):
#    return get_hex_string_from_int(int.from_bytes(data, byteorder='big'), l)

#def get_hex_string_from_int(i, length):
#        return ""
#    result = hex(i)[2:]
#    result = "0" * (length - len(result)) + result
#    return result
