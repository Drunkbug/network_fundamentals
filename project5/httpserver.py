import sys
import os
from util import *
import socket
import json
import urllib

CONST_10MB_IN_BYTES = 10485760


class UrlData:
    """
    Construct a url data object
    :type url_list: list
    :param url_list: the list of url
    :type data: str
    :param data: the data of html
    :type hit_count: number
    :param hit_count: the hit count of the data
    """
    def __init__(self, url_list, data, hit_count):
        self.urlList = url_list
        self.data = data
        self.hitCount = hit_count


class CacheManager:
    """
    Construct a CacheManager
    """
    def __init__(self):
        self.cacheFileHandler = CacheFileHandler()
        self.cacheData = self.__load_cache_file()

    """
    load the cache file
    """
    def __load_cache_file(self):
        try:
            j_string = json.loads(self.cacheFileHandler.read())
            cache_data = []
            for url_data in j_string:
                cache_data.append(UrlData(url_data['urlList'], url_data['data'], url_data['hitCount']))
            return cache_data
        # if exception happens, just return an empty list
        except:
            return []

    """
    save cache data in the file
    """
    def __save_cache_data__(self):
        self.cacheFileHandler.write(self.__to_json_string_cacheData__())

    """
    add url and data to the cache file
    :type url: string
    :param url: the url
    :type data: str
    :param data: the data of html
    """
    def add_url_data(self, url, data):
        flag = False
        # go through each urlData in the list
        for ud in self.cacheData:
            if url in ud.urlList:
                flag = True
                ud.hitCount += 1
            elif ud.data == data:
                flag = True
                ud.hitCount += 1
                ud.urlList.append(url)

        if not flag:
            ud = UrlData([url], data, 1)
            self.cacheData.append(ud)

        self.__larger_than_10mb_handler()
        self.__save_cache_data__()

    """
    handle the 10mb cache
    TODO need to remove some data
    """
    def __larger_than_10mb_handler(self):
        sorted(self.cacheData, key=lambda ud: ud.hitCount, reverse=True)
        j_string = self.__to_json_string_cacheData__()
        if sys.getsizeof(j_string) > CONST_10MB_IN_BYTES:
            # TODO remove some data to keep the file size under 10MB
            print('TODO remove some data to keep the file size under 10MB')

    """
    check whether the url is already in cache
    :type url: string
    :param url: the url
    """
    def is_url_in_cache(self, url):
        for ud in self.cacheData:
            if url in ud.urlList:
                return True, ud.data
        return False, ""

    """
    convert cacheData to json
    """
    def __to_json_string_cacheData__(self):
        return json.dumps([ob.__dict__ for ob in self.cacheData])


class CacheFileHandler:
    """
    Construct a CacheFileHandler objext
    """
    def __init__(self):
        self.fileName = 'cacheData.dat'

    """
    read the cache data from file
    """
    def read(self):
        cache_data = open(self.fileName, 'r')
        result = cache_data.read()
        cache_data.close()
        return result

    """
    write the data to the cache file
    :type data: str
    :param data: the data of html
    """
    def write(self, data):
        cache_data = open(self.fileName, 'w')
        cache_data.write(data)
        cache_data.close()


class HTTPServer(object):
    """
    Construct a HTTPServer object
    """
    def __init__(self):
        self.http_server = None
        self.cache_manager = CacheManager()

    """
    build the http server
    """
    def build_server(self):
        self.http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.http_server.bind(('', PORT))

    """
    retrive the data from the destination host
    :type url: string
    :param url: the url
    """
    def retrieve_data(self, url):
        response = urllib.urlopen(url)
        # Convert bytes to string type and string type to dict
        return response.read().decode('utf-8')

    """
    handle http request
    :type http_request: string
    :param http_request: the http_request content
    """
    def handle_request(self, http_request):
        request_path = get_http_request_path(http_request)
        url = ORIGIN + request_path
        is_in, data = self.cache_manager.is_url_in_cache(url)
        if not is_in:
            data = self.retrieve_data("http://" + url)
        self.cache_manager.add_url_data(url, data)
        return data

    """
    listen to a port
    """
    def serve_forever(self):
        self.http_server.listen(1)
        while 1:
            try:
                client_socket, client_address = self.http_server.accept()
                http_request = client_socket.recv(1024)
                data = self.handle_request(http_request)
                print(data)
                client_socket.sendall(data)
                client_socket.close()
            except KeyboardInterrupt:
                self.http_server.close()
                return

if __name__ == '__main__':

    PORT, ORIGIN = parse_http_server_input(sys.argv)

    http_server = HTTPServer()
    http_server.build_server()
    http_server.serve_forever()



