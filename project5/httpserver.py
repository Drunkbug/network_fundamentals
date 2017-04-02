import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class HttpServerHandler(BaseHTTPRequestHandler):
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


def argparse(inputs):
    port = 0
    origin = ''
    if len(inputs) == 5:
        if inputs[1] == '-p':
            port = int(inputs[2])
        elif inputs[3] == '-p':
            port = int(inputs[4])
        else:
            sys.exit("Usage: -p <port> -o <origin>")
        if inputs[1] == '-o':
            origin = inputs[2]
        elif inputs[3] == '-o':
            origin = inputs[4]
        else:
            sys.exit("Usage: -p <port> -o <origin>")
    else:
        sys.exit("Usage: -p <port> -o <origin>")
    if port < 40000 or port > 65535:
        sys.exit("Invalid port number. Range: 40000-65535.")
    return port, origin 
        
def run(port, origin, server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_handler = HttpServerHandler(port, origin)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    https.serve_forever()

port, origin = argparse(sys.argv)
run(port, origin)

