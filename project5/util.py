import sys

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
