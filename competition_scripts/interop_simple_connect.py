from __future__ import print_function
import argparse
import datetime
import getpass
import logging
import pprint
import sys
import time

from interop import Client
from interop import Telemetry

logger = logging.getLogger(__name__)

def probe(args, client):
    while True:
        start_time = datetime.datetime.now()

        telemetry = Telemetry(0, 0, 0, 0)
        telemetry_resp = client.post_telemetry(telemetry)
        stationary_obstacles, moving_obstacles = client.get_obstacles()
        for stationary_obstacle in stationary_obstacles:
            print(stationary_obstacle.latitude)

        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        logger.info('Executed interop. Total latency: %f', elapsed_time)

        delay_time = args.interop_time - elapsed_time
        if delay_time > 0:
            try:
                time.sleep(delay_time)
            except KeyboardInterrupt:
                sys.exit(0)

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')

    # Parse command line args.
    parser = argparse.ArgumentParser(description='AUVSI SUAS Interop CLI.')
    parser.add_argument('--url',
                        required=True,
                        help='URL for interoperability.')
    parser.add_argument('--username',
                        required=True,
                        help='Username for interoperability.')
    parser.add_argument('--password', help='Password for interoperability.')

    subparsers = parser.add_subparsers(help='Sub-command help.')

    subparser = subparsers.add_parser('probe', help='Send dummy requests.')
    subparser.set_defaults(func=probe)
    subparser.add_argument('--interop_time',
                           type=float,
                           default=1.0,
                           help='Time between sent requests (sec).')

    # Parse args, get password if not provided.
    args = parser.parse_args()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass('Interoperability Password: ')

    # Create client and dispatch subcommand.
    client = Client(args.url, args.username, password)
    args.func(args, client)

if __name__ == '__main__':
    main()
