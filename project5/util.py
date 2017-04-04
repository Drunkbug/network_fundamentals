import sys

def parse_http_server_input(inputs):
    port = 0
    origin = ''
    if len(inputs) == 5:
        if inputs[1] == '-p':
            port = int(inputs[2])
        elif inputs[3] == '-p':
            port = int(inputs[4])
        else:
            http_input_usage()
        if inputs[1] == '-o':
            origin = inputs[2]
        elif inputs[3] == '-o':
            origin = inputs[4]
        else:
            http_input_usage()
    else:
        http_input_usage()
    if port < 40000 or port > 65535:
        sys.exit("Invalid port number. Range: 40000-65535.")
    return port, origin 

def http_input_usage():
    sys.exit("Usage: -p <port> -o <origin>")

def parse_dns_server_input(inputs):
    port = 0
    origin = ''
    if len(inputs) == 5:
        if inputs[1] == '-p':
            port = int(inputs[2])
        elif inputs[3] == '-p':
            port = int(inputs[4])
        else:
            dns_input_usage()
        if inputs[1] == '-n':
            origin = inputs[2]
        elif inputs[3] == '-n':
            origin = inputs[4]
        else:
            dns_input_usage()
    else:
        dns_input_usage()
    if port < 40000 or port > 65535:
        sys.exit("Invalid port number. Range: 40000-65535.")
    return port, origin 

def dns_input_usage():
    sys.exit("Usage: -p <port> -n <name>")
 
def encode_domain(domain):
    labels = domain.split('.')
    tmp = ''
    for label in labels:
        tmp += chr(len(label))
        tmp += label
    tmp += '\x00'
    return tmp

def integer_to_hex(i):
    return hex(i)

def get_http_request_path(request):
    request = request.rstrip('\r\n\r\n')
    fields = request.split('\r\n')
    get_request = fields[0]
    get_requests = get_request.split(' ')
    if (get_requests[0] == 'GET'):
        path = get_requests[1]
        return path
    return
