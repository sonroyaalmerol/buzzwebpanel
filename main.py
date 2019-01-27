#!/usr/bin/env python2.7

import argparse
import sys
import waitress
import buzzwebpanel
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing web server for buzzwebpanel.')
    parser.add_argument('--host', default=get_ip(),
                        help='ip for the server to listen on')
    parser.add_argument('--port', '-p', type=int, default=5000,
                        help='port for the server to listen on')
    args = parser.parse_args()

    buzzwebpanel.register_blueprints()
    sys.stderr.write(' * Starting buzzwebpanel server.\n')
    waitress.serve(buzzwebpanel.app, host=args.host, port=args.port)
