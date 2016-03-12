from SimpleXMLRPCServer import SimpleXMLRPCServer
from interop import AsyncClient
from interop import Telemetry
from time import time
import argparse

__author__ = 'Joseph Moster'


class RelayService:
    def __init__(self, url, username, password):
        self.client = AsyncClient(url=url,
                                  username=username,
                                  password=password)
        self.last_telemetry = time()

    def telemetry(self, lat, lon, alt, heading):
        t = Telemetry(latitude=lat,
                      longitude=lon,
                      altitude_msl=alt,
                      uas_heading=heading)
        self.client.post_telemetry(t)

        new_time = time()
        print 1 / (new_time - self.last_telemetry)
        self.last_telemetry = new_time

        return True

    def server_info(self):
        info = self.client.get_server_info().result()
        return str(info.message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AUVSI SUAS Server Interface Relay')
    parser.add_argument(
        '--url',
        dest='url',
        help='Interoperability Server URL, example: http://10.10.130.10:80')
    parser.add_argument(
        '--username',
        dest='username',
        help='Interoperability Username, example: calpoly-broncos')
    parser.add_argument('--password',
                        dest='password',
                        help='Interoperability Password, example: 4597630144')

    cmd_args = parser.parse_args()
    relay = RelayService(url=cmd_args.url,
                         username=cmd_args.username,
                         password=cmd_args.password)

    server = SimpleXMLRPCServer(
        ('127.0.0.1', 9000),
        logRequests=True,
        allow_none=True)
    server.register_instance(relay)

    try:
        print 'Use Control-C to exit'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Exiting'
