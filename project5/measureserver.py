import socket


class MeasureServer:

    def __init__(self, port_):
        self.port = port_
        self.socket= None
        self.hosts = {"54.166.234.74": 99999,
                "52.90.80.45": 99999,
                "54.183.23.203": 99999,
                "54.70.111.57": 99999,
                "52.215.87.92": 99999,
                "52.28.249.79": 99999,
                "54.169.10.54": 99999,
                "52.62.198.57": 99999,
                "52.192.64.163": 99999,
                "54.233.152.50": 99999}

    def send_request(self, client_ip):
        for host in ["52.90.80.45"]:
            self.socket = socket.socket()
            self.socket.connect((host, self.port))
            self.socket.send("GET /leyiqiangshichenxiyuandeerzi" + str(client_ip) + " HTTP/1.1\r\n\r\n")
            self.get_rtt(host)
            self.socket.close()

    def get_rtt(self, host):
        while 1:
            rtt = self.socket.recv(1024)
            self.hosts[host] = float(rtt)
            return

    def get_min_host(self):
        min_host = None
        for host in self.hosts.keys():
            if not min_host or self.hosts[host] < self.hosts[min_host]:
                min_host = host
        return min_host


    def best_replica(self, client_ip):
        self.send_request(client_ip)
        return self.get_min_host()

