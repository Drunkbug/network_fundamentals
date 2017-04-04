import sys
import os
from util import *
import socket

PORT, ORIGIN = parse_http_server_input(sys.argv)

# self.send_response(200)
# self.send_header("Content-type", "text/html")
# self.path: request path
# wfile writing a response back to the client
# use self.path to check if local cache
# if yes wfile cache
# else get from origin server
# os.path.isdir
# cache_path = os.pardir + self.path
# if(os.path.exists(cache_path)):
#    self.response(cache_path)
# else:
#    cache_path = cacheFile(self.path)  
#    self.response(cache_path)

class HTTPServer(object):

    def __init__(self):
        self.http_server = None 

    def build_server(self):
        self.http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.http_server.bind(('', PORT))

    def serve_forever(self):
        self.http_server.listen(1)
        while 1:
            try:
                client_socket, client_address = self.http_server.accept()
                http_request = client_socket.recv(1024)

                request_path = get_http_request_path(http_request)
                print (request_path)

            except KeyboardInterrupt:
                self.http_server.close()
                sys.close(0)
        return
        

http_server = HTTPServer()
http_server.build_server()
http_server.serve_forever()
