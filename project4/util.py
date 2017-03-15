#!/bin/python
# imports
import socket
from urlparse import urlparse
def get_source_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        source_ip = s.getsockname()[0]
        s.close()
    except socket.error, msg:
        print 'Error occurs. Err: ' + str(msg[0]) + ' Message ' + msg[1]
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
