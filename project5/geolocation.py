import socket
import urllib
import json
from math import sin, cos, sqrt, atan2, radians
# get the geo location from client ip
class GeoLocator(object):

    # initialize geo locator
    def __init__(self, ec2_hosts_):
        self.ec2_hosts = ec2_hosts_ 
        self.ec2_host_locations = {}
        self.distances_to_client = []

    # get location from ip-api
    def get_location_tuple(self, ip_address):
        try:
            response = urllib.urlopen('http://ip-api.com/json/' + ip_address)
            json_response = json.load(response)
        except:
            print ("Connection refused on host:" + str(ip_address))
            pass

        if json_response['status'] == 'success':
            return (json_response['lon'], json_response['lat'])
        else:
            return None

    # get geo location of EC2 hosts
    def get_ec2_locations(self):
        for ec2_host in self.ec2_hosts:
            self.ec2_host_locations[ec2_host] = self.get_location_tuple(ec2_host)

    # get distance from ec2 to client
    def get_distances_to_client(self, client_address):
        client_location_tuple = self.get_location_tuple(client_address)
        for host in self.ec2_host_locations.keys():
            host_location_tuple = self.ec2_host_locations[host]
            if self.ec2_host_locations[host]:
                distance = self.calculate_distance(client_location_tuple, host_location_tuple)
                self.distances_to_client.append((host, distance))
            else:
                self.distances_to_client.append((host, None))

    # calculate distance between ec2 host and client
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

        return distance

    # get the top three closest ec2 host locations
    def get_top_three_locations(self):
        max_dist = None
        sorted_distances = sorted(self.distances_to_client, key=lambda tup:tup[1])
        top_three_locations = sorted_distances[0:3]
        print (top_three_locations)
        return top_three_locations

    # reset distance to client
    def reset(self):
        self.distances_to_client = []

