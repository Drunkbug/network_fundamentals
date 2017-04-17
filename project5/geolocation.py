import socket
import urllib
import json
from math import sin, cos, sqrt, atan2, radians

class GeoLocator(object):
    def __init__(self, ec2_hosts_):
        self.ec2_hosts = ec2_hosts_ 
        self.ec2_host_locations = {}
        self.distances_to_client = []

    def get_location_tuple(self, ip_address):
        response = urllib.urlopen('http://ip-api.com/json/' + ip_address)
        json_response = json.load(response)

        if json_response['status'] == 'success':
            return (json_response['lon'], json_response['lat'])
        else:
            return None

    def get_ec2_locations(self):
        for ec2_host in self.ec2_hosts:
            self.ec2_host_locations[ec2_host] = self.get_location_tuple(ec2_host)

    def get_distances_to_client(self, client_address):
        client_location_tuple = self.get_location_tuple(client_address)
        for host in self.ec2_host_locations.keys():
            host_location_tuple = self.ec2_host_locations[host]
            if self.ec2_host_locations[host]:
                distance = self.calculate_distance(client_location_tuple, host_location_tuple)
                self.distances_to_client.append((host, distance))
            else:
                self.distances_to_client.append((host, None))

        print (self.distances_to_client)

    def calculate_distance(self, location_tuple1, location_tuple2):
        R = 6373

        lon1 = radians(location_tuple1[0])
        lat1 = radians(location_tuple1[1])
        lon2 = radians(location_tuple2[0])
        lat2 = radians(location_tuple2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        print("Result:", distance)
        return distance

    def get_top_three_locations(self, hosts):
        for host in hosts:
            location_tuple = get_location_tuple(host)
            print(location_tuple)


if __name__=='__main__':
    locator = GeoLocator(['54.166.234.74']) 
    locator.get_ec2_locations()
    locator.get_distances_to_client("54.169.10.54")
    
     
