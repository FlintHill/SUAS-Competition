import argparse
from time import time
try:
    # Python 3
    from xmlrpc.client import ServerProxy
except ImportError:
    # Python 2
    from SimpleXMLRPCServer import ServerProxy

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AUVSI SUAS TRA')
    parser.add_argument(
        '--url',
        dest='url',
        help='Interoperability Client URL, example: http://10.10.130.10:80',
        required=True)

    cmd_args = parser.parse_args()

    print("[*] Starting Target Recognition Application...")

    try:
        print('[*] Use Control-C to exit')
    except KeyboardInterrupt:
        print('Exiting')
