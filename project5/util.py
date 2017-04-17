import sys
import argparse
import json

def parse_http_server_input(inputs):
    parser = argparse.ArgumentParser(description='Http Server Inputs')
    parser.add_argument('-p', type=int, metavar='<port>', help='Port Number from 40000-65535' , required=True)
    parser.add_argument('-o', type=str, metavar='<origin>', help='Name of the origin server for your CND' , required=True)
    args = parser.parse_args()
    if args.p < 40000 or args.p > 65535:
        sys.exit("Invalid port number. Range: 40000-65535.")
    return args.p, args.o 

def parse_dns_server_input(inputs):
    parser = argparse.ArgumentParser(description='DNS Server Inputs')
    parser.add_argument('-p', type=int, metavar='<port>', help='Port Number from 40000-65535' , required=True)
    parser.add_argument('-n', type=str, metavar='<name>', help='CND specific name' , required=True)
    args = parser.parse_args()
    if args.p < 40000 or args.p > 65535:
        sys.exit("Invalid port number. Range: 40000-65535.")
    return args.p, args.n


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


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data
