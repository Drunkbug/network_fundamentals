import sys
import os
from util import *
#from http.server import HTTPServer, BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import socket

PORT, ORIGIN = parse_http_server_input(sys.argv)

class MyHttpHandler(BaseHTTPRequestHandler):

    def __init__(self, port_, origin_):
        self.port = port_
        self.origin = origin_
        
    def httpGET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # self.path: request path
        # wfile writing a response back to the client
        # use self.path to check if local cache
        # if yes wfile cache
        # else get from origin server

        # os.path.isdir
        cache_path = os.pardir + self.path
        if(os.path.exists(cache_path)):
            self.response(cache_path)
        else:
            cache_path = cacheFile(self.path)  
            self.response(cache_path)

    def response(self, path):
        f = open(cache_path, 'r')
        self.wfile.write(f.read())
        f.close()
            
    def cacheFile(self, path):
        print("todo")  
        return

def run(port, origin, server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_handler = MyHttpHandler(port, origin)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    https.serve_forever()

class HTTPServer(object):

    def __init__(self):
        self.http_server = None 

    def build_server(self):
        self.http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.http_server.bind(('', PORT))

    def serve_forever(self):
        while 1:
            try:
                client_socket, client_address = self.http_server.accept()
                http_request = self.http_server.recv(1024)
                print (http_request)
            except KeyboardInterrupt:
                self.http_server.close()
                sys.close(0)
                
        return
        

