import socket

# server for contacting http host and get latency from http host to client
class MeasureServer:

    def __init__(self, port_, hosts_=[]):
        self.port = port_
        self.socket= None
        self.hosts = hosts_
        self.hosts_latency = [] # list of tuples

    # send get to http host
    def send_request(self, client_ip):
        for host in self.hosts:
            self.socket = socket.socket()
            try:
                self.socket.connect((host, self.port))
            except:
                self.hosts_latency.append((host, 99999))
                continue
            self.socket.send("GET /leyiqiangshichenxiyuandeerzi" + str(client_ip) + " HTTP/1.1\r\n\r\n")
            self.get_rtt(host)
            self.socket.close()

    # receive rtt info from http server
    def get_rtt(self, host):
        while 1:
            rtt = self.socket.recv(1024)
            self.hosts_latency.append((host, float(rtt)))
            return

    # get the ec2 host with minimum latency
    def get_min_host(self):
        min_host = None
        # (hostname, latency)
        for host_tuple in self.hosts_latency:
            if not min_host or float(host_tuple[1]) < min_host[1]:
                min_host = host_tuple 
        return min_host[0]

    # get the best replica
    def best_replica(self, client_ip):
        self.send_request(client_ip)
        return self.get_min_host()

