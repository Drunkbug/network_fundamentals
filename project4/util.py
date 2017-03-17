#!/bin/python3
# imports
import socket
import array
from random import randint
from urllib.parse import urlparse
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
    if not path:
        filename = 'index.html'
    else:
        filename = path.split('/')[-1]
    return host, dest_ip, filename

def checksum(msg):
    s = 0
    s = sum(array.array("H", msg))
    s = (s >> 16) + (s& 0xffff)
    s += (s >> 16)

    #complement and mask to 4 byte short
    s = ~s & 0xffff

    return s

def get_valid_port():
    port = randint(1024, 65535)
    return port

