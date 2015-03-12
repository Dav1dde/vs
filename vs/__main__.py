from vs import create_application
import argparse
import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser('vs')
    parser.add_argument('--port', default=5000, help='Port to listen on.')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to.')
    parser.add_argument('--debug', action='store_true', help='TESTING ONLY')
    ns = parser.parse_args(argv)

    app = create_application()
    app.run(
        debug=ns.debug, port=int(ns.port), host=ns.host
    )
