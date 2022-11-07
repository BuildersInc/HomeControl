import argparse

from WebServer import WebServer


def parser():
    """
    Creates new argument parser

    Returns:
        argument_parser
    """
    new_parser = argparse.ArgumentParser(
        description=""
    )

    new_parser.add_argument("-p", "--port",
                            help="The port the Webserver is running on",
                            dest="port",
                            default=5005)

    new_parser.add_argument("-d", "--debug",
                            help="Turns on debug mode",
                            dest="debug_mode",
                            action="store_true",
                            default=False)

    return new_parser


def main(args):
    web_app = WebServer.WebServer(port=args.port, debug=args.debug_mode)
    web_app.run()


if __name__ == '__main__':
    main(parser().parse_args())
