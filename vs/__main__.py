from vs import create_application
import vs

import argparse
import sys


def init(ns):
    import vs.config
    vs.config.DATABASE.initialize()


def www(ns):
    app = create_application()
    app.run(
        debug=ns.debug, port=int(ns.port), host=ns.host
    )


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser('vs')
    parser.add_argument('--port', default=5000, help='Port to listen on.')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to.')
    parser.add_argument('--debug', action='store_true', help='TESTING ONLY')
    parser.add_argument('operation', choices=['init', 'www'])
    ns = parser.parse_args(argv)

    import vs.__main__
    # workaround for setuptools generated script
    # not beeing able to import local_config.py
    if '' not in sys.path:
        sys.path.insert(0, '')
    getattr(vs.__main__, ns.operation)(ns)


if __name__ == '__main__':
    main()
